# -*- coding: utf-8 -*-
"""Mezikrok mezi navrhem portu a jeho zapsanim do katalogu.

Agent, ktery porty navrhuje, obcas tvrdi vydani, ktere nikdy nevyslo — v pilotni
davce se takhle objevilo "Call of Duty: Modern Warfare: Reflex Edition" na PS2,
prestoze ta verze byla jen na Wii. Na webu by z toho byl fakt, takze kazde
navrzene vydani projde druhym agentem v roli advokata dabla
(tools/ports_verify.workflow.js) a projdou jen potvrzena.

Pouziti:
  python tools/porty_verify_prep.py <workdir_portu>            pripravi overovaci davky
  python tools/porty_verify_prep.py <workdir_portu> --uplatni  zahodi zamitnuta vydani
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def nacti_navrhy(work: Path):
    """[(soubor, index, polozka)] ze vsech ports_*_out.json."""
    out = []
    for f in sorted(work.glob("ports_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        if isinstance(got, list):
            for i, it in enumerate(got):
                out.append((f, i, it))
    return out


def prepare(work: Path, size: int) -> None:
    navrhy = nacti_navrhy(work)
    radky = [{"id": n, "name": it.get("name", ""), "platform": it.get("platform", ""),
              "year": str(it.get("year", ""))}
             for n, (_f, _i, it) in enumerate(navrhy)]
    # mapa id -> (soubor, index), aby se po overeni vedelo, co zahodit
    mapa = [{"id": n, "file": _f.name, "idx": _i} for n, (_f, _i, _it) in enumerate(navrhy)]
    (work / "_mapa.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
    n = 0
    for i in range(0, len(radky), size):
        (work / f"verify_{n:02d}.json").write_text(
            json.dumps(radky[i: i + size], ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
    print(f"navrzenych vydani: {len(radky)} -> {n} overovacich davek po {size}")
    print(f'args: {{"base": "{work.as_posix()}", "batches": {n}}}')


def uplatni(work: Path) -> None:
    mapa = json.loads((work / "_mapa.json").read_text("utf-8"))
    podle_id = {m["id"]: (m["file"], m["idx"]) for m in mapa}

    verdikt = {}
    for f in sorted(work.glob("verify_*_out.json")):
        try:
            got = json.loads(f.read_text("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  [x] {f.name}: {e}")
            continue
        for it in got if isinstance(got, list) else []:
            if "id" in it:
                verdikt[it["id"]] = (bool(it.get("ok")), it.get("proc") or "")

    # Neoverene radky se NEZAHAZUJI — overeni jen nedobehlo a zahodit je by
    # znamenalo tise prijit o praci. Zahazuji se jen vyslovne zamitnute.
    zahodit = {}
    for i, (ok, proc) in verdikt.items():
        if ok or i not in podle_id:
            continue
        fname, idx = podle_id[i]
        zahodit.setdefault(fname, {})[idx] = proc

    celkem = zamitnuto = 0
    for f in sorted(work.glob("ports_*_out.json")):
        got = json.loads(f.read_text("utf-8"))
        if not isinstance(got, list):
            continue
        celkem += len(got)
        vyhodit = zahodit.get(f.name, {})
        if not vyhodit:
            continue
        for idx, proc in sorted(vyhodit.items()):
            it = got[idx]
            print(f"  [zamitnuto] {it.get('name')} / {it.get('platform')}: {proc[:70]}")
        nove = [it for i, it in enumerate(got) if i not in vyhodit]
        zamitnuto += len(got) - len(nove)
        f.write_text(json.dumps(nove, ensure_ascii=False, indent=1), encoding="utf-8")

    neovereno = sum(1 for m in mapa if m["id"] not in verdikt)
    print(f"\nnavrhu: {celkem}, zamitnuto: {zamitnuto}" +
          (f", neovereno (ponechano): {neovereno}" if neovereno else ""))


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    work = Path(a[0])
    if not work.is_absolute():
        work = ROOT / work
    if "--uplatni" in a:
        uplatni(work)
    else:
        size = int(a[a.index("--size") + 1]) if "--size" in a else 25
        prepare(work, size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
