#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, os, sys, time, re, json
from urllib.parse import urlencode, quote
import requests
from random import shuffle

IA_SEARCH = "https://archive.org/advancedsearch.php"
IA_META   = "https://archive.org/metadata/"
BBC_COLLECTIONS = {"BBCSoundEffectsComplete", "bbcsoundeffects"}
AUDIO_EXTS = {".wav", ".aiff", ".aif", ".mp3"}  # tolto flac per PD

def dbg(flag, *msg):
    if flag:
        print("[DEBUG]", *msg, file=sys.stdout)

def parse_len(value):
    if value is None:
        return None
    try:
        return int(float(value))
    except Exception:
        pass
    m = re.match(r"^\s*(\d+):(\d{1,2})\s*$", str(value))
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    return None

def load_history(path):
    s = set()
    if not path or not os.path.exists(path):
        return s
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            u = line.strip().rstrip(";")
            if u:
                s.add(u)
    return s

def append_history(path, urls):
    if not path:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for u in urls:
            f.write(u + ";\n")

def valid_audio_file(fobj, max_dur):
    name = fobj.get("name") or ""
    ext = os.path.splitext(name.lower())[1]
    if ext not in AUDIO_EXTS:
        return False
    if max_dur > 0:
        dur = parse_len(fobj.get("length"))
        if dur is not None and dur > max_dur:
            return False
    return True

def files_from_identifier(identifier, max_dur, debug, name_contains=None):
    url = IA_META + identifier
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    meta = r.json()
    files = meta.get("files", []) or []
    out = []
    for f in files:
        name = f.get("name") or ""
        if name_contains and name_contains.lower() not in name.lower():
            continue
        if not valid_audio_file(f, max_dur):
            continue
        encoded_name = quote(name, safe="/")  # <-- encode per PureData
        out.append(f"https://archive.org/download/{identifier}/{encoded_name}")
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            uniq.append(u)
            seen.add(u)
    dbg(debug, f"identifier={identifier} -> {len(uniq)} candidates (filter='{name_contains}')")
    return uniq

def search_bbc_docs(query_text, rows, debug):
    query = f'(collection:({" OR ".join(BBC_COLLECTIONS)})) AND mediatype:audio AND text:{query_text}'
    params = {
        "q": query,
        "rows": rows,
        "page": 1,
        "output": "json",
        "fl[]": ["identifier", "title", "collection", "mediatype"]
    }
    url = IA_SEARCH + "?" + urlencode(params, doseq=True)
    dbg(debug, "search URL:", url)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    docs = (data.get("response") or {}).get("docs") or []
    dbg(debug, f"hits (bbc-only) = {len(docs)}")
    dbg(debug, "primi identifier:", [d.get("identifier") for d in docs[:10]])
    return docs

def main():
    ap = argparse.ArgumentParser(description="BBC (Archive.org) search → raw URL list")
    ap.add_argument("--q", required=True, help="search text (e.g., wind)")
    ap.add_argument("--max-dur", type=int, default=0, help="max duration seconds (0 = no limit)")
    ap.add_argument("--count", type=int, default=8, help="how many URLs to output")
    ap.add_argument("--rows", type=int, default=300, help="advancedsearch rows per page")
    ap.add_argument("--out-dir", required=True, help="output directory for lists")
    ap.add_argument("--basename", default=None, help="basename for output list")
    ap.add_argument("--history", default=None, help="history file (for dedupe)")
    ap.add_argument("--dedupe", action="store_true", help="skip URLs already in history")
    ap.add_argument("--no-fallback", action="store_true", help="do not fall back to non-BBC items")
    ap.add_argument("--debug", action="store_true", help="debug prints")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # 1) query “docs”
    try:
        docs = search_bbc_docs(args.q, args.rows, args.debug)
    except Exception as e:
        print(f"[ERROR] search request failed: {e}", file=sys.stderr)
        docs = []

    candidates = []

    # 2) tenta dai docs
    if docs:
        shuffle(docs)
        for d in docs:
            raw_colls = d.get("collection")
            if isinstance(raw_colls, list):
                colls = set(raw_colls)
            elif isinstance(raw_colls, str):
                colls = {raw_colls}
            else:
                colls = set()
            if args.no-fallback and not (colls & BBC_COLLECTIONS):
                continue
            ident = d.get("identifier")
            if not ident:
                continue
            try:
                urls = files_from_identifier(ident, args.max_dur, args.debug)
                candidates.extend(urls)
            except Exception as e:
                dbg(args.debug, f"metadata fetch failed for {ident}: {e}")
            if len(candidates) >= args.count * 3:
                break

    # 3) fallback diretto nella collezione BBC
    if not candidates:
        dbg(args.debug, "fallback: scan files of BBCSoundEffectsComplete by filename match")
        try:
            from_bbc_root = files_from_identifier(
                "BBCSoundEffectsComplete",
                args.max_dur,
                args.debug,
                name_contains=args.q
            )
            shuffle(from_bbc_root)
            candidates.extend(from_bbc_root)
        except Exception as e:
            dbg(args.debug, f"fallback scan failed: {e}")

    # 4) dedupe + limit
    history = load_history(args.history) if args.dedupe else set()
    final = []
    for u in candidates:
        if args.dedupe and u in history:
            dbg(args.debug, "skip (history):", u)
            continue
        final.append(u)
        if len(final) >= args.count:
            break

    if not final:
        print("[WARN] No candidates found with current filters.", file=sys.stderr)
        sys.exit(1)

    base = args.basename or f"bbc_{re.sub(r'\\W+', '_', args.q.strip())}"
    stamp = time.strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(args.out_dir, f"{base}_{stamp}.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        for u in final:
            f.write(u + ";\n")

    append_history(args.history, final)

    print(f"[OK] wrote {len(final)} URLs → {out_path}")
    for u in final:
        print("  ", u + ";")

if __name__ == "__main__":
    main()
