# -*- coding: utf-8 -*-
"""Pripravi davky pro titles.workflow.js z konkretniho seznamu nazvu.

Na rozdil od newgames_prep, kde agent tituly sam vymysli podle tematickeho
okruhu, tady dostane hotovy seznam — treba z zebricku na Vimm's Lair — a jeho
ukolem je jen napsat k nim zaznamy. Diky tomu se do katalogu dostanou presne
ty hry, ktere chybi, a ne nahodny vyber.

Vstupem je report.json z tools/vimm_ranks.py (klic "chybi").

Pouziti:
  python tools/titles_prep.py <workdir> <report.json> [--size 10]
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    report = Path(sys.argv[2])
    if not report.is_absolute():
        report = ROOT / report
    size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 10

    work.mkdir(parents=True, exist_ok=True)
    chybi = json.loads(report.read_text("utf-8"))["chybi"]
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    jmena = {p["slug"]: p["name"] for p in data["platforms"]}
    # hry, ktere uz na platforme mame — aby agent nenavrhl duplicitu
    stavajici = {p["slug"]: sorted(g["name"] for g in p["games"])
                 for p in data["platforms"]}

    n = 0
    for slug, tituly in sorted(chybi.items()):
        for i in range(0, len(tituly), size):
            cast = tituly[i:i + size]
            davka = {
                "slug": slug,
                "platform": jmena.get(slug, slug),
                "tituly": cast,
                "uz_mame": stavajici.get(slug, []),
            }
            with io.open(work / f"tit_{n:03d}.json", "w", encoding="utf-8", newline="\n") as fh:
                json.dump(davka, fh, ensure_ascii=False, indent=1)
            n += 1

    celkem = sum(len(v) for v in chybi.values())
    print(f"titulu k doplneni: {celkem} -> {n} davek")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
