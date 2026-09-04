# -*- coding: utf-8 -*-
"""Slouci vystupy titles.workflow.js do davky pro add_games_meta.py.

Vystup agenta je pole zaznamu bez slugu platformy — ten je ve vstupnim
souboru tehoz cisla, takze se dvojice paruje podle nazvu souboru.

Deduplikuje proti katalogu i uvnitr davky: agenti pracuji nezavisle a nektere
tituly vraci pod mirne jinym nazvem, nez pod jakym uz hra v katalogu je.

Pouziti:  python tools/titles_merge.py <workdir> <batch_out.json> [--min-article 1300]
"""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
POVOLENE_FLAGS = {"mustplay", "puzzle", "mature", "homebrew"}
POVOLENE_LENGTH = {"S", "M", "L", "XL"}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    out_path = Path(sys.argv[2])
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    min_clanek = (int(sys.argv[sys.argv.index("--min-article") + 1])
                  if "--min-article" in sys.argv else 1300)

    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    mame = {p["slug"]: {P.norm_name(g["name"]) for g in p["games"]}
            for p in data["platforms"]}

    davka, statistiky = [], {}
    videne = {}
    for vstup in sorted(work.glob("tit_[0-9][0-9][0-9].json")):
        vystup = vstup.with_name(vstup.stem + "_out.json")
        if not vystup.exists():
            continue
        try:
            zadani = json.loads(vstup.read_text("utf-8"))
            hry = json.loads(vystup.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {vystup.name}: {e}")
            continue
        slug = zadani["slug"]
        s = statistiky.setdefault(slug, {"navrzeno": 0, "prijato": 0,
                                         "duplicit": 0, "kratkych": 0, "spatnych": 0})
        for g in (hry if isinstance(hry, list) else []):
            s["navrzeno"] += 1
            nazev = (g.get("name") or "").strip()
            clanek = (g.get("detail") or "").strip()
            if not nazev or not clanek:
                s["spatnych"] += 1
                continue
            n = P.norm_name(nazev)
            if n in mame.get(slug, set()) or (slug, n) in videne:
                s["duplicit"] += 1
                continue
            if len(clanek) < min_clanek:
                s["kratkych"] += 1
                continue
            flags = [f for f in (g.get("flags") or []) if f in POVOLENE_FLAGS]
            delka = g.get("length") if g.get("length") in POVOLENE_LENGTH else "M"
            davka.append({
                "slug": slug, "name": nazev,
                "genre": (g.get("genre") or "").strip() or "Hra",
                "length": delka, "year": str(g.get("year") or "").strip(),
                "studio": (g.get("studio") or "").strip(),
                "flags": flags, "detail": clanek,
            })
            videne[(slug, n)] = True
            s["prijato"] += 1

    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(davka, fh, ensure_ascii=False, indent=1)

    print(f"davka: {len(davka)} her -> {out_path}")
    for slug, s in sorted(statistiky.items()):
        print(f"  {slug:16} navrzeno {s['navrzeno']:3} | prijato {s['prijato']:3} "
              f"| duplicit {s['duplicit']:3} | kratkych {s['kratkych']:2} "
              f"| vadnych {s['spatnych']:2}")
    if davka:
        d = sorted(len(x["detail"]) for x in davka)
        print(f"  delky clanku: min {d[0]}, median {d[len(d) // 2]}, max {d[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
