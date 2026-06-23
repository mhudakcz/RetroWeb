# -*- coding: utf-8 -*-
"""Velké rozšíření knihovny: kurátorské seznamy esenciálních her pro SNES, GBA,
Mega Drive, Arcade + víc Lego her (PS1/GBA/N64). Dedup proti stávajícímu datasetu.
Přidá do extra_games.json (genre/length/flags). Players/obrázky/články řeší další kroky."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

# (name, genre, length)
SNES = [
    ("Chrono Trigger", "JRPG", "XL"), ("Secret of Mana", "Action-RPG", "L"),
    ("Seiken Densetsu 3", "Action-RPG", "L"), ("Final Fantasy VI", "JRPG", "XL"),
    ("Super Metroid", "Metroidvania", "L"), ("Super Mario World", "Plošinovka", "L"),
    ("Super Mario World 2: Yoshi's Island", "Plošinovka", "L"),
    ("Donkey Kong Country", "Plošinovka", "L"), ("Donkey Kong Country 2", "Plošinovka", "L"),
    ("Donkey Kong Country 3", "Plošinovka", "L"), ("Super Mario Kart", "Racing", "M"),
    ("F-Zero", "Racing", "M"), ("Super Mario RPG", "JRPG", "L"), ("EarthBound", "JRPG", "XL"),
    ("The Legend of Zelda: A Link to the Past", "Action-adventure", "L"),
    ("Star Fox", "Rail shooter", "M"), ("Contra III: The Alien Wars", "Run & gun", "M"),
    ("Super Castlevania IV", "Action-platformer", "M"), ("Mega Man X", "Action-platformer", "M"),
    ("Mega Man X2", "Action-platformer", "M"), ("Mega Man X3", "Action-platformer", "M"),
    ("Super Ghouls 'n Ghosts", "Action-platformer", "M"), ("Gradius III", "Shmup", "M"),
    ("Super Star Wars", "Action-platformer", "M"), ("ActRaiser", "Action / Sim", "L"),
    ("Illusion of Gaia", "Action-RPG", "L"), ("Terranigma", "Action-RPG", "XL"),
    ("Breath of Fire II", "JRPG", "XL"), ("Lufia II: Rise of the Sinistrals", "JRPG", "XL"),
    ("Kirby Super Star", "Plošinovka", "M"), ("Super Punch-Out!!", "Sport / Box", "M"),
    ("Pilotwings", "Sim", "M"), ("Tetris Attack", "Puzzle", "M"),
    ("Demon's Crest", "Action-platformer", "M"), ("Zombies Ate My Neighbors", "Run & gun", "M"),
    ("Harvest Moon", "Sim / Farma", "XL"), ("Aladdin", "Plošinovka", "M"),
    ("The Lion King", "Plošinovka", "M"), ("Pocky & Rocky", "Run & gun", "M"),
    ("U.N. Squadron", "Shmup", "M"), ("Axelay", "Shmup", "M"),
    ("Rock n' Roll Racing", "Racing", "M"), ("Kirby's Dream Course", "Sport / Puzzle", "M"),
    ("Tiny Toon Adventures: Buster Busts Loose", "Plošinovka", "M"),
    ("Joe & Mac", "Plošinovka", "M"), ("Goof Troop", "Action-adventure", "M"),
    ("Street Fighter Alpha 2", "Fighting", "S"),
]
GBA = [
    ("Metroid: Zero Mission", "Metroidvania", "M"), ("Metroid Fusion", "Metroidvania", "M"),
    ("Castlevania: Aria of Sorrow", "Metroidvania", "M"),
    ("Castlevania: Circle of the Moon", "Metroidvania", "M"),
    ("Castlevania: Harmony of Dissonance", "Metroidvania", "M"),
    ("Mario Kart: Super Circuit", "Racing", "M"),
    ("Mario & Luigi: Superstar Saga", "JRPG", "L"), ("Golden Sun", "JRPG", "XL"),
    ("Golden Sun: The Lost Age", "JRPG", "XL"), ("Advance Wars", "Tactics", "L"),
    ("Advance Wars 2: Black Hole Rising", "Tactics", "L"),
    ("Fire Emblem", "Tactics-RPG", "XL"),
    ("The Legend of Zelda: The Minish Cap", "Action-adventure", "L"),
    ("WarioWare, Inc.: Mega Microgames!", "Party / Mini-hry", "M"),
    ("Wario Land 4", "Plošinovka", "M"), ("Kirby & the Amazing Mirror", "Metroidvania", "M"),
    ("Kirby: Nightmare in Dream Land", "Plošinovka", "M"), ("Mega Man Zero", "Action-platformer", "M"),
    ("Mega Man Zero 2", "Action-platformer", "M"), ("Mega Man Battle Network 3", "Action-RPG", "L"),
    ("Final Fantasy VI Advance", "JRPG", "XL"), ("Final Fantasy I & II: Dawn of Souls", "JRPG", "L"),
    ("Sonic Advance", "Plošinovka", "M"), ("Sonic Advance 2", "Plošinovka", "M"),
    ("Astro Boy: Omega Factor", "Action / Beat", "M"), ("Drill Dozer", "Plošinovka", "M"),
    ("Boktai: The Sun Is in Your Hand", "Action-adventure", "L"),
    ("Gunstar Super Heroes", "Run & gun", "M"), ("Sword of Mana", "Action-RPG", "L"),
    ("Mother 3", "JRPG", "XL"), ("Rhythm Tengoku", "Rhythm", "M"),
    ("Mario vs. Donkey Kong", "Puzzle / Plošinovka", "M"),
    ("Lego Star Wars: The Video Game", "Action / rodinné", "M"),
    ("Lego Star Wars II: The Original Trilogy", "Action / rodinné", "M"),
    ("Bionicle: The Game", "Action", "M"), ("Drome Racers", "Racing", "M"),
    ("Lego Racers 2", "Racing / rodinné", "M"),
    ("Tony Hawk's Pro Skater 2", "Sport / Skate", "M"), ("Klonoa: Empire of Dreams", "Plošinovka", "M"),
    ("Ninja Five-O", "Action-platformer", "M"), ("Car Battler Joe", "Action-RPG", "L"),
    ("Banjo-Kazooie: Grunty's Revenge", "Plošinovka", "M"),
]
MEGADRIVE = [
    ("Sonic the Hedgehog 2", "Plošinovka", "M"), ("Sonic the Hedgehog 3", "Plošinovka", "M"),
    ("Sonic & Knuckles", "Plošinovka", "M"), ("Streets of Rage", "Beat em up", "M"),
    ("Streets of Rage 2", "Beat em up", "M"), ("Streets of Rage 3", "Beat em up", "M"),
    ("Gunstar Heroes", "Run & gun", "M"), ("Castlevania: Bloodlines", "Action-platformer", "M"),
    ("Contra: Hard Corps", "Run & gun", "M"), ("Ristar", "Plošinovka", "M"),
    ("Dynamite Headdy", "Plošinovka", "M"), ("Rocket Knight Adventures", "Action-platformer", "M"),
    ("Vectorman", "Run & gun", "M"), ("Vectorman 2", "Run & gun", "M"),
    ("Earthworm Jim", "Plošinovka", "M"), ("Earthworm Jim 2", "Plošinovka", "M"),
    ("ToeJam & Earl", "Akční / Roguelike", "M"),
    ("ToeJam & Earl in Panic on Funkotron", "Plošinovka", "M"),
    ("Thunder Force III", "Shmup", "M"), ("Thunder Force IV", "Shmup", "M"),
    ("Alien Soldier", "Run & gun", "M"), ("Landstalker", "Action-RPG", "L"),
    ("Light Crusader", "Action-adventure", "L"), ("Ecco the Dolphin", "Action-adventure", "L"),
    ("Castle of Illusion Starring Mickey Mouse", "Plošinovka", "M"),
    ("QuackShot Starring Donald Duck", "Plošinovka", "M"),
    ("World of Illusion", "Plošinovka", "M"), ("Kid Chameleon", "Plošinovka", "M"),
    ("Strider", "Action-platformer", "M"), ("Golden Axe II", "Beat em up", "M"),
    ("Altered Beast", "Beat em up", "S"), ("Mega Turrican", "Run & gun", "M"),
    ("Pulseman", "Plošinovka", "M"), ("Ecco: The Tides of Time", "Action-adventure", "L"),
    ("Herzog Zwei", "Strategy", "M"), ("Sub-Terrania", "Akční / Sim", "M"),
    ("Gaiares", "Shmup", "M"), ("Rolo to the Rescue", "Plošinovka", "M"),
    ("The Adventures of Batman & Robin", "Run & gun", "M"), ("Story of Thor", "Action-RPG", "L"),
    ("Wiz 'n' Liz", "Plošinovka", "M"), ("Shining in the Darkness", "Dungeon RPG", "L"),
    ("Aladdin", "Plošinovka", "M"),
]
ARCADE = [
    ("Pac-Man", "Arcade / Maze", "S"), ("Ms. Pac-Man", "Arcade / Maze", "S"),
    ("Galaga", "Shmup", "S"), ("Galaxian", "Shmup", "S"), ("Donkey Kong", "Arcade / Plošinovka", "S"),
    ("Donkey Kong Jr.", "Arcade / Plošinovka", "S"), ("Dig Dug", "Arcade / Maze", "S"),
    ("Frogger", "Arcade / Akce", "S"), ("Defender", "Shmup", "S"), ("Robotron: 2084", "Run & gun", "S"),
    ("Joust", "Arcade / Akce", "S"), ("Q*bert", "Arcade / Puzzle", "S"), ("Centipede", "Shmup", "S"),
    ("Asteroids", "Shmup", "S"), ("Tempest", "Shmup", "S"), ("Bomb Jack", "Arcade / Plošinovka", "S"),
    ("1942", "Shmup", "S"), ("1943: The Battle of Midway", "Shmup", "S"), ("Gradius", "Shmup", "M"),
    ("Salamander", "Shmup", "M"), ("Space Harrier", "Rail shooter", "M"),
    ("After Burner II", "Rail shooter", "M"), ("Pang", "Arcade / Akce", "S"),
    ("Rastan", "Action-platformer", "M"), ("Gauntlet", "Akční / Dungeon", "M"),
    ("Smash TV", "Run & gun", "M"), ("Rampage", "Arcade / Akce", "M"),
    ("Sunset Riders", "Run & gun", "M"), ("The Simpsons", "Beat em up", "M"),
    ("X-Men", "Beat em up", "M"), ("Teenage Mutant Ninja Turtles", "Beat em up", "M"),
    ("Captain Commando", "Beat em up", "M"), ("The King of Dragons", "Beat em up", "M"),
    ("Knights of the Round", "Beat em up", "M"), ("Cadillacs and Dinosaurs", "Beat em up", "M"),
    ("Aliens", "Run & gun", "M"), ("Dungeons & Dragons: Tower of Doom", "Beat em up", "L"),
    ("Daytona USA", "Racing", "M"), ("Virtua Fighter", "Fighting", "S"),
    ("Crazy Taxi", "Racing", "M"), ("Out Run", "Racing", "M"), ("Sega Rally Championship", "Racing", "M"),
    ("Time Crisis", "Light-gun shooter", "M"), ("Point Blank", "Light-gun shooter", "S"),
    ("Puzzle Bobble", "Puzzle", "S"),
]
# víc Lego napříč platformami
LEGO = {
    "playstation": [("Lego Racers 2", "Racing / rodinné", "M"), ("Lego Stunt Rally", "Racing / rodinné", "M"),
                    ("Lego Rock Raiders", "Strategy / rodinné", "M")],
    "n64": [("Lego Racers", "Racing / rodinné", "M")],
}

PLATS = {"snes": SNES, "game-boy-advance": GBA, "mega-drive": MEGADRIVE, "arcade": ARCADE}

d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
present = {p["slug"]: {P.norm_name(g["name"]) for g in p["games"]} for p in d["platforms"]}
p_file = ROOT / "src/data/extra_games.json"
eg = json.loads(p_file.read_text("utf-8"))

added = {}
def add(slug, items):
    arr = eg.setdefault(slug, [])
    exist = {P.norm_name(g["name"]) for g in arr} | present.get(slug, set())
    n = 0
    for nm, ge, ln in items:
        k = P.norm_name(nm)
        if k in exist:
            continue
        flags = ["puzzle"] if ("puzzle" in ge.lower() or "maze" in ge.lower()) else []
        arr.append({"name": nm, "genre": ge, "length": ln, "flags": flags})
        exist.add(k); n += 1
    added[slug] = n

for slug, items in PLATS.items():
    add(slug, items)
for slug, items in LEGO.items():
    add(slug, items)

p_file.write_text(json.dumps(eg, ensure_ascii=False, indent=2), encoding="utf-8")
print("Přidáno:")
for s, n in added.items():
    print(f"  {s}: +{n}")
print("celkem:", sum(added.values()))
