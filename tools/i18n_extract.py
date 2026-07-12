# -*- coding: utf-8 -*-
"""Vytáhne veškerý překladatelný CS obsah do scratchpad/i18n/src_*.json
pro strojový překlad (workflow). Zdroje: dataset.json (hry, historie platforem),
studio_articles/*.md, hardware_sections.json."""
import json, sys, glob, os
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scratchpad_i18n"
OUT.mkdir(parents=True, exist_ok=True)

d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))

# --- hry: teaser / detail / article ---
games = {}
for p in d["platforms"]:
    for g in p["games"]:
        fields = {}
        for f in ("teaser", "detail", "article"):
            if g.get(f):
                fields[f] = g[f]
        if fields:
            games[g["slug"]] = fields
(OUT / "src_games.json").write_text(json.dumps(games, ensure_ascii=False, indent=1), encoding="utf-8")

# --- platformy: history ---
plats = {p["slug"]: {"history": p["history"]} for p in d["platforms"] if p.get("history")}
(OUT / "src_platforms.json").write_text(json.dumps(plats, ensure_ascii=False, indent=1), encoding="utf-8")

# --- studia: markdown ---
studios = {}
for f in glob.glob(str(ROOT / "src/data/studio_articles/*.md")):
    slug = os.path.basename(f)[:-3]
    studios[slug] = Path(f).read_text("utf-8")
(OUT / "src_studios.json").write_text(json.dumps(studios, ensure_ascii=False, indent=1), encoding="utf-8")

# --- hardware sekce (deep) ---
hs_file = ROOT / "src/data/hardware_sections.json"
hs = json.loads(hs_file.read_text("utf-8")) if hs_file.exists() else {}
(OUT / "src_hardware_sections.json").write_text(json.dumps(hs, ensure_ascii=False, indent=1), encoding="utf-8")

def cc(obj):
    return len(json.dumps(obj, ensure_ascii=False))

print(f"OUT: {OUT}")
print(f"  games:     {len(games):>5} her     ({cc(games):>9,} znaků)")
print(f"  platforms: {len(plats):>5}         ({cc(plats):>9,} znaků)")
print(f"  studios:   {len(studios):>5}         ({cc(studios):>9,} znaků)")
print(f"  hardware:  {len(hs):>5}         ({cc(hs):>9,} znaků)")
