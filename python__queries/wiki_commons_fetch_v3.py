#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wiki_commons_fetch_v3.py — Wikimedia Commons audio fetch (solido):
1) Tenta con generator=search (namespace File) + prop=imageinfo (url,mime)
2) Accetta solo MIME che iniziano per 'audio/'
3) Fallback: list=allimages con aimime=audio/*
4) Scrive URL raw con ';' finale (compat PD), dedupe opzionale
"""

import argparse, os, sys, json, time
from urllib.parse import urlencode, quote
import urllib.request

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = "Envion-NetAudio/1.2 (contact: user)"

AUDIO_MIME = [
    "audio/ogg","audio/opus","audio/vorbis",
    "audio/wav","audio/x-wav",
    "audio/flac","audio/x-flac",
    "audio/mpeg","audio/mp3","audio/x-mp3"
]
AUDIO_EXT = [".ogg",".oga",".opus",".wav",".flac",".mp3"]

def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")

def pages_via_generator_search(q, limit, timeout, verbose):
    # aggiungo un filtro filetype minimo per ridurre immagini
    gq = f"({q}) (filetype:ogg OR filetype:oga OR filetype:wav OR filetype:flac OR filetype:mp3)"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": gq,
        "gsrnamespace": "6",     # File:
        "gsrlimit": "200",
        "prop": "imageinfo",
        "iiprop": "url|mime",
        "origin": "*",
    }
    url = COMMONS_API + "?" + urlencode(params)
    if verbose: print("[gensearch]", url)
    data = json.loads(http_get(url, timeout))
    return (data.get("query", {}).get("pages", {}) or {})

def list_allimages_audio(limit, aicontinue=None, timeout=15, verbose=False):
    params = {
        "action": "query",
        "format": "json",
        "list": "allimages",
        "ailimit": "200",
        "aimime": "|".join(AUDIO_MIME),
        "origin": "*",
    }
    if aicontinue:
        params["aicontinue"] = aicontinue
    url = COMMONS_API + "?" + urlencode(params)
    if verbose: print("[allimages]", url)
    data = json.loads(http_get(url, timeout))
    return data

def is_audio(title, url, mime):
    t = (title or "").lower()
    u = (url or "").lower()
    m = (mime or "").lower()
    if m.startswith("audio/"):
        return True
    for ext in AUDIO_EXT:
        if u.endswith(ext) or t.endswith(ext):
            return True
    return False

def read_history_set(path):
    s=set()
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                u=line.strip()
                if u: s.add(u)
    return s

def main():
    ap = argparse.ArgumentParser(description="Fetch audio URLs from Wikimedia Commons (v3 robust).")
    ap.add_argument("--q", required=True)
    ap.add_argument("--count", type=int, default=8)
    ap.add_argument("--out-dir", default="netsound/wiki")
    ap.add_argument("--out-file", default="urls.txt")
    ap.add_argument("--history", default="netsound/wiki/netsound_history.txt")
    ap.add_argument("--dedupe", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, args.out_file)
    hist_path = args.history
    seen = read_history_set(hist_path) if args.dedupe else set()

    if args.verbose:
        print("→ Query:", args.q)
        print("→ Out:", out_path)
        print("→ History:", hist_path, "(dedupe:", args.dedupe, ")")

    urls = []

    # 1) generator=search
    pages = pages_via_generator_search(args.q, args.count, args.timeout, args.verbose)
    if args.verbose: print("[gensearch pages]", len(pages))
    for pid, page in pages.items():
        title = page.get("title","")
        infos = page.get("imageinfo",[]) or []
        if not infos: 
            continue
        url = infos[0].get("url","")
        mime = infos[0].get("mime","")
        if not url:
            continue
        if not is_audio(title, url, mime):
            continue
        if args.dedupe and url in seen:
            if args.verbose: print("  · già in history:", url)
            continue
        urls.append(url)
        if args.verbose: print("  ✓", url, "|", mime)
        if len(urls) >= args.count:
            break

    # 2) fallback: allimages (aimime=audio/*)
    aicont = None
    while len(urls) < args.count:
        data = list_allimages_audio(args.count, aicont, args.timeout, args.verbose)
        items = data.get("query",{}).get("allimages",[]) or []
        if args.verbose: print("[allimages items]", len(items))
        if not items:
            break
        for it in items:
            url = it.get("url","")
            title = it.get("title","")
            mime = it.get("mime","")
            if not url:
                continue
            if not is_audio(title, url, mime):
                continue
            if args.dedupe and url in seen:
                continue
            urls.append(url)
            if args.verbose: print("  ✓", url, "|", mime)
            if len(urls) >= args.count:
                break
        aicont = (data.get("continue",{}) or {}).get("aicontinue")
        if not aicont:
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
