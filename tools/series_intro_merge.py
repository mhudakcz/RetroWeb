# -*- coding: utf-8 -*-
"""Slouci vystupy series_intro.workflow.js do src/data/series.json.

Workflow uklada davky jako intro_NN.json ve tvaru
{"<slug>": {"cs": ..., "en": ..., "de": ..., "fr": ...}}. Skript je nacte,
overi, ze slug v serii existuje a ze jsou vsechny ctyri jazyky dost dlouhe,
a zapise je k prislusnym seriim.

Pouziti:  python tools/series_intro_merge.py <workdir> [--min 900]
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERIES = ROOT / "src/data/series.json"
LANGS = ("cs", "en", "de", "fr")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    minimum = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 900

    series = json.loads(SERIES.read_text("utf-8"))
    by_slug = {s["slug"]: s for s in series}

    added = skipped = 0
    for f in sorted(work.glob("intro_*.json")):
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
            short = [k for k in LANGS if len((texts.get(k) or "").strip()) < minimum]
            if short:
                print(f"  [x] {slug}: prilis kratke jazyky {short}")
                skipped += 1
                continue
            s["intro"] = {k: texts[k].strip() for k in LANGS}
            added += 1

    with io.open(SERIES, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(series, fh, ensure_ascii=False, indent=1)
    total = sum(1 for s in series if s.get("intro"))
    print(f"uvodu doplneno: {added}" + (f", preskoceno: {skipped}" if skipped else ""))
    print(f"serii s uvodem: {total}/{len(series)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
