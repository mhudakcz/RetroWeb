# -*- coding: utf-8 -*-
"""Najde herní obrázky se shodným obsahem. Stejná fotka u RŮZNÝCH her = falešná
shoda z fallback párování -> ke smazání. Stejná hra na více platformách (stejný
snímek) je legitimní a necháme ji.

  python tools/find_dup_images.py            # jen vypíše
  python tools/find_dup_images.py delete     # smaže falešné fallback duplicity
"""
import hashlib, re, sys
from pathlib import Path
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / "public" / "images" / "games"


def base_name(f):
    """Jméno hry bez prefixu platformy a bez -snap/-title."""
    stem = f.stem
    stem = re.sub(r"-(snap|title)$", "", stem)
    stem = stem.split("__", 1)[-1]  # odstraň 'platform__'
    return stem


def is_fallback(f):
    return f.stem.endswith("-snap") or f.stem.endswith("-title")


groups = defaultdict(list)
for f in GAMES.rglob("*.webp"):
    groups[hashlib.md5(f.read_bytes()).hexdigest()].append(f)

# zajímají nás jen skupiny, kde se shodný obsah objevuje u RŮZNÝCH her
bad = []
for k, v in groups.items():
    if len(v) < 2:
        continue
    names = {base_name(f) for f in v}
    if len(names) > 1:  # různé hry -> falešná shoda
        bad.append((k, v, names))

print(f"Skupin falešných duplicit (různé hry, stejná fotka): {len(bad)}")
for k, v, names in sorted(bad, key=lambda x: -len(x[1])):
    print(f"\n[{len(v)}×] hry: {', '.join(sorted(names))}")
    for f in v:
        print(f"   {f.relative_to(GAMES)}")

if len(sys.argv) > 1 and sys.argv[1] == "delete":
    # Stejný obsah u RŮZNÝCH her = vždy falešná shoda (jeden obrázek omylem
    # přiřazený více titulům). Smažeme CELOU skupinu — i „boxart" bez přípony.
    deleted = 0
    for k, v, names in bad:
        for f in v:
            if f.exists():
                f.unlink(); deleted += 1
    print(f"Smazáno {deleted} falešných duplicitních souborů z {len(bad)} skupin.")
