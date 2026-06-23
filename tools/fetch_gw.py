# -*- coding: utf-8 -*-
"""Najde fotky Game & Watch LCD jednotek na Wikimedia Commons (foto přístroje
se hrou). Páruje podle názvu, ukládá jako game-watch/<slug>.png. Ověřit vizuálně."""
import json, re, sys, time, subprocess, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "games" / "game-watch"
OUT.mkdir(parents=True, exist_ok=True)
UA = "RetroWeb-imagefetch/1.0 (personal retro gaming site)"


def get(url, binary=False):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def clean(name):
    return re.sub(r"\(g&w\)|\(g&w.*?\)|\(.*?\)", "", name, flags=re.I).strip()


def search(term, limit=12):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "list": "search",
                                "srsearch": term, "srnamespace": "6", "srlimit": str(limit)})
    url = "https://commons.wikimedia.org/w/api.php?" + q
    for attempt in range(4):
        raw = get(url)
        try:
            data = json.loads(raw)
            return [x["title"] for x in data.get("query", {}).get("search", [])]
        except Exception:
            time.sleep(1.5 * (attempt + 1))  # rate-limit -> počkej a zkus znovu
    return []


def thumb(filetitle, width=760):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": filetitle,
                                "prop": "imageinfo", "iiprop": "url|mime", "iiurlwidth": str(width)})
    raw = get("https://commons.wikimedia.org/w/api.php?" + q)
    try:
        data = json.loads(raw)
    except Exception:
        return None
    for pg in data.get("query", {}).get("pages", {}).values():
        info = (pg.get("imageinfo") or [{}])[0]
        if info.get("mime") in ("image/jpeg", "image/png"):
            return info.get("thumburl") or info.get("url")
    return None


d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
gw = next(p for p in d["platforms"] if p["slug"] == "game-watch")
ok = 0
for g in gw["games"]:
    dest = OUT / f"{g['slug']}.png"
    if dest.exists():
        continue
    title = clean(g["name"])
    cands = []
    for term in (f"Game and Watch {title}", f"Game & Watch {title}", f"{title} Game and Watch"):
        try:
            cands = search(term)
        except Exception:
            cands = []
        if cands:
            break
    # vyber soubor, jehož název nejlíp sedí na "game watch <title>" a je to foto
    best, best_sc = None, -1.0
    want = P.norm_name("game and watch " + title)
    for f in cands:
        fn = f.replace("File:", "")
        if re.search(r"\.(svg|ogg|webm|pdf)$", fn, re.I):
            continue
        sc = P.match_metrics(want, P.norm_name(fn))[0]
        if "game" in fn.lower() and "watch" in fn.lower():
            sc += 0.2
        if sc > best_sc:
            best_sc, best = sc, f
    if not best or best_sc < 0.45:
        print(f"  [--] {g['name']}: bez jisté shody (kandidáti: {cands[:3]})")
        continue
    url = thumb(best)
    if not url:
        print(f"  [--] {g['name']}: bez URL ({best})")
        continue
    try:
        img = get(url, binary=True)
        if len(img) < 1500:
            print(f"  [x] {g['name']}: malý soubor"); continue
        import io
        from PIL import Image
        try:
            Image.open(io.BytesIO(img)).verify()  # ověř, že to je reálný obrázek (ne HTML chyba)
        except Exception:
            print(f"  [x] {g['name']}: není obrázek (asi rate-limit HTML)"); time.sleep(2); continue
        dest.write_bytes(img)
        ok += 1
        print(f"  [OK] {g['name']:28} <- {best.replace('File:', '')}  ({best_sc:.2f})")
        time.sleep(0.2)
    except Exception as e:
        print(f"  [x] {g['name']}: {e}")
print(f"\nStaženo {ok} G&W fotek. OVĚŘIT VIZUÁLNĚ.")
