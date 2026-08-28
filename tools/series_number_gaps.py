# -*- coding: utf-8 -*-
"""Najde dily, ktere v ciselne rade chybi.

Kdyz je v katalogu Tekken 3 a Tekken 5, ale ne Tekken 4, je to videt az kdyz
si nekdo radu projde rucne. Skript vytahne z nazvu poradove cislo (rimske
i arabske), seskupi hry podle zakladu nazvu a vypise mezery v rade.

Prvni dil se cislem obvykle neoznacuje, takze samotny zaklad nazvu se pocita
jako jednicka ("Tekken" = 1).

Hlasi se jen rady, kde uz mame aspon dva dily — jinak by kazda jednotlivá hra
vypadala jako zacatek nedokoncene serie.

Pouziti:  python tools/series_number_gaps.py [--min-known 2]
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7,
         "viii": 8, "ix": 9, "x": 10, "xi": 11, "xii": 12, "xiii": 13,
         "xiv": 14, "xv": 15, "xvi": 16}

# Slova, ktera za nazvem nesou cislo, ale nejsou poradim dilu.
NOT_SEQUEL = {"64", "2000", "2001", "2002", "2003", "2004", "2005", "2006",
              "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014",
              "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022",
              "2023", "2024", "2025", "2026", "3d", "4k"}


def split_number(name: str):
    """Vrati (zaklad, cislo dilu) — cislo je None, kdyz ho nazev nema."""
    # podnazev za dvojteckou poradi neurcuje: "Tekken 3: Something"
    head = re.split(r"[:–—(]", name)[0].strip()
    m = re.search(r"\s(\d{1,2}|[ivx]{1,6})\s*$", head, re.I)
    if not m:
        return head.lower(), None
    tok = m.group(1).lower()
    if tok in NOT_SEQUEL:
        return head.lower(), None
    # Samotne "X" byva pismeno v nazvu, ne desitka: F-Zero X, Mega Man X,
    # Xenoblade Chronicles X. Stejne tak "V" u Grand Theft Auto V uz cislo je,
    # takze se vylucuje jen "x".
    if tok == "x":
        return head.lower(), None
    num = ROMAN.get(tok) if not tok.isdigit() else int(tok)
    if not num or num > 16:
        return head.lower(), None
    return head[: m.start()].strip().lower(), num


def main() -> int:
    min_known = (int(sys.argv[sys.argv.index("--min-known") + 1])
                 if "--min-known" in sys.argv else 2)
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))

    have: dict[str, dict[int, set[str]]] = defaultdict(lambda: defaultdict(set))
    for p in data["platforms"]:
        for g in p["games"]:
            base, num = split_number(g["name"])
            if not base:
                continue
            have[base][num or 1].add(p["slug"])

    found = 0
    for base in sorted(have):
        nums = have[base]
        known = sorted(nums)
        if len(known) < min_known or max(known) < 2:
            continue
        missing = [n for n in range(1, max(known) + 1) if n not in nums]
        if not missing:
            continue
        found += 1
        mame = ", ".join(str(n) for n in known)
        print(f"  {base}")
        print(f"      mame: {mame}   CHYBI: {', '.join(str(n) for n in missing)}")

    print(f"\nrad s mezerou: {found}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
