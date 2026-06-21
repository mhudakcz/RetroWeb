# -*- coding: utf-8 -*-
"""Stáhne náhledy kazet PICO-8 her z Lexaloffle BBS (cat=7).
Náhledy (thumbs/pico8_*.png) jsou label art kazet — ideální „obal".
Páruje podle názvu v souboru; výsledek je nutné vizuálně ověřit."""
import json, re, sys, time, urllib.parse, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "games" / "pico-8"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (RetroWeb personal retro site image fetch)"


def get(url, binary=False):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def search_thumbs(term):
    q = urllib.parse.urlencode({"search": term, "cat": "7"})
    html = get("https://www.lexaloffle.com/bbs/?" + q)
    # zachovej pořadí, bez duplicit
    seen, out = set(), []
    for m in re.finditer(r"thumbs/(pico8_[A-Za-z0-9_.-]+|pico\d+)\.png", html):
        f = m.group(0)
        if f not in seen:
            seen.add(f); out.append(f)
    return out


def pick(name, thumbs):
    """Vyber náhled, jehož název souboru nejlíp sedí na jméno hry."""
    key = P.norm_name(name)
    best, best_sc = None, -1.0
    for t in thumbs[:12]:
        stem = t.split("/")[-1][:-4]
        named = stem.startswith("pico8_")
        cand = stem[6:] if named else stem
        cand = re.sub(r"-\d+$", "", cand).replace("_", " ")
        sc = P.match_metrics(name, cand)[0]
        if named:
            sc += 0.15  # pojmenované thumbnaily jsou spolehlivější než pico12345
        if sc > best_sc:
            best_sc, best = sc, t
    return best, best_sc


games = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
pico = next(p for p in games["platforms"] if p["slug"] == "pico-8")
log = []
for g in pico["games"]:
    if g.get("image"):
        continue
    # vyčisti název pro hledání (vezmi část před '/', bez 'pico')
    term = re.split(r"[/(]", g["name"])[0].strip()
    term = re.sub(r"\bpico-?8?\b", "", term, flags=re.I).strip() or g["name"]
    try:
        thumbs = search_thumbs(term)
    except Exception as e:
        print(f"  [x] {g['name']}: {e}"); continue
    if not thumbs:
        print(f"  [--] {g['name']}: nic ({term})"); continue
    fn, sc = pick(g["name"], thumbs)
    url = "https://www.lexaloffle.com/bbs/" + fn
    dest = OUT / f"{g['slug']}.png"
    try:
        img = get(url, binary=True)
        if len(img) < 800:
            print(f"  [x] {g['name']}: prázdné"); continue
        dest.write_bytes(img)
        log.append((g["name"], fn, round(sc, 2)))
        print(f"  [OK] {g['name']:24} <- {fn}  (skore {sc:.2f})")
        time.sleep(0.3)
    except Exception as e:
        print(f"  [x] {g['name']}: {e}")
print(f"\nStaženo {len(log)} náhledů PICO-8. OVĚŘIT VIZUÁLNĚ a smazat špatné.")
