# -*- coding: utf-8 -*-
"""Pripravi davky pro magazine.workflow.js a slouci vysledek.

Rejstrik (src/data/magazine.json) rika, CO je v kterem cisle. Tenhle skript
k tomu dopise redakcni obsah: editorial, tema cisla, zebricek a upoutavku na
dalsi cislo. Kazde cislo = jedna davka pro jednoho agenta, protoze editorial
musi znat cely obsah cisla najednou.

Uz napsana cisla se preskakuji — text vydaneho cisla se nemeni, stejne jako
se nemeni jeho obsah.

Pouziti:
  python tools/magazine_prep.py <workdir> [--rok 1994]   pripravi davky
  python tools/magazine_prep.py <workdir> --merge         slouci vystupy
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "src" / "data" / "magazine.json"
TEXT = ROOT / "src" / "data" / "magazine_text.json"


def load_text() -> dict:
    return json.loads(TEXT.read_text("utf-8")) if TEXT.exists() else {}


def game_index() -> tuple[dict, dict]:
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    games, plats = {}, {}
    for p in data["platforms"]:
        plats[p["slug"]] = {"name": p["name"], "maker": p["maker"], "year": p["year"]}
        for g in p["games"]:
            games[g["slug"]] = {
                "name": g["name"], "platform": p["name"], "genre": g.get("genre") or "",
                "year": str(g.get("year") or ""), "studio": g.get("studio") or "",
                "mustplay": "mustplay" in (g.get("flags") or []),
                "teaser": g.get("teaser") or "",
            }
    return games, plats


def prepare(work: Path, rok: int | None) -> None:
    work.mkdir(parents=True, exist_ok=True)
    ledger = json.loads(LEDGER.read_text("utf-8"))
    hotovo = load_text()
    games, plats = game_index()

    vydani = ledger["vydani"]
    todo = [v for v in vydani if (not rok or v["rok"] == rok) and v["id"] not in hotovo]
    if not todo:
        print("vsechna cisla uz text maji")
        return

    poradi = {v["id"]: i for i, v in enumerate(vydani)}
    n = 0
    for v in todo:
        i = poradi[v["id"]]
        dalsi = vydani[i + 1] if i + 1 < len(vydani) else None
        payload = {
            "id": v["id"], "rok": v["rok"], "cislo": v["cislo"],
            "platformy": [plats[s] | {"slug": s} for s in v["platformy"] if s in plats],
            "hry": [games[s] | {"slug": s} for s in v["hry"] if s in games],
            # upoutavka na dalsi cislo musi vedet, co v nem bude
            "dalsi": None if not dalsi else {
                "id": dalsi["id"],
                "hry": [games[s]["name"] for s in dalsi["hry"][:10] if s in games],
                "platformy": [plats[s]["name"] for s in dalsi["platformy"] if s in plats],
            },
            "odhad_roku": len(v.get("odhad_roku") or []),
        }
        with io.open(work / f"mag_{n:03d}.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        n += 1

    print(f"cisel bez textu: {len(todo)} -> {n} davek")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def merge(work: Path) -> None:
    text = load_text()
    ledger = json.loads(LEDGER.read_text("utf-8"))
    znam = {v["id"] for v in ledger["vydani"]}
    hry = {s for v in ledger["vydani"] for s in v["hry"]}

    pridano = spatne = 0
    for f in sorted(work.glob("mag_*_out.json")):
        try:
            d = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        cid = d.get("id")
        if cid not in znam:
            print(f"  [x] {f.name}: cislo {cid!r} neni v rejstriku")
            spatne += 1
            continue
        if cid in text:
            continue
        chybi = [k for k in ("editorial", "tema", "zebricek", "chystame") if not d.get(k)]
        if chybi:
            print(f"  [x] {cid}: chybi {', '.join(chybi)}")
            spatne += 1
            continue
        # zebricek smi ukazovat jen na hry, ktere v cisle opravdu jsou
        z = [p for p in d["zebricek"] if p.get("slug") in hry]
        if len(z) < 3:
            print(f"  [x] {cid}: zebricek ma jen {len(z)} platnych polozek")
            spatne += 1
            continue
        text[cid] = {"titulek": d.get("titulek") or "", "editorial": d["editorial"],
                     "tema": d["tema"], "zebricek": z, "chystame": d["chystame"]}
        pridano += 1

    with io.open(TEXT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(text, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"cisel s textem: {len(text)} (+{pridano})")
    if spatne:
        print(f"  zahozeno vadnych: {spatne}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    if "--merge" in sys.argv:
        merge(work)
    else:
        rok = int(sys.argv[sys.argv.index("--rok") + 1]) if "--rok" in sys.argv else None
        prepare(work, rok)
    return 0


if __name__ == "__main__":
    sys.exit(main())
