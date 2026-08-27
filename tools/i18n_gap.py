# -*- coding: utf-8 -*-
"""Vytáhne do pracovní složky JEN obsah, který v zadaných jazycích ještě chybí.

Použití:  python tools/i18n_gap.py <workdir> [locales] [--stale slugs.json]

Zapíše <workdir>/src_{games,platforms,studios,hardware_sections}.json obsahující
pouze slugy, které chybí alespoň v jednom z <locales>. Na to pak navazuje
tools/i18n_chunk.py a překladové workflow (viz i18n_finish.workflow.js).

--stale <soubor>: JSON list slugů, jejichž CZ originál se změnil — berou se jako
nepřeložené, i když překlad existuje (starý překlad zůstane, dokud ho nový nepřepíše)."""
import json, sys, glob, os
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1])
LOCALES = (sys.argv[2].split(",") if len(sys.argv) > 2 and not sys.argv[2].startswith("--")
           else ["en", "de", "fr"])
STALE = set()
if "--stale" in sys.argv:
    STALE = set(json.loads(Path(sys.argv[sys.argv.index("--stale") + 1]).read_text("utf-8")))
OUT.mkdir(parents=True, exist_ok=True)
I18N = ROOT / "src" / "data" / "i18n"


def have(typ):
    """(slug, pole) -> set jazyků, ve kterých už to pole přeložené je.

    Nestačí sledovat samotný slug. Hra může mít přeložený článek a zároveň
    postrádat úvodní větu — dřív se v takovém případě považovala za hotovou
    a věta se do fronty nikdy nedostala, takže 91 % cizojazyčných stránek
    mělo českou větu i po „dokončeném“ překladu.
    """
    got = {}
    for loc in LOCALES:
        f = I18N / loc / f"{typ}.json"
        if not f.exists():
            continue
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception:
            continue
        for slug, val in d.items():
            fields = val.keys() if isinstance(val, dict) else ("_",)
            for fld in fields:
                if isinstance(val, dict) and not (val.get(fld) or "").strip():
                    continue
                got.setdefault((slug, fld), set()).add(loc)
    return got


def gap(typ, src):
    """Nech jen to, co aspoň v jednom jazyce chybí.

    U položek, které jsou slovníkem polí, se do výstupu dávají POUZE pole,
    která opravdu chybí — agent tak nepřekládá znovu to, co už hotové je.
    """
    got = have(typ)
    out = {}
    for slug, val in src.items():
        if not isinstance(val, dict):
            if slug in STALE or got.get((slug, "_"), set()) < set(LOCALES):
                out[slug] = val
            continue
        missing = {
            fld: v for fld, v in val.items()
            if slug in STALE or got.get((slug, fld), set()) < set(LOCALES)
        }
        if missing:
            out[slug] = missing
    return out


d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))

games = {}
for p in d["platforms"]:
    for g in p["games"]:
        fields = {f: g[f] for f in ("teaser", "detail", "article") if g.get(f)}
        if fields:
            games[g["slug"]] = fields

plats = {p["slug"]: {"history": p["history"]} for p in d["platforms"] if p.get("history")}

studios = {}
for f in glob.glob(str(ROOT / "src/data/studio_articles/*.md")):
    studios[os.path.basename(f)[:-3]] = Path(f).read_text("utf-8")

hs_file = ROOT / "src/data/hardware_sections.json"
hs = json.loads(hs_file.read_text("utf-8")) if hs_file.exists() else {}

SRC = {"games": games, "platforms": plats, "studios": studios, "hardware_sections": hs}

print(f"OUT: {OUT}   jazyky: {', '.join(LOCALES)}")
for typ, src in SRC.items():
    miss = gap(typ, src)
    (OUT / f"src_{typ}.json").write_text(
        json.dumps(miss, ensure_ascii=False, indent=1), encoding="utf-8")
    chars = len(json.dumps(miss, ensure_ascii=False))
    print(f"  {typ:18} {len(miss):>5} / {len(src):<5} chybí  ({chars:>9,} znaků)")
