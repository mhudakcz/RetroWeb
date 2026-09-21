# -*- coding: utf-8 -*-
"""Pripravi davky pro hardware.workflow.js a slouci je do hardware_extra.json.

Katalog hardwaru mel dvanact polozek a z toho jen tri kapesni konzole, prestoze
prave ty jsou dnes hlavni cesta k retro hrani. Seznam nize jde po rodinach:
Anbernic ma desitky modelu, ktere se lisi tvarem a vykonem, a vedle nej stoji
dalsi znacky.

Zarizeni, kterym si agent nebude jisty, vynecha — radsi chybejici polozka nez
vymyslene parametry.

Pouziti:
  python tools/hardware_prep.py <workdir> [--size 4]
  python tools/hardware_prep.py <workdir> --merge
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CIL = ROOT / "src/data/hardware_extra.json"
RUCNE = ROOT / "src/data/hardware.ts"

# (slug, nazev, znacka)
ZARIZENI = [
    # --- Anbernic, rada RG35XX ---
    ("rg35xx", "Anbernic RG35XX", "Anbernic"),
    ("rg35xx-plus", "Anbernic RG35XX Plus", "Anbernic"),
    ("rg35xx-h", "Anbernic RG35XX H", "Anbernic"),
    ("rg35xx-sp", "Anbernic RG35XX SP", "Anbernic"),
    ("rg28xx", "Anbernic RG28XX", "Anbernic"),
    ("rg34xx", "Anbernic RG34XX", "Anbernic"),
    # --- Anbernic, vetsi modely ---
    ("rg40xx-h", "Anbernic RG40XX H", "Anbernic"),
    ("rg40xx-v", "Anbernic RG40XX V", "Anbernic"),
    ("rg-cubexx", "Anbernic RG CubeXX", "Anbernic"),
    ("rg556", "Anbernic RG556", "Anbernic"),
    ("rg505", "Anbernic RG505", "Anbernic"),
    ("rg405m", "Anbernic RG405M", "Anbernic"),
    ("rg405v", "Anbernic RG405V", "Anbernic"),
    ("rg353v", "Anbernic RG353V", "Anbernic"),
    ("rg353m", "Anbernic RG353M", "Anbernic"),
    ("rg503", "Anbernic RG503", "Anbernic"),
    ("rg-arc-d", "Anbernic RG ARC-D", "Anbernic"),
    # --- klony a levnejsi rady, na ktere se lide ptaji ---
    ("r36-max", "R36 Max", "klony R36"),
    ("s36r", "S36R", "klony R36"),
    ("x9-handheld", "Black Hawk X9", "levne handheldy"),
    ("x20-handheld", "Black Hawk X20", "levne handheldy"),
    # --- ostatni znacky ---
    ("miyoo-mini-v4", "Miyoo Mini V4", "Miyoo"),
    ("miyoo-a30", "Miyoo A30", "Miyoo"),
    ("miyoo-flip", "Miyoo Flip", "Miyoo"),
    ("retroid-pocket-4-pro", "Retroid Pocket 4 Pro", "Retroid"),
    ("retroid-pocket-5", "Retroid Pocket 5", "Retroid"),
    ("retroid-pocket-mini", "Retroid Pocket Mini", "Retroid"),
    ("ayn-odin-2", "AYN Odin 2", "AYN"),
    ("powkiddy-rgb30", "Powkiddy RGB30", "Powkiddy"),
    ("powkiddy-x55", "Powkiddy X55", "Powkiddy"),
    ("trimui-smart-pro", "TrimUI Smart Pro", "TrimUI"),
    ("trimui-brick", "TrimUI Brick", "TrimUI"),
    ("gkd-pixel", "GKD Pixel", "GKD"),
]

POVOLENE_UROVNE = {"ok", "most", "some"}


def _uz_mame() -> set:
    """Slugy rucne psanych polozek — ty se znovu nezakladaji."""
    s = RUCNE.read_text("utf-8")
    return set(re.findall(r"slug:\s*'([^']+)'", s))


def prepare(work: Path, size: int) -> None:
    mame = _uz_mame()
    todo = [{"slug": s, "name": n, "znacka": z}
            for s, n, z in ZARIZENI if s not in mame]
    work.mkdir(parents=True, exist_ok=True)
    n = 0
    for i in range(0, len(todo), size):
        (work / f"hw_{n:02d}_in.json").write_text(
            json.dumps(todo[i: i + size], ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
    print(f"zarizeni k popsani: {len(todo)} -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path) -> None:
    mame = _uz_mame()
    stare = json.loads(CIL.read_text("utf-8")) if CIL.exists() else []
    podle_slugu = {x["slug"]: x for x in stare}

    pridano = preskoceno = 0
    duvody = {}

    def zahod(d):
        duvody[d] = duvody.get(d, 0) + 1

    for f in sorted(work.glob("hw_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        if not isinstance(got, list):
            print(f"  [x] {f.name}: neni pole")
            continue
        for it in got:
            slug = (it.get("slug") or "").strip()
            if not slug or slug in mame:
                zahod("chybi slug nebo uz je rucne psany")
                preskoceno += 1
                continue
            # Bez techto poli by stranka zarizeni byla prazdna.
            if not it.get("name") or not it.get("intro") or not it.get("sections"):
                zahod("chybi nazev, uvod nebo oddily")
                preskoceno += 1
                continue
            urovne = {c.get("level") for c in (it.get("canPlay") or [])}
            if urovne - POVOLENE_UROVNE:
                zahod("neplatna uroven v canPlay")
                preskoceno += 1
                continue
            it.setdefault("art", "handheld-h")
            it.setdefault("color", "#7c5cff")
            it.setdefault("color2", "#1a1030")
            it.setdefault("specs", [])
            it.setdefault("canPlay", [])
            it.setdefault("options", [])
            podle_slugu[slug] = it
            pridano += 1

    vysledek = sorted(podle_slugu.values(), key=lambda x: x["slug"])
    CIL.write_text(json.dumps(vysledek, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(f"zarizeni zapsano: {pridano}, preskoceno: {preskoceno}, celkem v souboru: {len(vysledek)}")
    for k, v in sorted(duvody.items(), key=lambda x: -x[1]):
        print(f"  {v:4}  {k}")


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
        size = int(a[a.index("--size") + 1]) if "--size" in a else 4
        prepare(work, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
