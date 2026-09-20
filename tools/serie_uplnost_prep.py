# -*- coding: utf-8 -*-
"""Pripravi davky pro serie_uplnost.workflow.js a slouci jeho vystupy.

Doplnovani portu resi jen tituly, ktere uz v katalogu jsou. Kdyz cely dil serie
chybi (Legend of Grimrock, Hades II, puvodni Rogue), zadny port ho nezalozi.
Tenhle nastroj preda agentovi serii i s tim, co uz mame, a chce jen to, co chybi.

Vystup se sloucenim promeni v davky pro platform_ports.workflow.js — ten uz umi
z {name, year, have} vyrobit plny zaznam vcetne clanku.

Pouziti:
  python tools/serie_uplnost_prep.py <workdir> [--serie "a,b,c"] [--size 6]
  python tools/serie_uplnost_prep.py <workdir> --merge <cil_pro_porty>
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _hry_serie(d, hry):
    skip = [e.lower() for e in (d.get("exclude") or [])]
    explicit = set(d.get("games") or [])
    rx = [re.compile(r"(?<![a-z0-9])" + re.escape(m.lower()) + r"(?![a-z0-9])")
          for m in d["match"]]
    out = set()
    for g in hry:
        if explicit:
            if g["slug"] in explicit:
                out.add(g["name"])
            continue
        n = g["name"].lower()
        if any(e in n for e in skip):
            continue
        if any(r.search(n) for r in rx):
            out.add(g["name"])
    return sorted(out)


def prepare(work: Path, jen: list, size: int) -> None:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    defs = json.loads((ROOT / "src/data/series.json").read_text("utf-8"))
    hry = [g for p in data["platforms"] for g in p["games"]]

    polozky = []
    for d in defs:
        if jen and d["slug"] not in jen and d["name"].lower() not in jen:
            continue
        mame = _hry_serie(d, hry)
        if not mame:
            continue
        polozky.append({"serie": d["name"], "mame": mame})

    work.mkdir(parents=True, exist_ok=True)
    n = 0
    for i in range(0, len(polozky), size):
        (work / f"uplnost_{n:03d}_in.json").write_text(
            json.dumps(polozky[i: i + size], ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
    print(f"serii k posouzeni: {len(polozky)} -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path, cil: Path, size: int) -> None:
    """Chybejici tituly promeni v davky pro platform_ports.workflow.js."""
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    kde = {}
    for p in data["platforms"]:
        for g in p["games"]:
            kde.setdefault(g["name"].lower(), set()).add(p["slug"])

    nalezeno, preskoceno = [], 0
    videno = set()
    for f in sorted(work.glob("uplnost_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        if not isinstance(got, list):
            print(f"  [x] {f.name}: neni pole")
            continue
        for it in got:
            nazev = (it.get("name") or "").strip()
            if not nazev:
                continue
            klic = nazev.lower()
            if klic in videno:
                preskoceno += 1
                continue
            # Agent obcas vrati titul, ktery uz mame pod presne stejnym nazvem.
            if klic in kde:
                preskoceno += 1
                continue
            videno.add(klic)
            nalezeno.append({
                "name": nazev,
                "year": str(it.get("year") or ""),
                "have": [],
                "serie": it.get("serie") or "",
            })

    cil.mkdir(parents=True, exist_ok=True)
    n = 0
    for i in range(0, len(nalezeno), size):
        (cil / f"ports_{n:02d}.json").write_text(
            json.dumps([{k: v for k, v in x.items() if k != "serie"}
                        for x in nalezeno[i: i + size]], ensure_ascii=False, indent=1),
            encoding="utf-8")
        n += 1
    (cil / "_nalezeno.json").write_text(
        json.dumps(nalezeno, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"chybejicich titulu: {len(nalezeno)}" +
          (f", preskoceno (uz mame nebo duplicita): {preskoceno}" if preskoceno else ""))
    print(f'args: {{"base": "{cil.as_posix()}", "batches": {n}}}')


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    work = Path(a[0])
    if not work.is_absolute():
        work = ROOT / work
    size = int(a[a.index("--size") + 1]) if "--size" in a else 6
    if "--merge" in a:
        cil = Path(a[a.index("--merge") + 1])
        if not cil.is_absolute():
            cil = ROOT / cil
        merge(work, cil, size)
    else:
        jen = [x.strip().lower() for x in a[a.index("--serie") + 1].split(",")] \
            if "--serie" in a else []
        prepare(work, jen, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
