# -*- coding: utf-8 -*-
"""Pripravi davky pro studios.workflow.js a slouci dohledane vyvojare.

914 her v katalogu nema uvedene studio. Na karte hry tim chybi radek, hra se
neobjevi na strance zadneho vyvojare a rozpada se na tom i prehled "od stejneho
studia". Postup je stejny jako u roku vydani (tools/years_prep.py): agent dostane
davku her, vrati {slug: "studio"} a nejiste tituly vynecha.

Studio se plni do src/data/game_meta.json, odkud si ho parse_content.py bere
jako zalohu, kdyz ho podklady neuvadeji.

Pouziti:
  python tools/studios_prep.py <workdir> [--size 30]   pripravi davky
  python tools/studios_prep.py <workdir> --merge       slouci vystupy
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "src/data/game_meta.json"

# Co se do pole "studio" nepusti. Agenti sem obcas davaji vydavatele nebo
# zastupnou frazi misto jmena vyvojare.
NEPLATNE = {
    "neznámé", "nezname", "unknown", "n/a", "na", "-", "?", "various",
    "ruzne", "různé", "homebrew", "indie", "nezname studio",
}


def missing() -> list[dict]:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    out = []
    for p in data["platforms"]:
        for g in p["games"]:
            if (g.get("studio") or "").strip():
                continue
            out.append(
                {
                    "slug": g["slug"],
                    "name": g["name"],
                    "platform": p["name"],
                    "year": str(g.get("year") or ""),
                    "genre": g.get("genre") or "",
                }
            )
    return out


def prepare(work: Path, size: int) -> None:
    work.mkdir(parents=True, exist_ok=True)
    todo = missing()
    if not todo:
        print("vsechny hry uz maji studio")
        return
    # davky po platformach, at agent resi jednu eru a jednu scenu najednou
    todo.sort(key=lambda g: (g["platform"], g["name"]))
    n = 0
    for i in range(0, len(todo), size):
        with io.open(work / f"studios_{n:03d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(todo[i: i + size], fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"bez studia: {len(todo)} her -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path) -> None:
    meta = json.loads(META.read_text("utf-8")) if META.exists() else {}
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    known = {g["slug"] for p in data["platforms"] for g in p["games"]}

    added = bad = 0
    for f in sorted(work.glob("studios_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for slug, studio in got.items():
            s = re.sub(r"\s+", " ", str(studio or "")).strip(" .,;")
            if slug not in known or len(s) < 2 or s.lower() in NEPLATNE:
                bad += 1
                continue
            # Delsi nez jmeno studia byva veta ("vyvinulo studio X"), ne udaj.
            if len(s) > 60:
                bad += 1
                continue
            entry = meta.setdefault(slug, {})
            entry["studio"] = s
            added += 1

    with io.open(META, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"studii doplneno: {added}" + (f", zahozeno: {bad}" if bad else ""))
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
