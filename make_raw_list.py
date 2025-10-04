#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, urllib.request, urllib.parse, ssl, uuid, re, pathlib, time

# disattiva controlli SSL (compatibilità con macOS Mojave)
ssl._create_default_https_context = ssl._create_unverified_context

RAW_EXTS = (".wav", ".aif", ".aiff", ".flac", ".mp3", ".ogg", ".m4a")

def with_cache_buster(base_url: str) -> str:
    u = list(urllib.parse.urlsplit(base_url))
    q = urllib.parse.parse_qs(u[3], keep_blank_values=True)
    q["_rnd"] = [uuid.uuid4().hex]
    u[3] = urllib.parse.urlencode(q, doseq=True)
    return urllib.parse.urlunsplit(u)

def extract_raw_url(url: str, timeout=20):
    req = urllib.request.Request(with_cache_buster(url), headers={"User-Agent":"EnvionNetAudio/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", errors="ignore").strip()
    if body.startswith("http"):
        candidate = body.split()[0].strip()
        if any(candidate.lower().split("?")[0].endswith(ext) for ext in RAW_EXTS):
            return candidate
    m = re.search(r"https?://[^\s'\"<>]+", body)
    if m:
        candidate = m.group(0)
        if any(candidate.lower().split("?")[0].endswith(ext) for ext in RAW_EXTS):
            return candidate
    return None

def next_sequence_path(out_dir, prefix="envion_random_raw_", digits=3, suffix=".txt"):
    out_dir = pathlib.Path(out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(rf"^{re.escape(prefix)}(\d{{{digits}}}){re.escape(suffix)}$")
    max_idx = 0
    for p in out_dir.glob(f"{prefix}*{suffix}"):
        m = pattern.match(p.name)
        if m:
            max_idx = max(max_idx, int(m.group(1)))
    nxt = 1 if max_idx == 0 else max_idx + 1
    return out_dir / f"{prefix}{str(nxt).zfill(digits)}{suffix}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL freesound_get.php")
    ap.add_argument("--count", type=int, default=10, help="Quante URL valide raccogliere")
    ap.add_argument("--out-dir", default=".", help="Cartella di output")
    args = ap.parse_args()

    out_path = next_sequence_path(args.out_dir)
    urls = []
    attempts = 0

    print(f"Salvo in: {out_path.name}\n")

    while len(urls) < args.count and attempts < args.count * 20:
        attempts += 1
        try:
            raw = extract_raw_url(args.url)
            if raw:
                urls.append(raw)
                print(f"[OK {len(urls)}/{args.count}] {raw}")
            else:
                print(f"[SKIP {attempts}] no valid URL")
        except Exception as e:
            print(f"[ERR {attempts}] {e}")
        time.sleep(0.2)

    with open(out_path, "w", encoding="utf-8") as f:
        for u in urls:
            f.write(u.rstrip() + ";\n")

    print(f"\nCreato: {out_path}")

if __name__ == "__main__":
    main()
