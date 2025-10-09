#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wiki_commons_fetch_v2.py — Commons audio fetch robusto:
- Usa list=search su namespace File, poi prop=imageinfo (url,mime)
- Accetta il file se MIME inizia con 'audio/' OPPURE l'estensione è tra quelle permesse
- Aggiunge ';' a fine riga per compatibilità Pure Data
"""

import argparse, os, sys, json
from urllib.parse import urlencode
import urllib.request

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = "Envion-NetAudio/1.1 (contact: user)"

def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")

def search_pages(q, limit, timeout, verbose):
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": f"({q}) (filetype:ogg OR filetype:oga OR filetype:wav OR filetype:flac)",
        "srnamespace": "6",  # File:
        "srlimit": "200",
        "srinfo": "totalhits",
        "srqiprofile": "classic_noboostlinks",
        "origin": "*",
    }
    url = COMMONS_API + "?" + urlencode(params)
    if verbose: print("[search]", url)
    data = json.loads(http_get(url, timeout))
    return data.get("query", {}).get("search", [])

def fetch_imageinfo(pageids, timeout, verbose):
    if not pageids:
        return {}
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|mime",
        "pageids": "|".join(map(str, pageids)),
        "origin": "*",
    }
    url = COMMONS_API + "?" + urlencode(params)
    if verbose: print("[imageinfo]", url)
    data = json.loads(http_get(url, timeout))
    return data.get("query", {}).get("pages", {})

def read_history_set(path):
    s=set()
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                u=line.strip()
                if u: s.add(u)
    return s

def is_audio_ok(title, url, mime, include_exts, exclude_terms):
    t = (title or "").lower()
    u = (url or "").lower()
    m = (mime or "").lower()
    # escludi parole
    for term in exclude_terms:
        if term and (term.lower() in t or term.lower() in u):
            return False
    # MIME prevale
    if m.startswith("audio/"):
        return True
    # fallback: estensione
    return any(u.endswith(ext) or t.endswith(ext) for ext in include_exts)

def main():
    ap = argparse.ArgumentParser(description="Fetch audio URLs from Wikimedia Commons (robusto).")
    ap.add_argument("--q", required=True)
    ap.add_argument("--count", type=int, default=8)
    ap.add_argument("--out-dir", default="netsound/wiki")
    ap.add_argument("--out-file", default="urls.txt")
    ap.add_argument("--history", default="netsound/wiki/netsound_history.txt")
    ap.add_argument("--dedupe", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--exclude", default="")
    ap.add_argument("--extensions", default=".ogg,.oga,.wav,.flac")
    args = ap.parse_args()

    include_exts = [e.strip().lower() for e in args.extensions.split(",") if e.strip()]
    exclude_terms = [t.strip() for t in args.exclude.split(",") if t.strip()]
    exclude_terms += [".mid", ".midi"]

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, args.out_file)
    hist_path = args.history

    if args.verbose:
        print("→ Query:", args.q)
        print("→ Estensioni:", include_exts)
        print("→ Escludi:", exclude_terms)
        print("→ Out:", out_path)
        print("→ History:", hist_path, "(dedupe:", args.dedupe, ")")

    hits = search_pages(args.q, args.count, args.timeout, args.verbose)
    if args.verbose: print("[hits]", len(hits))

    pageids = [str(r["pageid"]) for r in hits]
    pages = fetch_imageinfo(pageids, args.timeout, args.verbose)

    seen = read_history_set(hist_path) if args.dedupe else set()
    urls = []
    for pid, page in pages.items():
        title = page.get("title", "")
        infos = page.get("imageinfo", []) or []
        if not infos: 
            continue
        url = infos[0].get("url", "")
        mime = infos[0].get("mime", "")
        if not url:
            continue
        if args.dedupe and url in seen:
            if args.verbose: print("  · già in history:", url)
            continue
        if not is_audio_ok(title, url, mime, include_exts, exclude_terms):
            continue
        urls.append(url)
        if args.verbose: print("  ✓", url, "|", mime)
        if len(urls) >= args.count:
            break

    if not urls:
        print("❌  Nessun file audio utile trovato — nulla salvato.")
        sys.exit(1)

    with open(out_path, "a", encoding="utf-8") as f:
        for u in urls:
            f.write(u.strip() + ";\n")
    if hist_path:
        with open(hist_path, "a", encoding="utf-8") as f:
            for u in urls:
                f.write(u.strip() + "\n")

    print(f"✅ Salvati {len(urls)} URL in: {out_path}")
    if args.dedupe:
        print(f"🗂️  History aggiornata: {hist_path}")

if __name__ == "__main__":
    main()
