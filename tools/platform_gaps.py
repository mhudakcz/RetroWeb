# -*- coding: utf-8 -*-
"""Najde hry, ktere v katalogu stoji jen na casti platforem, kde vysly.

Multiplatformni titul mame casto jen na jedne konzoli — Prototype je na Xbox 360,
ale uz ne na PS3, prestoze tam vysel soucasne. Skript sam o vydanich nic nevi,
takze jen pripravuje PODKLAD pro davku: vypise hry z vybranych let, ktere jsou
v katalogu na mensim poctu platforem, nez byva u titulu te doby obvykle, a k nim
platformy, kde uz jsou.

Rozhodnuti, kam titul doplnit, dela az agent — ten totiz vi, kde hra skutecne
vysla. Skript slouzi k tomu, aby se davka nezabyvala hrami, ktere uz pokryte
jsou, a aby se dalo omezit na obdobi, kde jsou multiplatformni vydani pravidlem.

Pouziti:
  python tools/platform_gaps.py [--from 2005] [--to 2020] [--max-plat 1] [--limit 400]
"""
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

# Platformy, na kterych ma smysl multiplatformni vydani hledat. Handheldy
# a retro stroje sem nepatri — tam byly porty spis vyjimkou nez pravidlem.
MULTI = {
    "pc-modern": "PC", "ps3": "PS3", "ps4": "PS4", "ps5": "PS5",
    "xbox-360": "Xbox 360", "xbox-one": "Xbox One", "xbox-series": "Xbox Series",
    "switch": "Switch", "ps2": "PS2", "xbox": "Xbox", "gamecube": "GameCube",
    "wii": "Wii", "wii-u": "Wii U",
}


def norm(name: str) -> str:
    s = name.lower().replace("&", " and ")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def main() -> int:
    def arg(flag, default):
        return type(default)(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default

    y_from, y_to = arg("--from", 2005), arg("--to", 2020)
    max_plat, limit = arg("--max-plat", 1), arg("--limit", 400)

    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    by_title: dict[str, dict] = defaultdict(lambda: {"name": "", "plats": set(), "year": 0})
    for p in data["platforms"]:
        if p["slug"] not in MULTI:
            continue
        for g in p["games"]:
            m = re.search(r"\d{4}", str(g.get("year") or ""))
            year = int(m.group()) if m else p["year"]
            if not (y_from <= year <= y_to):
                continue
            e = by_title[norm(g["name"])]
            e["name"] = e["name"] or g["name"]
            e["plats"].add(p["slug"])
            e["year"] = e["year"] or year

    rows = [e for e in by_title.values() if len(e["plats"]) <= max_plat]
    rows.sort(key=lambda e: e["year"])
    rows = rows[:limit]

    print(f"hry z let {y_from}-{y_to} na nejvyse {max_plat} platformach: {len(rows)}\n")
    for e in rows:
        plats = ", ".join(MULTI[s] for s in sorted(e["plats"]))
        print(f"  {e['year']}  {e['name'][:52]:52} [{plats}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
