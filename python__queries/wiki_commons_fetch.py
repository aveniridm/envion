#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wiki_commons_fetch.py — Cerca file audio su Wikimedia Commons e salva URL raw.
- Usa MediaWiki API (Commons) con CirrusSearch: mediatype:audio + filetype filters
- Estensioni coperte: .ogg, .wav, .flac (escludi .mid/.midi di default)
- Scrive una lista di URL (uno per riga) e aggiorna una history opzionale
"""

import argparse, os, sys, time, json, re
from urllib.parse import urlencode
import urllib.request

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = "Envion-NetAudio/1.0 (contact: user)"

def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")

def search_pages(q, limit, timeout, verbose):
    # CirrusSearch via list=search; limitiamo a namespace File (6), audio only
    # Aggiungiamo filetype per restringere
    cirrus = f'({q})'
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": cirrus,
        "srnamespace": "6",   # File:
        "srlimit": str(max(50, limit)),  # chiedi un po' di più in ingresso
        "srinfo": "totalhits",
        "srqiprofile": "classic_noboostlinks",
        "origin": "*",
    }
    url = COMMONS_API + "?" + urlencode(params)
    if verbose: print("[search]", url)
    data = json.loads(http_get(url, timeout))
    return data.get("query", {}).get("search", [])

def fetch_imageinfo(pageids, timeout, verbose):
    # Per pageids -> imageinfo.url (originale)
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

def pass_filters(filename, url, include_exts, exclude_terms, verbose):
    name_lower = filename.lower()
    url_lower  = url.lower()
    # estensione
    ok_ext = any(name_lower.endswith(ext) or url_lower.endswith(ext) for ext in include_exts)
    if not ok_ext:
        return False
    # exclude terms nel titolo o url
    for term in exclude_terms:
        if term and (term.lower() in name_lower or term.lower() in url_lower):
            if verbose: print("  · skip (exclude term):", term, "→", filename)
            return False
    return True

def read_history_set(history_path):
    s = set()
    if history_path and os.path.isfile(history_path):
        with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                u = line.strip()
                if u: s.add(u)
    return s

def main():
    p = argparse.ArgumentParser(description="Fetch audio URLs from Wikimedia Commons.")
    p.add_argument("--q", required=True, help="Query (es: 'whisper OR hiss')")
    p.add_argument("--count", type=int, default=8, help="Quanti URL salvare (default: 8)")
    p.add_argument("--out-dir", default="netsound/wiki", help="Cartella output (default: netsound/wiki)")
    p.add_argument("--out-file", default="urls.txt", help="Nome file URL (default: urls.txt)")
    p.add_argument("--history", default="netsound/wiki/netsound_history.txt", help="File history per dedupe")
    p.add_argument("--dedupe", action="store_true", help="Evita URL già visti (usa history)")
    p.add_argument("--verbose", action="store_true", help="Log verboso")
    p.add_argument("--timeout", type=int, default=15, help="Timeout HTTP sec (default: 15)")
    p.add_argument("--exclude", default="", help="Parole da escludere (comma-separated)")
    p.add_argument("--extensions", default=".ogg,.wav,.flac", help="Estensioni ammesse (comma-separated)")
    args = p.parse_args()

    include_exts = [e.strip().lower() for e in args.extensions.split(",") if e.strip()]
    # Aggiungi esclusioni MIDI sempre
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

    # 1) Cerca pagine (File:) coerenti
    results = search_pages(args.q, args.count, args.timeout, args.verbose)
    if args.verbose: print("[hits]", len(results))

    # 2) pageids → imageinfo
    pageids = [str(r["pageid"]) for r in results]
    pages = fetch_imageinfo(pageids, args.timeout, args.verbose)

    # 3) Filtra e prepara lista URL
    seen = read_history_set(hist_path) if args.dedupe else set()
    urls = []
    for pid, page in pages.items():
        title = page.get("title", "")
        infos = page.get("imageinfo", []) or []
        if not infos: 
            continue
        url = infos[0].get("url", "")
        if not url: 
            continue
        if args.dedupe and url in seen:
            if args.verbose: print("  · già in history:", url)
            continue
        if not pass_filters(title, url, include_exts, exclude_terms, args.verbose):
            continue
        urls.append(url)
        if args.verbose: print("  ✓", url)
        if len(urls) >= args.count:
            break

    if not urls:
        print("❌  Nessun file audio utile trovato — nulla salvato.")
        sys.exit(1)

    # 4) Scrivi (append) nel file di output e nella history (se richiesto)
    with open(out_path, "a", encoding="utf-8") as f:
        for u in urls:
            f.write(u.strip() + ";\n")  # punto e virgola finale (compat PD)
    if hist_path:
        with open(hist_path, "a", encoding="utf-8") as f:
            for u in urls:
                f.write(u.strip() + "\n")

    print(f"✅ Salvati {len(urls)} URL in: {out_path}")
    if args.dedupe:
        print(f"🗂️  History aggiornata: {hist_path}")

if __name__ == "__main__":
    main()
