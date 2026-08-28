# -*- coding: utf-8 -*-
"""Prevěří obrázky stažené z libretra proti současnému, přísnějšímu párování.

Párování se během práce několikrát opravovalo — jednopísmenné názvy, pořadová
čísla dílů a nakonec podnázvy ("Wing Commander: Prophecy" bral obal jedničky).
Obrázky stažené starším, volnějším párováním ale zůstaly na disku.

Skript pro každou hru s obrázkem znovu spustí best_boxart a nahlásí ty, které
by se dnes už NEnapárovaly.

POZOR: nález sám o sobě NEZNAMENÁ špatný obrázek. Ze souboru na disku nejde
poznat, odkud přišel — obal mohl přijít ze Steamu nebo z Wikipedie, kde je
správně, i když ho libretro nezná. Na pc-9x je takových her většina, protože
platforma se v libretru hledá v DOSovém repozitáři a Quake II ani Unreal
Tournament tam nejsou. Výstup je proto podklad pro ruční kontrolu, ne pro
hromadné mazání; --delete používej jen na platformu, kde je libretro jediný
zdroj.

Použití:
  python tools/recheck_boxart.py [--delete] [platforma,...]
    --delete smaže obal i snímky u her, které dnešním párováním neprojdou
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import fetch_images as F  # noqa: E402

IMG = ROOT / "public" / "images" / "games"


def main() -> int:
    delete = "--delete" in sys.argv
    rest = [a for a in sys.argv[1:] if not a.startswith("--")]
    only = set(rest[0].split(",")) if rest else None

    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    plat_games = {p["slug"]: p["games"] for p in data["platforms"]}

    bad_total = removed = 0
    for slug, repo in F.LIBRETRO.items():
        if only and slug not in only:
            continue
        games = [g for g in plat_games.get(slug, []) if g.get("image")]
        if not games:
            continue
        try:
            names = F.list_boxarts(repo)
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {slug}: {e}")
            continue
        if not names:
            continue
        idx = F.index_boxarts(names)

        bad = []
        for g in games:
            # zajima nas jen obrazek, ktery ma tvar souboru z libretra
            files = list((IMG / slug).glob(f"{g['slug']}.*")) + \
                    list((IMG / slug).glob(f"{g['slug']}-snap.*")) + \
                    list((IMG / slug).glob(f"{g['slug']}-title.*"))
            if not files:
                continue
            if F.best_boxart(g["name"], names, idx) is None:
                bad.append((g["name"], files))

        if bad:
            print(f"\n== {slug}: {len(bad)} her by se dnes nenapárovalo ==")
            for name, files in bad[:12]:
                print(f"   {name}")
            if len(bad) > 12:
                print(f"   … a dalších {len(bad) - 12}")
            bad_total += len(bad)
            if delete:
                for _, files in bad:
                    for f in files:
                        f.unlink()
                        removed += 1

    print(f"\nceLkem podezřelých her: {bad_total}")
    if delete:
        print(f"smazáno souborů: {removed}")
        print("spusť ještě tools/parse_content.py")
    elif bad_total:
        print("(nic se nesmazalo — spusť znovu s --delete)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
