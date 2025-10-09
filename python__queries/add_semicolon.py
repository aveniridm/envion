#!/usr/bin/env python3
import pathlib

NETSOUND_DIR = pathlib.Path("netsound")

def ensure_semicolon(url: str) -> str:
    u = url.strip()
    if not u:
        return ""
    if not u.endswith(";"):
        u += ";"
    return u

def process_file(p: pathlib.Path):
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    fixed = [ensure_semicolon(line) for line in lines if line.strip()]
    if fixed == lines:
        return
    backup = p.with_suffix(p.suffix + ".bak")
    backup.write_text("\n".join(lines) + "\n", encoding="utf-8")
    p.write_text("\n".join(fixed) + "\n", encoding="utf-8")
    print(f"✓ {p.name}: aggiunti ; dove mancavano ({len(fixed)} righe)")

def main():
    files = sorted(NETSOUND_DIR.glob("*.txt"))
    if not files:
        print("Nessun file .txt trovato in netsound/")
        return
    for f in files:
        process_file(f)
    print("✓ Tutti i file controllati.")

if __name__ == "__main__":
    main()
