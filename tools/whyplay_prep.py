# -*- coding: utf-8 -*-
"""Pripravi davky pro whyplay.workflow.js a slouci vysledek do clanku.

Cast clanku konci shrnujici vetou "**Proč hrát:** ...", ktera ctenari rovnou
rekne, proc si titul pustit. Vzniklo to jen u nekterych davek, takze ji ma
zhruba tretina her. Skript najde clanky bez ni, rozseka je do davek a po
dobehnuti workflow vetu pripoji na konec clanku.

Veta se pripisuje PRIMO do souboru, ze ktereho clanek pochazi — clanky jsou
rozsypane po src/data/articles/*.json a pozdejsi soubor drivejsi prepisuje,
takze zapis do zvlastniho souboru by cast z nich zase zahodil.

Pouziti:
  python tools/whyplay_prep.py <workdir> [--size 25]   pripravi davky
  python tools/whyplay_prep.py <workdir> --merge       slouci vystupy
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "src" / "data" / "articles"
MARK = "**Proč hrát:**"
MIN_LEN, MAX_LEN = 60, 320


def article_files() -> list[Path]:
    return sorted(ART.glob("*.json"))


def load_all() -> tuple[dict, dict]:
    """slug -> text a slug -> soubor, ve kterem text nakonec plati."""
    text, owner = {}, {}
    for f in article_files():
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for slug, md in d.items():
            if md and md.strip():
                text[slug] = md
                owner[slug] = f
    return text, owner



def uklid_stare_vystupy(work: Path) -> None:
    """Smaze vystupy z drivejsiho behu ve stejnem adresari.

    Bez toho agent najde cizi <davka>_out.json, vrati SKIP a prislusne hry
    zustanou nezpracovane, aniz to workflow ohlasi jako chybu.
    """
    stare = sorted(work.glob("*_out.json"))
    for f in stare:
        f.unlink()
    if stare:
        print(f"  (smazano {len(stare)} vystupu z drivejsiho behu)")


def prepare(work: Path, size: int) -> None:
    work.mkdir(parents=True, exist_ok=True)
    uklid_stare_vystupy(work)
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    text, _ = load_all()

    rows = []
    for p in data["platforms"]:
        for g in p["games"]:
            md = text.get(g["slug"])
            if not md or MARK in md:
                continue
            rows.append({
                "slug": g["slug"],
                "name": g["name"],
                "platform": p["name"],
                "year": str(g.get("year") or ""),
                "studio": g.get("studio") or "",
                "genre": g.get("genre") or "",
                # posledni odstavec nese vyzneni clanku, ze ktereho veta vychazi
                "zaver": re.sub(r"\s+", " ", md.strip().split("\n\n")[-1])[:700],
            })

    if not rows:
        print("vsechny clanky uz zaverecnou vetu maji")
        return
    n = 0
    for i in range(0, len(rows), size):
        with io.open(work / f"why_{n:03d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(rows[i: i + size], fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"bez zaverecne vety: {len(rows)} clanku -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path) -> None:
    text, owner = load_all()
    add: dict[Path, dict] = {}
    short = long = miss = 0

    for f in sorted(work.glob("why_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for slug, veta in got.items():
            veta = (veta or "").strip().rstrip()
            if slug not in text:
                miss += 1
                continue
            if MARK in text[slug]:
                continue
            if len(veta) < MIN_LEN:
                short += 1
                continue
            if len(veta) > MAX_LEN:
                long += 1
                continue
            add.setdefault(owner[slug], {})[slug] = veta

    total = 0
    for f, items in add.items():
        d = json.loads(f.read_text("utf-8"))
        for slug, veta in items.items():
            if MARK in d.get(slug, ""):
                continue
            d[slug] = d[slug].rstrip() + f"\n\n{MARK} {veta}"
            total += 1
        with io.open(f, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1)

    print(f"vet doplneno: {total} v {len(add)} souborech")
    if short or long or miss:
        print(f"  zahozeno: {short} kratkych, {long} dlouhych, {miss} neznamych slugu")
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
        size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 25
        prepare(work, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
