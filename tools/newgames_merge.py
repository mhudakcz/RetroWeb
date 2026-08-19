# -*- coding: utf-8 -*-
"""Sloučí vygenerované hry (out_<slug>_NN.json) do dávky pro add_games_meta.py.

Použití:  python tools/newgames_merge.py <workdir> <batch_out.json> [--min-article 1500]

Deduplikuje proti stávajícímu datasetu i uvnitř vygenerované sady (agenti pracují
na tematických okruzích nezávisle, takže se občas potkají na stejném titulu),
zkontroluje slovník flags/length a vyhodí příliš krátké články.
"""
import json, sys, glob, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

args = sys.argv[1:]
if len(args) < 2:
    print(__doc__)
    sys.exit(1)
BASE, OUT = Path(args[0]), Path(args[1])
MIN_ART = int(args[args.index("--min-article") + 1]) if "--min-article" in args else 1500

OK_FLAGS = {"mustplay", "puzzle", "mature", "homebrew"}
OK_LEN = {"S", "M", "L", "XL"}

# co už v katalogu je
d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
seen = {(p["slug"], P.norm_name(g["name"])) for p in d["platforms"] for g in p["games"]}

batch, stats = [], {}
for f in sorted(glob.glob(str(BASE / "out_*.json"))):
    m = re.match(r"out_(.+)_(\d+)\.json", Path(f).name)
    if not m:
        continue
    plat_default = m.group(1)
    try:
        items = json.loads(Path(f).read_text("utf-8"))
        if not isinstance(items, list):
            raise ValueError("není pole")
    except Exception as e:
        stats.setdefault(plat_default, {}).setdefault("vadne_davky", []).append(f"{Path(f).name}: {e}")
        continue

    for it in items:
        # dávka může být i mezplatformní (jedna značka napříč konzolemi) —
        # pak si každá hra nese vlastní platformu a jméno souboru je jen štítek
        plat = (it.get("platform") or plat_default).strip()
        s = stats.setdefault(plat, {})
        s["navrzeno"] = s.get("navrzeno", 0) + 1
        name = (it.get("name") or "").strip()
        art = (it.get("article") or "").strip()
        if not name or not art:
            s["bez_nazvu_ci_clanku"] = s.get("bez_nazvu_ci_clanku", 0) + 1
            continue
        key = (plat, P.norm_name(name))
        if key in seen:
            s["duplicita"] = s.get("duplicita", 0) + 1
            continue
        if len(art) < MIN_ART:
            s["kratky_clanek"] = s.get("kratky_clanek", 0) + 1
            continue
        length = (it.get("length") or "M").strip().upper()
        if length not in OK_LEN:
            length = "M"
        flags = [x for x in (it.get("flags") or []) if x in OK_FLAGS]
        seen.add(key)
        batch.append({
            "slug": plat,
            "name": name,
            "genre": (it.get("genre") or "").strip() or "Akcni",
            "length": length,
            "year": str(it.get("year") or "").strip(),
            "studio": (it.get("studio") or "").strip(),
            "flags": flags,
            "detail": art,
        })
        s["prijato"] = s.get("prijato", 0) + 1

OUT.write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")

have = {p["slug"]: len(p["games"]) for p in d["platforms"]}
print(f"dávka: {len(batch)} her -> {OUT}")
for plat in sorted(stats):
    s = stats[plat]
    add = s.get("prijato", 0)
    print(f"  {plat:10} navrženo {s.get('navrzeno', 0):3} | přijato {add:3} | "
          f"duplicit {s.get('duplicita', 0):3} | krátkých {s.get('kratky_clanek', 0):2}"
          f"  => katalog {have.get(plat, 0)} -> {have.get(plat, 0) + add}")
    for b in s.get("vadne_davky", []):
        print(f"    VADNÁ DÁVKA {b}")
if batch:
    L = sorted(len(g["detail"]) for g in batch)
    print(f"  délky článků: min {L[0]}, medián {L[len(L)//2]}, max {L[-1]}")
