# -*- coding: utf-8 -*-
"""Najde herni rady, ktere v katalogu jsou, ale nemaji zaznam v series.json.

Kdyz rada nema svou serii, nemaji jeji dily na strankach sekci "Ze stejne
serie" a ctenar se z Portalu nedostane na Portal 2. Pritom staci, ze v nazvech
je poradove cislo — z toho se rada pozna sama.

Skript seskupi hry podle zakladu nazvu (bez poradoveho cisla), necha jen ty se
dvema a vice DILY, a vypise ty, ktere zadna existujici serie nepokryva.
Zohlednuje SERIES_MIN: rada, ktera by mela min her nez prah, by stejne vlastni
stranku nedostala, takze se hlasi zvlast.

Skript sam nic nemeni — vystup je podklad pro doplneni series.json.

Pouziti:  python tools/missing_series.py [--json out.json]
"""
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from series_number_gaps import split_number  # noqa: E402

SERIES_MIN = 4  # musi odpovidat SERIES_MIN v src/lib/data.ts


def covered_by(name: str, defs) -> str | None:
    """Vrati slug serie, ktera titul uz pokryva."""
    low = name.lower()
    for s in defs:
        if any(re.search(r"\b" + re.escape(m.lower()) + r"\b", low) for m in s.get("match", [])):
            if not any(re.search(r"\b" + re.escape(x.lower()) + r"\b", low)
                       for x in s.get("exclude", [])):
                return s["slug"]
    return None


def main() -> int:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    defs = json.loads((ROOT / "src/data/series.json").read_text("utf-8"))
    explicit = {g for s in defs for g in s.get("games", [])}

    groups = defaultdict(lambda: {"nums": set(), "games": [], "name": ""})
    for p in data["platforms"]:
        for g in p["games"]:
            base, num = split_number(g["name"])
            if not base:
                continue
            e = groups[base]
            e["nums"].add(num or 1)
            e["games"].append(g)
            if not e["name"] or (num or 1) == 1:
                # zastupcem je prvni dil, jeho nazev je zaklad rady
                e["name"] = re.split(r"[:–—(]", g["name"])[0].strip()

    rows = []
    for base, e in groups.items():
        if len(e["nums"]) < 2:
            continue
        if any(covered_by(g["name"], defs) or g["slug"] in explicit for g in e["games"]):
            continue
        rows.append({
            "name": e["name"],
            "dily": sorted(e["nums"]),
            "her": len(e["games"]),
            "staci_na_stranku": len(e["games"]) >= SERIES_MIN,
        })

    rows.sort(key=lambda r: (-r["her"], r["name"]))
    ok = [r for r in rows if r["staci_na_stranku"]]
    small = [r for r in rows if not r["staci_na_stranku"]]

    print(f"rad bez serie, ktere by stranku dostaly: {len(ok)}\n")
    for r in ok:
        print(f"  {r['name'][:44]:46} dily {r['dily']}  ({r['her']} her)")
    if small:
        print(f"\npod prahem SERIES_MIN={SERIES_MIN} (stranku by nedostaly): {len(small)}")
        for r in small[:15]:
            print(f"  {r['name'][:44]:46} dily {r['dily']}  ({r['her']} her)")

    if "--json" in sys.argv:
        out = ROOT / sys.argv[sys.argv.index("--json") + 1]
        with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(ok, fh, ensure_ascii=False, indent=1)
        print(f"\nulozeno -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
