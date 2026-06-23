# -*- coding: utf-8 -*-
"""Doplnění žánrových děr per platforma (skutečně existující slavné tituly).
Dedup proti datasetu."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

ADD = {
    "game-boy": [
        ("Final Fantasy Adventure", "Action-RPG", "L"), ("The Final Fantasy Legend", "JRPG", "L"),
        ("Final Fantasy Legend II", "JRPG", "L"), ("Sword of Hope II", "RPG", "M"),
        ("Pokémon Red / Blue", "JRPG", "XL"), ("Street Fighter II", "Fighting", "S"),
        ("Wave Race", "Racing", "S"), ("Nintendo World Cup", "Sport / Fotbal", "M"),
    ],
    "game-boy-advance": [
        ("Street Fighter Alpha 3 Upper", "Fighting", "S"), ("Tekken Advance", "Fighting", "S"),
        ("Gradius Galaxies", "Shmup", "M"), ("Iridion II", "Shmup", "M"),
        ("Mario Tennis: Power Tour", "Sport / Tenis", "M"),
    ],
    "game-boy-color": [
        ("Survival Kids", "Survival / Adventura", "M"), ("Top Gear Pocket", "Racing", "M"),
        ("Street Fighter Alpha", "Fighting", "S"),
    ],
    "nes": [
        ("Yie Ar Kung-Fu", "Fighting", "S"), ("Karate Champ", "Fighting", "S"),
        ("Nobunaga's Ambition", "Strategy / Sim", "XL"),
        ("Romance of the Three Kingdoms", "Strategy / Sim", "XL"), ("Rampart", "Strategy / Akce", "M"),
    ],
    "arcade": [
        ("NBA Jam", "Sport / Basketbal", "S"), ("Punch-Out!!", "Sport / Box", "M"),
        ("Tehkan World Cup", "Sport / Fotbal", "S"), ("Hat Trick", "Sport / Hokej", "S"),
    ],
    "amiga": [
        ("Eye of the Beholder", "Dungeon RPG", "XL"), ("Ishar: Legend of the Fortress", "RPG", "L"),
        ("Body Blows", "Fighting", "S"),
    ],
    "psp": [
        ("Virtua Tennis: World Tour", "Sport / Tenis", "M"),
        ("Pro Evolution Soccer 2011", "Sport / Fotbal", "M"), ("FIFA Street 2", "Sport / Fotbal", "M"),
    ],
    "n64": [
        ("Killer Instinct Gold", "Fighting", "S"), ("Mortal Kombat Trilogy", "Fighting", "S"),
    ],
    "c64": [
        ("The Bard's Tale", "Dungeon RPG", "XL"), ("Ultima IV: Quest of the Avatar", "RPG", "XL"),
        ("Summer Games", "Sport", "M"), ("International Soccer", "Sport / Fotbal", "S"),
    ],
    "saturn": [
        ("Sega Worldwide Soccer", "Sport / Fotbal", "M"), ("Baku Baku Animal", "Puzzle", "S"),
        ("Mr. Bones", "Akční / Adventura", "L"), ("Enemy Zero", "Survival horror / Adventura", "L"),
    ],
    "dreamcast": [
        ("Mr. Driller", "Puzzle", "M"), ("Super Puzzle Fighter II X", "Puzzle", "S"),
    ],
    "nds": [
        ("Jump Ultimate Stars", "Fighting", "M"), ("Need for Speed: Most Wanted", "Racing", "M"),
        ("Mario & Sonic at the Olympic Games", "Sport", "M"),
    ],
    "pc-engine": [
        ("Fatal Fury 2", "Fighting", "S"), ("Street Fighter II: Champion Edition", "Fighting", "S"),
        ("Final Lap Twin", "Racing / RPG", "M"),
    ],
    "master-system": [
        ("California Games", "Sport", "M"), ("Super Monaco GP", "Racing", "M"),
        ("Hang-On", "Racing / motorky", "S"),
    ],
    "game-gear": [
        ("World Series Baseball", "Sport / Baseball", "S"), ("Mortal Kombat", "Fighting", "S"),
    ],
    "3ds": [
        ("Super Street Fighter IV: 3D Edition", "Fighting", "S"),
        ("Tekken 3D: Prime Edition", "Fighting", "S"), ("Mario Sports Superstars", "Sport", "M"),
    ],
    "msx": [
        ("Konami's Soccer", "Sport / Fotbal", "S"), ("Aleste 2", "Shmup", "M"),
    ],
    "atari-2600": [
        ("RealSports Baseball", "Sport / Baseball", "S"), ("Boxing", "Sport / Box", "S"),
        ("Enduro", "Racing", "S"), ("Grand Prix", "Racing", "S"),
    ],
    "zx-spectrum": [
        ("Daley Thompson's Decathlon", "Sport / Atletika", "M"),
        ("Way of the Exploding Fist", "Fighting", "M"),
    ],
    "amstrad-cpc": [
        ("Barbarian: The Ultimate Warrior", "Fighting", "M"),
        ("Daley Thompson's Decathlon", "Sport / Atletika", "M"),
    ],
    "atari-st": [
        ("Kick Off 2", "Sport / Fotbal", "M"), ("International Karate +", "Sport / Bojové", "M"),
    ],
}

d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
present = {p["slug"]: {P.norm_name(g["name"]) for g in p["games"]} for p in d["platforms"]}
p_file = ROOT / "src/data/extra_games.json"
eg = json.loads(p_file.read_text("utf-8"))
added = {}
for slug, items in ADD.items():
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
print("Přidáno:", {k: v for k, v in added.items() if v}, "celkem", sum(added.values()))
