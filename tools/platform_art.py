# -*- coding: utf-8 -*-
"""Poskládá k platformě pás z obalů jejích her (jako tools/series_art.py pro série).

Hodí se tam, kde fotka hardwaru moc neřekne — u PC je „fotka počítače" jen béžová
skříň, zatímco obaly her nesou dobovou atmosféru.

Výstup: public/images/platforms/extra/<slug>-games.webp
Použití: python tools/platform_art.py <slug[,slug...]>
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "platforms" / "extra"

W, H = 1200, 420
SLOTS = 6
CARD_H = 300


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

    if len(sys.argv) < 2:
        print(__doc__)
        return
    wanted = set(sys.argv[1].split(","))
    d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    for plat in d["platforms"]:
        if plat["slug"] not in wanted:
            continue
        withimg = [g for g in plat["games"] if g.get("image")]
        if len(withimg) < 3:
            print(f"  [-] {plat['slug']}: jen {len(withimg)} obalů")
            continue
        withimg.sort(key=lambda g: _year(g) or plat["year"])
        # tentyz titul byva v katalogu vickrat -> nech z kazdeho jen prvni
        seen, uniq = set(), []
        for g in withimg:
            k = P.norm_name(g["name"])
            if k in seen:
                continue
            seen.add(k)
            uniq.append(g)
        picked = pick_spread(uniq, SLOTS)

        base = Image.new("RGB", (W, H), plat.get("color2") or "#16181f")
        top = Image.new("RGB", (W, H), plat.get("color") or "#2a3040")
        mask = Image.linear_gradient("L").rotate(-90, expand=True).resize((W, H))
        base = Image.composite(top, base, mask)
        base = base.filter(ImageFilter.GaussianBlur(2))

        cards = []
        for g in picked:
            src = ROOT / "public" / g["image"].lstrip("/")
            if not src.exists():
                continue
            try:
                im = Image.open(src).convert("RGBA")
            except Exception:
                continue
            k = CARD_H / im.height
            cards.append(im.resize((max(1, int(im.width * k)), CARD_H), Image.LANCZOS))
        if not cards:
            print(f"  [-] {plat['slug']}: obaly se nepodařilo načíst")
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

        dst = OUT / f"{plat['slug']}-games.webp"
        base.save(dst, "WEBP", quality=82, method=6)
        names = ", ".join(g["name"][:22] for g in picked)
        print(f"  [OK] {plat['slug']}: {dst.name}  ({names})")


if __name__ == "__main__":
    main()
