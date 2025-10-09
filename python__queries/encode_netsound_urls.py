import sys, re, pathlib
from urllib.parse import urlsplit, urlunsplit, quote

def encode_url(u: str) -> str:
    u = u.strip().rstrip(';')  # via i ; finali
    if not u:
        return u
    parts = urlsplit(u)
    # Encoda path e filename preservando /-_.~
    path_enc = quote(parts.path, safe="/-_.~")
    # (opzionale) encoda anche query e fragment se presenti
    query_enc = quote(parts.query, safe="=&-_.~")
    frag_enc = quote(parts.fragment, safe="-_.~")
    return urlunsplit((parts.scheme, parts.netloc, path_enc, query_enc, frag_enc))

def process(infile):
    p = pathlib.Path(infile)
    out = p.with_name(p.stem + "_encoded" + p.suffix)
    with open(infile, "r", encoding="utf-8") as f, open(out, "w", encoding="utf-8") as g:
        for line in f:
            g.write(encode_url(line) + "\n")
    print(f"✓ Encodate e salvate in: {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 encode_netsound_urls.py <file_lista.txt>")
        sys.exit(1)
    process(sys.argv[1])
