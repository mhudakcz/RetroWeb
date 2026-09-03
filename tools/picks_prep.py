# -*- coding: utf-8 -*-
"""Pripravi davky pro picks.workflow.js a slouci vyber "co si tu zahrat".

Na strance platformy chybel odpovednik na nejcastejsi otazku ctenare: mam sto
her v abecednim seznamu, cim zacit. Priznak mustplay by se nabizel, ale je
rozdany velmi nerovnomerne (SNES, arkady i N64 maji nulu), takze se o nej
oprit nejde a vyber dela agent.

Agent vybira VYHRADNE ze slugu, ktere dostane — jinak by doporucoval hry,
ktere v katalogu nejsou.

Vystup: src/data/platform_picks.json  {slug platformy: [{slug, why}]}

Pouziti:
  python tools/picks_prep.py <workdir> [--pocet 8]   pripravi davky
  python tools/picks_prep.py <workdir> --merge       slouci vystupy
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "data" / "platform_picks.json"
MIN_HER = 8          # pod tim se vyber nedela, seznam si ctenar projde cely
MIN_LEN, MAX_LEN = 40, 220


def _zebricek() -> dict:
    """Slugy her, ktere externi zebricek radi mezi nejlepsi na platforme.

    Bereme je jako voditko, ne jako hotovy vyber — zebricek nezna zanrovou
    pestrost, kterou po agentovi chceme, a nektere tituly uz ve vyberu jsou.
    """
    if "--zebricek" not in sys.argv:
        return {}
    cesta = Path(sys.argv[sys.argv.index("--zebricek") + 1])
    if not cesta.is_absolute():
        cesta = ROOT / cesta
    if not cesta.exists():
        return {}
    rep = json.loads(cesta.read_text("utf-8"))
    out = {}
    for slug, polozky in (rep.get("do_picku") or {}).items():
        out[slug] = [{"slug": p[0], "name": p[1], "skore": p[2]} for p in polozky]
    return out


def prepare(work: Path, pocet: int) -> None:
    work.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    hotovo = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    zebricky = _zebricek()

    n = 0
    for p in data["platforms"]:
        cil = min(pocet, max(4, len(p["games"]) // 6))
        maji = len(hotovo.get(p["slug"]) or [])
        if len(p["games"]) < MIN_HER:
            continue
        # bez --doplnit se hotove platformy preskakuji; s nim se znovu zpracuji ty,
        # kterym by dnes nalezelo vic titulu
        ma_zebricek = bool(zebricky.get(p["slug"]))
        if maji and not ("--doplnit" in sys.argv and maji < cil) and not ma_zebricek:
            continue
        hry = [{
            "slug": g["slug"], "name": g["name"],
            "year": str(g.get("year") or ""), "genre": g.get("genre") or "",
            "mustplay": "mustplay" in (g.get("flags") or []),
            "teaser": (g.get("teaser") or "")[:120],
        } for g in p["games"]]
        # Velka a popularni platforma unese sirsi doporuceni: u sta her je osm
        # titulu spis ochutnavka nez rozcestnik. Maly katalog si naopak ctenar
        # projde cely, tam staci ctyri.
        payload = {"slug": p["slug"], "platform": p["name"], "rok": p["year"],
                   "pocet": min(pocet, max(4, len(hry) // 6)), "hry": hry}
        if zebricky.get(p["slug"]):
            payload["zebricek"] = zebricky[p["slug"]]
        if hotovo.get(p["slug"]):
            payload["uz_ve_vyberu"] = [x["slug"] for x in hotovo[p["slug"]]]
        with io.open(work / f"picks_{n:03d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        n += 1

    if not n:
        print("vsechny platformy uz vyber maji")
        return
    print(f"platforem k vyberu: {n}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path) -> None:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    znam = {g["slug"] for p in data["platforms"] for g in p["games"]}
    plat_hry = {p["slug"]: {g["slug"] for g in p["games"]} for p in data["platforms"]}
    hotovo = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}

    pridano = spatne = 0
    for f in sorted(work.glob("picks_*_out.json")):
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        slug = d.get("slug")
        if slug not in plat_hry:
            continue
        vyber = []
        for it in d.get("vyber") or []:
            s, why = it.get("slug"), (it.get("why") or "").strip()
            # hra musi byt z TETO platformy — jinak by odkaz vedl jinam
            if s not in znam or s not in plat_hry[slug]:
                spatne += 1
                continue
            if not (MIN_LEN <= len(why) <= MAX_LEN):
                spatne += 1
                continue
            vyber.append({"slug": s, "why": why})
        # sirsi vyber stavajici prepise, uzsi ne — jinak by opakovany beh
        # doporuceni zase osekal
        if len(vyber) >= 4 and len(vyber) >= len(hotovo.get(slug) or []):
            hotovo[slug] = vyber
            pridano += 1

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(hotovo, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"platforem s vyberem: {len(hotovo)} (+{pridano})")
    if spatne:
        print(f"  zahozeno polozek: {spatne} (cizi slug nebo spatna delka)")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    if "--merge" in sys.argv:
        merge(work)
    else:
        pocet = int(sys.argv[sys.argv.index("--pocet") + 1]) if "--pocet" in sys.argv else 20
        prepare(work, pocet)
    return 0


if __name__ == "__main__":
    sys.exit(main())
