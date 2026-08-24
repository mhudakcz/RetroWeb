# -*- coding: utf-8 -*-
"""Najde tutez hru uvedenou na jedne platforme dvakrat.

Seznamy her vznikaly po castech z ruznych podkladu, takze se obcas stalo, ze
se stejny titul dostal do jednoho seznamu dvakrat pod mirne jinym zapisem —
"Eastern Front (1941)" a "Eastern Front 1941", "Out Run" a "Outrun". Na webu
pak platforma ukazuje dve karty tehoz, kazdou s vlastnim clankem.

Porovnava se dvema normalizacemi, protoze ani jedna sama nestaci:
  * bez zavorek  — spoji "Doom (1993)" s "Doom"
  * se zavorkami — spoji "Eastern Front (1941)" s "Eastern Front 1941"

Skript jen hlasi; opravuje se v podkladech, ze kterych parse_content.py cte.

Pouziti:  python tools/dup_games.py
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def keys(name: str) -> set[str]:
    plain = re.sub(r"[^a-z0-9]+", "", name.lower())
    no_paren = re.sub(r"[^a-z0-9]+", "", re.sub(r"\([^)]*\)", "", name).lower())
    return {k for k in (plain, no_paren) if k}


def main() -> int:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    found = 0
    for p in data["platforms"]:
        buckets: dict[str, list[str]] = defaultdict(list)
        for g in p["games"]:
            for k in keys(g["name"]):
                buckets[k].append((g["slug"], g["name"]))
        seen_pairs = set()
        for k, items in buckets.items():
            uniq = {s: n for s, n in items}
            if len(uniq) < 2:
                continue
            pair = tuple(sorted(uniq))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            found += 1
            print(f"  {p['slug']}")
            for s, n in sorted(uniq.items()):
                print(f"      {s:48} {n}")
    print(f"\nduplicitnich titulu v ramci platformy: {found}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
