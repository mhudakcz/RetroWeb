# -*- coding: utf-8 -*-
"""Zkontroluje hry proti PRAVIDLA-HER.md a vypise, co kteremu titulu chybi.

Duvod existence: dosud se po kazde davce kontrolovalo jen to, co zrovna
nekoho napadlo, takze nektere hry mely uvodni vetu, ale ne obrazky, jine
naopak. Tenhle skript projde vsechno naraz.

Pouziti:
  python tools/kontrola_her.py                 souhrn za cely katalog
  python tools/kontrola_her.py --platforma X   jen jedna platforma
  python tools/kontrola_her.py --nove N        jen N naposledy pridanych
  python tools/kontrola_her.py --seznam        vypise konkretni hry, ne jen pocty
"""
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MIN_CLANEK = 1300          # kratsi slucovani zahazuje
MIN_TEASER, MAX_TEASER = 30, 110
CIL_OBRAZKU = 3


def nacti():
    return json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))


def problemy_hry(g: dict, serie_slugy: set) -> list:
    """Seznam nedostatku jedne hry. Prazdny = hra je hotova."""
    out = []
    obrazku = len(g.get("gallery") or [])
    if obrazku == 0:
        out.append("bez obrazku")
    elif obrazku < CIL_OBRAZKU:
        out.append(f"jen {obrazku} obr.")

    teaser = (g.get("teaser") or "").strip()
    if not teaser:
        out.append("bez uvodni vety")
    elif not (MIN_TEASER <= len(teaser) <= MAX_TEASER):
        out.append(f"uvodni veta {len(teaser)} znaku")

    clanek = g.get("article") or ""
    if len(clanek) < MIN_CLANEK:
        out.append(f"clanek {len(clanek)} znaku")

    if "Proč hrát" not in clanek:
        out.append("bez zaverecne vety")

    if not str(g.get("year") or "").strip():
        out.append("bez roku")

    if not (g.get("genre") or "").strip():
        out.append("bez zanru")
    if not (g.get("studio") or "").strip():
        out.append("bez studia")

    return out


def mozna_serie(hry: list) -> list:
    """Tituly, ktere vypadaji jako dil serie, ale zadnou nemaji.

    Hleda dvojice a vic her se stejnym zacatkem nazvu — "Gauntlet"
    a "Gauntlet 2" patri k sobe, i kdyz je zatim nic nespojuje.
    """
    zaklad = {}
    for g in hry:
        if g.get("series"):
            continue
        # nazev bez cisla, podtitulu a rimske cislice na konci
        k = re.sub(r"[:\-–].*$", "", g["name"])
        k = re.sub(r"\s+(\d+|[IVX]+)$", "", k).strip().lower()
        if len(k) >= 4:
            zaklad.setdefault(k, []).append(g)

    # Serie potrebuje RUZNE tituly. Bez teto podminky se hlasila kazda hra,
    # ktera vysla na vic platforem — "2048, 2048" neni serie, ale tentyz titul.
    out = []
    for k, v in sorted(zaklad.items()):
        nazvy = {g["name"] for g in v}
        if len(nazvy) >= 2:
            out.append((k, v))
    return out


def main() -> int:
    a = sys.argv[1:]
    data = nacti()
    serie_slugy = {s["slug"] for s in data.get("series", [])}

    jen_plat = a[a.index("--platforma") + 1] if "--platforma" in a else None
    nove = int(a[a.index("--nove") + 1]) if "--nove" in a else 0
    seznam = "--seznam" in a

    hry = []
    for p in data["platforms"]:
        if jen_plat and p["slug"] != jen_plat:
            continue
        for g in p["games"]:
            hry.append((p, g))
    if nove:
        hry = hry[-nove:]

    pocty = Counter()
    vadne = []
    for p, g in hry:
        pr = problemy_hry(g, serie_slugy)
        if pr:
            vadne.append((p["slug"], g["name"], pr))
            for x in pr:
                pocty[re.sub(r"\d+", "N", x)] += 1

    print(f"kontrolovano her: {len(hry)}")
    print(f"  bez nedostatku: {len(hry) - len(vadne)}")
    print(f"  s nedostatkem:  {len(vadne)}\n")
    for druh, n in pocty.most_common():
        print(f"  {n:5}  {druh}")

    if seznam:
        print("\nKONKRETNE:")
        for plat, nazev, pr in vadne[:200]:
            print(f"  [{plat}] {nazev}: {', '.join(pr)}")

    # serie se hlasi zvlast — je to navrh k posouzeni, ne chyba
    vsechny = [g for _p, g in hry]
    navrhy = mozna_serie(vsechny)
    if navrhy:
        print(f"\nMOZNA SERIE (bez zarazeni): {len(navrhy)} skupin")
        for k, v in navrhy[:25]:
            print(f"  {k}: " + ", ".join(g["name"] for g in v[:4]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
