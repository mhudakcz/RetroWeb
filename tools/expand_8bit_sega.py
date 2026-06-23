# -*- coding: utf-8 -*-
"""Rozšíření NES, GBC, Master System, Game Gear, PC Engine, Neo Geo, Saturn
o esenciální kánon. Dedup proti datasetu."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

NES = [
    ("Mega Man 2", "Action-platformer", "M"), ("Mega Man 3", "Action-platformer", "M"),
    ("Mega Man", "Action-platformer", "M"), ("Mega Man 4", "Action-platformer", "M"),
    ("Mega Man 5", "Action-platformer", "M"), ("Mega Man 6", "Action-platformer", "M"),
    ("Castlevania", "Action-platformer", "M"), ("Castlevania III: Dracula's Curse", "Action-platformer", "M"),
    ("Metroid", "Metroidvania", "M"), ("Ninja Gaiden", "Action-platformer", "M"),
    ("Ninja Gaiden II: The Dark Sword of Chaos", "Action-platformer", "M"),
    ("DuckTales", "Action-platformer", "M"), ("Kirby's Adventure", "Plošinovka", "M"),
    ("Punch-Out!!", "Sport / Box", "M"), ("Battletoads", "Beat em up", "M"),
    ("Final Fantasy", "JRPG", "XL"), ("Dragon Warrior", "JRPG", "XL"),
    ("Blaster Master", "Action-adventure", "M"), ("Crystalis", "Action-RPG", "L"),
    ("StarTropics", "Action-adventure", "L"), ("Chip 'n Dale Rescue Rangers", "Plošinovka", "M"),
    ("River City Ransom", "Beat em up / RPG", "M"), ("Faxanadu", "Action-RPG", "L"),
    ("Kid Icarus", "Action-platformer", "M"), ("Life Force", "Shmup", "M"),
    ("Adventure Island", "Plošinovka", "M"), ("Snake Rattle 'n' Roll", "Plošinovka", "M"),
    ("Shatterhand", "Action-platformer", "M"), ("Gargoyle's Quest II", "Action-platformer", "M"),
    ("Tecmo Super Bowl", "Sport", "M"),
]
GBC = [
    ("Pokémon Gold / Silver", "JRPG", "XL"), ("Pokémon Crystal", "JRPG", "XL"),
    ("Pokémon Red / Blue / Yellow", "JRPG", "XL"),
    ("The Legend of Zelda: Link's Awakening DX", "Action-adventure", "L"),
    ("The Legend of Zelda: Oracle of Seasons", "Action-adventure", "L"),
    ("The Legend of Zelda: Oracle of Ages", "Action-adventure", "L"),
    ("Wario Land 3", "Plošinovka", "L"), ("Wario Land II", "Plošinovka", "M"),
    ("Super Mario Bros. Deluxe", "Plošinovka", "M"),
    ("Donkey Kong Country", "Plošinovka", "L"), ("Dragon Warrior III", "JRPG", "XL"),
    ("Shantae", "Metroidvania", "L"), ("Tetris DX", "Puzzle", "M"),
    ("Kirby Tilt 'n' Tumble", "Akční / Puzzle", "M"), ("Pokémon Pinball", "Pinball", "M"),
    ("Dragon Warrior Monsters", "JRPG", "XL"), ("Toki Tori", "Puzzle", "M"),
    ("R-Type DX", "Shmup", "M"), ("Harvest Moon GBC", "Sim / Farma", "L"),
    ("Conker's Pocket Tales", "Action-adventure", "M"),
]
MASTER = [
    ("Wonder Boy", "Plošinovka", "M"), ("Wonder Boy III: The Dragon's Trap", "Action-platformer", "L"),
    ("Wonder Boy in Monster World", "Action-RPG", "L"),
    ("Alex Kidd in Miracle World", "Plošinovka", "M"), ("Sonic the Hedgehog", "Plošinovka", "M"),
    ("Psycho Fox", "Plošinovka", "M"), ("Castle of Illusion", "Plošinovka", "M"),
    ("Land of Illusion", "Plošinovka", "M"), ("Fantasy Zone", "Shmup", "M"),
    ("Golvellius", "Action-RPG", "L"), ("Ys: The Vanished Omens", "Action-RPG", "L"),
    ("Master of Darkness", "Action-platformer", "M"), ("Power Strike", "Shmup", "M"),
    ("Phantasy Star", "JRPG", "XL"),
]
GAMEGEAR = [
    ("Sonic the Hedgehog", "Plošinovka", "M"), ("Sonic Chaos", "Plošinovka", "M"),
    ("Sonic Triple Trouble", "Plošinovka", "M"), ("Shinobi", "Action-platformer", "M"),
    ("Shining Force Gaiden", "Tactics-RPG", "L"), ("Columns", "Puzzle", "S"),
    ("Defenders of Oasis", "JRPG", "L"), ("GG Aleste / Power Strike II", "Shmup", "M"),
    ("Tails Adventure", "Action-platformer", "M"), ("Dragon Crystal", "Roguelike RPG", "M"),
    ("Gunstar Heroes", "Run & gun", "M"), ("Ax Battler", "Action-RPG", "M"),
]
PCE = [
    ("Bonk's Adventure", "Plošinovka", "M"), ("Bonk's Revenge", "Plošinovka", "M"),
    ("Ys Book I & II", "Action-RPG", "L"), ("Lords of Thunder", "Shmup", "M"),
    ("Gate of Thunder", "Shmup", "M"), ("Soldier Blade", "Shmup", "M"),
    ("Super Star Soldier", "Shmup", "M"), ("Splatterhouse", "Beat em up", "M"),
    ("Blazing Lazers", "Shmup", "M"), ("Devil's Crush", "Pinball", "M"),
    ("Military Madness", "Strategy", "L"), ("Ninja Spirit", "Action-platformer", "M"),
    ("Dungeon Explorer", "Action-RPG", "L"), ("Neutopia", "Action-adventure", "L"),
    ("Air Zonk", "Shmup", "M"), ("Parasol Stars", "Arcade / Plošinovka", "M"),
]
NEOGEO = [
    ("The King of Fighters '94", "Fighting", "S"), ("The King of Fighters '95", "Fighting", "S"),
    ("The King of Fighters '97", "Fighting", "S"), ("The King of Fighters '98", "Fighting", "S"),
    ("Garou: Mark of the Wolves", "Fighting", "S"), ("The Last Blade", "Fighting", "S"),
    ("The Last Blade 2", "Fighting", "S"), ("Samurai Shodown II", "Fighting", "S"),
    ("Windjammers", "Sport / Arcade", "S"), ("Shock Troopers", "Run & gun", "M"),
    ("Sengoku", "Beat em up", "M"), ("Top Hunter", "Action-platformer", "M"),
    ("Aero Fighters 2", "Shmup", "S"), ("Neo Turf Masters", "Sport / Golf", "S"),
    ("Waku Waku 7", "Fighting", "S"),
]
SATURN = [
    ("Panzer Dragoon", "Rail shooter", "M"), ("Panzer Dragoon II Zwei", "Rail shooter", "M"),
    ("Panzer Dragoon Saga", "JRPG", "XL"), ("NiGHTS into Dreams", "Akční / Arkáda", "M"),
    ("Guardian Heroes", "Beat em up / RPG", "M"), ("Radiant Silvergun", "Shmup", "M"),
    ("Dragon Force", "Strategy / RPG", "XL"), ("Shining Force III", "Tactics-RPG", "XL"),
    ("Burning Rangers", "Akční / 3D", "M"), ("Virtua Fighter 2", "Fighting", "S"),
    ("Sega Rally Championship", "Racing", "M"), ("Astal", "Plošinovka", "M"),
    ("Clockwork Knight", "Plošinovka", "M"), ("Shining the Holy Ark", "Dungeon RPG", "XL"),
    ("Dragon Ball Z: Shin Butōden", "Fighting", "S"), ("Street Fighter Alpha 2", "Fighting", "S"),
]
PLATS = {"nes": NES, "game-boy-color": GBC, "master-system": MASTER, "game-gear": GAMEGEAR,
         "pc-engine": PCE, "neogeo": NEOGEO, "saturn": SATURN}

d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
present = {p["slug"]: {P.norm_name(g["name"]) for g in p["games"]} for p in d["platforms"]}
p_file = ROOT / "src/data/extra_games.json"
eg = json.loads(p_file.read_text("utf-8"))
added = {}
for slug, items in PLATS.items():
    arr = eg.setdefault(slug, [])
    exist = {P.norm_name(g["name"]) for g in arr} | present.get(slug, set())
    n = 0
    for nm, ge, ln in items:
        k = P.norm_name(nm)
        if k in exist:
            continue
        flags = ["puzzle"] if "puzzle" in ge.lower() else []
        arr.append({"name": nm, "genre": ge, "length": ln, "flags": flags})
        exist.add(k); n += 1
    added[slug] = n
p_file.write_text(json.dumps(eg, ensure_ascii=False, indent=2), encoding="utf-8")
print("Přidáno:", added, "celkem", sum(added.values()))
