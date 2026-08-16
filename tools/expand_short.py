# -*- coding: utf-8 -*-
"""Vytáhne hry s příliš krátkým článkem do dávek pro rozšiřovací workflow.

Použití:
    python tools/expand_short.py <workdir> [--min 1600] [--platforms ps3,ps4,...] [--size 20]

Zapíše <workdir>/chunks/exp_NNN.json — každá dávka je list objektů
{slug, platform, name, year, studio, genre, current} (stejný tvar, jaký používal
předchozí běh rozšiřování). Workflow k nim dopíše exp_NNN_out.json = {slug: markdown},
který se pak slučuje přes tools/expand_merge.py.
"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

args = sys.argv[1:]
if not args:
    print(__doc__)
    sys.exit(1)
BASE = Path(args[0])


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


MIN = int(opt("--min", 1600))
SIZE = int(opt("--size", 20))
PLATS = opt("--platforms", "")
wanted = set(PLATS.split(",")) if PLATS else None

d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))

items = []
for p in d["platforms"]:
    if wanted and p["slug"] not in wanted:
        continue
    for g in p["games"]:
        art = g.get("article") or ""
        if not art or len(art) >= MIN:
            continue
        items.append({
            "slug": g["slug"],
            "platform": p["name"],
            "name": g["name"],
            "year": g.get("year") or "",
            "studio": g.get("studio") or "",
            "genre": g.get("genre") or "",
            "current": art,
        })

CH = BASE / "chunks"
CH.mkdir(parents=True, exist_ok=True)
n = 0
for i in range(0, len(items), SIZE):
    (CH / f"exp_{i // SIZE:03d}.json").write_text(
        json.dumps(items[i:i + SIZE], ensure_ascii=False, indent=1), encoding="utf-8")
    n += 1

(BASE / "targets.json").write_text(
    json.dumps([it["slug"] for it in items], ensure_ascii=False), encoding="utf-8")

print(f"OUT: {BASE}")
print(f"  her pod {MIN} znaků: {len(items)}")
print(f"  dávek (po {SIZE}): {n}")
if items:
    L = sorted(len(it["current"]) for it in items)
    print(f"  délky: min {L[0]}, medián {L[len(L)//2]}, max {L[-1]}")
