# -*- coding: utf-8 -*-
"""Pripravi davky pro years.workflow.js a slouci dohledane roky vydani.

913 her v katalogu nema uvedeny rok. Chybi tim udaj na karte hry, rozpada se
na tom parovani "Tentyz titul jinde" (hra bez roku spadne na rok platformy,
takze okno +-6 let neplati) a hlavne by takove hry nesly umistit na casovou osu.

Rok se plni do src/data/game_meta.json, odkud si ho parse_content.py bere jako
zalohu, kdyz ho podklady neuvadeji.

Pouziti:
  python tools/years_prep.py <workdir> [--size 30]   pripravi davky
  python tools/years_prep.py <workdir> --merge       slouci vystupy
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "src/data/game_meta.json"


def missing() -> list[dict]:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    out = []
    for p in data["platforms"]:
        for g in p["games"]:
            if re.search(r"\d{4}", str(g.get("year") or "")):
                continue
            out.append(
                {
                    "slug": g["slug"],
                    "name": g["name"],
                    "platform": p["name"],
                    "platform_years": f"{p['year']}+",
                    "studio": g.get("studio") or "",
                }
            )
    return out


def prepare(work: Path, size: int) -> None:
    work.mkdir(parents=True, exist_ok=True)
    todo = missing()
    if not todo:
        print("vsechny hry uz maji rok")
        return
    # davky po platformach, aby agent resil jednu éru najednou
    todo.sort(key=lambda g: (g["platform"], g["name"]))
    n = 0
    for i in range(0, len(todo), size):
        with io.open(work / f"years_{n:03d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(todo[i: i + size], fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"bez roku: {len(todo)} her -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path) -> None:
    meta = json.loads(META.read_text("utf-8")) if META.exists() else {}
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    plat_year = {p["slug"]: p["year"] for p in data["platforms"]}
    known = {g["slug"]: p["slug"] for p in data["platforms"] for g in p["games"]}

    added = bad = 0
    for f in sorted(work.glob("years_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for slug, year in got.items():
            m = re.search(r"\d{4}", str(year or ""))
            if not m or slug not in known:
                bad += 1
                continue
            y = int(m.group())
            # Hra nemohla vyjit pred uvedenim platformy ani po roce 2026.
            # Agent obcas vrati rok arkadoveho originalu misto roku portu.
            floor = plat_year.get(known[slug], 1970)
            if y < floor - 1 or y > 2026:
                print(f"  [x] {slug}: rok {y} mimo rozsah platformy ({floor}+)")
                bad += 1
                continue
            entry = meta.setdefault(slug, {})
            entry["year"] = str(y)
            added += 1

    with io.open(META, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"roku doplneno: {added}" + (f", zahozeno: {bad}" if bad else ""))
    print("spust jeste tools/parse_content.py")


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
        size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 30
        prepare(work, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
