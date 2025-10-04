#!/usr/bin/env python3
"""
Envion NetSound RAW URL Generator — Pd-ready format
---------------------------------------------------
- Interroga la tua freesound_get.php finché non ottiene N URL RAW valide
- Salva SOLO URL valide terminate da ';' per compatibilità con text define
- Crea file con timestamp in ./netsound/envion_raw_YYYYMMDD_HHMMSS.txt
- Aggiorna ./netsound/envion_raw_latest.txt (ultimo run)
- Aggiorna ./netsound/envion_master.txt (db cumulativo deduplicato)
"""

import argparse, ssl, certifi, urllib.request, urllib.parse, uuid, re, pathlib, datetime, time, random

def ssl_ctx():
    return ssl.create_default_context(cafile=certifi.where())

def with_cache_buster(base_url: str) -> str:
    u = list(urllib.parse.urlsplit(base_url))
    q = urllib.parse.parse_qs(u[3], keep_blank_values=True)
    q["_rnd"] = [uuid.uuid4().hex]
    u[3] = urllib.parse.urlencode(q, doseq=True)
    return urllib.parse.urlunsplit(u)

def extract_raw_url(url: str, timeout=30) -> str | None:
    """Legge la risposta e cerca URL diretta (mp3/wav/flac)."""
    ctx = ssl_ctx()
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=timeout) as r:
            body = r.read(8192).decode("utf-8", errors="ignore")

            # HTML/testo
            m = re.search(r"https://cdn\.freesound\.org/[^\s\"']+\.(?:mp3|wav|flac)", body)
            if m:
                return m.group(0)

            # JSON
            m = re.search(r'"(https://cdn\.freesound\.org/[^\"]+\.(?:mp3|wav|flac))"', body)
            if m:
                return m.group(1)

            # Plain text già URL
            body_stripped = body.strip()
            if body_stripped.startswith("http"):
                return body_stripped.split()[0]

            return None
    except Exception:
        return None

def write_lines(path: pathlib.Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + ";\n")  # <-- ; per text define in Pd

def update_master(master_path: pathlib.Path, new_lines: list[str]) -> int:
    master_path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if master_path.exists():
        existing = [ln.strip().rstrip(";") for ln in master_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    seen = set(existing)
    appended = 0
    with master_path.open("a", encoding="utf-8") as f:
        for ln in new_lines:
            if ln not in seen:
                f.write(ln + ";\n")
                seen.add(ln)
                appended += 1
    return appended

def main():
    parser = argparse.ArgumentParser(description="Generate timestamped Pd-ready TXT with RAW audio URLs.")
    parser.add_argument("--url", required=True, help="Dynamic PHP URL (e.g. https://.../freesound_get.php?...&mode=raw)")
    parser.add_argument("--target", type=int, default=8, help="How many VALID URLs to collect (default: 8)")
    parser.add_argument("--max-attempts", type=int, default=80, help="Safety cap (default: 10x target)")
    parser.add_argument("--min-delay", type=float, default=0.25, help="Seconds between attempts (min)")
    parser.add_argument("--max-delay", type=float, default=0.6, help="Seconds between attempts (max)")
    parser.add_argument("--no-latest", action="store_true", help="Do not update envion_raw_latest.txt")
    parser.add_argument("--no-master", action="store_true", help="Do not update envion_master.txt")
    args = parser.parse_args()

    base_dir = pathlib.Path(__file__).parent
    netsound_dir = base_dir / "netsound"
    netsound_dir.mkdir(exist_ok=True)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_ts = netsound_dir / f"envion_raw_{ts}.txt"
    out_latest = netsound_dir / "envion_raw_latest.txt"
    out_master = netsound_dir / "envion_master.txt"

    collected: list[str] = []
    seen = set()
    attempts = 0
    max_attempts = max(args.max_attempts, args.target * 10)

    print(f"Target valid URLs: {args.target}  |  Max attempts: {max_attempts}")

    while len(collected) < args.target and attempts < max_attempts:
        attempts += 1
        req_url = with_cache_buster(args.url)
        raw = extract_raw_url(req_url)
        if raw and raw.startswith("https://") and raw not in seen:
            collected.append(raw)
            seen.add(raw)
            print(f"[OK {len(collected)}/{args.target}] {raw}")
        else:
            print(f"[SKIP {attempts}] no valid URL")

        time.sleep(random.uniform(args.min_delay, args.max_delay))

    # salva file timestampato
    write_lines(out_ts, collected)
    print(f"\nSaved {len(collected)} valid RAW URLs → {out_ts}")

    # aggiorna latest
    if not args.no_latest:
        write_lines(out_latest, collected)
        print(f"Updated latest → {out_latest}")

    # aggiorna master cumulativo
    if not args.no_master:
        added = update_master(out_master, collected)
        print(f"Appended {added} new to master → {out_master}")

    if len(collected) < args.target:
        print(f"\nNote: target not fully reached ({len(collected)}/{args.target}). Try again or increase --max-attempts.")

if __name__ == "__main__":
    main()
