# -*- coding: utf-8 -*-
"""Pripravi davky pro teasers.workflow.js a slouci jejich vystup.

Uvodni shrnujici vetu ma kazda hra na starsich platformach; nove pridane hry
ji nemaji, dokud ji nekdo nedopise. Skript najde hry bez vety, rozseka je do
davek po N kusech a po dobehnuti workflow je slouci zpet do
src/data/game_teasers.json.

Pouziti:
  python tools/teasers_prep.py <workdir> [--size 25] [--platform mobil]
  python tools/teasers_prep.py <workdir> --merge       slouci vystupy
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEASER_FILE = ROOT / "src/data/game_teasers.json"
# Musi odpovidat kontrole delky v teasers.workflow.js.
MIN_LEN, MAX_LEN = 30, 140


def load_missing(platform: str | None = None) -> list[dict]:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    teasers = json.loads(TEASER_FILE.read_text("utf-8")) if TEASER_FILE.exists() else {}
    articles = {}
    for f in sorted((ROOT / "src/data/articles").glob("*.json")):
        articles.update(json.loads(f.read_text("utf-8")))

    out = []
    for p in data["platforms"]:
        # nova platforma se doplnuje po castech; bez filtru by davka nabrala
        # i stovky her odjinud, ktere na vetu jeste cekaji
        if platform and p["slug"] != platform:
            continue
        for g in p["games"]:
            if g.get("teaser") or teasers.get(g["slug"]):
                continue
            art = articles.get(g["slug"]) or ""
            # Prvni odstavec staci jako podklad; cely clanek by davky zbytecne nafoukl.
            snippet = re.sub(r"\s+", " ", art.split("\n\n")[0])[:700]
            out.append(
                {
                    "slug": g["slug"],
                    "name": g["name"],
                    "platform": p["name"],
                    "genre": g.get("genre") or "",
                    "year": str(g.get("year") or ""),
                    "studio": g.get("studio") or "",
                    "uryvek": snippet,
                }
            )
    return out



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


def prepare(work: Path, size: int, platform: str | None = None) -> int:
    work.mkdir(parents=True, exist_ok=True)
    uklid_stare_vystupy(work)
    missing = load_missing(platform)
    if not missing:
        print("vsechny hry uz uvodni vetu maji")
        return 0
    n = 0
    for i in range(0, len(missing), size):
        chunk = missing[i: i + size]
        dst = work / f"teaser_{i // size:03d}.json"
        with io.open(dst, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(chunk, fh, ensure_ascii=False, indent=1)
        n += 1
    print(f"bez uvodni vety: {len(missing)} her -> {n} davek po {size} v {work}")
    print(f'spust workflow s args {{"base": "{work.as_posix()}", "batches": {n}}}')
    return n


def merge(work: Path) -> int:
    teasers = json.loads(TEASER_FILE.read_text("utf-8")) if TEASER_FILE.exists() else {}
    before = len(teasers)
    added = short = long = 0
    for f in sorted(work.glob("teaser_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for slug, veta in got.items():
            veta = (veta or "").strip()
            if len(veta) < MIN_LEN:
                short += 1
                continue
            if len(veta) > MAX_LEN:
                long += 1
                continue
            teasers[slug] = veta
            added += 1
    with io.open(TEASER_FILE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(teasers, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"teasery: {before} -> {len(teasers)} (+{added})")
    if short or long:
        print(f"  zahozeno mimo delku {MIN_LEN}-{MAX_LEN}: {short} kratkych, {long} dlouhych")
    print("spust jeste tools/parse_content.py")
    return added


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = ROOT / sys.argv[1] if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    if "--merge" in sys.argv:
        merge(work)
        return 0
    size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 25
    platform = sys.argv[sys.argv.index("--platform") + 1] if "--platform" in sys.argv else None
    prepare(work, size, platform)
    return 0


if __name__ == "__main__":
    sys.exit(main())
