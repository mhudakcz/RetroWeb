# -*- coding: utf-8 -*-
"""Sestaví game_players.json (slug -> text počtu hráčů) pro nové hry + kurátorskou
sadu slavných multiplayer titulů. Páruje vzory (platforma|*, podřetězec názvu)."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))

# (platforma nebo '*', podřetězec v názvu malými, hodnota). Pozdější vyhrává.
RULES = [
    # obecné žánrové vzory
    ("*", "street fighter", "1–2 · versus"),
    ("*", "mortal kombat", "1–2 · versus"),
    ("*", "fatal fury", "1–2 · versus"),
    ("*", "art of fighting", "1–2 · versus"),
    ("*", "samurai shodown", "1–2 · versus"),
    ("*", "world heroes", "1–2 · versus"),
    ("*", "darkstalkers", "1–2 · versus"),
    ("*", "vampire savior", "1–2 · versus"),
    ("*", "marvel super heroes", "1–2 · versus"),
    ("*", "killer instinct", "1–2 · versus"),
    ("*", "virtua fighter", "1–2 · versus"),
    ("*", "power stone", "1–4 · versus"),
    ("*", "marvel vs", "1–2 · versus"),
    ("*", "soul calibur", "1–2 · versus"),
    ("*", "soulcalibur", "1–2 · versus"),
    ("*", "dead or alive", "1–2 · versus"),
    ("*", "dissidia", "1–2 · versus"),
    ("*", "king of fighters", "1–2 · versus"),
    ("*", "garou", "1–2 · versus"),
    ("*", "last blade", "1–2 · versus"),
    ("*", "windjammers", "1–2 · versus"),
    ("*", "virtua tennis", "1–4 · sport"),
    ("*", "samba de amigo", "1–2 · party"),
    ("*", "chuchu rocket", "1–4 · party"),
    ("*", "crazy taxi", "1"),
    ("*", "tekken", "1–2 · versus"),
    ("*", "toshinden", "1–2 · versus"),
    ("*", "soul edge", "1–2 · versus"),
    ("*", "tobal", "1–2 · versus"),
    ("*", "bomberman", "1–4 · party"),
    ("*", "double dragon", "1–2 · co-op"),
    ("*", "streets of rage", "1–2 · co-op"),
    ("*", "golden axe", "1–2 · co-op"),
    ("*", "final fight", "1–2 · co-op"),
    ("*", "turtles", "1–4 · co-op"),
    ("*", "ninja turtles", "1–4 · co-op"),
    ("*", "battletoads", "1–2 · co-op"),
    ("*", "contra", "1–2 · co-op"),
    ("*", "probotector", "1–2 · co-op"),
    ("*", "super c", "1–2 · co-op"),
    ("*", "bubble bobble", "1–2 · co-op"),
    ("*", "snow bros", "1–2 · co-op"),
    ("*", "rainbow islands", "1–2 · co-op"),
    ("*", "gauntlet", "1–4 · co-op"),
    ("*", "metal slug", "1–2 · co-op"),
    ("*", "micro machines", "1–2"),
    ("*", "nba jam", "1–4 · arkáda"),
    ("*", "wild guns", "1–2 · co-op"),
    ("*", "sensible soccer", "1–2"),
    ("*", "kick off", "1–2"),
    ("*", "international superstar soccer", "1–2"),
    ("*", "nhl", "1–2"),
    # platformově specifické
    ("amiga", "worms", "2–4 · hot-seat"),
    ("snes", "super mario kart", "1–2 · split-screen"),
    ("snes", "top gear", "1–2 · split-screen"),
    ("snes", "nba jam", "1–2"),
    ("n64", "mario kart", "1–4 · split-screen"),
    ("n64", "diddy kong racing", "1–4 · split-screen"),
    ("n64", "goldeneye", "1–4 · split-screen"),
    ("n64", "perfect dark", "1–4 · split-screen"),
    ("n64", "mario party", "1–4 · party"),
    ("n64", "smash", "1–4 · party"),
    ("n64", "mario tennis", "1–4"),
    ("n64", "bomberman", "1–4 · party"),
    ("saturn", "bomberman", "1–10 · party"),
    ("playstation", "porsche challenge", "1–2 · split-screen"),
    ("playstation", "lego racers", "1–2 · split-screen"),
    ("playstation", "micro machines", "1–8 · pass-pad"),
    ("playstation", "bushido blade", "1–2 · versus"),
    ("mega-drive", "nba jam", "1–4 · arkáda"),
    ("mega-drive", "micro machines", "1–4 · pass-pad"),
    ("mega-drive", "comix zone", "1"),
    ("nds", "mario kart", "1–8 · Wi-Fi / download play"),
    ("nds", "new super mario bros", "1–4 · download play"),
    ("nds", "tetris", "1–10 · Wi-Fi / download play"),
    ("nds", "mario party", "1–4 · download play"),
    ("nds", "metroid prime hunters", "1–4 · Wi-Fi"),
    ("nds", "bomberman", "1–8 · download play"),
]

out = {}
for p in d["platforms"]:
    for g in p["games"]:
        nm = g["name"].lower()
        for plat, sub, val in RULES:
            if (plat == "*" or plat == p["slug"]) and sub in nm:
                out[g["slug"]] = val  # pozdější pravidlo přepíše

(ROOT / "src/data/game_players.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
print(f"game_players.json: {len(out)} her")
for s in sorted(out)[:15]:
    print(" ", s, "->", out[s])
