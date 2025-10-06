#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter, Retry

ADV_SEARCH_URL = "https://archive.org/advancedsearch.php"
METADATA_URL = "https://archive.org/metadata"
DOWNLOAD_BASE = "https://archive.org/download"

AUDIO_EXTS = {
    ".mp3", ".wav", ".flac", ".ogg", ".oga", ".aiff", ".aif", ".m4a", ".mp4"
}
AUDIO_FORMAT_HINTS = {
    "mp3", "mpeg layer 3", "vbr mp3", "wave", "wav", "flac", "ogg", "vorbis",
    "aiff", "m4a", "mp4", "aac", "audio"
}

# Collezioni pulite per SFX (evita flussi radio)
SFX_COLLECTIONS = [
    "BBCSoundEffectsComplete",
    "bbcsoundeffects",
    "folksoundomy_effects",
    # "community_audio",  # troppo rumorosa; riaggiungi se vuoi
]

EXCLUSIONS = [
    'NOT title:"BBC Radio"',
    'NOT title:BBC_Radio_',
    'NOT collection:bbc_radio',
]

FIELDS = ["identifier", "title", "creator", "mediatype", "collection"]

def make_session(insecure: bool = False) -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.6,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    if insecure:
        s.verify = False
        requests.packages.urllib3.disable_warnings()  # type: ignore
    return s


def looks_advanced(q: str) -> bool:
    tokens = [' OR ', ' AND ', ' NOT ', '(', ')', 'title:', 'creator:',
              'collection:', 'mediatype:', 'subject:', 'text:']
    return any(t in q for t in tokens)


def q_text_for_user(q: str) -> str:
    q = q.strip()
    if looks_advanced(q):
        return q  # passa raw
    return f"text:{q}"  # niente virgolette → no frase esatta


def build_q1(user_q: str) -> str:
    colls = " OR ".join(f"collection:{c}" for c in SFX_COLLECTIONS)
    base = f"({colls}) AND mediatype:audio"
    qtext = q_text_for_user(user_q)
    excl = " AND ".join(EXCLUSIONS)
    return f"{base} AND {qtext} AND {excl}"


def build_q2(user_q: str) -> str:
    # Fallback senza 'bbc' per evitare flussi radio
    base = 'mediatype:audio AND ("sound effects" OR sfx OR fx)'
    qtext = q_text_for_user(user_q)
    excl = " AND ".join(EXCLUSIONS)
    return f"{base} AND {qtext} AND {excl}"


def ia_search(session: requests.Session, q: str, rows: int, page: int, debug: bool) -> Dict:
    params = {
        "q": q,
        "rows": rows,
        "page": page,
        "output": "json",
        "fl[]": FIELDS,  # <-- FIX: passiamo la LISTA intera (no override)
    }
    url = f"{ADV_SEARCH_URL}?{urlencode(params, doseq=True)}"
    if debug:
        print(f"[DEBUG] search URL: {url}")
    r = session.get(url, timeout=20)
    r.raise_for_status()
    return r.json()


def parse_duration_str(s: str) -> Optional[float]:
    s = str(s).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        pass
    if re.match(r"^\d{1,2}:\d{2}:\d{2}(\.\d+)?$", s):
        hh, mm, ss = s.split(":")
        return int(hh) * 3600 + int(mm) * 60 + float(ss)
    if re.match(r"^\d{1,2}:\d{2}(\.\d+)?$", s):
        mm, ss = s.split(":")
        return int(mm) * 60 + float(ss)
    return None


def pick_audio_files(files: List[Dict], max_dur: int) -> List[Tuple[str, Optional[float]]]:
    out = []
    for f in files:
        name = f.get("name") or ""
        fmt = (f.get("format") or "").lower()
        ext = Path(name).suffix.lower()
        if not name:
            continue

        is_audio = (ext in AUDIO_EXTS) or any(h in fmt for h in AUDIO_FORMAT_HINTS)
        if not is_audio:
            continue

        dur = None
        for key in ("length", "duration"):
            if key in f and f[key]:
                dur = parse_duration_str(f[key])
                break

        if max_dur > 0 and dur is not None and dur > max_dur:
            continue

        out.append((name, dur))
    return out


def ia_metadata(session: requests.Session, identifier: str, debug: bool) -> Dict:
    url = f"{METADATA_URL}/{identifier}"
    if debug:
        print(f"[DEBUG] metadata URL: {url}")
    r = session.get(url, timeout=20)
    r.raise_for_status()
    return r.json()


def ensure_outdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def load_history(history_file: Path) -> set:
    if not history_file.exists():
        return set()
    urls = set()
    with history_file.open("r", encoding="utf-8") as f:
        for line in f:
            u = line.strip()
            if not u:
                continue
            if u.endswith(";"):
                u = u[:-1]
            urls.add(u)
    return urls


def append_history(history_file: Path, urls: Iterable[str]):
    with history_file.open("a", encoding="utf-8") as f:
        for u in urls:
            f.write(u + ";\n")


def next_progressive_filename(out_dir: Path, basename_prefix: str = "envion_random_raw_", width: int = 3) -> Path:
    max_n = 0
    pat = re.compile(rf"{re.escape(basename_prefix)}(\d+)\.txt$")
    for p in out_dir.glob(f"{basename_prefix}*.txt"):
        m = pat.search(p.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    next_n = max_n + 1
    return out_dir / f"{basename_prefix}{next_n:0{width}d}.txt"


def main():
    ap = argparse.ArgumentParser(description="Search Internet Archive for SFX audio and emit raw URL lists.")
    ap.add_argument("--q", required=True, help="Query term(s). Use IA syntax for advanced (OR/AND/fields).")
    ap.add_argument("--rows", type=int, default=120, help="Rows per page.")
    ap.add_argument("--count", type=int, default=8, help="Target number of URLs to collect.")
    ap.add_argument("--max-dur", type=int, default=0, help="Max duration in seconds (0 = no limit).")
    ap.add_argument("--out-dir", default="netsound", help="Output directory for list files.")
    ap.add_argument("--basename", default="envion_random_raw_", help="Basename prefix for generated list files.")
    ap.add_argument("--history", default="netsound/netsound_history.txt", help="History file for dedupe.")
    ap.add_argument("--dedupe", action="store_true", help="Avoid URLs already present in history.")
    ap.add_argument("--no-fallback", action="store_true", help="Disable wide fallback query.")
    ap.add_argument("--insecure", action="store_true", help="Skip TLS verification (not recommended).")
    ap.add_argument("--debug", action="store_true", help="Verbose logging.")
    args = ap.parse_args()

    session = make_session(insecure=args.insecure)

    out_dir = Path(args.out_dir).expanduser().resolve()
    ensure_outdir(out_dir)
    hist_path = Path(args.history).expanduser().resolve()
    ensure_outdir(hist_path.parent)

    history = load_history(hist_path) if args.dedupe else set()
    if args.debug:
        print(f"[DEBUG] dedupe={args.dedupe} history_count={len(history)}")

    wanted = args.count
    collected: List[str] = []
    seen_ids = set()

    # Prima passata: collezioni SFX
    q1 = build_q1(args.q)
    page = 1
    total_docs_seen = 0

    while len(collected) < wanted:
        try:
            j = ia_search(session, q1, rows=args.rows, page=page, debug=args.debug)
        except Exception as e:
            print(f"[WARN] search failed (q1, page {page}): {e}")
            break

        resp = j.get("response", {})
        docs = resp.get("docs", [])
        if args.debug:
            prev = [d.get("identifier", "") for d in docs[:6]]
            print(f"[DEBUG] collections+text: docs={len(docs)} preview={prev}")

        if not docs:
            break

        for d in docs:
            if len(collected) >= wanted:
                break
            identifier = d.get("identifier")
            if not identifier or identifier in seen_ids:
                continue
            seen_ids.add(identifier)

            try:
                meta = ia_metadata(session, identifier, debug=args.debug)
            except Exception as e:
                print(f"[WARN] metadata failed for {identifier}: {e}")
                continue

            files = meta.get("files", []) or []
            candidates = pick_audio_files(files, args.max_dur)

            # preferisci: mp3/ogg/m4a < wav/aif (peso); poi durata crescente
            def score(t):
                name, dur = t
                ext = Path(name).suffix.lower()
                rank = {".mp3": 0, ".ogg": 1, ".m4a": 2, ".mp4": 3, ".flac": 4, ".wav": 5, ".aif": 6, ".aiff": 6}
                return (rank.get(ext, 9), dur if dur is not None else 99999)

            candidates.sort(key=score)

            for name, dur in candidates:
                url = f"{DOWNLOAD_BASE}/{identifier}/{name}"
                if args.dedupe and url in history:
                    continue
                if url in collected:
                    continue
                collected.append(url)
                if args.debug:
                    d_str = f"{dur:.2f}s" if dur is not None else "?"
                    print(f"[OK {len(collected)}/{wanted}] {url} (dur={d_str})")
                if len(collected) >= wanted:
                    break

        total_docs_seen += len(docs)
        page += 1
        time.sleep(0.25)
        if page > 20:
            break

    # Fallback opzionale
    if len(collected) < wanted and not args.no_fallback:
        q2 = build_q2(args.q)
        page = 1
        while len(collected) < wanted:
            try:
                j = ia_search(session, q2, rows=args.rows, page=page, debug=args.debug)
            except Exception as e:
                print(f"[WARN] search failed (q2, page {page}): {e}")
                break

            resp = j.get("response", {})
            docs = resp.get("docs", [])
            if args.debug:
                prev = [d.get("identifier", "") for d in docs[:6]]
                print(f"[DEBUG] fallback+text: docs={len(docs)} preview={prev}")

            if not docs:
                break

            for d in docs:
                if len(collected) >= wanted:
                    break
                identifier = d.get("identifier")
                if not identifier or identifier in seen_ids:
                    continue
                seen_ids.add(identifier)

                try:
                    meta = ia_metadata(session, identifier, debug=args.debug)
                except Exception as e:
                    print(f"[WARN] metadata failed for {identifier}: {e}")
                    continue

                files = meta.get("files", []) or []
                candidates = pick_audio_files(files, args.max_dur)
                candidates.sort(key=lambda t: (0 if Path(t[0]).suffix.lower() == ".mp3" else 1,
                                               t[1] if t[1] is not None else 99999))
                for name, dur in candidates:
                    url = f"{DOWNLOAD_BASE}/{identifier}/{name}"
                    if args.dedupe and url in history:
                        continue
                    if url in collected:
                        continue
                    collected.append(url)
                    if args.debug:
                        d_str = f"{dur:.2f}s" if dur is not None else "?"
                        print(f"[OK {len(collected)}/{wanted}] {url} (dur={d_str})")
                    if len(collected) >= wanted:
                        break

            page += 1
            time.sleep(0.25)
            if page > 20:
                break

    if args.debug:
        print(f"[DEBUG] total_docs_seen={total_docs_seen} pool_before_dedupe={len(collected)}")

    if not collected:
        print("[WARN] nessun file audio adatto trovato su IA con questi criteri.")
        sys.exit(0)

    out_file = next_progressive_filename(out_dir=out_dir, basename_prefix=args.basename, width=3)
    with out_file.open("w", encoding="utf-8") as f:
        for u in collected:
            f.write(u + ";\n")

    if args.dedupe:
        append_history(hist_path, collected)

    print(f"[DONE] wrote {len(collected)} URLs -> {out_file}")
    if args.dedupe:
        print(f"[DONE] history updated -> {hist_path}")


if __name__ == "__main__":
    main()
