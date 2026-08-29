# -*- coding: utf-8 -*-
"""Sestavi nova cisla magazinu z her, ktere jeste v zadnem cisle nejsou.

Magazin deli katalog casove: kazde cislo pokryva vyrez jednoho roku. Roku
s vic hrami vyjde vic cisel, hubenemu roku jedno.

KLICOVE PRAVIDLO: obsah uz vydaneho cisla se NIKDY nemeni. Kdyby se clenstvi
pocitalo pri kazdem buildu, pridani jedne hry z roku 1994 by preskladalo vsechna
cisla toho rocniku a odkazy na starsi by ukazovaly jinam. Skript proto cte
rejstrik vydanych cisel, bere jen hry, ktere v zadnem nejsou, a sklada z nich
cisla NOVA. Casem tak vznikne i prirozena historie doplnovani.

Hry bez roku se zarazuji priblizne podle roku uvedeni platformy a v cisle jsou
oznacene, aby ctenar vedel, ze datum je odhad.

Rejstrik: src/data/magazine.json
Pouziti:
  python tools/magazine_issue.py            vypise, co by vyslo (nic nemeni)
  python tools/magazine_issue.py --write    zapise nova cisla do rejstriku
  python tools/magazine_issue.py --write --rok 1994   jen jeden rocnik
"""
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "src" / "data" / "magazine.json"

PER_ISSUE = 25   # cilovy pocet her v cisle
MIN_ISSUE = 8    # pod tim se cislo nevyda a hry pockaji na dalsi kolo


def year_of(g, p):
    m = re.search(r"(19|20)\d{2}", str(g.get("year") or ""))
    return (int(m.group(0)), True) if m else (p["year"], False)


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text("utf-8"))
    return {"vydani": []}


def main() -> int:
    write = "--write" in sys.argv
    only_year = int(sys.argv[sys.argv.index("--rok") + 1]) if "--rok" in sys.argv else None

    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    ledger = load_ledger()
    published = {s for v in ledger["vydani"] for s in v["hry"]}
    pub_plat = {s for v in ledger["vydani"] for s in v["platformy"]}

    by_year = defaultdict(lambda: {"hry": [], "platformy": []})
    for p in data["platforms"]:
        if p["slug"] not in pub_plat:
            by_year[p["year"]]["platformy"].append(p["slug"])
        for g in p["games"]:
            if g["slug"] in published:
                continue
            y, exact = year_of(g, p)
            by_year[y]["hry"].append({
                "slug": g["slug"],
                "name": g["name"],
                "presny_rok": exact,
                # cislo 1 nese ty nejvyraznejsi tituly, jako v opravdovem casopise
                "vaha": (2 if "mustplay" in (g.get("flags") or []) else 0)
                        + (1 if g.get("image") else 0),
            })

    # dalsi poradove cislo v rocniku navazuje na uz vydana
    next_no = defaultdict(lambda: 1)
    for v in ledger["vydani"]:
        next_no[v["rok"]] = max(next_no[v["rok"]], v["cislo"] + 1)

    nove = []
    for year in sorted(by_year):
        if only_year and year != only_year:
            continue
        e = by_year[year]
        hry = sorted(e["hry"], key=lambda g: (-g["vaha"], g["name"]))
        plat = e["platformy"]
        if len(hry) < MIN_ISSUE and not plat:
            continue
        pocet = max(1, round(len(hry) / PER_ISSUE)) if hry else 1
        velikost = -(-len(hry) // pocet) if pocet else 0
        for i in range(pocet):
            chunk = hry[i * velikost:(i + 1) * velikost]
            if not chunk and not (i == 0 and plat):
                continue
            nove.append({
                "id": f"{year}-{next_no[year] + i}",
                "rok": year,
                "cislo": next_no[year] + i,
                "hry": [g["slug"] for g in chunk],
                # platformy patri do prvniho cisla rocniku
                "platformy": plat if i == 0 else [],
                "odhad_roku": [g["slug"] for g in chunk if not g["presny_rok"]],
            })

    print(f"rejstrik ma {len(ledger['vydani'])} vydanych cisel")
    print(f"nevydanych her: {sum(len(e['hry']) for e in by_year.values())}")
    print(f"pripraveno novych cisel: {len(nove)}\n")
    for v in nove[:20]:
        odhad = f", {len(v['odhad_roku'])} s odhadem roku" if v["odhad_roku"] else ""
        plat = f", {len(v['platformy'])} platforem" if v["platformy"] else ""
        print(f"  {v['id']:9} {len(v['hry']):3} her{plat}{odhad}")
    if len(nove) > 20:
        print(f"  … a dalsich {len(nove) - 20}")

    if write:
        ledger["vydani"].extend(nove)
        ledger["vydani"].sort(key=lambda v: (v["rok"], v["cislo"]))
        with io.open(LEDGER, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(ledger, fh, ensure_ascii=False, indent=1)
        print(f"\nzapsano -> {LEDGER.relative_to(ROOT)} ({len(ledger['vydani'])} cisel)")
    elif nove:
        print("\n(nic se nezapsalo — spust znovu s --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
