# -*- coding: utf-8 -*-
"""Poskládá ke každému číslu magazínu obálku z obalů her, které v něm jsou.

Nic se nestahuje — bere se, co už v public/images/games je. Přednost mají hry
ze žebříčku čísla: to jsou tituly, kvůli kterým si člověk číslo otevře, takže
patří na obálku.

Výstup: public/images/magazine/<id>.webp  (1200×480, poměr karty na webu)
Použití: python tools/magazine_art.py [--force]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "magazine"

W, H = 1200, 480
SLOTS = 5
CARD_H = 340
MIN_COVERS = 3


def _year(g):
    m = re.search(r"(19|20)\d{2}", str(g.get("year") or ""))
    return int(m.group(0)) if m else 0


def pick_spread(items, n):
    if len(items) <= n:
        return items
    step = (len(items) - 1) / (n - 1)
    return [items[round(i * step)] for i in range(n)]


def main() -> int:
    from PIL import Image, ImageFilter

    force = "--force" in sys.argv
    ledger = json.loads((ROOT / "src/data/magazine.json").read_text("utf-8"))
    texts_file = ROOT / "src/data/magazine_text.json"
    texts = json.loads(texts_file.read_text("utf-8")) if texts_file.exists() else {}
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    gmap = {g["slug"]: (g, p) for p in data["platforms"] for g in p["games"]}
    OUT.mkdir(parents=True, exist_ok=True)

    made = skipped = 0
    for v in ledger["vydani"]:
        cid = v["id"]
        dst = OUT / f"{cid}.webp"
        if dst.exists() and not force:
            continue
        # cislo bez textu se na webu neukazuje, obalka by byla zbytecna
        if cid not in texts:
            continue

        # hry ze zebricku napred, zbytek cisla za nimi
        top = [z["slug"] for z in texts[cid].get("zebricek") or []]
        poradi = top + [s for s in v["hry"] if s not in top]
        s_obalem = [gmap[s] for s in poradi if s in gmap and gmap[s][0].get("image")]

        # tentyz titul byva na vic platformach se stejnym obalem
        seen, uniq = set(), []
        for g, p in s_obalem:
            key = P.norm_name(g["name"])
            if key in seen:
                continue
            seen.add(key)
            uniq.append((g, p))

        if len(uniq) < MIN_COVERS:
            skipped += 1
            print(f"  [-] {cid}: jen {len(uniq)} obalů")
            continue

        # zebricek si drzi poradi, zbytek se rozprostre podle roku
        hlavni, ostatni = uniq[:len(top)], uniq[len(top):]
        ostatni.sort(key=lambda x: _year(x[0]) or x[1]["year"])
        picked = pick_spread(hlavni + ostatni, SLOTS)

        c1 = picked[0][1].get("color2") or "#181c26"
        c2 = picked[-1][1].get("color") or "#2a3040"
        base = Image.new("RGB", (W, H), c1)
        top_layer = Image.new("RGB", (W, H), c2)
        mask = Image.linear_gradient("L").rotate(-90, expand=True).resize((W, H))
        base = Image.composite(top_layer, base, mask)
        base = base.filter(ImageFilter.GaussianBlur(2))

        cards = []
        for g, _p in picked:
            src = ROOT / "public" / g["image"].lstrip("/")
            if not src.exists():
                continue
            try:
                im = Image.open(src).convert("RGBA")
            except Exception:  # noqa: BLE001
                continue
            ratio = CARD_H / im.height
            cards.append(im.resize((max(1, int(im.width * ratio)), CARD_H), Image.LANCZOS))
        if not cards:
            continue

        MARGIN = 40
        avail = W - 2 * MARGIN
        total = sum(c.width for c in cards)
        if total > avail:
            k = avail / total
            cards = [c.resize((max(1, int(c.width * k)), max(1, int(c.height * k))), Image.LANCZOS)
                     for c in cards]
            total = sum(c.width for c in cards)
        gap = (avail - total) // max(1, len(cards) - 1) if len(cards) > 1 else 0
        x = MARGIN + (avail - total - gap * (len(cards) - 1)) // 2
        for c in cards:
            y = (H - c.height) // 2
            shadow = Image.new("RGBA", (c.width + 24, c.height + 24), (0, 0, 0, 0))
            shadow.paste((0, 0, 0, 120), (12, 12, c.width + 12, c.height + 12))
            shadow = shadow.filter(ImageFilter.GaussianBlur(9))
            base.paste(shadow, (x - 12, y - 12), shadow)
            base.paste(c, (x, y), c)
            x += c.width + gap

        base.save(dst, "WEBP", quality=86, method=6)
        made += 1
        print(f"  [OK] {cid}  ({len(cards)} obalů)")

    print(f"\nobálek vyrobeno: {made}, přeskočeno pro málo obalů: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
