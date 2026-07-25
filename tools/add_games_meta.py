# -*- coding: utf-8 -*-
"""Přidá dávku her přes extra_games + game_meta (rok/studio) + articles (popis).
Funguje pro JAKOUKOLI platformu (nezávisle na 'plus' průvodci).
Postup: extra_games -> reparse -> namapuj slugy -> game_meta + articles -> reparse.
Použití: python tools/add_games_meta.py <batch.json>
batch = [{slug,name,genre,length,year,studio,detail,flags?}]"""
import json, sys, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
EXTRA = ROOT / "src/data/extra_games.json"
META = ROOT / "src/data/game_meta.json"
ARTDIR = ROOT / "src/data/articles"
DATASET = ROOT / "src/data/dataset.json"

batch = json.loads(Path(sys.argv[1]).read_text("utf-8"))

# 1) extra_games
extra = json.loads(EXTRA.read_text("utf-8"))
added = 0
for g in batch:
    extra.setdefault(g["slug"], [])
    have = {x["name"] for x in extra[g["slug"]]}
    if g["name"] not in have:
        extra[g["slug"]].append({"name": g["name"], "genre": g["genre"], "length": g["length"], "flags": g.get("flags", [])})
        added += 1
EXTRA.write_text(json.dumps(extra, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"extra_games: +{added}")

# 2) reparse
subprocess.run([sys.executable, str(ROOT / "tools/parse_content.py")], check=True, capture_output=True)

# 3) namapuj (slug_platformy, name) -> gameslug
d = json.loads(DATASET.read_text("utf-8"))
key2slug = {}
for p in d["platforms"]:
    for gm in p["games"]:
        key2slug[(p["slug"], gm["name"])] = gm["slug"]

meta = json.loads(META.read_text("utf-8")) if META.exists() else {}
art_file = ARTDIR / "added_games.json"
arts = json.loads(art_file.read_text("utf-8")) if art_file.exists() else {}
mm = aa = miss = 0
for g in batch:
    gs = key2slug.get((g["slug"], g["name"]))
    if not gs:
        print(f"  [!] nenamapováno: {g['slug']} / {g['name']}"); miss += 1; continue
    meta.setdefault(gs, {})
    if g.get("year"):
        meta[gs]["year"] = g["year"]; mm += 1
    if g.get("studio"):
        meta[gs]["studio"] = g["studio"]
    if g.get("detail"):
        arts[gs] = g["detail"]; aa += 1
META.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
art_file.write_text(json.dumps(arts, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"game_meta: +{mm} rok/studio | articles: +{aa} | nenamapováno: {miss}")

# 4) reparse
subprocess.run([sys.executable, str(ROOT / "tools/parse_content.py")], check=True, capture_output=True)
print("hotovo (reparsed)")
