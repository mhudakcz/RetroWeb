# -*- coding: utf-8 -*-
"""Najde davky portu, ktere vratily podezrele malo, a smaze jejich vystup.

Vznikla potreba po tom, co soubezne bezely dve verze zadani: starsi byla
tak prisna, ze u chybejicich titulu nevracela nic, a prepisovala vystupy
te opravene. Pozna se to podle pomeru — davka sesti chybejicich titulu ma
vratit aspon polovinu z nich, protoze titul, ktery v katalogu neni, ma
vzniknout vzdycky.

U davek portu (neprazdne "have") tohle merítko neplati: tam je nula legitimni
odpoved, kdyz se zadna verze nelisila.

Pouziti:
  python tools/porty_kontrola.py <workdir>            jen vypise
  python tools/porty_kontrola.py <workdir> --smazat   smaze vystupy k prepocitani
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    work = Path(a[0])
    if not work.is_absolute():
        work = ROOT / work
    smazat = "--smazat" in a

    podezrele, ok, chybi = [], 0, []
    for vstup in sorted(work.glob("ports_*.json")):
        if vstup.name.endswith("_out.json"):
            continue
        cislo = vstup.stem.split("_")[1]
        vystup = work / f"ports_{cislo}_out.json"
        try:
            zadano = json.loads(vstup.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        # merítko plati jen na chybejici tituly
        nove_tituly = [z for z in zadano if not z.get("have")]
        if not nove_tituly:
            continue
        if not vystup.exists():
            chybi.append(cislo)
            continue
        try:
            vraceno = json.loads(vystup.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            podezrele.append((cislo, "nevalidni JSON", 0, len(nove_tituly)))
            continue
        if not isinstance(vraceno, list):
            podezrele.append((cislo, "neni pole", 0, len(nove_tituly)))
            continue
        pokryte = {z.get("name", "").lower() for z in vraceno}
        trefy = sum(1 for z in nove_tituly if z["name"].lower() in pokryte)
        if trefy * 2 < len(nove_tituly):
            podezrele.append((cislo, "malo titulu", trefy, len(nove_tituly)))
        else:
            ok += 1

    print(f"davek v poradku: {ok}")
    if chybi:
        print(f"davek bez vystupu: {len(chybi)} -> {', '.join(chybi[:12])}"
              + (" ..." if len(chybi) > 12 else ""))
    if podezrele:
        print(f"davek k prepocitani: {len(podezrele)}")
        for cislo, duvod, trefy, celkem in podezrele[:15]:
            print(f"  {cislo}: {duvod} ({trefy} z {celkem} titulu)")
        if len(podezrele) > 15:
            print(f"  ... a dalsich {len(podezrele) - 15}")
        if smazat:
            for cislo, *_ in podezrele:
                (work / f"ports_{cislo}_out.json").unlink(missing_ok=True)
            print(f"\nsmazano {len(podezrele)} vystupu — pust workflow znovu")
        else:
            print("\n(spust s --smazat, aby se daly prepocitat)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
