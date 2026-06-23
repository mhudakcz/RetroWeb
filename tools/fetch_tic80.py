# -*- coding: utf-8 -*-
"""Stáhne cover.gif kazet TIC-80 z tic80.com (oficiální stránka, kde autoři
kazety veřejně sdílejí). Páruje podle názvu (první výsledek hledání), ukládá
jako <slug>.png. Nutno vizuálně ověřit a smazat falešné."""
import json, re, sys, time, io, subprocess, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "games" / "tic-80"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (RetroWeb personal retro site)"


def get(url, binary=False):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def clean(name):
    t = re.split(r"[/(\[]", name)[0]
    return t.strip() or name


d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
tic = next(p for p in d["platforms"] if p["slug"] == "tic-80")
from PIL import Image
ok = 0
for g in tic["games"]:
    dest = OUT / f"{g['slug']}.png"
    if dest.exists() or (OUT / f"{g['slug']}.webp").exists():
        continue
    term = clean(g["name"])
    html = get("https://tic80.com/play?" + urllib.parse.urlencode({"search": term}))
    m = re.findall(r"cart/([0-9a-f]{16,})/cover\.gif", html)
    if not m:
        print(f"  [--] {g['name']}: nic ({term})"); continue
    url = f"https://tic80.com/cart/{m[0]}/cover.gif"
    try:
        img = get(url, binary=True)
        im = Image.open(io.BytesIO(img))  # ověř, že je to obrázek
        im.seek(0)
        im = im.convert("RGB")
        im.thumbnail((480, 480), Image.LANCZOS)
        im.save(dest)
        ok += 1
        print(f"  [OK] {g['name']:22} <- {m[0][:10]}")
        time.sleep(0.25)
    except Exception as e:
        print(f"  [x] {g['name']}: {e}")
print(f"\nStaženo {ok} TIC-80 obalů. OVĚŘIT VIZUÁLNĚ.")
