# -*- coding: utf-8 -*-
"""Pripravi davky pro platform_ports.workflow.js a slouci jeho vystupy.

Katalog vede hru zvlast pro kazdou platformu, ale u vetsiny multiplatformnich
titulu mame jen nektera vydani: Call of Duty: Black Ops III jen na Xboxu One,
Ghosts jen na Wii U. Na strance hry pak chybi "tentyz titul jinde" a na platforme
chybi hra, ktera na ni doopravdy vysla.

Tenhle skript najde tituly, ktere vypadaji multiplatformne, a preda je agentovi,
at doplni vydani, kterymi si je jisty.

Pouziti:
  python tools/porty_prep.py <workdir> [--serie] [--od ROK] [--size 8]
      --serie   jen tituly patrici do nektere vedene serie (nejviditelnejsi mezera)
      --od ROK  jen tituly vydane od daneho roku
  python tools/porty_prep.py <workdir> --merge
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXTRA = ROOT / "src/data/extra_games.json"
META = ROOT / "src/data/game_meta.json"
ARTDIR = ROOT / "src/data/articles"

# Platformy, na ktere smi agent doplnovat. Drzi se seznamu ve workflow —
# u osmibitu a arkad je "port" casto uplne jina hra pod stejnym nazvem.
POVOLENE = {
    "pc-modern", "pc-9x", "pc-dos", "ps2", "ps3", "ps4", "ps5", "playstation",
    "xbox", "xbox-360", "xbox-one", "xbox-series", "switch", "gamecube", "wii",
    "wii-u", "nds", "psp", "ps-vita", "dreamcast", "saturn", "n64", "snes",
    "mega-drive",
}


def _serie_vzory():
    defs = json.loads((ROOT / "src/data/series.json").read_text("utf-8"))
    out = []
    for d in defs:
        skip = [e.lower() for e in (d.get("exclude") or [])]
        rx = [re.compile(r"(?<![a-z0-9])" + re.escape(m.lower()) + r"(?![a-z0-9])")
              for m in d["match"]]
        out.append((rx, skip))
    return out


def _v_serii(nazev, vzory):
    n = nazev.lower()
    for rx, skip in vzory:
        if any(e in n for e in skip):
            continue
        if any(r.search(n) for r in rx):
            return True
    return False


def prepare(work: Path, jen_serie: bool, od_roku: int, size: int) -> None:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    vzory = _serie_vzory() if jen_serie else None

    kde = {}
    rok = {}
    for p in data["platforms"]:
        for g in p["games"]:
            kde.setdefault(g["name"], set()).add(p["slug"])
            y = str(g.get("year") or "")
            if y.isdigit():
                rok[g["name"]] = min(int(y), rok.get(g["name"], 9999))

    todo = []
    for nazev, platformy in sorted(kde.items()):
        # Titul, ktery uz je na vsech povolenych platformach, nema co doplnovat.
        if POVOLENE <= platformy:
            continue
        # Hra, ktera u nas zije jen mimo povolene platformy (arkada, osmibit),
        # se sem netahne — tam by "port" byla jina hra pod stejnym nazvem.
        if not (platformy & POVOLENE):
            continue
        if jen_serie and not _v_serii(nazev, vzory):
            continue
        r = rok.get(nazev, 0)
        if od_roku and r and r < od_roku:
            continue
        todo.append({"name": nazev, "year": str(r or ""), "have": sorted(platformy)})

    work.mkdir(parents=True, exist_ok=True)
    n = 0
    for i in range(0, len(todo), size):
        with io.open(work / f"ports_{n:02d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(todo[i: i + size], fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"titulu k posouzeni: {len(todo)} -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def _slugify(platform: str, name: str) -> str:
    z = name.lower()
    z = z.replace("&", " and ")
    z = re.sub(r"[^a-z0-9]+", "-", z).strip("-")
    return f"{platform}__{z}"


def merge(work: Path) -> None:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    zname = {(p["slug"], g["name"].lower()) for p in data["platforms"] for g in p["games"]}
    znamy_slug = {g["slug"] for p in data["platforms"] for g in p["games"]}
    plat_rok = {p["slug"]: p["year"] for p in data["platforms"]}

    extra = json.loads(EXTRA.read_text("utf-8")) if EXTRA.exists() else {}
    meta = json.loads(META.read_text("utf-8")) if META.exists() else {}
    clanky = {}

    pridano = preskoceno = 0
    duvody = {}

    def zahod(duvod):
        duvody[duvod] = duvody.get(duvod, 0) + 1

    for f in sorted(work.glob("ports_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        if not isinstance(got, list):
            print(f"  [x] {f.name}: neni pole")
            continue
        for it in got:
            plat = (it.get("platform") or "").strip()
            nazev = (it.get("name") or "").strip()
            clanek = (it.get("article") or "").strip()
            if plat not in POVOLENE or not nazev:
                zahod("neplatna platforma nebo nazev")
                preskoceno += 1
                continue
            if (plat, nazev.lower()) in zname:
                zahod("uz v katalogu")
                preskoceno += 1
                continue
            if len(clanek) < 1300:
                zahod("clanek pod limitem")
                preskoceno += 1
                continue
            rok = re.search(r"\d{4}", str(it.get("year") or ""))
            if not rok:
                zahod("bez roku")
                preskoceno += 1
                continue
            y = int(rok.group())
            # Hra nemohla vyjit pred uvedenim platformy. Agent obcas vrati rok
            # puvodni verze misto roku portu.
            if y < plat_rok.get(plat, 1970) - 1 or y > 2026:
                zahod("rok mimo rozsah platformy")
                preskoceno += 1
                continue

            gslug = _slugify(plat, nazev)
            # extra_games drzi seznam objektu {name, genre, ...}, ne slugu
            uz_v_extra = any(_slugify(plat, x.get("name", "")) == gslug
                             for x in extra.get(plat, []))
            if gslug in znamy_slug or uz_v_extra:
                zahod("slug uz existuje")
                preskoceno += 1
                continue

            extra.setdefault(plat, []).append({
                "name": nazev,
                "genre": (it.get("genre") or "").strip(),
                "length": (it.get("length") or "M").strip(),
                "flags": it.get("flags") or [],
            })
            meta.setdefault(gslug, {})["year"] = str(y)
            if (it.get("studio") or "").strip():
                meta[gslug]["studio"] = it["studio"].strip()
            clanky[gslug] = clanek
            znamy_slug.add(gslug)
            zname.add((plat, nazev.lower()))
            pridano += 1

    EXTRA.write_text(json.dumps(extra, ensure_ascii=False, indent=1), encoding="utf-8")
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True),
                    encoding="utf-8")
    if clanky:
        cil = ARTDIR / "porty.json"
        stare = json.loads(cil.read_text("utf-8")) if cil.exists() else {}
        stare.update(clanky)
        cil.write_text(json.dumps(stare, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"vydani pridano: {pridano}, preskoceno: {preskoceno}")
    for k, v in sorted(duvody.items(), key=lambda x: -x[1]):
        print(f"  {v:5}  {k}")
    print("spust jeste tools/parse_content.py")


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    work = Path(a[0])
    if not work.is_absolute():
        work = ROOT / work
    if "--merge" in a:
        merge(work)
    else:
        size = int(a[a.index("--size") + 1]) if "--size" in a else 8
        od = int(a[a.index("--od") + 1]) if "--od" in a else 0
        prepare(work, "--serie" in a, od, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
