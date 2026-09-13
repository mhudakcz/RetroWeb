# -*- coding: utf-8 -*-
"""Pripravi davky pro series_intro.workflow.js vcetne cilove delky textu.

Dosud mely vsechny serie stejne zadani (1100-1400 znaku, dva odstavce). U velkych
znacek jako Mario nebo Final Fantasy je to na tri desitky her zoufale malo, u male
serie o dvou dilech naopak akorat. Delka se proto odvozuje od vahy serie: kolik
dilu v katalogu je, pres kolik let a platforem se rozklada.

Pouziti:
  python tools/series_intro_prep.py              vypise args pro workflow
  python tools/series_intro_prep.py --chybejici  jen serie bez textu
  python tools/series_intro_prep.py --kratke N   jen serie s textem pod N znaku
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# (minimum znaku, maximum znaku, pocet odstavcu) podle vahy serie
PASMA = {
    "velka": (3200, 4200, "4 az 5"),
    "stredni": (2200, 2900, "3 az 4"),
    "mala": (1500, 2000, "2 az 3"),
}


def _vzory(d):
    skip = [e.lower() for e in (d.get("exclude") or [])]
    explicit = set(d.get("games") or [])
    rx = [re.compile(r"(?<![a-z0-9])" + re.escape(m.lower()) + r"(?![a-z0-9])")
          for m in d["match"]]
    return rx, skip, explicit


def hry_serie(d, hry):
    rx, skip, explicit = _vzory(d)
    out = []
    for plat, g in hry:
        if explicit:
            if g["slug"] in explicit:
                out.append((plat, g))
            continue
        n = g["name"].lower()
        if any(e in n for e in skip):
            continue
        if any(r.search(n) for r in rx):
            out.append((plat, g))
    return out


def pasmo(pocet, rozpeti, platforem):
    """Vaha serie. Nejde jen o pocet her — serie, ktera se drzi dvacet let
    a prosla deseti platformami, ma o cem vypravet i kdyz ma dilu mene."""
    body = 0
    body += 2 if pocet >= 12 else 1 if pocet >= 6 else 0
    body += 2 if rozpeti >= 20 else 1 if rozpeti >= 10 else 0
    body += 2 if platforem >= 8 else 1 if platforem >= 4 else 0
    if body >= 5:
        return "velka"
    if body >= 3:
        return "stredni"
    return "mala"


def main() -> int:
    a = sys.argv[1:]
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    defs = json.loads((ROOT / "src/data/series.json").read_text("utf-8"))
    hry = [(p["slug"], g) for p in data["platforms"] for g in p["games"]]

    jen_chybejici = "--chybejici" in a
    kratke = int(a[a.index("--kratke") + 1]) if "--kratke" in a else 0

    polozky = []
    for d in defs:
        cs = ((d.get("intro") or {}).get("cs") or "").strip()
        if jen_chybejici and cs:
            continue
        if kratke and len(cs) >= kratke:
            continue
        v = hry_serie(d, hry)
        if not v:
            continue
        roky = [int(g["year"]) for _p, g in v if str(g.get("year") or "").isdigit()]
        rozpeti = (max(roky) - min(roky)) if roky else 0
        span = f"{min(roky)}-{max(roky)}" if roky else "?"
        platformy = sorted({p for p, _g in v})
        p = pasmo(len(v), rozpeti, len(platformy))
        polozky.append({
            "slug": d["slug"], "name": d["name"], "count": len(v), "span": span,
            "platforms": ", ".join(platformy[:8]),
            "pasmo": p, "min": PASMA[p][0], "max": PASMA[p][1], "odstavcu": PASMA[p][2],
        })

    # velke serie maji delsi text, takze jich na agenta patri min
    davky, cur, vaha = [], [], 0
    for it in polozky:
        w = 3 if it["pasmo"] == "velka" else 2 if it["pasmo"] == "stredni" else 1
        if vaha + w > 6 and cur:
            davky.append(cur)
            cur, vaha = [], 0
        cur.append(it)
        vaha += w
    if cur:
        davky.append(cur)

    poc = {}
    for it in polozky:
        poc[it["pasmo"]] = poc.get(it["pasmo"], 0) + 1
    print(f"serii k napsani: {len(polozky)} ({poc}) -> {len(davky)} davek")
    # Davky jdou do souboru, ne do argumentu workflow — inline by to bylo
    # pres tricet kilobajtu a stejny vzor uz pouzivaji roky i studia.
    work = ROOT / ".i18n-work" / "serie_intro"
    work.mkdir(parents=True, exist_ok=True)
    for i, b in enumerate(davky):
        (work / f"intro_{i:03d}_in.json").write_text(
            json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {len(davky)}}}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
