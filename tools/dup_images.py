# -*- coding: utf-8 -*-
"""Najde jeden a tyz obrazek pouzity u vic ruznych her.

Obaly a snimky se paruji podle nazvu hry. Kdyz se parovani netrefi, hra
dostane obrazek nekoho jineho — a protoze se stahuje z jednoho zdroje, stejny
soubor pak casto sedi u nekolika her najednou. Shoda otisku je proto spolehlivy
ukazatel spatneho parovani (napr. Tomb Raider II i III mely titulni obrazovku
hry "D" od Warp Inc.).

Ruzne hry TEZE serie mohou legitimne sdilet obal jen vyjimecne, takze kazdy
nalez stoji za rucni kontrolu.

Pouziti:  python tools/dup_images.py [--delete]
  --delete smaze soubory ve skupinach o trech a vice hrach (tam je jiste, ze
  parovani selhalo). Dvojice necha byt — casto jde o tutez hru vedenou
  v katalogu dvakrat, coz se ma resit v podkladech, ne mazanim obrazku.
"""
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "images" / "games"


def main() -> int:
    delete = "--delete" in sys.argv
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for f in IMG.rglob("*.*"):
        if f.suffix.lower() not in (".webp", ".png", ".jpg", ".jpeg"):
            continue
        by_hash[hashlib.sha1(f.read_bytes()).hexdigest()].append(f)

    groups = []
    for h, files in by_hash.items():
        # Zajima nas tentyz soubor u RUZNYCH her na TEZE platforme. Shoda napric
        # platformami je vetsinou v poradku — Halo Infinite na Xbox One i Series
        # ma pochopitelne stejny obal. Shoda uvnitr jedne platformy ale znamena,
        # ze se parovani netrefilo.
        per_plat = defaultdict(set)
        for f in files:
            stem = f.name.split("-snap")[0].split("-title")[0].split(".")[0]
            per_plat[f.parent.name].add(stem)
        if any(len(v) > 1 for v in per_plat.values()):
            groups.append(sorted(files))

    removed = 0
    for files in sorted(groups, key=len, reverse=True):
        print(f"  {len(files)}x stejny soubor:")
        for f in files:
            print(f"      {f.relative_to(IMG)}")
        if delete:
            # Kdyz tentyz soubor sdili tri a vic her, neni to nahoda ani
            # legitimni spolecny obal — parovani se netrefilo a spravna hra
            # mezi nimi neni, takze jdou pryc vsechny. U dvojic muze jit
            # o tutez hru vedenou v katalogu dvakrat, tam se necha rucni
            # kontrole a nemaze se nic.
            if len(files) >= 3:
                for f in files:
                    f.unlink()
                    removed += 1

    print(f"\nskupin se sdilenym obrazkem: {len(groups)}")
    if delete:
        print(f"smazano souboru: {removed}")
        print("spust jeste tools/parse_content.py")
    elif groups:
        print("(nic se nesmazalo — spust znovu s --delete)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
