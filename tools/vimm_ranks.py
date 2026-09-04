# -*- coding: utf-8 -*-
"""Vytahne z Vimm's Lair zebricky nejlepe hodnocenych her a porovna je s katalogem.

Vimm's Lair vede u kazde platformy nekolik zebricku (celkove hodnoceni, grafika,
zvuk, hratelnost a mesicni Top 10). Jsou to nazvy her a cisla, tedy fakta —
bereme z nich jen seznam titulu jako voditko, co v katalogu chybi a co by melo
byt mezi doporucenimi.

Neni to zdroj obrazku ani souboru; stahuje se jedna stranka na platformu.

Pouziti:
  python tools/vimm_ranks.py <workdir>            stahne zebricky
  python tools/vimm_ranks.py <workdir> --report   porovna s katalogem
"""
import html
import io
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

# nas slug -> nazev systemu ve Vimm's Lair
SYSTEMY = {
    "mega-drive": "Genesis", "snes": "SNES", "nes": "NES", "n64": "N64",
    "gamecube": "GameCube", "wii": "Wii", "wii-u": "WiiU",
    "playstation": "PS1", "ps2": "PS2", "ps3": "PS3", "psp": "PSP",
    "saturn": "Saturn", "dreamcast": "Dreamcast", "mega-cd": "SegaCD",
    "sega-32x": "32X", "master-system": "SMS",
    "game-boy": "GB", "game-boy-color": "GBC", "game-boy-advance": "GBA",
    "nds": "DS", "3ds": "3DS", "xbox": "Xbox",
    "atari-2600": "Atari2600", "atari-5200": "Atari5200",
    "atari-7800": "Atari7800", "atari-lynx": "Lynx", "jaguar": "Jaguar",
    "pc-engine": "TG16",
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
TABULKA = re.compile(r"<caption>([^<]+)</caption>(.*?)</table>", re.S)
RADEK = re.compile(r'<a href="/vault/\d+">([^<]+)</a>\s*</td>\s*<td[^>]*>([\d.]+)', re.S)
TOP = re.compile(r'Top 10(.*?)</div>', re.S)


def stahni(url: str) -> str:
    r = subprocess.run(["curl", "-s", "--ssl-no-revoke", "--max-time", "25",
                        "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def sber(work: Path) -> None:
    work.mkdir(parents=True, exist_ok=True)
    vysledek = {}
    for slug, system in SYSTEMY.items():
        stranka = stahni(f"https://vimm.net/vault/{system}")
        if not stranka:
            print(f"  [x] {slug}: prazdna odpoved")
            continue
        tituly = {}
        for nadpis, telo in TABULKA.findall(stranka):
            for nazev, skore in RADEK.findall(telo):
                nazev = nazev.strip()
                # nejvyssi skore napric kategoriemi
                if nazev not in tituly or float(skore) > tituly[nazev]["skore"]:
                    tituly[nazev] = {"skore": float(skore), "kategorie": nadpis.strip()}
        vysledek[slug] = [{"nazev": n, **v} for n, v in
                          sorted(tituly.items(), key=lambda x: -x[1]["skore"])]
        print(f"  {slug:18} {len(vysledek[slug]):3} titulu ({system})")
        time.sleep(1.0)          # zdvorily odstup mezi dotazy

    out = work / "ranks.json"
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(vysledek, fh, ensure_ascii=False, indent=1)
    print(f"\nulozeno: {out}  ({sum(len(v) for v in vysledek.values())} titulu)")


def report(work: Path) -> None:
    ranks = json.loads((work / "ranks.json").read_text("utf-8"))
    data = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
    picks = json.loads((ROOT / "src/data/platform_picks.json").read_text("utf-8"))

    chybi_celkem = pridat_celkem = 0
    chybi_vse, do_picku = {}, {}
    for slug, tituly in ranks.items():
        plat = next((p for p in data["platforms"] if p["slug"] == slug), None)
        if not plat:
            continue
        # normalizovany index her na platforme
        mame = {}
        for g in plat["games"]:
            for varianta in _varianty(g["name"]):
                mame.setdefault(varianta, g)
        ve_vyberu = {p["slug"] for p in (picks.get(slug) or [])}

        chybi, pridat = [], []
        for t in tituly:
            varianty = _varianty(_uprav(t["nazev"]))
            n = varianty[0]
            g = next((mame[v] for v in varianty if v in mame), None)
            if not g:
                g = next((_s_podtitulem(v, mame) for v in varianty
                          if _s_podtitulem(v, mame)), None)
            if not g:
                if not _pokryto_kompilaci(n, mame):
                    chybi.append(_uprav(t["nazev"]))
            elif g["slug"] not in ve_vyberu:
                pridat.append((g["slug"], g["name"], t["skore"]))
        if chybi:
            chybi_vse[slug] = chybi
            chybi_celkem += len(chybi)
        if pridat:
            do_picku[slug] = pridat
            pridat_celkem += len(pridat)

    print(f"CHYBI V KATALOGU: {chybi_celkem} titulu")
    for slug, v in sorted(chybi_vse.items(), key=lambda x: -len(x[1]))[:12]:
        print(f"  {slug:18} {len(v):2}  {', '.join(v[:4])}")
    print(f"\nMAME, ALE NEJSOU V 'CIM ZACIT': {pridat_celkem} titulu")
    for slug, v in sorted(do_picku.items(), key=lambda x: -len(x[1]))[:12]:
        print(f"  {slug:18} {len(v):2}  {', '.join(n for _, n, _ in v[:4])}")

    with io.open(work / "report.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"chybi": chybi_vse, "do_picku": do_picku}, fh,
                  ensure_ascii=False, indent=1)


def _uprav(nazev: str) -> str:
    """Vimm pise clen na konec ("Revenge of Shinobi, The"), k nazvu pripojuje
    kompilace v zavorce a apostrofy uklada jako HTML entitu (&#039;) —
    bez uprav by se proti katalogu neparovalo nic z toho."""
    nazev = html.unescape(nazev)
    nazev = re.sub(r"\s*[(~][^)]*\)?$", "", nazev).strip()
    # "Pokemon: Blue Version" -> "Pokemon Blue"; slovo Version je jen zapis Vimmu
    nazev = re.sub(r"\s+Version$", "", nazev).strip()

    m = re.match(r"^(.*),\s*(The|A|An)$", nazev)
    if m:
        nazev = f"{m.group(2)} {m.group(1)}"
    return nazev


# znackove predpony, ktere jedna strana uvadi a druha ne
_PREDPONY = ("shin megami tensei ", "tom clancy s ", "the elder scrolls iii ",
             "elder scrolls iii the ", "disney s ", "sid meier s ")


def _varianty(nazev: str) -> list:
    """Normalizovany nazev plus varianta bez znackove predpony a bez podtitulu."""
    zaklad = P.norm_name(nazev)
    out = [zaklad]
    for p in _PREDPONY:
        if zaklad.startswith(p):
            out.append(zaklad[len(p):])
    # podtitul za dvojteckou nebo pomlckou muze mit jen jedna strana
    kratky = P.norm_name(nazev.split(":")[0].split(" - ")[0])
    if kratky and kratky not in out and len(kratky.split()) >= 2:
        out.append(kratky)
    return out


def _s_podtitulem(n: str, mame: dict):
    """Tentyz titul, jen s podtitulem navic.

    Vimm pise "Street Fighter II Turbo", katalog "Street Fighter II Turbo:
    Hyper Fighting". Aby se ale "Final Fantasy" neparovalo na "Final Fantasy
    Tactics", musi jit o skutecny podtitul — dotaz musi mit aspon dve slova
    a v katalogu smi nasledovat jen jeden zaznam.
    """
    if len(n.split()) < 2:
        return None
    shody = [g for kn, g in mame.items() if kn.startswith(n + " ")]
    return shody[0] if len(shody) == 1 else None


def _pokryto_kompilaci(n: str, mame: dict) -> bool:
    """Je titul soucasti slouceneho zaznamu v katalogu?

    Nektere serie vedeme jako jednu polozku ("Sonic the Hedgehog 1-3"), takze
    jednotlive dily by se hlasily jako chybejici. Aby se ale "Sonic The
    Hedgehog" nenaparoval na "Sonic The Hedgehog 2", musi zaznam vypadat jako
    kompilace — obsahovat rozsah nebo spojku.
    """
    slova = set(n.split())
    if not slova:
        return False
    for kn, g in mame.items():
        if not re.search(r"[-–+/]|\band\b", g["name"].lower()):
            continue
        if slova and slova.issubset(set(kn.split())):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    work = Path(sys.argv[1])
    if not work.is_absolute():
        work = ROOT / work
    if "--report" in sys.argv:
        report(work)
    else:
        sber(work)
    return 0


if __name__ == "__main__":
    sys.exit(main())
