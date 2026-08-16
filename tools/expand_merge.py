# -*- coding: utf-8 -*-
"""Sloučí rozšířené články (chunks/exp_NNN_out.json = {slug: markdown}) do
src/data/articles/<name>.json. Vadné dávky přeskočí a nahlásí.

Použití:  python tools/expand_merge.py <workdir> [nazev-souboru] [--min 1500]

Soubor se ukládá do src/data/articles/, kde ho parse_content.py načte. Články se
načítají v abecedním pořadí souborů a pozdější přepisuje dřívější — proto výchozí
název začíná na "zz-", aby rozšířená verze měla přednost před původní.
"""
import json, sys, glob, os
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

args = sys.argv[1:]
if not args:
    print(__doc__)
    sys.exit(1)
BASE = Path(args[0])
NAME = args[1] if len(args) > 1 and not args[1].startswith("--") else "zz-expanded"
MIN = int(args[args.index("--min") + 1]) if "--min" in args else 1500

acc, bad, short = {}, [], []
for f in sorted(glob.glob(str(BASE / "chunks" / "*_out.json"))):
    name = os.path.basename(f)
    try:
        d = json.loads(Path(f).read_text("utf-8"))
        if not isinstance(d, dict):
            raise ValueError("není objekt")
    except Exception as e:
        bad.append(f"{name} ({e})")
        continue
    for slug, md in d.items():
        if not isinstance(md, str) or not md.strip():
            continue
        if len(md) < MIN:
            short.append((slug, len(md)))
            continue
        acc[slug] = md.strip()

dst = ROOT / "src" / "data" / "articles" / f"{NAME}.json"
existing = {}
if dst.exists():
    try:
        existing = json.loads(dst.read_text("utf-8"))
    except Exception:
        existing = {}
existing.update(acc)
dst.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")

L = sorted(len(v) for v in acc.values())
print(f"sloučeno článků: {len(acc)}  -> {dst.relative_to(ROOT)}  (celkem v souboru {len(existing)})")
if L:
    print(f"  délky: min {L[0]}, medián {L[len(L)//2]}, max {L[-1]}")
if short:
    print(f"  příliš krátké (pod {MIN}, přeskočeno): {len(short)}")
    for s, n in short[:10]:
        print(f"    {s} = {n}")
if bad:
    print(f"  VADNÉ dávky: {len(bad)}")
    for b in bad[:10]:
        print(f"    {b}")
