#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
make_bbc_search_ia.py
Genera una lista di URL "raw" (con punto e virgola finale) da Internet Archive
per Envion NET-AUDIO.

Caratteristiche:
- Ricerca su IA via advancedsearch (collections BBC o sitewide)
- Per ogni item: /metadata/<identifier> per estrarre i file reali
- Filtri per formato e durata (se disponibile)
- Dedupe via history file + dedupe in memoria
- Output: file con nome progressivo envion_random_raw_XXX.txt in --out-dir
- Ogni URL termina con ';' come richiesto

Uso tipico (solo BBC):
  python3 make_bbc_search_ia.py \
    --q "wind" \
    --max-dur 8 \
    --count 8 \
    --rows 300 \
    --out-dir "netsound" \
    --history "netsound/netsound_history.txt" \
    --dedupe \
    --debug \
    --scope bbc

Uso sitewide (tutto IA):
  python3 make_bbc_search_ia.py \
    --q "wind" \
    --max-dur 8 \
    --count 8 \
    --rows 300 \
    --out-dir "netsound" \
    --history "netsound/netsound_history.txt" \
    --dedupe \
    --debug \
    --scope sitewide
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlencode

import requests

# --- Costanti e default -------------------------------------------------------

IA_SEARCH = "https://archive.org/advancedsearch.php"
IA_META   = "https://archive.org/metadata"

# collezioni BBC su Internet Archive (le più usate)
BBC_COLLECTIONS = [
    "BBCSoundEffectsComplete",
    "bbcsoundeffects",
]

# formati preferiti (estensioni) per Envion
DEFAULT_EXTS = {"wav", "wave", "aiff", "aif", "flac", "mp3"}

# --- Utilità ------------------------------------------------------------------

def dbg(enabled, *msg):
    if enabled:
        print("[DEBUG]", *msg, file=sys.stderr, flush=True)

def ensure_dir(path):
    if not path:
        return
    os.makedirs(path, exist_ok=True)

def read_history_set(history_path):
    s = set()
    if not history_path:
        return s
    if os.path.isfile(history_path):
        try:
            with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    url = line.strip().rstrip(";")
                    if url:
                        s.add(url)
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
    """
    Trova il prossimo nome progressivo envion_random_raw_XXX.txt
    scansionando out_dir. Se non ne trova, parte da 001.
    """
    ensure_dir(out_dir)
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+){re.escape(ext)}$")
    max_n = 0
    for name in os.listdir(out_dir):
        m = pattern.match(name)
        if m:
            try:
                n = int(m.group(1))
                if n > max_n:
                    max_n = n
            except ValueError:
                pass
    return os.path.join(out_dir, f"{prefix}{max_n+1:03d}{ext}")

def safe_get(url, timeout=30):
    return requests.get(url, timeout=timeout)

# --- Query IA -----------------------------------------------------------------

def search_docs(query_text, rows, scope, debug, no_fallback=False, exclude_tokens=None):
    """
    Ritorna il vettore 'docs' da IA advancedsearch in base allo scope.

    scope:
      - "bbc": limita a collezioni BBCSoundEffectsComplete / bbcsoundeffects
      - "sitewide": tutto IA ma solo mediatype:audio (+ qualche esclusione leggera)

    exclude_tokens: lista di parole da escludere dal titolo (sitewide)
    """
    if scope == "bbc":
        base_q = f'(collection:({" OR ".join(BBC_COLLECTIONS)})) AND mediatype:audio'
        fl_fields = ["identifier", "title", "collection", "mediatype"]
        sort = None
        # nota: no_fallback True = non allarghiamo ad altre collezioni (già fatto)
    else:
        base_q = 'mediatype:audio AND NOT collection:bbc_radio'
        fl_fields = ["identifier", "title", "collection", "mediatype", "downloads", "addeddate"]
        sort = ["downloads desc"]

    # testo libero
    text_q = f'TEXT:{query_text}' if query_text else ""
    q_parts = [base_q]
    if text_q:
        q_parts.append(text_q)

    # esclusioni di rumore nel titolo (solo sitewide ha senso)
    if scope == "sitewide" and exclude_tokens:
        for tok in exclude_tokens:
            tok = tok.strip()
            if tok:
                # escludiamo match basilari su title
                q_parts.append(f'NOT title:"{tok}"')

    query = " AND ".join(q_parts)

    params = {
        "q": query,
        "rows": rows,
        "page": 1,
        "output": "json",
    }
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
    url = f"{IA_META}/{identifier}"
    r = safe_get(url)
    r.raise_for_status()
    data = r.json()
    return data

def files_from_metadata(md):
    """Ritorna lista di dict file da md['files'] (o [])"""
    return md.get("files") or []

# --- Filtri file --------------------------------------------------------------

def is_good_ext(name, wanted_exts):
    if not name or "." not in name:
        return False
    ext = name.rsplit(".", 1)[-1].lower()
    return ext in wanted_exts

def length_ok(fobj, max_dur):
    """
    max_dur <= 0: nessun limite
    se disponibile, usa 'length' (in secondi) nel file object; se assente, passa.
    """
    if max_dur is None or max_dur <= 0:
        return True
    length = fobj.get("length")
    if length is None:
        # spesso mancante: se non c'è, non blocchiamo
        return True
    try:
        return float(length) <= float(max_dur)
    except Exception:
        return True

def build_download_url(identifier, name):
    return f"https://archive.org/download/{identifier}/{name}"

# --- Selezione file -----------------------------------------------------------

def collect_urls_from_docs(docs, count, wanted_exts, max_dur, history_set, dedupe, debug):
    """
    Scorre i docs, legge /metadata, filtra i file e restituisce fino a 'count' URL unici.
    Aggiunge ';' alla fine di ciascun URL.
    """
    out = []
    seen = set()

    for doc in docs:
        ident = doc.get("identifier")
        if not ident:
            continue
        try:
            md = fetch_metadata(ident, debug=debug)
        except Exception as e:
            dbg(debug, f"metadata error for {ident}: {e}")
            continue

        files = files_from_metadata(md)
        if not files:
            continue

        for f in files:
            name = f.get("name")
            if not name:
                continue
            if not is_good_ext(name, wanted_exts):
                continue
            if not length_ok(f, max_dur):
                continue

            url = build_download_url(ident, name)

            # dedupe: history + turno corrente
            if dedupe:
                if url in seen:
                    continue
                if url.rstrip(";") in history_set:
                    dbg(debug, "skip (history):", url)
                    continue

            out.append(url + ";")
            seen.add(url)

            if len(out) >= count:
                return out

    return out

# --- Main ---------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Generate raw URL lists from Internet Archive (BBC or sitewide) for Envion NET-AUDIO.")
    ap.add_argument("--q", type=str, default="", help="testo da cercare (es. wind, drums, wood)")
    ap.add_argument("--rows", type=int, default=300, help="righe per advancedsearch (default 300)")
    ap.add_argument("--count", type=int, default=8, help="quanti URL finali generare (default 8)")
    ap.add_argument("--max-dur", type=float, default=0.0, help="durata massima (sec); 0 = nessun limite")
    ap.add_argument("--out-dir", type=str, required=True, help="cartella di output per il file lista")
    ap.add_argument("--basename", type=str, default="", help="basename opzionale per il file (senza numero). Se vuoto usa envion_random_raw_XXX.txt")
    ap.add_argument("--history", type=str, default="", help="file di history per dedupe")
    ap.add_argument("--dedupe", action="store_true", help="evita URL già presenti in history e duplicati nel run")
    ap.add_argument("--debug", action="store_true", help="stampa log di debug")
    ap.add_argument("--no-fallback", action="store_true", help="(compat) non allargare ad altre collezioni quando in scope bbc")
    ap.add_argument("--scope", choices=["bbc", "sitewide"], default="bbc",
                    help="bbc = solo collezioni BBC (default); sitewide = tutto IA (audio)")
    ap.add_argument("--exclude", type=str, default="",
                    help='(sitewide) parole da escludere dal titolo, separate da virgola, es: "podcast,sermon,radio"')
    ap.add_argument("--formats", type=str, default="wav,wave,aiff,aif,flac,mp3",
                    help="estensioni accettate separate da virgola")
    args = ap.parse_args()

    debug = args.debug

    # setup
    ensure_dir(args.out_dir)
    wanted_exts = {e.strip().lower() for e in args.formats.split(",") if e.strip()}
    if not wanted_exts:
        wanted_exts = set(DEFAULT_EXTS)

    # history per dedupe
    history_set = read_history_set(args.history) if args.dedupe else set()
    dbg(debug, "dedupe=", args.dedupe, "history_count=", len(history_set))

    # exclude tokens
    exclude_tokens = []
    if args.exclude:
        exclude_tokens = [t.strip() for t in args.exclude.split(",") if t.strip()]
        dbg(debug, "exclude tokens:", exclude_tokens)

    # 1) advancedsearch
    try:
        docs = search_docs(
            query_text=args.q,
            rows=args.rows,
            scope=args.scope,
            debug=debug,
            no_fallback=args.no_fallback,
            exclude_tokens=exclude_tokens
        )
    except Exception as e:
        print(f"[ERROR] search failed: {e}", file=sys.stderr)
        sys.exit(2)

    if not docs:
        print("[WARN] Nessun risultato dalla ricerca.", file=sys.stderr)
        # usciamo generando file vuoto per coerenza?
        # meglio uscire con codice 1
        sys.exit(1)

    # 2) metadata -> filtra -> raccogli URL
    urls = collect_urls_from_docs(
        docs=docs,
        count=args.count,
        wanted_exts=wanted_exts,
        max_dur=args.max_dur,
        history_set=history_set,
        dedupe=args.dedupe,
        debug=debug
    )

    if not urls:
        print("[WARN] Nessun file compatibile trovato (formato/durata/dedupe).", file=sys.stderr)
        sys.exit(1)

    # 3) output file
    if args.basename:
        # se l'utente fornisce un basename, aggiungiamo timestamp per non sovrascrivere
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(args.out_dir, f"{args.basename}_{stamp}.txt")
    else:
        out_path = next_progressive_filename(args.out_dir, prefix="envion_random_raw_", ext=".txt")

    with open(out_path, "w", encoding="utf-8") as f:
        for u in urls:
            f.write(u + ("\n" if not u.endswith("\n") else ""))

    print(out_path)

    # 4) aggiorna history
    if args.dedupe and args.history:
        append_history(args.history, urls)
        dbg(debug, f"history updated: +{len(urls)}")

if __name__ == "__main__":
    main()
