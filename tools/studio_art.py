# -*- coding: utf-8 -*-
"""Poskládá ke každému studiu obrázek z obalů jeho her (stejně jako series_art.py).

Nic se nestahuje — bere se, co už v public/images/games je. Hry se vybírají
rovnoměrně po časové ose, aby byl vidět rozsah tvorby studia.

Výstup: public/images/studios/<slug>.webp
Použití: python tools/studio_art.py [--min 3]
"""
import json, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "studios"

MIN_COVERS = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 3
# musí odpovídat STUDIO_MIN a studioSlug v src/lib/data.ts, jinak by obrázky
# nesedly na stránky studií
STUDIO_MIN = 3
STUDIO_SKIP = {"komunita", "various", "ruzni", "ruzne", ""}
W, H = 1200, 420
SLOTS = 6
CARD_H = 300


def studio_slug(name):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _year(g):
    m = re.search(r"(19|20)\d{2}", str(g.get("year") or ""))
    return int(m.group(0)) if m else 0


def pick_spread(items, n):
    if len(items) <= n:
        return items
    step = (len(items) - 1) / (n - 1)
    return [items[round(i * step)] for i in range(n)]


def main():
    from PIL import Image, ImageFilter

    d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    groups = {}
    for plat in d["platforms"]:
        for g in plat["games"]:
            raw = (g.get("studio") or "").strip()
            if not raw:
                continue
            slug = studio_slug(raw)
            if slug in STUDIO_SKIP:
                continue
            groups.setdefault(slug, {"name": raw, "games": []})["games"].append((g, plat))

    made = skipped = 0
    for slug, grp in sorted(groups.items()):
        if len(grp["games"]) < STUDIO_MIN:
            continue
        withimg = [(g, p) for g, p in grp["games"] if g.get("image")]
        if len(withimg) < MIN_COVERS:
            skipped += 1
            continue

        withimg.sort(key=lambda x: _year(x[0]) or x[1]["year"])
        seen, uniq = set(), []
        for g, p in withimg:
            k = P.norm_name(g["name"])
            if k in seen:
                continue
            seen.add(k)
            uniq.append((g, p))
        if len(uniq) < MIN_COVERS:
            skipped += 1
            continue
        picked = pick_spread(uniq, SLOTS)

        c1 = picked[0][1].get("color2") or "#181c26"
        c2 = picked[-1][1].get("color") or "#2a3040"
        base = Image.new("RGB", (W, H), c1)
        top = Image.new("RGB", (W, H), c2)
        mask = Image.linear_gradient("L").rotate(-90, expand=True).resize((W, H))
        base = Image.composite(top, base, mask)
        base = base.filter(ImageFilter.GaussianBlur(2))

        cards = []
        for g, _p in picked:
            src = ROOT / "public" / g["image"].lstrip("/")
            if not src.exists():
                continue
            try:
                im = Image.open(src).convert("RGBA")
            except Exception:
                continue
            k = CARD_H / im.height
            cards.append(im.resize((max(1, int(im.width * k)), CARD_H), Image.LANCZOS))
        if len(cards) < MIN_COVERS:
            skipped += 1
            continue

        MARGIN = 36
        avail = W - 2 * MARGIN
        total = sum(c.width for c in cards)
        if total > avail:
            k = avail / total
            cards = [c.resize((max(1, int(c.width * k)), max(1, int(c.height * k))), Image.LANCZOS)
                     for c in cards]
            total = sum(c.width for c in cards)
        gap = (avail - total) // max(1, len(cards) - 1) if len(cards) > 1 else 0
        x = MARGIN
        for c in cards:
            y = (H - c.height) // 2
            sh = Image.new("RGBA", (c.width + 24, c.height + 24), (0, 0, 0, 0))
            sh.paste((0, 0, 0, 120), (12, 12, c.width + 12, c.height + 12))
            sh = sh.filter(ImageFilter.GaussianBlur(9))
            base.paste(sh, (x - 12, y - 12), sh)
            base.paste(c, (x, y), c)
            x += c.width + gap

        base.save(OUT / f"{slug}.webp", "WEBP", quality=82, method=6)
        made += 1

    print(f"obrázky studií: vytvořeno {made}, přeskočeno {skipped} (málo obalů)")
    print(f"výstup: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
