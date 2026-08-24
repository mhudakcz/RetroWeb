# -*- coding: utf-8 -*-
"""Prejmenuje snimky ze Steamu a eShopu z pripony -title na -snap2.

Parser popisuje priponu -title jako "Titulni obrazovka". To sedi u snimku
z libretro-thumbnails (repozitar ma Named_Titles se skutecnymi titulnimi
obrazovkami), ale ne u Steamu a Nintendo eShopu — tam jsou VSECHNY snimky ze
hry a druhy z nich se drive ukladal pod -title. Na strankach modernich her tak
u bezneho zaberu ze hry stalo "Titulni obrazovka".

Puvod souboru uz z disku nezjistime (optimalizace vsechno prevedla na WebP),
takze se rozhoduje podle pomeru stran. Snimky ze Steamu a eShopu jsou PRESNE
16:9, kdezto libretro uklada nativni rozliseni konzole, ktere 16:9 skoro nikdy
neni — GBA ma 240x160 (1.500), PSP 480x272 (1.765), 3DS 400x240 (1.667), retro
konzole 4:3. Tolerance je proto uzka; sirsi prah by sebral titulni obrazovky
handheldu, ktere maji taky pomerne siroky displej.

Pouziti:  python tools/fix_shot_labels.py [--write]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "images" / "games"
MIN_YEAR = 2000  # musi odpovidat STEAM_MIN_PLATFORM_YEAR v fetch_images.py
SIXTEEN_NINE = 16 / 9
# 480x270 je 1.7778, PSP 480x272 je 1.7647 — mezi nimi musi prah bezpecne projit
TOLERANCE = 0.006


def main() -> int:
    write = "--write" in sys.argv
    from PIL import Image

    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    modern = {p["slug"] for p in data["platforms"] if p["year"] >= MIN_YEAR}

    moved = kept = 0
    per: dict[str, int] = {}
    for slug in sorted(modern):
        d = IMG / slug
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*-title.*")):
            try:
                w, h = Image.open(f).size
            except Exception:  # noqa: BLE001
                continue
            if not h or abs(w / h - SIXTEEN_NINE) > TOLERANCE:
                kept += 1
                continue
            dst = f.with_name(f.name.replace("-title.", "-snap2.", 1))
            if dst.exists():
                kept += 1
                continue
            moved += 1
            per[slug] = per.get(slug, 0) + 1
            if write:
                f.rename(dst)

    for s, n in sorted(per.items(), key=lambda t: -t[1]):
        print(f"  {s:16} {n}")
    print(f"\nk prejmenovani: {moved} snimku, ponechano jako titulni: {kept}")
    if not write:
        print("(nic se nezmenilo — spust znovu s --write)")
    else:
        print("spust jeste tools/parse_content.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
