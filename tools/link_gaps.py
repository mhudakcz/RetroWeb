"""Najde tituly, ktere jsou v katalogu na vic platformach, ale neprovazou se.

Sekce "Tentyz titul jinde" paruje hry podle normalizovaneho nazvu a roku
vydani s toleranci nekolika let. Ta heuristika ma dve slepa mista:

  * edicni pripona — "The Witcher 3: Wild Hunt" a "The Witcher 3: Wild Hunt -
    Complete Edition" jsou pro ni dva ruzne tituly,
  * odstup let — klasicky Doom vysel v roce 1993 a znovu v roce 2019, coz je
    mimo okno.

Skript projde dataset, seskupi hry podle nazvu ocesaneho o edicni pripony
a vypise skupiny, ktere se prave ted NEspoji. Vysledek je podklad pro rucni
skupiny v src/data/game_editions.json — skript sam nic nemeni.

Pouziti:  python tools/link_gaps.py [--json out.json]
"""

import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Musi odpovidat SAME_GAME_YEARS v src/lib/data.ts
SAME_GAME_YEARS = 6

# Pripony, ktere oznacuji jinou edici tehoz titulu, ne jinou hru.
EDITION_RE = re.compile(
    r"\s*[-–—:(]?\s*\b("
    r"enhanced|complete|definitive|special|ultimate|deluxe|premium|anniversary|"
    r"legendary|redux|remaster(?:ed)?|remake|hd|classic|goty|"
    r"game of the year|director'?s cut|gold|platinum|collection|edition"
    r")\b[\w' ]*\)?\s*$",
    re.I,
)


def norm(name: str) -> str:
    """Stejna normalizace jako normGameName v src/lib/data.ts."""
    s = name.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


# Musi odpovidat EDITION_SUFFIX v src/lib/data.ts. Zamerne bez "classic"
# (Celeste Classic je jina hra) a bez "remake" (predelavka je samostatny titul).
SUFFIX_RE = re.compile(
    r"\s*(?:[-\u2013\u2014:]\s*)?\b(?:enhanced|complete|definitive|special|ultimate|"
    r"deluxe|premium|anniversary|legendary|redux|remaster(?:ed)?|hd|goty|"
    r"game of the year|director's cut|gold|platinum)\b[\w' ]*$",
    re.I,
)


def edition_key(name: str) -> tuple[str, bool]:
    """Nazev bez edicni pripony + priznak, ze se neco odriznulo."""
    x, suffixed = name, False
    for _ in range(3):
        y = SUFFIX_RE.sub("", x).strip()
        if y == x or not y:
            break
        x, suffixed = y, True
    plus = x.rstrip().rstrip("+").strip()
    if plus and plus != x.strip():
        x, suffixed = plus, True
    return norm(x), suffixed


def loose(name: str) -> str:
    """Nazev bez edicnich pripon — 'Witcher 3 ... Complete Edition' -> 'witcher 3 ...'."""
    prev = None
    s = name
    while prev != s:
        prev = s
        s = EDITION_RE.sub("", s).strip(" -–—:")
    return norm(s)


def year_of(game: dict, platform: dict) -> int:
    m = re.search(r"\d{4}", str(game.get("year") or ""))
    return int(m.group()) if m else platform["year"]


def main() -> int:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    ed_file = ROOT / "src/data/game_editions.json"
    groups = json.loads(ed_file.read_text("utf-8"))["groups"] if ed_file.exists() else {}
    edition_of = {slug: gid for gid, slugs in groups.items() for slug in slugs}

    games = []
    for p in data["platforms"]:
        for g in p["games"]:
            games.append(
                {
                    "slug": g["slug"],
                    "name": g["name"],
                    "platform": p["slug"],
                    "year": year_of(g, p),
                }
            )

    by_loose: dict[str, list[dict]] = {}
    for g in games:
        by_loose.setdefault(loose(g["name"]), []).append(g)

    def links(a: dict, b: dict) -> bool:
        """Spoji se tato dvojice v soucasne podobe webu?

        Musi odpovidat sameGameElsewhere v src/lib/data.ts.
        """
        ea, eb = edition_of.get(a["slug"]), edition_of.get(b["slug"])
        if ea or eb:
            return ea is not None and ea == eb
        ka, sa = edition_key(a["name"])
        kb, sb = edition_key(b["name"])
        if ka != kb:
            return False
        if sa or sb:
            return True
        return abs(a["year"] - b["year"]) <= SAME_GAME_YEARS

    report = []
    for key, items in sorted(by_loose.items()):
        if len(items) < 2 or not key:
            continue
        # rozpad na komponenty podle toho, co se dnes spoji
        unlinked = [
            (a, b)
            for i, a in enumerate(items)
            for b in items[i + 1:]
            if not links(a, b)
        ]
        if not unlinked:
            continue
        report.append(
            {
                "key": key,
                "games": [
                    {"slug": g["slug"], "name": g["name"], "year": g["year"]}
                    for g in sorted(items, key=lambda x: x["year"])
                ],
                "chybi_dvojic": len(unlinked),
            }
        )

    out = None
    if "--json" in sys.argv:
        out = ROOT / sys.argv[sys.argv.index("--json") + 1]

    print(f"Titulu na vic platformach bez uplneho provazani: {len(report)}\n")
    for r in report:
        print(f"  {r['key']}  ({r['chybi_dvojic']} nespojenych dvojic)")
        for g in r["games"]:
            mark = "*" if g["slug"] in edition_of else " "
            print(f"    {mark} {g['year']}  {g['slug']:52} {g['name']}")
    if out:
        with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=1)
        print(f"\nulozeno -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
