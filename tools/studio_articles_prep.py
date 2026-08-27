# -*- coding: utf-8 -*-
"""Pripravi davky pro studio_articles.workflow.js.

Na vypisu studii je pres dve stovky karet, ale clanek ma jen 23 z nich —
chybi i takova jmena jako id Software, BioWare, FromSoftware nebo LucasArts.
Skript vybere studia bez clanku serazena podle poctu her v katalogu a ke
kazdemu prilozi jeho tituly s roky a platformami, aby agent psal z podkladu
a nemusel si vybavovat, co studio delalo.

Pouziti:  python tools/studio_articles_prep.py <workdir> [--top 40] [--size 3]
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "src" / "data" / "studio_articles"

# Musi odpovidat studioSlug v src/lib/data.ts
def studio_slug(name: str) -> str:
    x = name.normalize() if hasattr(name, "normalize") else name
    import unicodedata
    x = unicodedata.normalize("NFKD", x)
    x = "".join(c for c in x if not unicodedata.combining(c))
    x = x.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", x).strip("-")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 40
    size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 3

    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    have = {f.stem for f in ARTICLES.glob("*.md")}

    studios: dict[str, dict] = {}
    for p in data["platforms"]:
        for g in p["games"]:
            name = (g.get("studio") or "").strip()
            if not name:
                continue
            slug = studio_slug(name)
            s = studios.setdefault(slug, {"slug": slug, "name": name, "games": []})
            s["games"].append(
                {"name": g["name"], "year": str(g.get("year") or ""), "platform": p["short"]}
            )

    todo = sorted(
        (s for slug, s in studios.items() if slug not in have),
        key=lambda s: -len(s["games"]),
    )[:top]
    if not todo:
        print("vsechna vybrana studia uz clanek maji")
        return 0

    work.mkdir(parents=True, exist_ok=True)
    for s in todo:
        # nejznamejsi tituly napred, at se agent chyti; cely seznam by byl zbytecne dlouhy
        s["games"] = sorted(s["games"], key=lambda g: g["year"] or "9999")[:25]

    n = 0
    for i in range(0, len(todo), size):
        with io.open(work / f"stud_{n:02d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(todo[i: i + size], fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"studii bez clanku: {len(todo)} -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')
    for s in todo[:10]:
        print(f"   {s['name']:32} {len(s['games'])} her")
    return 0


if __name__ == "__main__":
    sys.exit(main())
