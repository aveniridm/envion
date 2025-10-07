# presets_admin.py
import os, json, hmac, hashlib

PRESETS_JSON = "netsound/presets.json"
PRESETS_SIG  = "netsound/presets.sig"
SECRET_PATH  = "netsound/presets.key"

def _load_secret():
    os.makedirs("netsound", exist_ok=True)
    if not os.path.exists(SECRET_PATH):
        with open(SECRET_PATH, "wb") as f:
            f.write(os.urandom(32))
    return open(SECRET_PATH, "rb").read()

def canonical_dump(obj)->bytes:
    # JSON canonico e stabile
    return json.dumps(obj, sort_keys=True, separators=(",",":")).encode("utf-8")

def sign():
    secret = _load_secret()
    data = json.load(open(PRESETS_JSON, "r"))
    sig = hmac.new(secret, canonical_dump(data), hashlib.sha256).hexdigest()
    with open(PRESETS_SIG, "w") as f:
        f.write(sig)
    print("[admin] Presets firmati con successo.")
    print(f"Firma salvata in {PRESETS_SIG}")

if __name__ == "__main__":
    sign()
