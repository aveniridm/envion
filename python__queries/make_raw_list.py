#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
make_raw_list.py
Genera una lista di URL (una per riga, con ';' finale) pescandole da una URL remota (es. freesound_get.php?mode=raw).
Supporta:
- --history: file di storico persistente (append) per deduplica
- --dedupe: salta URL già viste nello storico
- --insecure: disabilita la verifica SSL (workaround per macOS vecchi)
- auto-increment del file di output: envion_random_raw_001.txt, _002, ...
- usa 'certifi' se disponibile per risolvere CERTIFICATE_VERIFY_FAILED su sistemi vecchi
"""

import argparse
import pathlib
import re
import sys
import time
import ssl
from urllib import request, error

MP3_URL_RE = re.compile(r"https?://[^\s\"'<>]+?\.mp3", re.IGNORECASE)

def norm(u: str) -> str:
    return u.strip().rstrip(';')

def find_next_index(out_dir: pathlib.Path, prefix: str) -> int:
    max_idx = 0
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)\.txt$", re.IGNORECASE)
    if not out_dir.exists():
        return 1
    for p in out_dir.iterdir():
        if p.is_file():
            m = pattern.match(p.name)
            if m:
                try:
                    idx = int(m.group(1))
                    if idx > max_idx:
                        max_idx = idx
                except ValueError:
                    pass
    return max_idx + 1

def build_output_path(out_dir: pathlib.Path, prefix: str) -> pathlib.Path:
    idx = find_next_index(out_dir, prefix)
    return out_dir / f"{prefix}{idx:03d}.txt"

def make_ssl_context(insecure: bool = False) -> ssl.SSLContext:
    if insecure:
        return ssl._create_unverified_context()
    try:
        import certifi  # type: ignore
        ctx = ssl.create_default_context(cafile=certifi.where())
        return ctx
    except Exception:
        return ssl.create_default_context()

def http_get_text(url: str, timeout: float, ctx: ssl.SSLContext) -> str:
    req = request.Request(
        url,
        headers={"User-Agent": "Envion-NetAudio/1.0 (+https://www.peamarte.it/)"}
    )
    with request.urlopen(req, timeout=timeout, context=ctx) as resp:
        raw = resp.read()
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="replace")

def extract_raw_url(source_url: str, ctx: ssl.SSLContext):
    try:
        text = http_get_text(source_url, timeout=10.0, ctx=ctx).strip()
    except error.HTTPError as e:
        print(f"[HTTP {e.code}] {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[HTTP ERR] {e}", file=sys.stderr)
        return None

    candidate = norm(text.splitlines()[0]) if text else ""
    if candidate.lower().startswith("http") and candidate.lower().endswith(".mp3"):
        return candidate

    m = MP3_URL_RE.search(text)
    if m:
        return norm(m.group(0))
    return None

def main():
    ap = argparse.ArgumentParser(description="Genera liste di URL MP3 casuali (una per riga, con ';').")
    ap.add_argument("--url", required=True, help="Endpoint remoto che restituisce una URL .mp3 (es. freesound_get.php?mode=raw).")
    ap.add_argument("--count", type=int, default=8, help="Quante URL raccogliere per la lista (default: 8).")
    ap.add_argument("--out-dir", default=".", help="Directory di output per i file lista (default: .).")
    ap.add_argument("--out-prefix", default="envion_random_raw_", help="Prefisso per il nome file (default: envion_random_raw_).")
    ap.add_argument("--history", default=None, help="File di storico (append) per deduplica persistente.")
    ap.add_argument("--dedupe", action="store_true", help="Salta URL già presenti nello storico.")
    ap.add_argument("--insecure", action="store_true", help="Disabilita la verifica SSL (solo se necessario).")
    ap.add_argument("--max-multiplier", type=int, default=50, help="Tentativi max = count * max-multiplier (default: 50).")
    ap.add_argument("--sleep", type=float, default=0.2, help="Pausa fra tentativi in secondi (default: 0.2).")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    ssl_ctx = make_ssl_context(insecure=args.insecure)

    seen = set()
    if args.history and args.dedupe:
        hist_path = pathlib.Path(args.history).expanduser().resolve()
        if hist_path.exists():
            try:
                with open(hist_path, "r", encoding="utf-8") as hf:
                    for line in hf:
                        s = norm(line)
                        if s:
                            seen.add(s)
            except Exception as e:
                print(f"[WARN] Impossibile leggere history: {e}", file=sys.stderr)
        else:
            hist_path.parent.mkdir(parents=True, exist_ok=True)

    urls = []
    attempts = 0
    max_attempts = max(args.count, 1) * max(args.max_multiplier, 1)

    print(f"[START] target={args.count} | dedupe={args.dedupe} | history={'ON' if args.history else 'OFF'} | insecure={args.insecure}")
    while len(urls) < args.count and attempts < max_attempts:
        attempts += 1
        u = extract_raw_url(args.url, ctx=ssl_ctx)
        if not u:
            print(f"[SKIP {attempts}] no valid URL")
            time.sleep(args.sleep)
            continue

        u_clean = norm(u)
        if args.dedupe and u_clean in seen:
            print(f"[SKIP {attempts}] duplicate")
            time.sleep(args.sleep)
            continue

        urls.append(u_clean + ";")
        print(f"[OK {len(urls)}/{args.count}] {u_clean}")

        if args.history:
            try:
                with open(pathlib.Path(args.history).expanduser().resolve(), "a", encoding="utf-8") as hf:
                    hf.write(u_clean + ";\n")
                seen.add(u_clean)
            except Exception as e:
                print(f"[WARN] Impossibile scrivere history: {e}", file=sys.stderr)

        time.sleep(args.sleep)

    if len(urls) < args.count:
        print(f"[END] Raccolte {len(urls)}/{args.count} URL (raggiunto limite tentativi: {attempts}).")

    out_path = build_output_path(out_dir, args.out_prefix)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            for line in urls:
                f.write(line + ("\n" if not line.endswith("\n") else ""))
        print(f"[WRITE] {out_path} ({len(urls)} righe)")
    except Exception as e:
        print(f"[ERROR] Scrittura output fallita: {e}", file=sys.stderr)
        sys.exit(1)

    print("[DONE]")

if __name__ == "__main__":
    main()
