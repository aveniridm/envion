#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
internet_archive_fine_tuning.py
Ricerca raffinata su Internet Archive per Envion NET-AUDIO.

Funzionalità:
- Modalità sitewide o BBC
- Filtri su subject (inclusione) e collection (esclusione)
- Filtri per titolo, formato, durata, dimensione, nome file
- Dedupe via history
- Output: envion_random_raw_XXX.txt (ogni URL termina con ';')
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urlencode
import requests

# --- Directory di lavoro ------------------------------------------------------

os.chdir("/Users/emiliano/Documents/PureData/Envion-Algo-Score")

# --- Costanti -----------------------------------------------------------------

IA_SEARCH = "https://archive.org/advancedsearch.php"
IA_META   = "https://archive.org/metadata"

BBC_COLLECTIONS = ["BBCSoundEffectsComplete", "bbcsoundeffects"]

DEFAULT_EXTS = {"wav", "wave", "aiff", "aif", "flac", "mp3"}

EXCLUDED_COLLECTIONS_DEFAULT = [
    "librivoxaudio",
    "audio_bookspoetry",
    "oldtimeradio",
    "radioprograms",
    "communitypodcast",
]

# --- Utilità ------------------------------------------------------------------

def dbg(enabled, *msg):
    if enabled:
        print("[DEBUG]", *msg, file=sys.stderr, flush=True)

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def read_history_set(history_path):
    s = set()
    if history_path and os.path.isfile(history_path):
        try:
            with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    u = line.strip().rstrip(";")
                    if u:
                        s.add(u)
        except Exception:
            pass
    return s

def append_history(history_path, urls):
    if not history_path or not urls:
        return
    ensure_dir(os.path.dirname(history_path))
    with open(history_path, "a", encoding="utf-8") as f:
        for u in urls:
            f.write(u.rstrip(";") + ";\n")

def next_progressive_filename(out_dir, prefix="envion_random_raw_", ext=".txt"):
    ensure_dir(out_dir)
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+){re.escape(ext)}$")
    max_n = 0
    for n in os.listdir(out_dir):
        m = pattern.match(n)
        if m:
            try:
                max_n = max(max_n, int(m.group(1)))
            except:
                pass
    return os.path.join(out_dir, f"{prefix}{max_n+1:03d}{ext}")

def safe_get(url, timeout=30):
    return requests.get(url, timeout=timeout)

# --- Query IA -----------------------------------------------------------------

def search_docs(query_text, rows, scope, debug,
                exclude_tokens=None, exclude_collections=None,
                include_subjects=None):
    """Costruisce e invia una query avanzata su Internet Archive."""
    if scope == "bbc":
        base_q = f'(collection:({" OR ".join(BBC_COLLECTIONS)})) AND mediatype:audio'
        fl_fields = ["identifier", "title", "collection", "mediatype"]
        sort = None
        excl_cols = []
    else:
        base_q = 'mediatype:audio AND NOT collection:bbc_radio'
        fl_fields = ["identifier", "title", "collection", "mediatype", "downloads", "addeddate"]
        sort = ["downloads desc"]
        excl_cols = list(EXCLUDED_COLLECTIONS_DEFAULT)

    # aggiunte da CLI
    if exclude_collections:
        for c in exclude_collections:
            c = c.strip()
            if c and c not in excl_cols:
                excl_cols.append(c)

    q_parts = [base_q]

    # testo libero
    if query_text:
        q_parts.append(f'TEXT:{query_text}')

    # vincoli di subject
    if include_subjects:
        subjects = [f'subject:"{s.strip()}"' for s in include_subjects if s.strip()]
        if subjects:
            q_parts.append("(" + " OR ".join(subjects) + ")")

    # esclusioni nel titolo
    if exclude_tokens:
        for tok in exclude_tokens:
            tok = tok.strip()
            if tok:
                q_parts.append(f'NOT title:"{tok}"')

    # esclusioni di collection
    for col in excl_cols:
        q_parts.append(f'NOT collection:{col}')

    query = " AND ".join(q_parts)

    params = {"q": query, "rows": rows, "page": 1, "output": "json"}
    for f in fl_fields:
        params.setdefault("fl[]", []).append(f)
    if sort:
        for s in sort:
            params.setdefault("sort[]", []).append(s)

    url = IA_SEARCH + "?" + urlencode(params, doseq=True)
    dbg(debug, "search URL:", url)

    r = safe_get(url)
    r.raise_for_status()
    data = r.json()
    docs = (data.get("response") or {}).get("docs") or []
    dbg(debug, f"hits ({scope}) = {len(docs)}")
    if docs:
        dbg(debug, "first identifiers:", [d.get("identifier") for d in docs[:10]])
    return docs

def fetch_metadata(identifier, debug=False):
    r = safe_get(f"{IA_META}/{identifier}")
    r.raise_for_status()
    return r.json()

# --- Filtri -------------------------------------------------------------------

def is_good_ext(name, exts):
    return name and "." in name and name.rsplit(".", 1)[-1].lower() in exts

def length_ok(fobj, max_dur):
    if max_dur <= 0:
        return True
    l = fobj.get("length")
    if l is None:
        return True
    try:
        return float(l) <= float(max_dur)
    except:
        return True

def size_ok(fobj, max_mb):
    if max_mb <= 0:
        return True
    s = fobj.get("size")
    if s is None:
        return True
    try:
        return int(s) <= int(max_mb * 1_000_000)
    except:
        return True

def build_url(identifier, name):
    return f"https://archive.org/download/{identifier}/{name}"

# --- Raccolta URL -------------------------------------------------------------

def collect_urls(docs, count, exts, max_dur, max_mb,
                 history_set, dedupe, debug):
    out, seen = [], set()
    for d in docs:
        ident = d.get("identifier")
        if not ident:
            continue
        try:
            md = fetch_metadata(ident)
        except Exception as e:
            dbg(debug, f"metadata fail {ident}: {e}")
            continue
        files = md.get("files") or []
        for f in files:
            name = f.get("name")
            if not name or not is_good_ext(name, exts):
                continue
            if not length_ok(f, max_dur):
                continue
            if not size_ok(f, max_mb):
                continue
            url = build_url(ident, name)
            if dedupe:
                if url in seen or url.rstrip(";") in history_set:
                    continue
            out.append(url + ";")
            seen.add(url)
            if len(out) >= count:
                return out
    return out

# --- Main ---------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Fine-tuned Internet Archive search for Envion NET-AUDIO")
    ap.add_argument("--q", type=str, default="", help="termine da cercare")
    ap.add_argument("--rows", type=int, default=300)
    ap.add_argument("--count", type=int, default=8)
    ap.add_argument("--max-dur", type=float, default=0.0)
    ap.add_argument("--max-size-mb", type=float, default=10.0)
    ap.add_argument("--out-dir", type=str, required=True)
    ap.add_argument("--basename", type=str, default="")
    ap.add_argument("--history", type=str, default="")
    ap.add_argument("--dedupe", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--scope", choices=["bbc", "sitewide"], default="sitewide")
    ap.add_argument("--exclude", type=str, default="",
                    help="parole da escludere nel titolo, separate da virgola")
    ap.add_argument("--exclude-collections", type=str, default="",
                    help="collection da escludere (virgole)")
    ap.add_argument("--include-subjects", type=str, default="",
                    help="subject richiesti (virgole)")
    ap.add_argument("--formats", type=str, default="wav,wave,aiff,aif,flac,mp3")
    args = ap.parse_args()

    debug = args.debug
    ensure_dir(args.out_dir)


    exts = {x.strip().lower() for x in args.formats.split(",") if x.strip()}
    history_set = read_history_set(args.history) if args.dedupe else set()
    exclude_tokens = [t.strip() for t in args.exclude.split(",") if t.strip()]
    excl_cols = [c.strip() for c in args.exclude_collections.split(",") if c.strip()]
    incl_subj = [s.strip() for s in args.include_subjects.split(",") if s.strip()]

    dbg(debug, "exclude_collections:", excl_cols)
    dbg(debug, "include_subjects:", incl_subj)

    docs = search_docs(
        query_text=args.q,
        rows=args.rows,
        scope=args.scope,
        debug=debug,
        exclude_tokens=exclude_tokens,
        exclude_collections=excl_cols,
        include_subjects=incl_subj
    )

    if not docs:
        print("[WARN] Nessun risultato dalla ricerca.", file=sys.stderr)
        sys.exit(1)

    urls = collect_urls(
        docs, args.count, exts, args.max_dur, args.max_size_mb,
        history_set, args.dedupe, debug
    )

    if not urls:
        print("[WARN] Nessun file compatibile trovato.", file=sys.stderr)
        sys.exit(1)

    if args.basename:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(args.out_dir, f"{args.basename}_{stamp}.txt")
    else:
        out_path = next_progressive_filename(args.out_dir)

    with open(out_path, "w", encoding="utf-8") as f:
        for u in urls:
            f.write(u + ("\n" if not u.endswith("\n") else ""))

    print(out_path)

    if args.dedupe and args.history:
        append_history(args.history, urls)
        dbg(debug, f"history updated +{len(urls)}")

if __name__ == "__main__":
    main()
