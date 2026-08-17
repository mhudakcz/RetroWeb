# -*- coding: utf-8 -*-
"""Rozseká src_*.json na menší dávky (chunky) pro překladové agenty.
Vytvoří chunks/<type>_<idx>.json a vypíše plán (list {in,out,type}) jako JSON.

Použití: python tools/i18n_chunk.py <workdir> [--games N]

--games N: kolik her na dávku (výchozí 12). Agent překládá do EN+DE+FR najednou,
takže výstup je zhruba 3× objem vstupu — u dlouhých článků (~1900 znaků) naráží
12 her na strop výstupních tokenů, pak zvol 6–8."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = Path(sys.argv[1])
CH = BASE / "chunks"
CH.mkdir(parents=True, exist_ok=True)

# velikost dávky podle typu (menší pro objemné články)
SIZES = {"games": 12, "platforms": 2, "studios": 3, "hardware_sections": 1}
if "--games" in sys.argv:
    SIZES["games"] = int(sys.argv[sys.argv.index("--games") + 1])
plan = []

for typ, size in SIZES.items():
    src = json.loads((BASE / f"src_{typ}.json").read_text("utf-8"))
    items = list(src.items())
    for i in range(0, len(items), size):
        chunk = dict(items[i:i + size])
        idx = i // size
        inp = CH / f"{typ}_{idx:03d}.json"
        inp.write_text(json.dumps(chunk, ensure_ascii=False), encoding="utf-8")
        plan.append({"type": typ, "in": str(inp).replace("\\", "/"),
                     "out": str(CH / f"{typ}_{idx:03d}_out.json").replace("\\", "/")})

(BASE / "plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
print(f"chunků celkem: {len(plan)}")
from collections import Counter
for k, v in Counter(p["type"] for p in plan).items():
    print(f"  {k}: {v}")
print(f"plan: {BASE / 'plan.json'}")
