# -*- coding: utf-8 -*-
"""Rozšíření N64 + Dreamcast + PSP o esenciální kánon. Dedup proti datasetu."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

N64 = [
    ("Banjo-Kazooie", "Plošinovka 3D", "L"), ("Banjo-Tooie", "Plošinovka 3D", "L"),
    ("Conker's Bad Fur Day", "Plošinovka 3D", "L"), ("Paper Mario", "JRPG", "L"),
    ("Mario Party", "Party", "M"), ("Mario Party 2", "Party", "M"), ("Mario Party 3", "Party", "M"),
    ("Star Fox 64", "Rail shooter", "M"), ("F-Zero X", "Racing", "M"),
    ("Wave Race 64", "Racing", "M"), ("1080° Snowboarding", "Sport", "M"),
    ("Sin & Punishment", "Rail shooter", "M"), ("Mischief Makers", "Action-platformer", "M"),
    ("Body Harvest", "Action-adventure", "L"), ("Ogre Battle 64", "Tactics-RPG", "XL"),
    ("Mystical Ninja Starring Goemon", "Action-adventure", "L"), ("Pilotwings 64", "Sim", "M"),
    ("Kirby 64: The Crystal Shards", "Plošinovka", "M"), ("Yoshi's Story", "Plošinovka", "M"),
    ("Excitebike 64", "Racing / motorky", "M"), ("Blast Corps", "Akční / Puzzle", "M"),
    ("Doom 64", "FPS", "M"), ("Turok 2: Seeds of Evil", "FPS", "L"),
    ("Space Station Silicon Valley", "Action-adventure", "M"),
    ("Beetle Adventure Racing", "Racing", "M"), ("Snowboard Kids", "Racing / Sport", "M"),
    ("Rocket: Robot on Wheels", "Plošinovka 3D", "M"), ("Glover", "Plošinovka 3D", "M"),
]
DREAMCAST = [
    ("Shenmue", "Action-adventure", "XL"), ("Shenmue II", "Action-adventure", "XL"),
    ("Jet Set Radio", "Action / Sport", "M"), ("Crazy Taxi", "Racing", "M"),
    ("Power Stone", "Fighting", "S"), ("Power Stone 2", "Fighting", "S"),
    ("Skies of Arcadia", "JRPG", "XL"), ("Soul Calibur", "Fighting", "S"),
    ("Sonic Adventure", "Plošinovka 3D", "L"), ("Sonic Adventure 2", "Plošinovka 3D", "L"),
    ("Marvel vs. Capcom 2", "Fighting", "S"), ("Ikaruga", "Shmup", "M"), ("Rez", "Rail shooter", "M"),
    ("Phantasy Star Online", "Action-RPG / online", "XL"), ("Grandia II", "JRPG", "XL"),
    ("ChuChu Rocket!", "Puzzle", "M"), ("Samba de Amigo", "Rhythm", "M"),
    ("Space Channel 5", "Rhythm", "M"), ("Virtua Tennis", "Sport", "M"),
    ("The House of the Dead 2", "Light-gun shooter", "M"),
    ("Resident Evil – Code: Veronica", "Survival horror", "L"), ("Bangai-O", "Shmup", "M"),
    ("Dead or Alive 2", "Fighting", "S"), ("Daytona USA 2001", "Racing", "M"),
    ("Quake III Arena", "FPS", "M"), ("Ecco the Dolphin: Defender of the Future", "Action-adventure", "L"),
    ("Toy Commander", "Akční / Sim", "M"), ("Cannon Spike", "Run & gun", "S"),
]
PSP = [
    ("God of War: Chains of Olympus", "Akční / Hack and slash", "M"),
    ("Grand Theft Auto: Liberty City Stories", "Action-adventure", "XL"),
    ("Grand Theft Auto: Vice City Stories", "Action-adventure", "XL"),
    ("Monster Hunter Freedom Unite", "Action-RPG", "XL"),
    ("Crisis Core: Final Fantasy VII", "Action-RPG", "L"),
    ("Persona 3 Portable", "JRPG", "XL"), ("Daxter", "Plošinovka", "M"),
    ("Patapon", "Rhythm / Strategy", "M"), ("Patapon 2", "Rhythm / Strategy", "M"),
    ("LocoRoco", "Plošinovka / Puzzle", "M"), ("Lumines", "Puzzle", "M"),
    ("Wipeout Pure", "Racing", "M"), ("Metal Gear Solid: Peace Walker", "Akční / Stealth", "XL"),
    ("Ridge Racer", "Racing", "M"), ("Tactics Ogre: Let Us Cling Together", "Tactics-RPG", "XL"),
    ("Jeanne d'Arc", "Tactics-RPG", "L"), ("Ys Seven", "Action-RPG", "L"),
    ("Gran Turismo", "Racing", "L"), ("Burnout Legends", "Racing", "M"),
    ("Killzone: Liberation", "Akční / Taktická", "M"), ("Resistance: Retribution", "Shooter", "L"),
    ("Castlevania: The Dracula X Chronicles", "Action-platformer", "L"),
    ("Dissidia Final Fantasy", "Fighting / RPG", "L"), ("Half-Minute Hero", "Akční / RPG", "M"),
    ("Valkyria Chronicles II", "Tactics-RPG", "XL"),
    ("Metal Gear Solid: Portable Ops", "Akční / Stealth", "L"),
    ("Syphon Filter: Dark Mirror", "Akční / Stealth", "L"), ("Lumines II", "Puzzle", "M"),
]
PLATS = {"n64": N64, "dreamcast": DREAMCAST, "psp": PSP}

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
