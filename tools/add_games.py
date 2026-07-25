# -*- coding: utf-8 -*-
"""Přidá dávku her: do extra_games.json (name/genre/length/flags) a do
retro-hry-pruvodce-plus.md (řádek s rokem/studiem/popisem pod danou sekci).
Spouštěj: python tools/add_games.py <batch_module.json>  (nebo uprav BATCH níže)."""
import json, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
EXTRA = ROOT / "src/data/extra_games.json"
PLUS = ROOT / "Podklady/extracted/retro-hry-pruvodce-plus.md"

# nadpis sekce v plus průvodci pro každý slug platformy
HEADING = {
    "nes": "Nintendo NES / Famicom",
    "snes": "Super Nintendo / Super Famicom (SNES)",
    "game-boy": "Nintendo Game Boy (GB)",
    "game-boy-color": "Nintendo Game Boy Color (GBC)",
    "mega-drive": "SEGA Mega Drive / Genesis",
    "playstation": "Sony PlayStation (PS1)",
    "n64": "Nintendo 64",
    "master-system": "SEGA Master System",
    "saturn": "SEGA Saturn",
    "neogeo": "SNK Neo Geo",
    "cps": "Arcade (MAME / FBNeo)",
    "arcade": "Arcade (MAME / FBNeo)",
    "c64": "Commodore 64 (C64)",
    "amiga": "Commodore Amiga",
    "msx": "MSX / MSX2",
}

# každá hra: (slug_platformy, name, genre, length, year, studio, est, detail)
BATCH = json.loads((Path(sys.argv[1])).read_text("utf-8")) if len(sys.argv) > 1 else []

extra = json.loads(EXTRA.read_text("utf-8"))
plus = PLUS.read_text("utf-8")
added_extra = 0
added_plus = 0

# seskup podle platformy
from collections import defaultdict
by_plat = defaultdict(list)
for g in BATCH:
    by_plat[g["slug"]].append(g)

for slug, games in by_plat.items():
    extra.setdefault(slug, [])
    have = {x["name"] for x in extra[slug]}
    lines = []
    for g in games:
        if g["name"] not in have:
            extra[slug].append({"name": g["name"], "genre": g["genre"], "length": g["length"], "flags": g.get("flags", [])})
            added_extra += 1
        est = g.get("est", "")
        estpart = f" *(⏱ {est})*" if est else ""
        lines.append(f'**{g["name"]}** — *{g["genre"]} · {g["year"]} · {g["studio"]}* — {g["detail"]}{estpart}\n')
    # vlož řádky za nadpis sekce (za "## Heading\n\n" nebo za úvodní odstavec sekce)
    head = "## " + HEADING[slug]
    idx = plus.find(head)
    if idx < 0:
        print(f"  [!] sekce nenalezena: {head}")
        continue
    # najdi konec řádku nadpisu, vlož za následující prázdný řádek
    nl = plus.find("\n", idx)
    block = "\n" + "\n".join(lines) + "\n"
    plus = plus[:nl + 1] + block + plus[nl + 1:]
    added_plus += len(lines)

EXTRA.write_text(json.dumps(extra, ensure_ascii=False, indent=1), encoding="utf-8")
PLUS.write_text(plus, encoding="utf-8")
print(f"přidáno do extra_games: {added_extra} | plus řádků: {added_plus}")
