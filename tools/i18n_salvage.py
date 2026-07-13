# -*- coding: utf-8 -*-
"""Posbírá hotové překladové dávky (*_out.json) z JAKÉKOLI session (i staré,
po vypnutí PC) do stabilní repo složky .i18n-work/chunks/. Robustní vůči změně
session-id: prohledá všechny scratchpady projektu."""
import glob, os, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / ".i18n-work" / "chunks"
DEST.mkdir(parents=True, exist_ok=True)

# možná umístění session scratchpadů (Temp\claude\<projekt>\<session>\scratchpad\i18n\chunks)
patterns = []
la = os.environ.get("LOCALAPPDATA")
for base in filter(None, [la, r"C:\Users\MICHAL~1\AppData\Local", os.path.expanduser("~/AppData/Local")]):
    patterns.append(os.path.join(base, "Temp", "claude", "*", "*", "scratchpad", "i18n", "chunks", "*_out.json"))

copied = 0
seen = set()
for pat in patterns:
    for f in glob.glob(pat):
        name = os.path.basename(f)
        if name in seen:
            continue
        dst = DEST / name
        # zkopíruj, pokud chybí nebo je zdroj novější a platný
        if not dst.exists() or os.path.getmtime(f) > os.path.getmtime(dst):
            try:
                shutil.copy2(f, dst)
                copied += 1
                seen.add(name)
            except Exception as e:  # noqa
                print(f"  [x] {name}: {e}")

print(f"salvage: zkopírováno/aktualizováno {copied} dávek")
print(f"celkem hotových v .i18n-work: {len(glob.glob(str(DEST / '*_out.json')))}")
