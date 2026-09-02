# -*- coding: utf-8 -*-
"""Pripravi plan a podklady pro newgames.workflow.js.

Workflow potrebuje dve veci: plan (ktera platforma, jake tematicke okruhy,
kolik her) a ke kazde platforme soubor existing_<slug>.txt se seznamem her,
ktere uz v katalogu jsou — bez nej agenti navrhuji to, co uz mame.

Cile jsou v CILE nize a berou ohled na skutecnou velikost knihovny: Virtual
Boy ma celkem 22 her, takze cil 20 je strop, ne skromnost. U velkych platforem
je cil naopak jen dalsi krok, ne uplnost.

Rozdeleni do okruhu ma dva duvody: agent na uzsim zadani sahne hloub nez po
peti nejznamejsich titulech, a nezavisle okruhy se min opakuji.

Pouziti:
  python tools/newgames_prep.py <workdir> [slug,slug,...]
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# slug -> cilovy pocet her v katalogu
CILE = {
    # male knihovny — cil je blizko uplnosti
    "virtual-boy": 20, "vectrex": 25, "sega-32x": 25, "sg-1000": 25,
    "atari-5200": 28, "jaguar": 28, "amiga-cd32": 28, "atari-7800": 30,
    "cd-i": 30, "game-watch": 30, "intellivision": 32, "colecovision": 32,
    "switch-2": 35, "ngpc": 35,
    # stredni
    "mega-cd": 45, "wonderswan": 45, "3do": 45, "atari-lynx": 40, "cps": 40,
    "game-gear": 50, "neogeo": 55, "atari-2600": 60,
    # velke knihovny — jen dalsi krok
    "master-system": 65, "pc-engine": 65, "wii-u": 65, "3ds": 80,
    "arcade": 130,
    # domaci pocitace: knihovny v tisicich titulu, tady jde o dalsich ~50
    "c64": 115, "zx-spectrum": 101, "atari-8bit": 100, "atari-st": 70,
    # kapesni Nintenda — knihovny v stovkach titulu, taky dalsich ~50
    "game-boy": 133, "game-boy-color": 126, "game-boy-advance": 145,
}

# Domaci pocitace maji jine okruhy nez konzole — vetsina jejich klasik jsou
# zanry, ktere na konzolich te doby skoro nebyly.
OKRUHY_POCITACE = [
    "akcni hry, plosinovky a arkadovky",
    "adventury, RPG a textovky",
    "strategie, simulatory a budovatelske hry",
    "zavodni a sportovni tituly",
    "domaci a evropska produkce vcetne ceske sceny",
]

# tematicke okruhy podle povahy platformy
OKRUHY_ARKADY = [
    "bojovky a versus tituly", "shmupy a vertikalni strilecky",
    "beat 'em up a run and gun", "zavodni a sportovni automaty",
    "plosinovky a akcni skakacky", "klasika prelomu 70. a 80. let",
    "puzzle a kuriozity", "japonske automaty, ktere na Zapad nedorazily",
]
OKRUHY_KONZOLE = [
    "akcni hry a plosinovky", "RPG, JRPG a adventury",
    "zavodni a sportovni tituly", "strilecky a shmupy",
    "puzzle, logicke a rodinne hry", "exkluzivity a skryte klenoty platformy",
]
OKRUHY_MALE = [
    "nejvyznamnejsi tituly platformy", "akcni hry a plosinovky",
    "zbytek zajimave knihovny vcetne kuriozit",
]


def okruhy(slug: str, potreba: int) -> list[str]:
    if slug == "arcade":
        zdroj = OKRUHY_ARKADY
    elif slug in ("c64", "zx-spectrum", "atari-8bit", "atari-st", "amiga",
                  "amstrad-cpc", "msx", "x68000", "pc-98"):
        zdroj = OKRUHY_POCITACE
    elif potreba <= 20:
        zdroj = OKRUHY_MALE
    else:
        zdroj = OKRUHY_KONZOLE
    # zhruba 10 her na agenta; min okruhu nez by vyslo, kdyz je potreba malo
    kolik = max(1, min(len(zdroj), -(-potreba // 10)))
    return zdroj[:kolik]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    work.mkdir(parents=True, exist_ok=True)
    jen = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None

    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    plan, celkem = [], 0

    for p in data["platforms"]:
        slug = p["slug"]
        if slug not in CILE or (jen and slug not in jen):
            continue
        mame = len(p["games"])
        potreba = CILE[slug] - mame
        if potreba <= 0:
            print(f"  [=] {p['name']}: uz ma {mame}, cil {CILE[slug]}")
            continue

        # seznam stavajicich her, aby je agenti neopakovali
        with io.open(work / f"existing_{slug}.txt", "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(sorted(g["name"] for g in p["games"])))

        sl = okruhy(slug, potreba)
        na_okruh = -(-potreba // len(sl))
        plan.append({"platform": p["name"], "slug": slug, "slices": sl, "count": na_okruh})
        celkem += na_okruh * len(sl)
        print(f"  [+] {p['name']:34} {mame:4} -> {CILE[slug]:4}  "
              f"({len(sl)} okruhu po {na_okruh})")

    if not plan:
        print("neni co doplnovat")
        return 0

    with io.open(work / "plan.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(plan, fh, ensure_ascii=False, indent=1)

    agentu = sum(len(x["slices"]) for x in plan)
    print(f"\nplatforem: {len(plan)}, agentu: {agentu}, her k navrzeni: ~{celkem}")
    print(f'args: {{"base": "{work.as_posix()}", "plan": <obsah {work.as_posix()}/plan.json>}}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
