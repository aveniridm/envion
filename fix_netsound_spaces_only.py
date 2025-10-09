#!/usr/bin/env python3
import pathlib
from urllib.parse import urlsplit, urlunsplit, quote

NETSOUND_DIR = pathlib.Path("netsound")

def fix_spaces_only(url: str) -> str:
    url = url.strip().rstrip(';')
    if " " not in url:
        return url
    try:
        s = urlsplit(url)
        path = quote(s.path, safe="/-_.~")
        return urlunsplit((s.scheme, s.netloc, path, s.query, s.fragment))
    except Exception:
        return url

def process_file(p: pathlib.Path):
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    fixed, changed = [], 0
    for line in lines:
        new = fix_spaces_only(line)
        if new != line:
            changed += 1
        fixed.append(new)
    if changed == 0:
        return
    backup = p.with_suffix(p.suffix + ".bak")
    backup.write_text("\n".join(lines) + "\n", encoding="utf-8")
    p.write_text("\n".join(fixed) + "\n", encoding="utf-8")
    print(f"✓ {p.name}: {changed} URL con spazi corretti")

def main():
    for f in sorted(NETSOUND_DIR.glob("*.txt")):
        process_file(f)

if __name__ == "__main__":
    main()
