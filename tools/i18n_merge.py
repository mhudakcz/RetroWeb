# -*- coding: utf-8 -*-
"""Sloučí přeložené dávky (chunks/*_out.json = {en?:{...}, de?:{...}, fr?:{...}}) do
src/data/i18n/<locale>/<type>.json. Nevalidní chunky přeskočí a nahlásí.
Slučuje do STÁVAJÍCÍCH souborů (idempotentní/akumulativní — pro resumovatelný běh)."""
import json, sys, glob, os, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = Path(sys.argv[1])
CH = BASE / "chunks"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "data" / "i18n"

TYPES = ["games", "platforms", "studios", "hardware_sections", "hardware_meta"]
LOCALES = ["en", "de", "fr"]
acc = {loc: {t: {} for t in TYPES} for loc in LOCALES}
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
    for loc in LOCALES:
        part = d.get(loc)
        if isinstance(part, dict):
            acc[loc][typ].update(part)
    ok += 1

for loc in LOCALES:
    (OUT / loc).mkdir(parents=True, exist_ok=True)
    for t in TYPES:
        data = acc[loc][t]
        if not data:
            continue
        dst = OUT / loc / f"{t}.json"
        existing = {}
        if dst.exists():
            try:
                existing = json.loads(dst.read_text("utf-8"))
                if not isinstance(existing, dict):
                    existing = {}
            except Exception:
                existing = {}
        # Slučuje se PO POLÍCH. Mělký update() by u her nahradil celý záznam:
        # dávka s pouhým {teaser} by přepsala {detail, article} a překlady článků
        # by zmizely. Slovník se proto doplňuje klíč po klíči, ostatní typy
        # (řetězec u studií, pole sekcí u hardwaru) se nahrazují celé.
        for slug, val in data.items():
            cur = existing.get(slug)
            if isinstance(cur, dict) and isinstance(val, dict):
                cur.update(val)
            else:
                existing[slug] = val
        dst.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"sloučeno chunků: {ok}  | nevalidních: {bad}")
if bad_files:
    print("  BAD:", ", ".join(bad_files[:20]))
for loc in LOCALES:
    counts = {t: len(acc[loc][t]) for t in TYPES if acc[loc][t]}
    if counts:
        print(f"  {loc}: {counts}")
