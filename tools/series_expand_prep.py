# -*- coding: utf-8 -*-
"""Pripravi davky pro series_expand.workflow.js a slouci jejich vystup.

Uvodni texty k seriim vznikly na cilovou delku 1100-1400 znaku, coz je na
pruvodce serii, ktera ma za sebou deset dilu, prilis strucne. Skript vezme
serie, ktere uz uvod maji, rozseka je do davek a ke kazde ulozi soucasny text
jako podklad, aby ho agent rozsiril misto psani od nuly.

Pouziti:
  python tools/series_expand_prep.py <workdir> [--size 5] [--min 2000]
  python tools/series_expand_prep.py <workdir> --merge [--min 2000]
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERIES = ROOT / "src/data/series.json"
LANGS = ("cs", "en", "de", "fr")


def series_stats() -> dict[str, dict]:
    """Ke kazde serii spocita, kolik her v katalogu pokryva a z jakych let."""
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    games = []
    for p in data["platforms"]:
        for g in p["games"]:
            m = re.search(r"\d{4}", str(g.get("year") or ""))
            games.append(
                {
                    "slug": g["slug"],
                    "name": g["name"],
                    "platform": p["name"],
                    "year": int(m.group()) if m else p["year"],
                }
            )

    out = {}
    for s in json.loads(SERIES.read_text("utf-8")):
        if s.get("games"):
            want = set(s["games"])
            hits = [g for g in games if g["slug"] in want]
        else:
            hits = [
                g
                for g in games
                if any(re.search(r"\b" + re.escape(m) + r"\b", g["name"], re.I)
                       for m in s.get("match", []))
                and not any(re.search(r"\b" + re.escape(x) + r"\b", g["name"], re.I)
                            for x in s.get("exclude", []))
            ]
        if not hits:
            continue
        yrs = sorted(g["year"] for g in hits)
        plats = sorted({g["platform"] for g in hits})
        out[s["slug"]] = {
            "slug": s["slug"],
            "name": s["name"],
            "count": len(hits),
            "span": f"{yrs[0]}-{yrs[-1]}",
            "platforms": ", ".join(plats[:8]) + (" a dalsi" if len(plats) > 8 else ""),
        }
    return out


def prepare(work: Path, size: int, minimum: int) -> None:
    work.mkdir(parents=True, exist_ok=True)
    stats = series_stats()
    series = json.loads(SERIES.read_text("utf-8"))
    todo = [
        s
        for s in series
        if s.get("intro")
        and s["slug"] in stats
        and len((s["intro"].get("cs") or "")) < minimum
    ]
    if not todo:
        print("vsechny serie uz maji dost dlouhy uvod")
        return

    batches = [todo[i: i + size] for i in range(0, len(todo), size)]
    meta = []
    for i, b in enumerate(batches):
        cur = {s["slug"]: {k: s["intro"].get(k, "") for k in LANGS} for s in b}
        with io.open(work / f"current_{i:02d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(cur, fh, ensure_ascii=False, indent=1)
        meta.append([stats[s["slug"]] for s in b])

    args = {"base": work.as_posix(), "batches": meta}
    with io.open(work / "args.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(args, fh, ensure_ascii=False, indent=1)
    print(f"k rozsireni: {len(todo)} serii -> {len(batches)} davek po {size}")
    print(f"args ulozeny v {work / 'args.json'}")


def merge(work: Path, minimum: int) -> None:
    series = json.loads(SERIES.read_text("utf-8"))
    by_slug = {s["slug"]: s for s in series}
    added = skipped = 0
    for f in sorted(work.glob("exp_*.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for slug, texts in got.items():
            s = by_slug.get(slug)
            if not s:
                print(f"  [x] {slug}: takova serie neexistuje")
                skipped += 1
                continue
            new = {k: (texts.get(k) or "").strip() for k in LANGS}
            old = s.get("intro") or {}
            # Kratsi vysledek by byl krok zpet — puvodni text je pak lepsi.
            worse = [k for k in LANGS if len(new[k]) <= len(old.get(k) or "")]
            if worse:
                print(f"  [x] {slug}: nova verze neni delsi v {worse}, ponechan puvodni")
                skipped += 1
                continue
            s["intro"] = new
            added += 1
    with io.open(SERIES, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(series, fh, ensure_ascii=False, indent=1)
    lens = sorted(len(s["intro"]["cs"]) for s in series if s.get("intro"))
    print(f"rozsireno: {added}" + (f", preskoceno: {skipped}" if skipped else ""))
    if lens:
        print(f"delky CZ: min {lens[0]}, median {lens[len(lens) // 2]}, max {lens[-1]}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    minimum = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 2000
    if "--merge" in sys.argv:
        merge(work, minimum)
    else:
        size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 5
        prepare(work, size, minimum)
    return 0


if __name__ == "__main__":
    sys.exit(main())
