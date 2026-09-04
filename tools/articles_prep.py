# -*- coding: utf-8 -*-
"""Pripravi davky pro articles_new.workflow.js a slouci vysledek.

Rozsirovaci nastroje (expand_short, whyplay) pocitaji s tim, ze clanek uz
existuje. Kdyz se do katalogu prida cela nova platforma, hry zadny clanek
nemaji a neni cim zacit — tenhle skript je ta chybejici prvni faze.

Vystup se zapisuje do src/data/articles/<prefix>.json. Pozdejsi soubor v tom
adresari prepisuje drivejsi, takze novy soubor nesmi mit jmeno, ktere uz
existuje; skript to hlida.

Pouziti:
  python tools/articles_prep.py <workdir> --platform mobil [--size 12]
  python tools/articles_prep.py <workdir> --merge --prefix mobil-01
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "src" / "data" / "articles"
# Musi odpovidat kontrole v articles_new.workflow.js.
MIN_LEN, MAX_LEN = 900, 3000


def existing_articles() -> dict:
    out = {}
    for f in sorted(ART.glob("*.json")):
        try:
            out.update(json.loads(f.read_text("utf-8")))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
    return out


def load_missing(platform: str | None) -> list[dict]:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    have = existing_articles()
    teasers = json.loads((ROOT / "src/data/game_teasers.json").read_text("utf-8"))

    rows = []
    for p in data["platforms"]:
        if platform and p["slug"] != platform:
            continue
        for g in p["games"]:
            if (have.get(g["slug"]) or "").strip():
                continue
            rows.append({
                "slug": g["slug"],
                "name": g["name"],
                "platform": p["name"],
                "year": str(g.get("year") or ""),
                "studio": g.get("studio") or "",
                "genre": g.get("genre") or "",
                "delka": g.get("length") or "",
                "teaser": teasers.get(g["slug"], ""),
            })
    return rows



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


def prepare(work: Path, platform: str | None, size: int) -> None:
    work.mkdir(parents=True, exist_ok=True)
    uklid_stare_vystupy(work)
    rows = load_missing(platform)
    if not rows:
        print("vsechny hry uz clanek maji")
        return
    n = 0
    for i in range(0, len(rows), size):
        with io.open(work / f"art_{n:03d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(rows[i: i + size], fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"bez clanku: {len(rows)} her -> {n} davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path, prefix: str) -> None:
    dst = ART / f"{prefix}.json"
    if dst.exists():
        print(f"[x] {dst.name} uz existuje — zvol jiny --prefix, prepsal bys hotovou davku")
        return
    have = existing_articles()
    out, short, long, dup = {}, 0, 0, 0

    for f in sorted(work.glob("art_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for slug, md in got.items():
            md = (md or "").strip()
            if (have.get(slug) or "").strip():
                dup += 1
                continue
            if len(md) < MIN_LEN:
                short += 1
                continue
            if len(md) > MAX_LEN:
                long += 1
                continue
            out[slug] = md

    if not out:
        print("nic k ulozeni")
        return
    with io.open(dst, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    whyplay = sum(1 for v in out.values() if "**Proč hrát:**" in v)
    print(f"clanku ulozeno: {len(out)} -> {dst.relative_to(ROOT)}")
    print(f"  se zaverecnou vetou: {whyplay}/{len(out)}")
    if short or long or dup:
        print(f"  zahozeno: {short} kratkych, {long} dlouhych, {dup} uz existujicich")
    print("spust jeste tools/parse_content.py")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d  # noqa: E731

    if "--merge" in sys.argv:
        prefix = arg("--prefix")
        if not prefix or not re.fullmatch(r"[a-z0-9-]+", prefix):
            print("[x] --merge potrebuje --prefix (mala pismena, cislice, pomlcky)")
            return 1
        merge(work, prefix)
    else:
        prepare(work, arg("--platform"), int(arg("--size", 12)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
