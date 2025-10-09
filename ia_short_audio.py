#!/usr/bin/env python3
import sys, json, time, urllib.parse
from urllib.request import urlopen, Request

# Script "tutto in uno":
# 1) interroga archive.org/advancedsearch per ottenere gli identifier
# 2) per ogni identifier scarica i metadata e filtra i file audio con length <= max_seconds
# 3) stampa le URL dirette con ; finale (ok per Envion)

ADV_URL = "https://archive.org/advancedsearch.php"
META_BASE = "https://archive.org/metadata/"
DOWNLOAD_BASE = "https://archive.org/download/"

DEFAULT_FIELDS = ["identifier"]
DEFAULT_ROWS = 50
DEFAULT_PAGES = 2
DEFAULT_MAX_SECONDS = 7.0
DEFAULT_EXT = {".mp3", ".wav", ".flac", ".ogg"}

def http_json(url):
    req = Request(url, headers={"User-Agent":"Envion-IA/1.0"})
    with urlopen(req) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))

def adv_search(q, rows=DEFAULT_ROWS, pages=DEFAULT_PAGES):
    ids = []
    for page in range(1, pages+1):
        params = {
            "q": q,
            "fl[]": DEFAULT_FIELDS,
            "output": "json",
            "rows": str(rows),
            "page": str(page),
        }
        url = ADV_URL + "?" + urllib.parse.urlencode(params, doseq=True)
        data = http_json(url)
        docs = data.get("response", {}).get("docs", [])
        for d in docs:
            ident = d.get("identifier")
            if ident:
                ids.append(ident)
        time.sleep(0.15)  # rate limit gentile
    return ids

def file_url(identifier, filename):
    return DOWNLOAD_BASE + identifier + "/" + urllib.parse.quote(filename) + ";"

def fetch_meta(identifier):
    url = META_BASE + urllib.parse.quote(identifier)
    return http_json(url)

def is_small_file(f, max_seconds, allow_ext):
    name = f.get("name","")
    if "." not in name:
        return False
    ext = "." + name.split(".")[-1].lower()
    if ext not in allow_ext:
        return False
    length = f.get("length", None)
    try:
        sec = float(length) if length is not None else None
    except:
        sec = None
    return (sec is not None) and (sec <= max_seconds)

def run(q, rows, pages, max_seconds, allow_ext):
    identifiers = adv_search(q, rows=rows, pages=pages)
    for ident in identifiers:
        try:
            meta = fetch_meta(ident)
            files = meta.get("files", [])
            for f in files:
                if is_small_file(f, max_seconds, allow_ext):
                    print(file_url(ident, f["name"]))
            time.sleep(0.1)
        except Exception as e:
            print(f"# errore su {ident}: {e}", file=sys.stderr)

def parse_args(argv):
    # parsing minimale (senza argparse per compatibilità massima)
    q = None
    rows = DEFAULT_ROWS
    pages = DEFAULT_PAGES
    max_seconds = DEFAULT_MAX_SECONDS
    allow_ext = set(DEFAULT_EXT)
    out_path = None

    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--q":
            i += 1; q = argv[i]
        elif a == "--rows":
            i += 1; rows = int(argv[i])
        elif a == "--pages":
            i += 1; pages = int(argv[i])
        elif a == "--max-seconds":
            i += 1; max_seconds = float(argv[i])
        elif a == "--ext":
            i += 1
            allow_ext = set()
            for part in argv[i].split(","):
                part = part.strip().lower()
                if not part.startswith("."):
                    part = "." + part
                allow_ext.add(part)
        elif a == "--out":
            i += 1; out_path = argv[i]
        else:
            print(f"# argomento sconosciuto: {a}", file=sys.stderr)
        i += 1

    if not q:
        print("Uso:\n  python3 ia_short_audio.py --q '<query advancedsearch>' [--rows 50] [--pages 2] [--max-seconds 7] [--ext mp3,wav,flac,ogg] [--out path]\n", file=sys.stderr)
        sys.exit(1)
    return q, rows, pages, max_seconds, allow_ext, out_path

if __name__ == "__main__":
    q, rows, pages, max_seconds, allow_ext, out_path = parse_args(sys.argv)
    if out_path:
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run(q, rows, pages, max_seconds, allow_ext)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(buf.getvalue())
    else:
        run(q, rows, pages, max_seconds, allow_ext)
