# -*- coding: utf-8 -*-
"""Poskládá ke každé sérii obrázek z obalů jejích dílů.

Nic se nestahuje — bere se, co už v public/images/games je. Vybírá se napříč
časovou osou série, aby na obrázku byl vidět i vývoj obalů, ne pět verzí jedné hry.

Výstup: public/images/series/<slug>.webp
Použití: python tools/series_art.py [--min 3]
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "series"

MIN_COVERS = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 3
W, H = 1200, 480          # poměr karty na webu
SLOTS = 5                 # kolik obalů se vejde
CARD_H = 340              # výška obalu na plátně


def series_hits(sdef, games):
    rx = [re.compile(r"(?<![a-z0-9])" + re.escape(m.lower()) + r"(?![a-z0-9])")
          for m in sdef["match"]]
    skip = [e.lower() for e in sdef.get("exclude", [])]
    out = []
    for g, p in games:
        low = g["name"].lower()
        if any(e in low for e in skip):
            continue
        if any(r.search(low) for r in rx):
            out.append((g, p))
    return out


def _year(g):
    """Rok jako cislo; v datech se najde i '1999/2000' nebo '199x'."""
    m = re.search(r"(19|20)\d{2}", str(g.get("year") or ""))
    return int(m.group(0)) if m else 0


def pick_spread(items, n):
    """Vybere n prvků rovnoměrně z časově seřazeného seznamu (ne n nejstarších)."""
    if len(items) <= n:
        return items
    step = (len(items) - 1) / (n - 1)
    return [items[round(i * step)] for i in range(n)]


def main():
    from PIL import Image, ImageFilter

    d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    defs = json.loads((ROOT / "src/data/series.json").read_text("utf-8"))
    games = [(g, p) for p in d["platforms"] for g in p["games"]]
    OUT.mkdir(parents=True, exist_ok=True)

    made = skipped = 0
    for sdef in defs:
        hits = series_hits(sdef, games)
        if len(hits) < 4:
            continue
        withimg = [(g, p) for g, p in hits if g.get("image")]
        if len(withimg) < MIN_COVERS:
            skipped += 1
            print(f"  [-] {sdef['name']}: jen {len(withimg)} obalů")
            continue

        withimg.sort(key=lambda x: _year(x[0]) or x[1]["year"])
        # tentyz titul je casto na vic platformach se stejnym obalem — na obrazku
        # by se pak Doom Eternal objevil dvakrat. Nech z kazdeho titulu jen prvni.
        seen, uniq = set(), []
        for g, pl in withimg:
            key = P.norm_name(g["name"])
            if key in seen:
                continue
            seen.add(key)
            uniq.append((g, pl))
        picked = pick_spread(uniq, SLOTS)

        # pozadí z barev platforem prvního a posledního dílu
        c1 = picked[0][1].get("color2") or "#181c26"
        c2 = picked[-1][1].get("color") or "#2a3040"
        base = Image.new("RGB", (W, H), c1)
        top = Image.new("RGB", (W, H), c2)
        mask = Image.linear_gradient("L").rotate(-90, expand=True).resize((W, H))
        base = Image.composite(top, base, mask)
        base = base.filter(ImageFilter.GaussianBlur(2))

        # obaly maji rozdilne pomery stran, takze se layout pocita ze skutecnych
        # sirek: nejdriv sjednotit vysku, pak podle souctu sirek dopocitat rozestup
        cards = []
        for g, p in picked:
            src = ROOT / "public" / g["image"].lstrip("/")
            if not src.exists():
                continue
            try:
                im = Image.open(src).convert("RGBA")
            except Exception:
                continue
            ratio = CARD_H / im.height
            cards.append(im.resize((max(1, int(im.width * ratio)), CARD_H), Image.LANCZOS))
        if not cards:
            continue

        MARGIN = 40
        avail = W - 2 * MARGIN
        total = sum(c.width for c in cards)
        # kdyz se nevejdou, zmensi se vsechny stejnym pomerem (misto rezani)
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

        dst = OUT / f"{sdef['slug']}.webp"
        base.save(dst, "WEBP", quality=82, method=6)
        made += 1

    print(f"\nobrázky sérií: vytvořeno {made}, přeskočeno {skipped} (málo obalů)")
    print(f"výstup: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
