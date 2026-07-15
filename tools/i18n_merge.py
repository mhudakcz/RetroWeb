# -*- coding: utf-8 -*-
"""Sloučí přeložené dávky (chunks/*_out.json = {en:{...}, de:{...}}) do
src/data/i18n/<locale>/<type>.json. Nevalidní chunky přeskočí a nahlásí."""
import json, sys, glob, os, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = Path(sys.argv[1])
CH = BASE / "chunks"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "data" / "i18n"

TYPES = ["games", "platforms", "studios", "hardware_sections", "hardware_meta"]
acc = {"en": {t: {} for t in TYPES}, "de": {t: {} for t in TYPES}}
ok = bad = 0
bad_files = []

for f in sorted(glob.glob(str(CH / "*_out.json"))):
    base = os.path.basename(f)
    m = re.match(r"(games|platforms|studios|hardware_sections|hardware_meta)_\d+_out\.json", base)
    if not m:
        continue
    typ = m.group(1)
    try:
        d = json.loads(Path(f).read_text("utf-8"))
    except Exception:
        bad += 1; bad_files.append(base); continue
    for loc in ("en", "de"):
        part = d.get(loc)
        if isinstance(part, dict):
            acc[loc][typ].update(part)
    ok += 1

for loc in ("en", "de"):
    (OUT / loc).mkdir(parents=True, exist_ok=True)
    for t in TYPES:
        data = acc[loc][t]
        if data:
            (OUT / loc / f"{t}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"sloučeno chunků: {ok}  | nevalidních: {bad}")
if bad_files:
    print("  BAD:", ", ".join(bad_files[:20]))
for loc in ("en", "de"):
    counts = {t: len(acc[loc][t]) for t in TYPES if acc[loc][t]}
    print(f"  {loc}: {counts}")
