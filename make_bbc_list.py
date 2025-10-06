#!/usr/bin/env python3
import argparse, json, os, random, re, ssl, sys, urllib.parse, urllib.request
from pathlib import Path

UA = "EnvionBBCLocal/1.0"
ADV = "https://archive.org/advancedsearch.php"
META = "https://archive.org/metadata/"

def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()  # usa certificati di sistema del Mac
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read().decode("utf-8", errors="ignore")

def adv_search(query, rows=50, page=1):
    params = {
        "q": query,
        "rows": rows,
        "page": page,
        "output": "json",
        "fl[]": ["identifier", "title"]
    }
    qs = urllib.parse.urlencode(params, doseq=True, safe=":() ")
    return json.loads(http_get(f"{ADV}?{qs}"))

def get_meta(identifier):
    return json.loads(http_get(META + urllib.parse.quote(identifier)))

def next_prog(out_dir: Path, basename: str) -> Path:
    pat = re.compile(rf"^{re.escape(basename)}_(\d{{3}})\.txt$")
    nums = []
    for p in out_dir.glob(f"{basename}_*.txt"):
        m = pat.match(p.name)
        if m: nums.append(int(m.group(1)))
    n = max(nums)+1 if nums else 1
    return out_dir / f"{basename}_{n:03d}.txt"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--max-dur", type=int, default=0)
    ap.add_argument("--count", type=int, default=8)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--basename", default="envion_bbc_raw")
    ap.add_argument("--history", default="")
    ap.add_argument("--dedupe", action="store_true")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    base_q = "((collection:BBCSoundEffectsComplete) OR (collection:bbcsoundeffects))"
    adv_q = f"{base_q} AND (title:{args.q} OR description:{args.q} OR subject:{args.q})" if args.q.strip() else base_q

    try:
        js = adv_search(adv_q)
    except Exception as e:
        print(f"[ERROR] search: {e}", file=sys.stderr); sys.exit(2)

    docs = (js.get("response") or {}).get("docs") or []
    if not docs:
        print("[WARN] nessun identifier", file=sys.stderr); sys.exit(1)

    pool = []
    for d in docs:
        ident = d.get("identifier")
        if not ident: continue
        try:
            meta = get_meta(ident)
        except Exception:
            continue
        for f in meta.get("files", []):
            name = f.get("name") or ""
            fmt = (f.get("format") or "").lower()
            if not name or fmt not in ("mp3","wav"): continue
            sec = 0.0
            length = f.get("length")
            if isinstance(length,(int,float)): sec = float(length)
            elif isinstance(length,str) and ":" in length:
                a = [int(x) for x in length.split(":")]
                sec = a[0]*3600+a[1]*60+a[2] if len(a)==3 else a[0]*60+a[1]
            if args.max_dur>0 and sec>0 and sec>args.max_dur: continue
            url = f"https://archive.org/download/{urllib.parse.quote(ident)}/{urllib.parse.quote(name)};"
            pool.append(url)

    if not pool:
        print("[WARN] pool vuoto", file=sys.stderr); sys.exit(1)

    if args.dedupe:
        seen=set(); pool=[x for x in pool if not (x in seen or seen.add(x))]

    if args.history and os.path.exists(args.history):
        with open(args.history,"r",encoding="utf-8",errors="ignore") as h:
            hist=set(l.strip() for l in h if l.startswith("http"))
        pool=[x for x in pool if x.strip() not in hist]

    picks = pool if len(pool)<=args.count else random.sample(pool, args.count)
    out_path = next_prog(out_dir, args.basename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(picks)+"\n")
    print(f"[OK] {out_path}")

    if args.history:
        with open(args.history,"a",encoding="utf-8") as h:
            for ln in picks: h.write(ln+"\n")

if __name__ == "__main__":
    main()
