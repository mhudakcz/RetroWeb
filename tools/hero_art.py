# -*- coding: utf-8 -*-
"""Poskláda koláž obalů pro hero sekci úvodní strany.

Nic se nestahuje — bere se, co už v public/images/games je (přes 4 000 obalů).
Vybírá se napříč platformami i desetiletími, aby na koláži byla vidět celá
šíře katalogu, ne pět verzí jedné hry ani samé moderní obaly.

Výstup: public/images/hero-wide.webp (2400×900, pozadí za textem hero sekce)

Použití:  python tools/hero_art.py
"""
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images"


def year_of(g, p):
    m = re.search(r"(19|20)\d{2}", str(g.get("year") or ""))
    return int(m.group(0)) if m else p["year"]


def pick_covers(n: int, seed: int):
    """Vybere n obalů rozprostřených přes platformy i dekády."""
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    by_bucket = defaultdict(list)
    for p in data["platforms"]:
        for g in p["games"]:
            if not g.get("image"):
                continue
            # kýbl = platforma + dekáda, aby se koláž netočila kolem jedné éry
            by_bucket[(p["slug"], year_of(g, p) // 10)].append(g["image"])

    rnd = random.Random(seed)
    buckets = sorted(by_bucket)
    rnd.shuffle(buckets)
    out, i = [], 0
    # kolo po kole po jednom z každého kýble, dokud není dost
    while len(out) < n and any(by_bucket.values()):
        b = buckets[i % len(buckets)]
        i += 1
        pool = by_bucket.get(b)
        if pool:
            out.append(pool.pop(rnd.randrange(len(pool))))
        if i > len(buckets) * 40:
            break
    return out


def build(w: int, h: int, cols: int, seed: int, dst: Path):
    from PIL import Image

    gap = 10
    cell_w = (w - gap * (cols + 1)) // cols
    cell_h = int(cell_w * 1.32)                      # obaly bývají na výšku
    rows = (h + cell_h) // (cell_h + gap) + 1
    covers = pick_covers(cols * rows, seed)
    if not covers:
        print("  žádné obaly")
        return

    canvas = Image.new("RGB", (w, h), (14, 15, 22))
    k = 0
    for r in range(rows):
        # každá druhá řada je posunutá, ať nevznikne přísná tabulka
        off = (cell_w + gap) // 2 if r % 2 else 0
        y = gap + r * (cell_h + gap) - cell_h // 3
        for c in range(cols + 1):
            if k >= len(covers):
                break
            x = gap + c * (cell_w + gap) - off
            try:
                im = Image.open(ROOT / "public" / covers[k].lstrip("/")).convert("RGB")
            except Exception:  # noqa: BLE001
                k += 1
                continue
            k += 1
            # ořez na poměr buňky bez deformace
            sc = max(cell_w / im.width, cell_h / im.height)
            im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))),
                           Image.LANCZOS)
            left = (im.width - cell_w) // 2
            top = (im.height - cell_h) // 2
            canvas.paste(im.crop((left, top, left + cell_w, top + cell_h)), (x, y))

    canvas.save(dst, "WEBP", quality=82, method=6)
    kb = dst.stat().st_size // 1024
    print(f"  {dst.name}: {w}×{h}, {k} obalů, {kb} kB")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    print("koláže pro hero:")
    build(2400, 900, 12, seed=7, dst=OUT / "hero-wide.webp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
