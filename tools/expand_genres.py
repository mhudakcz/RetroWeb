# -*- coding: utf-8 -*-
"""Doplnění tenkých žánrů: NES závody, metroidvanie, sport (napříč platformami).
Dedup proti datasetu."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

ADD = {
    "nes": [
        ("R.C. Pro-Am", "Racing", "S"), ("Rad Racer", "Racing", "S"),
        ("Mach Rider", "Racing", "S"), ("Micro Machines", "Racing", "S"),
        ("Cobra Triangle", "Racing / Akce", "S"), ("Bump 'n' Jump", "Racing", "S"),
        ("Days of Thunder", "Racing", "S"),
        ("Ice Hockey", "Sport / Hokej", "S"), ("Blades of Steel", "Sport / Hokej", "S"),
        ("Track & Field", "Sport / Atletika", "S"), ("Tecmo Bowl", "Sport / Fotbal", "M"),
        ("Castlevania II: Simon's Quest", "Metroidvania", "M"),
        ("Blaster Master", "Metroidvania", "M"),
    ],
    "snes": [
        ("Super Tennis", "Sport / Tenis", "M"),
        ("International Superstar Soccer Deluxe", "Sport / Fotbal", "M"),
        ("NHL '96", "Sport / Hokej", "M"), ("Super Soccer", "Sport / Fotbal", "M"),
        ("Top Gear", "Racing", "M"),
    ],
    "mega-drive": [
        ("Mutant League Football", "Sport / Fotbal", "M"),
        ("NHL '94", "Sport / Hokej", "M"),
        ("Virtua Racing", "Racing", "M"), ("Road Rash 3", "Racing / motorky", "M"),
    ],
    "game-boy": [
        ("Metroid II: Return of Samus", "Metroidvania", "L"),
        ("Castlevania: The Adventure", "Action-platformer", "M"),
        ("F-1 Race", "Racing", "S"),
    ],
    "master-system": [
        ("Wonder Boy in Monster Land", "Action-RPG / Metroidvania", "L"),
        ("Out Run", "Racing", "M"),
    ],
    "arcade": [
        ("Track & Field", "Sport / Atletika", "S"),
        ("Hang-On", "Racing / motorky", "S"),
        ("Pole Position", "Racing", "S"), ("Pole Position II", "Racing", "S"),
        ("Super Sprint", "Racing", "S"),
    ],
    "amiga": [
        ("Kick Off 2", "Sport / Fotbal", "M"), ("Sensible World of Soccer", "Sport / Fotbal", "L"),
        ("Nigel Mansell's World Championship", "Racing", "M"),
    ],
    "c64": [
        ("Pitstop II", "Racing", "S"), ("California Games", "Sport", "M"),
        ("International Karate +", "Sport / Bojové", "M"),
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
        arr.append({"name": nm, "genre": ge, "length": ln, "flags": []})
        exist.add(k); n += 1
    added[slug] = n
p_file.write_text(json.dumps(eg, ensure_ascii=False, indent=2), encoding="utf-8")
print("Přidáno:", added, "celkem", sum(added.values()))
