# -*- coding: utf-8 -*-
"""Vytvori pracovni adresar jen z davek, ktere jeste nemaji vystup.

Workflow spousti agenta ke KAZDE davce a hotove preskoci az uvnitr agenta.
Kdyz zbyva doplnit par davek z dvou set, stejne se nastartuje dve ste agentu
— a jakmile se cestou narazi na limit relace, spadnou naraz vsichni zbyli
ve fronte, i ti, kteri meli jen vratit SKIP.

Tenhle skript proto vybere jen chybejici davky, precisluje je od nuly do
noveho adresare a po dokonceni vrati vystupy zpet pod puvodnimi jmeny.

Pouziti:
  python tools/i18n_zbytek.py <zdroj> <cil>            pripravi zbytek
  python tools/i18n_zbytek.py <zdroj> <cil> --zpet     vrati vystupy zpet
"""
import io
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MAPA = "mapa.json"


def _cesta(p: str) -> Path:
    cesta = Path(p)
    return cesta if cesta.is_absolute() else ROOT / cesta


def priprav(zdroj: Path, cil: Path) -> None:
    src_chunks = zdroj / "chunks"
    dst_chunks = cil / "chunks"
    dst_chunks.mkdir(parents=True, exist_ok=True)
    for f in dst_chunks.glob("*.json"):
        f.unlink()

    chybi = []
    for vstup in sorted(src_chunks.glob("games_[0-9][0-9][0-9].json")):
        if not vstup.with_name(vstup.stem + "_out.json").exists():
            chybi.append(vstup)

    mapa = {}
    for i, vstup in enumerate(chybi):
        novy = dst_chunks / f"games_{i:03d}.json"
        shutil.copyfile(vstup, novy)
        mapa[f"games_{i:03d}"] = vstup.stem

    with io.open(cil / MAPA, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(mapa, fh, ensure_ascii=False, indent=1)

    print(f"chybejicich davek: {len(chybi)}")
    if chybi:
        print(f'args: {{"base": "{cil.as_posix()}", "counts": {{"games": {len(chybi)}}}}}')


def zpet(zdroj: Path, cil: Path) -> None:
    mapa = json.loads((cil / MAPA).read_text("utf-8"))
    vraceno = 0
    for novy, puvodni in mapa.items():
        out = cil / "chunks" / f"{novy}_out.json"
        if not out.exists():
            continue
        try:
            d = json.loads(out.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            print(f"  [x] {novy}: nevalidni JSON")
            continue
        if not (isinstance(d, dict) and d.get("en") and d.get("de")):
            print(f"  [x] {novy}: chybi en nebo de")
            continue
        shutil.copyfile(out, zdroj / "chunks" / f"{puvodni}_out.json")
        vraceno += 1
    print(f"vraceno vystupu: {vraceno}/{len(mapa)}")


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    zdroj, cil = _cesta(sys.argv[1]), _cesta(sys.argv[2])
    if "--zpet" in sys.argv:
        zpet(zdroj, cil)
    else:
        priprav(zdroj, cil)
    return 0


if __name__ == "__main__":
    sys.exit(main())
