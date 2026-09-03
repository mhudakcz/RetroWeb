# -*- coding: utf-8 -*-
"""
Stahování obrázků:
  - platformy: lead foto konzole z anglické Wikipedie (REST summary)
  - hry:       boxarty z libretro-thumbnails (standard pro RetroArch/Batocera)

Výstup:
  public/images/platforms/<slug>.<ext>
  public/images/games/<platform-slug>/<game-slug>.png

Po stažení spusť znovu parser (parse_content.py) — ten cesty k obrázkům
zapíše do datasetu podle existence souborů.

Použití:
  python tools/fetch_images.py            # vše
  python tools/fetch_images.py platforms  # jen platformy
  python tools/fetch_images.py games      # jen hry
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P  # norm_name, match_metrics, acceptable, PLATFORMS

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa
    pass

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "images"
GH_TOKEN = os.environ.get("GH_TOKEN", "").strip()
UA = "RetroWeb-imagefetch/1.0 (personal retro gaming site)"

# ---- platforma -> anglická Wikipedie (lead foto konzole) ----
WIKI = {
    "game-boy": "Game Boy",
    "game-boy-color": "Game Boy Color",
    "game-boy-advance": "Game Boy Advance",
    "nds": "Nintendo DS",
    "3ds": "Nintendo 3DS",
    "nes": "Nintendo Entertainment System",
    "snes": "Super Nintendo Entertainment System",
    "mega-drive": "Sega Genesis",
    "master-system": "Master System",
    "game-gear": "Game Gear",
    "atari-lynx": "Atari Lynx",
    "saturn": "Sega Saturn",
    "playstation": "PlayStation (console)",
    "psp": "PlayStation Portable",
    "ps-vita": "PlayStation Vita",
    "n64": "Nintendo 64",
    "arcade": "Arcade cabinet",
    "pc-engine": "TurboGrafx-16",
    "dreamcast": "Dreamcast",
    "ps2": "PlayStation 2",
    "gamecube": "GameCube",
    "xbox": "Xbox (console)",
    "xbox-360": "Xbox 360",
    "ps3": "PlayStation 3",
    "ps4": "PlayStation 4",
    "xbox-one": "Xbox One",
    "switch": "Nintendo Switch",
    "zx-spectrum": "ZX Spectrum",
    "amstrad-cpc": "Amstrad CPC",
    "msx": "MSX",
    "colecovision": "ColecoVision",
    "atari-2600": "Atari 2600",
    "atari-8bit": "Atari 8-bit computers",
    "c64": "Commodore 64",
    "amiga": "Amiga",
    "game-watch": "Game & Watch",
    "pico-8": "Pico-8",
    "tic-80": "TIC-80",
    "neogeo": "Neo Geo (system)",
    "atari-5200": "Atari 5200",
    "atari-7800": "Atari 7800",
    "zx81": "ZX81",
    "vic20": "Commodore VIC-20",
    "atari-st": "Atari ST",
    "wii": "Wii",
    "wii-u": "Wii U",
    "ps5": "PlayStation 5",
    "xbox-series": "Xbox Series X and Series S",
    "switch-2": "Nintendo Switch 2",
    "mega-cd": "Sega CD",
    "sega-32x": "32X",
    "sg-1000": "SG-1000",
    "virtual-boy": "Virtual Boy",
    "ngpc": "Neo Geo Pocket Color",
    "wonderswan": "WonderSwan",
    "3do": "3DO Interactive Multiplayer",
    "cd-i": "CD-i",
    "vectrex": "Vectrex",
    "x68000": "X68000",
    "pc-98": "PC-9800 series",
    "vfx1": "VFX1 Headgear",
    "virtuality": "Virtuality (product)",
    "cardboard": "Google Cardboard",
    "pc-vr": "Oculus Rift",
    "psvr": "PlayStation VR",
    "psvr2": "PlayStation VR2",
    "quest": "Meta Quest 3",
    "pc-dos": "IBM Personal Computer",
    "pc-9x": "Pentium (original)",
    "pc-modern": "Gaming computer",
    "intellivision": "Intellivision",
    "jaguar": "Atari Jaguar",
    "amiga-cd32": "Amiga CD32",
}

# ---- platforma -> konkrétní soubor na Wikimedia Commons ----
# U některých platforem je v infoboxu článku LOGO, ne fotka konzole
# (Switch, Switch 2, Xbox Series, CD-i) — tady se pro ně snímek určuje ručně.
PLATFORM_PHOTO_FILE = {
    "switch": "Nintendo-Switch-Console-Docked-wJoyConRB.jpg",
    "switch-2": "Nintendo Switch 2 in Docking Console.jpg",
    # pozor: "Xbox Series XとSeries S.jpg" je fotka krabic v regálu, ne konzolí
    "xbox-series": "Xbox Series X mit Controller (transparent background).png",
    # puvodni snimek byl amatersky zaber na stole s kabely a zlutou stenou;
    # mezi produktovymi fotkami ostatnich platforem pusobil cize
    "cd-i": "CD-i-910-Console-Set.png",
    # v infoboxu článku je logo WonderSwanu, ne konzole
    "wonderswan": "WonderSwan-Color-Blue-Left.png",
    # clanek o Quest ma nesvobodny produktovy snimek; tenhle je na Commons
    "quest": "Meta Quest 3 front View.jpg",
    # infobox clanku dava snimek s obrazovkou; tenhle je cely set na zelenem platne
    "psvr2": "PSVR2 (Non-Stereoscopic).png",
    # původní snímek měl vedle černého Xboxu i BÍLÝ Xbox One S, kterému
    # odmazávání pozadí vykouslo hranu (bílá konzole splývá s bílým podkladem);
    # tenhle je jen černý hardware a už s průhledností
    "xbox-one": "Microsoft-Xbox-One-Console-wKinect.png",
}

# Platformy, u kterých se pozadí NESMÍ odmazávat — produkt je sám bílý,
# takže výplň od okraje by se prokousala do konzole.
PLATFORM_TRIM_SKIP = {"xbox-one", "wii", "dreamcast", "wii-u", "atari-7800"}

# Fotky nafocene na zelenem platne (chroma key). Bily prah je na ne slepy, tak
# se u nich misto "skoro bila" hleda "vyrazne zelena" a nakonec se odstrani
# zeleny nadech, ktery plátno vrha na okraje produktu.
PLATFORM_CHROMA = {"psvr2"}

# Vyjimky z globalniho prahu. Kdyz je produkt cely tmavy, snese se prah mnohem
# nize a odmaze i sedive studiove pozadi, ktere by jinak zustalo jako svetly
# obdelnik. Naopak u svetleho produktu je nizky prah nebezpecny.
PLATFORM_TRIM_THRESH = {"vfx1": 160}

# ---- platforma -> libretro-thumbnails repo (boxarty) ----
LIBRETRO = {
    "game-boy": "Nintendo_-_Game_Boy",
    "game-boy-color": "Nintendo_-_Game_Boy_Color",
    "game-boy-advance": "Nintendo_-_Game_Boy_Advance",
    "nds": "Nintendo_-_Nintendo_DS",
    "3ds": "Nintendo_-_Nintendo_3DS",
    "nes": "Nintendo_-_Nintendo_Entertainment_System",
    "snes": "Nintendo_-_Super_Nintendo_Entertainment_System",
    "mega-drive": "Sega_-_Mega_Drive_-_Genesis",
    "master-system": "Sega_-_Master_System_-_Mark_III",
    "game-gear": "Sega_-_Game_Gear",
    "atari-lynx": "Atari_-_Lynx",
    "saturn": "Sega_-_Saturn",
    "playstation": "Sony_-_PlayStation",
    "psp": "Sony_-_PlayStation_Portable",
    "ps-vita": "Sony_-_PlayStation_Vita",
    "n64": "Nintendo_-_Nintendo_64",
    "arcade": "MAME",
    "pc-engine": "NEC_-_PC_Engine_-_TurboGrafx_16",
    "dreamcast": "Sega_-_Dreamcast",
    "ps2": "Sony_-_PlayStation_2",
    "gamecube": "Nintendo_-_GameCube",
    "xbox": "Microsoft_-_Xbox",
    "xbox-360": "Microsoft_-_Xbox_360",
    "ps3": "Sony_-_PlayStation_3",
    "ps4": "Sony_-_PlayStation_4",
    "xbox-one": "Microsoft_-_Xbox_One",
    "switch": "Nintendo_-_Nintendo_Switch",
    "zx-spectrum": "Sinclair_-_ZX_Spectrum",
    "amstrad-cpc": "Amstrad_-_CPC",
    "msx": "Microsoft_-_MSX",
    "colecovision": "Coleco_-_ColecoVision",
    "atari-2600": "Atari_-_2600",
    "atari-8bit": "Atari_-_8-bit",
    "c64": "Commodore_-_64",
    "amiga": "Commodore_-_Amiga",
    "neogeo": "SNK_-_Neo_Geo",
    "cps": "MAME",
    "atari-5200": "Atari_-_5200",
    "atari-7800": "Atari_-_7800",
    "zx81": "Sinclair_-_ZX81",
    "vic20": "Commodore_-_VIC-20",
    "atari-st": "Atari_-_ST",
    "wii": "Nintendo_-_Wii",
    "wii-u": "Nintendo_-_Wii_U",
    "mega-cd": "Sega_-_Mega-CD_-_Sega_CD",
    "sega-32x": "Sega_-_32X",
    "sg-1000": "Sega_-_SG-1000",
    "virtual-boy": "Nintendo_-_Virtual_Boy",
    "ngpc": "SNK_-_Neo_Geo_Pocket_Color",
    "wonderswan": "Bandai_-_WonderSwan_Color",
    "3do": "The_3DO_Company_-_3DO",
    "cd-i": "Philips_-_CD-i",
    "vectrex": "GCE_-_Vectrex",
    "x68000": "Sharp_-_X68000",
    "pc-98": "NEC_-_PC-98",
    "pc-dos": "DOS",
    # Windows 9x samostatny repozitar nema, ale rada titulu te doby vysla i pro
    # DOS (Quake, Tomb Raider, Carmageddon), takze se obaly hledaji tam. Parovani
    # je na presny nazev, takze se netrefi do nespravne hry.
    "pc-9x": "DOS",
    # Forte VFX1 byl headset pro DOSove PC — vsechny hry na nem jsou DOSove
    # tituly (Descent, Doom, System Shock), takze obaly i snimky sedi tamtez.
    "vfx1": "DOS",
    "intellivision": "Mattel_-_Intellivision",
    "jaguar": "Atari_-_Jaguar",
    "amiga-cd32": "Commodore_-_Amiga",
    # game-watch / pico-8 / tic-80: bez libretro boxartů -> emblém zůstane
}

# regiony, které preferujeme při výběru z více variant boxartu
REGION_PREF = ["(USA)", "(World)", "(USA, Europe)", "(Europe)", "(Japan, USA)", "(Japan)"]


def http_get(url, headers=None, retries=3, timeout=40):
    """Stažení přes curl (používá Windows cert store; Python urllib má prošlý CA bundle)."""
    # --ssl-no-revoke: Windows schannel jinak padá na CRYPT_E_NO_REVOCATION_CHECK,
    # když je revocation server (CRL/OCSP) nedostupný (firemní síť)
    cmd = ["curl", "-sL", "--fail", "--ssl-no-revoke", "--max-time", str(timeout), "-A", UA]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    cmd.append(url)
    last = None
    for i in range(retries):
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout
        last = r.stderr.decode("utf-8", "replace").strip() or f"curl exit {r.returncode}"
        time.sleep(1.2 * (i + 1))
    raise RuntimeError(last)


def gh_api(path):
    headers = {"Accept": "application/vnd.github+json"}
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"
    return json.loads(http_get("https://api.github.com" + path, headers=headers))


# ----------------------------------------------------------------- platformy
def wiki_image(title):
    """Lead image z MediaWiki API jako thumbnail ~960px (malý, neškrcený)."""
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "pageimages",
            "piprop": "thumbnail|original",
            "pithumbsize": "960",
            "redirects": "1",
        }
    )
    data = json.loads(http_get("https://en.wikipedia.org/w/api.php?" + q))
    for p in data.get("query", {}).get("pages", {}).values():
        thumb = (p.get("thumbnail") or {}).get("source")
        orig = (p.get("original") or {}).get("source")
        if thumb:
            return thumb
        if orig:
            return orig
    return None


def fetch_platforms():
    out = IMG / "platforms"
    out.mkdir(parents=True, exist_ok=True)
    ok = 0
    for slug, title in WIKI.items():
        existing = [f for f in out.glob(f"{slug}.*") if f.stat().st_size > 8192]
        if existing:
            ok += 1
            print(f"  [skip] {existing[0].name} už existuje")
            continue
        try:
            # Wikimedia při rychlé sérii dotazů začne odmítat stahování obrázků
            time.sleep(1.0)
            # u platforem, kde je v infoboxu logo místo konzole, bereme
            # ručně určený snímek z Commons (viz PLATFORM_PHOTO_FILE)
            override = PLATFORM_PHOTO_FILE.get(slug)
            src = _wiki_file_url(override, width=1200) if override else wiki_image(title)
            if not src:
                print(f"  [-] {slug}: bez obrazku ({title})")
                continue
            ext = os.path.splitext(urllib.parse.urlparse(src).path)[1].lower()
            if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                ext = ".jpg"
            img = http_get(src)
            # smazat případnou starou variantu s jinou příponou
            for old in out.glob(f"{slug}.*"):
                old.unlink()
            (out / f"{slug}{ext}").write_bytes(img)
            ok += 1
            print(f"  [OK] {slug}{ext}  ({len(img)//1024} kB)  <- {title}")
            time.sleep(0.2)
        except Exception as e:  # noqa
            print(f"  [x] {slug}: {e}")
    print(f"Platformy: stazeno {ok}/{len(WIKI)}")


# --------------------------------------------------- doprovodné fotky do článků
import re as _re

# soubory, které nechceme (ikony, loga wiki, mapy, zvuky, vlajky, diagramy…)
_JUNK_RE = _re.compile(
    r"commons-logo|wiki|edit-?clear|disambig|ambox|question|nuvola|"
    r"speaker|sound|\.ogg|\.oga|\.webm|\.mid|flag_of|map_of|locator|"
    r"padlock|symbol|oojs|red[_-]?x|increase|decrease|steady|"
    r"crystal|gnome|emblem|folder|text-x|pictogram|chart|diagram|"
    r"\.svg$",
    _re.I,
)


def _strip_html(s):
    return _re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", "", s or "")).strip()


def wiki_article_images(title, limit=60):
    """Vrátí seznam fotek použitých na wiki stránce: [{src,name,w,h,desc}]."""
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "titles": title,
            "redirects": "1",
            "generator": "images",
            "gimlimit": str(limit),
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": "760",  # vyžádej zmenšený thumbnail (originály Wikimedia blokuje/omezuje)
        }
    )
    data = json.loads(http_get("https://en.wikipedia.org/w/api.php?" + q))
    out = []
    for p in data.get("query", {}).get("pages", {}).values():
        info = (p.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        if mime not in ("image/jpeg", "image/png"):
            continue
        name = p.get("title", "").replace("File:", "")
        if _JUNK_RE.search(name):
            continue
        w, h = info.get("width", 0), info.get("height", 0)
        if w < 400 or h < 300:  # vyřaď ikonky / proužky
            continue
        meta = info.get("extmetadata", {})
        desc = _strip_html(meta.get("ImageDescription", {}).get("value", ""))
        obj = _strip_html(meta.get("ObjectName", {}).get("value", ""))
        # thumbnail URL ~900px přes Special:FilePath nebo přímý url se zmenší v optimize
        out.append(
            {
                "src": info.get("thumburl") or info.get("url"),
                "name": name,
                "w": w,
                "h": h,
                "desc": desc[:300] or obj[:120],
            }
        )
    # největší (=nejdůležitější) první
    out.sort(key=lambda x: x["w"] * x["h"], reverse=True)
    return out


def fetch_article_photos(per_platform=6):
    """Stáhne kandidátní doprovodné fotky z wiki článků platforem + manifest."""
    from PIL import Image
    import io

    base = IMG / "platforms" / "extra"
    base.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for slug, title in WIKI.items():
        try:
            cand = wiki_article_images(title)
        except Exception as e:  # noqa
            print(f"  [x] {slug}: {e}")
            continue
        outdir = base / slug
        outdir.mkdir(exist_ok=True)
        kept = []
        idx = 0
        for c in cand:
            if idx >= per_platform:
                break
            dest = outdir / f"{idx + 1}.webp"
            try:
                if not dest.exists():
                    raw = http_get(c["src"])
                    im = Image.open(io.BytesIO(raw))
                    im.thumbnail((760, 760), Image.LANCZOS)
                    if im.mode not in ("RGB", "RGBA"):
                        im = im.convert("RGB")
                    im.save(dest, "WEBP", quality=82, method=6)
                kept.append(
                    {
                        "file": f"/images/platforms/extra/{slug}/{idx + 1}.webp",
                        "src_name": c["name"],
                        "desc": c["desc"],
                    }
                )
                idx += 1
                time.sleep(0.15)
            except Exception as e:  # noqa
                print(f"    [skip] {slug} {c['name']}: {e}")
        manifest[slug] = kept
        print(f"  [OK] {slug}: {len(kept)} fotek")
    (ROOT / "tools" / "_article_photos.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Manifest: tools/_article_photos.json ({sum(len(v) for v in manifest.values())} fotek)")


# ----------------------------------------------------------------- hry
def list_boxarts(repo, folder="Named_Boxarts"):
    """Vrátí list názvů souborů (bez .png) ve zvolené složce daného repa."""
    for branch in ("master", "main"):
        # zkus rekurzivní strom
        try:
            tree = gh_api(f"/repos/libretro-thumbnails/{repo}/git/trees/{branch}?recursive=1")
            if not tree.get("truncated"):
                files = [
                    os.path.basename(t["path"])[:-4]
                    for t in tree.get("tree", [])
                    if t["path"].startswith(folder + "/") and t["path"].endswith(".png")
                ]
                if files:
                    return files
        except Exception:  # noqa
            pass
        # fallback: root -> <folder> sha -> jeho strom
        try:
            root = gh_api(f"/repos/libretro-thumbnails/{repo}/git/trees/{branch}")
            sha = next(
                (t["sha"] for t in root.get("tree", []) if t["path"] == folder), None
            )
            if sha:
                sub = gh_api(f"/repos/libretro-thumbnails/{repo}/git/trees/{sha}")
                files = [t["path"][:-4] for t in sub.get("tree", []) if t["path"].endswith(".png")]
                if files:
                    return files
        except Exception:  # noqa
            pass
    return []


def region_rank(fname):
    for i, r in enumerate(REGION_PREF):
        if r in fname:
            return i
    return len(REGION_PREF)


def index_boxarts(names):
    """norm_name -> nejlepší originální filename (dle preference regionu)."""
    idx = {}
    for n in names:
        key = P.norm_name(n)
        if not key:
            continue
        if key not in idx or region_rank(n) < region_rank(idx[key]):
            idx[key] = n
    return idx


# Poradova cisla dilu — rimska i arabska. Vic nez X se v nazvech her prakticky
# nevyskytuje a "i" se vynechava zamerne, protoze prvni dil se cislem neoznacuje.
_SEQUEL = {"ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
           "2", "3", "4", "5", "6", "7", "8", "9", "10"}


def _plausible_match(query, candidate):
    """Zamitne kandidata, ktery je proti dotazu nesmyslne kratky.

    Metrika dava vysoke skore i jednopismennym nazvum: hra "D (Europe) (Disc 1)"
    se normalizuje na pouhe "d" a proti "Tomb Raider II" dostane 0.93, tedy nad
    prahem. Kazda hra, ktera se nenapárovala presne, tak skoncila u "D" — na
    PlayStationu takhle deset titulu dostalo tentyz screenshot.

    Kandidat proto musi mit aspon polovicni delku dotazu a sdilet s nim aspon
    jedno slovo delsi nez dva znaky.
    """
    q, c = P.norm_name(query), P.norm_name(candidate)
    if not q or not c or len(c) < len(q) * 0.5:
        return False
    # KAZDE vyznamne slovo dotazu musi byt i v kandidatovi. Bez toho se
    # podnazev, ktery hry odlisuje, proste ignoruje: "Wing Commander: Prophecy"
    # se napároval na "Wing Commander (1990)", tedy na uplne jinou hru.
    # Naopak slova navic u kandidata vadit nemuzou — jsou to regionalni znacky
    # a cisla disku, "Doom (USA) (Rev 1)".
    # Prah ctyr znaku vynechava spojky: repozitar pise "&" jako "_", takze
    # "Command & Conquer" by jinak vzdy propadlo na chybejicim "and".
    qt = {w for w in q.split() if len(w) >= 4}
    ct = set(c.split())
    if qt and not qt.issubset(ct):
        return False
    # Poradove cislo dilu musi sedet. Repozitar PlayStationu nema Tomb Raider II
    # ani III, takze obe hry jinak spadnou na jednicku — a stejne tak by Doom II
    # dostal obal Doomu.
    qn = {w for w in q.split() if w in _SEQUEL}
    if qn and not (qn & {w for w in c.split() if w in _SEQUEL}):
        return False
    return True


def best_boxart(game_name, names, idx):
    key = P.norm_name(game_name)
    if key in idx:
        return idx[key]
    # fuzzy přes všechny názvy
    best, best_sc = None, 0.0
    for n in names:
        sc = P.match_metrics(game_name, n)[0]
        if sc > best_sc and _plausible_match(game_name, n):
            best_sc, best = sc, n
    if best and best_sc >= 0.78 and P.acceptable(game_name, best):
        return best
    return None


def fetch_games(only=None):
    """only: čárkou oddělené slugy platforem — omezí stahování jen na ně."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    plat_games = {p["slug"]: p["games"] for p in dataset["platforms"]}
    wanted = set(only.split(",")) if only else None

    grand_total = grand_ok = 0
    for slug, repo in LIBRETRO.items():
        if wanted and slug not in wanted:
            continue
        games = plat_games.get(slug, [])
        if not games:
            continue
        print(f"\n== {slug}  ({repo}) ==")
        try:
            names = list_boxarts(repo)
        except Exception as e:  # noqa
            print(f"  CHYBA seznamu boxartů: {e}")
            continue
        if not names:
            print("  žádné boxarty")
            continue
        idx = index_boxarts(names)
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)

        # napáruj
        raw_jobs = []
        for g in games:
            fn = best_boxart(g["name"], names, idx)
            if fn:
                raw_jobs.append((g["slug"], fn))
        # pojistka proti falešným shodám: když jeden boxart sedne na VÍC her,
        # je to nespolehlivá fuzzy shoda -> nepřiřazuj ho žádné z nich.
        from collections import Counter as _C
        fn_count = _C(fn for _, fn in raw_jobs)
        jobs = [(s, fn) for s, fn in raw_jobs if fn_count[fn] == 1]
        dropped = len(raw_jobs) - len(jobs)
        if dropped:
            print(f"  [pojistka] zahozeno {dropped} her sdílejících boxart (falešná shoda)")
        grand_total += len(games)

        def dl(job):
            gslug, fn = job
            dest = out / f"{gslug}.png"
            if (out / f"{gslug}.webp").exists() or (dest.exists() and dest.stat().st_size > 2048):
                return True  # už staženo (png nebo už převedené na webp)
            url = (
                f"https://raw.githubusercontent.com/libretro-thumbnails/{repo}"
                f"/master/Named_Boxarts/{urllib.parse.quote(fn)}.png"
            )
            try:
                img = http_get(url)
                (out / f"{gslug}.png").write_bytes(img)
                return True
            except Exception:  # noqa
                return False

        ok = 0
        with ThreadPoolExecutor(max_workers=10) as ex:
            for r in ex.map(dl, jobs):
                if r:
                    ok += 1
        grand_ok += ok
        print(f"  napárováno {len(jobs)}/{len(games)}, staženo {ok}")
    print(f"\nHry celkem: staženo {grand_ok} obrázků z {grand_total} her "
          f"({100*grand_ok//max(1,grand_total)} %)")


def fetch_screenshots(only=None):
    """Stáhne in-game screenshot (Named_Snaps) a title screen (Named_Titles) pro hry,
    které mají boxart. Stejné názvy souborů jako boxarty. Ukládá jako <slug>-snap.png / -title.png.
    only: pokud zadáno, omezí se jen na tuto platformu (slug)."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    plat_games = {p["slug"]: p["games"] for p in dataset["platforms"]}
    wanted = set(only.split(",")) if only else None
    grand = {"snap": 0, "title": 0}
    for slug, repo in LIBRETRO.items():
        if wanted and slug not in wanted:
            continue
        games = plat_games.get(slug, [])
        if not games:
            continue
        print(f"\n== {slug} ({repo}) ==")
        try:
            names = list_boxarts(repo)
        except Exception as e:  # noqa
            print(f"  CHYBA: {e}")
            continue
        if not names:
            continue
        idx = index_boxarts(names)
        out = IMG / "games" / slug
        jobs = []
        for g in games:
            fn = best_boxart(g["name"], names, idx)
            if fn:
                jobs.append((g["slug"], fn))

        def dl(job):
            gslug, fn = job
            got = 0
            for kind, folder in (("snap", "Named_Snaps"), ("title", "Named_Titles")):
                dest = out / f"{gslug}-{kind}.png"
                destw = out / f"{gslug}-{kind}.webp"
                if dest.exists() or destw.exists():
                    got += 1
                    continue
                url = (
                    f"https://raw.githubusercontent.com/libretro-thumbnails/{repo}"
                    f"/master/{folder}/{urllib.parse.quote(fn)}.png"
                )
                try:
                    img = http_get(url, retries=2)
                    # symlink? obsah je krátký text s názvem cílového .png
                    if len(img) < 300:
                        try:
                            tgt = img.decode("utf-8", "strict").strip()
                        except Exception:  # noqa
                            tgt = ""
                        if tgt.lower().endswith(".png") and "\n" not in tgt:
                            url2 = (
                                f"https://raw.githubusercontent.com/libretro-thumbnails/{repo}"
                                f"/master/{folder}/{urllib.parse.quote(tgt[:-4])}.png"
                            )
                            img = http_get(url2, retries=2)
                    dest.write_bytes(img)
                    got += 1
                except Exception:  # noqa
                    pass
            return got

        with ThreadPoolExecutor(max_workers=10) as ex:
            list(ex.map(dl, jobs))
        snaps = len(list(out.glob("*-snap.*")))
        titles = len(list(out.glob("*-title.*")))
        grand["snap"] += snaps
        grand["title"] += titles
        print(f"  snap {snaps}, title {titles} (z {len(jobs)} her)")
    print(f"\nCelkem: snap {grand['snap']}, title {grand['title']}")


def _dl_shot(repo, folder, fn, dest):
    """Stáhne jeden screenshot (s ošetřením symlinku) z daného repa/složky."""
    url = (
        f"https://raw.githubusercontent.com/libretro-thumbnails/{repo}"
        f"/master/{folder}/{urllib.parse.quote(fn)}.png"
    )
    img = http_get(url, retries=2)
    if len(img) < 300:  # možný symlink (text s cílovým názvem)
        try:
            tgt = img.decode("utf-8", "strict").strip()
        except Exception:  # noqa
            tgt = ""
        if tgt.lower().endswith(".png") and "\n" not in tgt:
            url2 = (
                f"https://raw.githubusercontent.com/libretro-thumbnails/{repo}"
                f"/master/{folder}/{urllib.parse.quote(tgt[:-4])}.png"
            )
            img = http_get(url2, retries=2)
    dest.write_bytes(img)


def fetch_fallback_shots(only=None):
    """Pro hry BEZ obalu zkusí napárovat titulní obrazovku (Named_Titles), případně
    in-game snímek (Named_Snaps) — páruje přímo proti jejich názvům (jiná konvence než
    obaly) a uloží jako <slug>-title.png / -snap.png. Parser je pak použije jako hlavní
    obrázek (image = obal || title || snap). 'only' = omez na jednu platformu."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    plat_games = {p["slug"]: p["games"] for p in dataset["platforms"]}
    wanted = set(only.split(",")) if only else None
    grand = 0
    for slug, repo in LIBRETRO.items():
        if wanted and slug not in wanted:
            continue
        games = plat_games.get(slug, [])
        # jen hry, které zatím nemají žádný obrázek (image je None v datasetu)
        need = [g for g in games if not g.get("image")]
        if not need:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        # hry, které navíc ještě nemají ani title/snap soubor
        need = [
            g for g in need
            if not list(out.glob(f"{g['slug']}-title.*")) and not list(out.glob(f"{g['slug']}-snap.*"))
        ]
        if not need:
            continue
        print(f"\n== {slug} ({repo}) — bez obalu: {len(need)} ==")
        recovered = 0
        for folder, suffix in (("Named_Titles", "title"), ("Named_Snaps", "snap")):
            if not need:
                break
            try:
                names = list_boxarts(repo, folder)
            except Exception as e:  # noqa
                print(f"  CHYBA {folder}: {e}")
                continue
            if not names:
                continue
            idx = index_boxarts(names)
            still = []
            for g in need:
                fn = best_boxart(g["name"], names, idx)
                if not fn:
                    still.append(g)
                    continue
                dest = out / f"{g['slug']}-{suffix}.png"
                try:
                    _dl_shot(repo, folder, fn, dest)
                    recovered += 1
                    print(f"  [OK] {g['name']}  <- {folder}/{fn}")
                    time.sleep(0.1)
                except Exception as e:  # noqa
                    print(f"  [x] {g['name']}: {e}")
                    still.append(g)
            need = still  # zbylé zkus z dalšího foldera (Named_Snaps)
        grand += recovered
        print(f"  získáno {recovered}, stále bez obrázku: {len(need)}")
    print(f"\nCelkem dohledáno fallback obrázků: {grand}")


def resolve_symlinks():
    """Některé položky v libretro repech jsou symlinky: stažený 'soubor' obsahuje
    jen cílový název .png. Dořeší je: stáhne skutečný obrázek a převede na WebP."""
    from PIL import Image

    gdir = IMG / "games"
    leftovers = list(gdir.rglob("*.png"))
    print(f"Symlink kandidátů (.png): {len(leftovers)}")
    fixed = dropped = 0
    for p in leftovers:
        # reálné obrázky (velké soubory) nech být – převede je optimize. Symlink je krátký text.
        if p.stat().st_size >= 1024:
            continue
        slug = p.parent.name
        repo = LIBRETRO.get(slug)
        try:
            target = p.read_text("utf-8", "replace").strip()
        except Exception:  # noqa
            target = ""
        # je to vážně symlink (krátký text končící .png)?
        if repo and target.lower().endswith(".png") and len(target) < 250 and "\n" not in target:
            tgt = target[:-4]
            url = (
                f"https://raw.githubusercontent.com/libretro-thumbnails/{repo}"
                f"/master/Named_Boxarts/{urllib.parse.quote(tgt)}.png"
            )
            try:
                img = http_get(url)
                tmp = p.with_suffix(".tmp")
                tmp.write_bytes(img)
                im = Image.open(tmp)
                im.thumbnail((480, 480), Image.LANCZOS)
                if im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGBA")
                im.save(p.with_suffix(".webp"), "WEBP", quality=80, method=6)
                tmp.unlink()
                p.unlink()
                fixed += 1
                continue
            except Exception as e:  # noqa
                print(f"  [x] {p.name} -> {target}: {e}")
        # nepodařilo se / není symlink -> zahodit vadný soubor
        p.unlink()
        dropped += 1
    print(f"Symlinky: opraveno {fixed}, zahozeno {dropped}")


def classify_platform_bg():
    """Rozliší fotky platforem: průhledný výřez / tmavé pozadí -> 'dark' (na tmavé kartě),
    světlé (bílé) pozadí -> 'light' (zobrazí se na světlé produktové kartě).
    Výsledek: src/data/platform_bg.json {slug: 'light'|'dark'}."""
    from PIL import Image
    pdir = IMG / "platforms"
    res = {}
    for p in sorted(pdir.iterdir()):
        slug = p.stem
        try:
            im = Image.open(p).convert("RGBA")
        except Exception:  # noqa
            continue
        w, h = im.size
        px = im.load()
        # vzorkuj okrajový prstenec
        step_x = max(1, w // 40)
        step_y = max(1, h // 40)
        coords = []
        for x in range(0, w, step_x):
            coords += [(x, 0), (x, h - 1)]
        for y in range(0, h, step_y):
            coords += [(0, y), (w - 1, y)]
        transp = 0
        bright = 0
        n = 0
        for (x, y) in coords:
            r, g, b, a = px[x, y]
            n += 1
            if a < 32:
                transp += 1
            elif (r + g + b) / 3 > 205:
                bright += 1
        if n == 0:
            res[slug] = "dark"
            continue
        # hodně průhledných okrajů -> výřez (dark karta sedí)
        if transp / n > 0.4:
            res[slug] = "dark"
        # převážně světlé neprůhledné okraje -> bílé pozadí
        elif bright / n > 0.6:
            res[slug] = "light"
        else:
            res[slug] = "dark"
    (ROOT / "src" / "data" / "platform_bg.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    light = [k for k, v in res.items() if v == "light"]
    print(f"Klasifikace: {len(res)} platforem, světlé pozadí: {light}")


def optimize_images():
    """Zmenší a překomprimuje obrázky pro web. Hry -> WebP ~480px; platformy -> max 900px."""
    from PIL import Image

    # --- hry: PNG/JPG -> WebP 480px ---
    # JPG sem chodi ze Steamu a Nintendo eShopu (obaly i snimky ze hry, klidne 1920px),
    # takze bez teto konverze by v repu lezely stovky MB.
    gdir = IMG / "games"
    srcs = [f for ext in ("*.png", "*.jpg", "*.jpeg") for f in gdir.rglob(ext)]
    before = sum(p.stat().st_size for p in srcs)
    conv = 0
    for p in srcs:
        try:
            im = Image.open(p)
            im.thumbnail((480, 480), Image.LANCZOS)
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA")
            if im.mode == "RGBA" and p.suffix.lower() != ".png":
                im = im.convert("RGB")
            webp = p.with_suffix(".webp")
            im.save(webp, "WEBP", quality=80, method=6)
            p.unlink()
            conv += 1
        except Exception as e:  # noqa
            print(f"  [x] {p.name}: {e}")
    after = sum(f.stat().st_size for f in gdir.rglob("*.webp"))
    print(f"Hry: {conv} obrázků -> WebP, {before//1024//1024} MB -> {after//1024//1024} MB")

    # --- platformy: zmenšit na 900 px a převést na WebP (mimo gif kvůli animaci) ---
    # PNG s průhledností jsou u fotek konzolí těžké (i 350 kB); WebP umí alfu taky
    # a je řádově menší, což se u deploye celého webu sečte.
    pdir = IMG / "platforms"
    pcount = pconv = 0
    pbefore = pafter = 0
    for p in list(pdir.iterdir()):
        if not p.is_file() or p.suffix.lower() == ".gif":
            continue
        try:
            before = p.stat().st_size
            im = Image.open(p)
            resized = False
            if max(im.size) > 900:
                im.thumbnail((900, 900), Image.LANCZOS)
                resized = True
            if p.suffix.lower() == ".webp":
                if resized:
                    im.save(p, "WEBP", quality=86, method=6)
                    pcount += 1
                continue
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA")
            webp = p.with_suffix(".webp")
            im.save(webp, "WEBP", quality=86, method=6)
            p.unlink()
            pconv += 1
            pbefore += before
            pafter += webp.stat().st_size
        except Exception as e:  # noqa
            print(f"  [x] {p.name}: {e}")
    msg = f"Platformy: zmenšeno {pcount}"
    if pconv:
        msg += (f", {pconv} převedeno na WebP "
                f"({pbefore // 1024 // 1024} MB -> {pafter // 1024 // 1024} MB)")
    print(msg)


def _wiki_search(query, limit=4):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "list": "search",
        "srsearch": query, "srlimit": limit, "srnamespace": 0,
    })
    try:
        data = json.loads(http_get("https://en.wikipedia.org/w/api.php?" + q))
    except Exception:  # noqa
        return []
    return [h["title"] for h in data.get("query", {}).get("search", [])]


def _wiki_is_videogame(title):
    """Ověř, že stránka je o videohře (kategorie obsahují 'video game(s)')."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": title,
        "prop": "categories", "cllimit": "100", "clshow": "!hidden", "redirects": "1",
    })
    try:
        data = json.loads(http_get("https://en.wikipedia.org/w/api.php?" + q))
    except Exception:  # noqa
        return False
    for p in data.get("query", {}).get("pages", {}).values():
        cats = " ".join(c.get("title", "").lower() for c in p.get("categories", []))
        if "video game" in cats:
            return True
    return False


def fetch_games_wiki(only=None):
    """Pro hry BEZ obrázku zkus lead foto (obal/screenshot) z anglické Wikipedie.
    Přísné ověření (kategorie 'video game' + překryv názvu) proti falešným shodám."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    ok = 0
    total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        missing = [g for g in plat["games"] if not g.get("image")]
        if not missing:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"\n== {slug} — bez obrázku: {len(missing)} ==")
        for g in missing:
            total += 1
            # název bez závorkových přípon typu (CD), (MD port), -ish
            base = P.re.sub(r"\([^)]*\)", " ", g["name"])
            base = base.replace(" -ish", "").replace("/", " ").strip()
            base = P.re.split(r"\s+[–—]\s+", base)[0].strip()
            gtoks = P.tokens(base)
            queries = [f"{base} video game", f"{base} {plat['short']} video game"]
            picked = None
            for query in queries:
                for title in _wiki_search(query):
                    ttoks = P.tokens(title)
                    jac = len(gtoks & ttoks) / len(gtoks | ttoks) if (gtoks and ttoks) else 0
                    if jac < 0.45:
                        continue
                    if not _wiki_is_videogame(title):
                        continue
                    picked = title
                    break
                if picked:
                    break
            if not picked:
                print(f"  [-] {g['name']}")
                continue
            try:
                src = wiki_image(picked)
                if not src:
                    print(f"  [-] {g['name']} (bez foto: {picked})")
                    continue
                img = http_get(src)
                if len(img) < 3000:
                    print(f"  [-] {g['name']} (maly soubor)")
                    continue
                (out / f"{g['slug']}.png").write_bytes(img)
                ok += 1
                print(f"  [OK] {g['name']}  <- WP:{picked}")
                time.sleep(0.15)
            except Exception as e:  # noqa
                print(f"  [x] {g['name']}: {e}")
    print(f"\nWikipedia: dohledáno {ok}/{total} obrázků")


_ITCH_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# itch.io dává smysl jen tam, kde je katalog opravdu z itch.io / homebrew scény.
# Na komerčních konzolích vrací shoda názvu cizí fan-game (viz fetch_games_itch).
GOG_OK = {"pc-dos", "pc-9x", "pc-modern", "web", "mobil"}  # GOG vede jen verze pro PC
ITCH_OK = {"pico-8", "tic-80", "game-watch", "web"}  # web: rada prohlizecovek zije na itch.io

# Steam se smi pouzivat jen pro platformy od roku 2000. U starsich to nefunguje:
# Steam vraci datum vydani NA STEAMU, ne originalni (DOOM + DOOM II ma na Steamu
# rok 2007, i kdyz hra je z 1993), takze rok nejde pouzit k overeni. Shoda podle
# nazvu pak u kazde stare hry s modernim rebootem sedne na ten reboot — DOS Doom
# z roku 1993 takhle dostal screenshoty z DOOMa 2016. Retro platformy maji libretro.
STEAM_MIN_PLATFORM_YEAR = 2000


def _itch_search(name):
    """Vrátí list (title, url) z itch.io vyhledávání."""
    url = "https://itch.io/search?" + urllib.parse.urlencode({"q": name})
    try:
        html = http_get(url, headers={"User-Agent": _ITCH_UA}).decode("utf-8", "replace")
    except Exception:  # noqa
        return []
    pat = P.re.compile(r'<a class="title game_link"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>')
    return [(P.re.sub(r"&amp;", "&", t).strip(), u) for u, t in pat.findall(html)]


def _itch_cover(page_url):
    try:
        html = http_get(page_url, headers={"User-Agent": _ITCH_UA}).decode("utf-8", "replace")
    except Exception:  # noqa
        return None
    m = P.re.search(r'og:image"\s+content="([^"]+)"', html)
    if not m:
        m = P.re.search(r'content="([^"]+)"\s+property="og:image"', html)
    return m.group(1) if m else None


def fetch_games_itch(only=None):
    """Pro hry BEZ obrázku zkus oficiální cover z itch.io (homebrew/indie).
    Přísné párování názvu (containment / jaccard >= 0.6) proti falešným shodám.

    JEN pro homebrew platformy (ITCH_OK). Na komerčních konzolích se shoda názvu
    trefí do úplně jiné hry — na itch.io existuje fan-game nebo stolní RPG stejného
    jména („Bulletstorm", „The Last of Us", „Journey", „ARMS"), takže i přesná shoda
    názvu vrátí cizí obrázek."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    if wanted:
        skip = wanted - ITCH_OK
        if skip:
            print(f"  [!] itch.io přeskakuje komerční platformy: {', '.join(sorted(skip))}")
        wanted &= ITCH_OK
        if not wanted:
            print("  itch.io: žádná z uvedených platforem není homebrew — nic k dělání")
            return
    else:
        wanted = set(ITCH_OK)
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        missing = [g for g in plat["games"] if not g.get("image")]
        if not missing:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"\n== {slug} — bez obrázku: {len(missing)} ==")
        for g in missing:
            total += 1
            time.sleep(0.6)  # šetrně k itch.io (jinak throttling)
            base = P.re.sub(r"\([^)]*\)", " ", g["name"])
            base = base.split(" -ish")[0].split(" / ")[0].strip()
            gnorm = P.norm_name(base)
            gtoks = P.tokens(base)
            if len(gnorm) < 3:
                continue
            picked = None
            # povolené „verzní" přípony za shodným názvem (jinak striktní shoda)
            SUFFIX_OK = {"md", "dx", "hd", "demo", "deluxe", "remaster", "remastered",
                         "version", "windows", "win", "edition", "port", "64", "plus",
                         "gold", "complete", "gb", "gbc", "gba", "nes", "snes", "pc"}
            for title, url in _itch_search(base)[:6]:
                tnorm = P.norm_name(title)
                if not gnorm or not tnorm:
                    continue
                accept = False
                if gnorm == tnorm:
                    accept = True
                elif tnorm.startswith(gnorm + " "):
                    extra = tnorm[len(gnorm) + 1:].split()
                    accept = all(w in SUFFIX_OK for w in extra)
                if accept:
                    picked = url
                    break
            if not picked:
                print(f"  [-] {g['name']}")
                continue
            src = _itch_cover(picked)
            if not src:
                print(f"  [-] {g['name']} (bez og:image)")
                continue
            try:
                img = http_get(src, headers={"User-Agent": _ITCH_UA})
                if len(img) < 3000:
                    print(f"  [-] {g['name']} (maly soubor)")
                    continue
                (out / f"{g['slug']}.png").write_bytes(img)
                ok += 1
                print(f"  [OK] {g['name']}  <- {picked}")
                time.sleep(0.2)
            except Exception as e:  # noqa
                print(f"  [x] {g['name']}: {e}")
    print(f"\nitch.io: dohledáno {ok}/{total} obrázků")


_STEAM_SKIP = {
    # slova, která ve jméně steamové aplikace znamenají, že to není samotná hra
    "soundtrack", "ost", "dlc", "demo", "trailer", "artbook", "art book", "wallpaper",
    "season pass", "expansion pass", "upgrade", "bundle", "beta", "server", "sdk",
    "the final hours", "digital deluxe upgrade", "theme", "avatar",
}
# povolené přívlastky za shodným názvem (reedice téže hry = stejný obal)
_STEAM_SUFFIX_OK = {
    "remastered", "remaster", "hd", "definitive", "edition", "goty", "game", "of", "the",
    "year", "complete", "enhanced", "anniversary", "collection", "redux", "classic",
    "deluxe", "ultimate", "special", "gold", "director's", "directors", "cut", "plus",
    # norm_name mění apostrof na mezeru, takže "Director's Cut" -> director / s / cut
    "director", "s",
}


# Kolik snimku ze hry stahovat. Galerie pobere deset polozek (obal, titulni
# obrazovka a snimky), takze osm snimku je strop, ktery ji jeste naplni.
MAX_SNIMKU = 8


def volne_snimky(out, gslug):
    """Vrati jmena volnych pozic pro snimky ze hry (-snap, -snap2 .. -snap9)."""
    jmena = [f"{gslug}-snap"] + [f"{gslug}-snap{i}" for i in range(2, 10)]
    return [n for n in jmena
            if not (out / f"{n}.jpg").exists()
            and not (out / f"{n}.png").exists()
            and not (out / f"{n}.webp").exists()]


def _steam_search(name, limit=6):
    """Veřejné hledání aplikací na Steamu (bez API klíče) -> list (appid, title)."""
    url = "https://steamcommunity.com/actions/SearchApps/" + urllib.parse.quote(name)
    try:
        data = json.loads(http_get(url))
    except Exception:  # noqa
        return []
    return [(a["appid"], a["name"]) for a in data[:limit] if a.get("appid")]


def _steam_clean(title):
    """Steam si do názvů píše ochranné známky — bez odstranění by norm_name z
    'DARK SOULS™ III' udělalo 'dark soulstm iii' a shoda by propadla."""
    return P.re.sub(r"[™®©℠]", " ", title)


def _steam_is_skippable(title):
    """Je to soundtrack/DLC/demo místo samotné hry?

    Jednoslovné termíny se musí shodovat na celé slovo — dřív se hledal podřetězec
    a 'ost' (soundtrack) tak zahodilo každý 'Lost Planet' i 'Ghost of Tsushima'."""
    low = title.lower()
    words = set(P.re.findall(r"[a-z0-9]+", low))
    for w in _STEAM_SKIP:
        if " " in w:
            if w in low:
                return True
        elif w in words:
            return True
    return False


def _steam_pick(game_name, hits):
    """Vyber appid, jehož název je opravdu tatáž hra (ne DLC, soundtrack ani sequel)."""
    gnorm = P.norm_name(game_name)
    if len(gnorm) < 3:
        return None
    for appid, title in hits:
        if _steam_is_skippable(title):
            continue
        tnorm = P.norm_name(_steam_clean(title))
        if not tnorm:
            continue
        if tnorm == gnorm:
            return appid, title
        # povol jen reedice: "BioShock" -> "BioShock Remastered"
        if tnorm.startswith(gnorm + " "):
            extra = tnorm[len(gnorm) + 1:].split()
            if not extra:
                continue
            if all(w in _STEAM_SUFFIX_OK for w in extra):
                return appid, title
            # "<neco> Edition" je pořád tatáž hra: "Bulletstorm: Full Clip Edition"
            if extra[-1] == "edition" and len(extra) <= 3:
                return appid, title
    return None


def fetch_games_steam(only=None):
    """Pro hry BEZ obrázku zkus portrétový box art ze Steamu (library_600x900, bez API klíče).
    Přísné párování názvu (přesná shoda nebo povolená reedice) proti falešným shodám —
    jinak by se k „BioShock" přilepil „BioShock Infinite"."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        # Web a mobil zaciname rokem vzniku platformy, ale hry na nich vychazeji
        # dodnes — Kingdom Rush i Cookie Clicker na Steamu jsou. U takovych
        # platforem rozhoduje rok HRY, ne rok platformy.
        prubezna = plat.get("type") in ("web", "mobile")
        if plat["year"] < STEAM_MIN_PLATFORM_YEAR and not prubezna:
            if wanted and slug in wanted:
                print(f"  [!] {slug}: Steam se pro platformy před {STEAM_MIN_PLATFORM_YEAR} nepoužívá")
            continue
        missing = [g for g in plat["games"] if not g.get("image")]
        if prubezna:
            missing = [g for g in missing
                       if str(g.get("year") or "0").isdigit()
                       and int(g["year"]) >= STEAM_MIN_PLATFORM_YEAR]
        if not missing:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"\n== {slug} — bez obrázku: {len(missing)} ==")
        for g in missing:
            total += 1
            time.sleep(0.35)  # šetrně ke Steamu
            base = P.re.sub(r"\([^)]*\)", " ", g["name"])
            base = base.split(" -ish")[0].split(" / ")[0].strip()
            hit = _steam_pick(base, _steam_search(base))
            if not hit:
                print(f"  [-] {g['name']}")
                continue
            appid, title = hit
            base_url = "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps"
            # portretovy obal nema na Steamu kazda hra -> fallback na sirokou hlavicku
            # (web uz landscape obrazky bezne pouziva, kdyz misto obalu vezme title screen)
            img = None
            for src in (f"{base_url}/{appid}/library_600x900.jpg",
                        f"{base_url}/{appid}/header.jpg"):
                try:
                    data = http_get(src)
                except Exception:  # noqa
                    continue
                if len(data) >= 3000:
                    img = data
                    break
            if img is None:
                print(f"  [x] {g['name']} (bez pouzitelneho obrazku)")
                continue
            (out / f"{g['slug']}.jpg").write_bytes(img)
            ok += 1
            print(f"  [OK] {g['name']}  <- steam:{appid} {title}")
    print(f"\nSteam: dohledáno {ok}/{total} obrázků")


# platformy, které má smysl hledat v Nintendo eShopu (system_type ve fasetách)
NINTENDO_SYSTEMS = {
    "switch": "nintendoswitch",
    "3ds": "3ds",
}


def _nintendo_search(name, system, limit=6):
    """Veřejné vyhledávání Nintendo eShopu (bez API klíče) -> list (title, image_url)."""
    q = urllib.parse.urlencode({
        "q": name,
        "fq": f"type:GAME AND system_type:{system}*",
        "rows": str(limit),
        "wt": "json",
    })
    try:
        data = json.loads(http_get("https://search.nintendo-europe.com/en/select?" + q))
    except Exception:  # noqa
        return []
    out = []
    for doc in data.get("response", {}).get("docs", []):
        img = doc.get("image_url")
        if doc.get("title") and img:
            out.append((doc["title"], img if img.startswith("http") else "https:" + img))
    return out


def fetch_games_nintendo(only=None):
    """Pro hry BEZ obrázku stáhne oficiální packshot z Nintendo eShopu.

    Nintendo exkluzivity nejsou na Steamu ani v libretro-thumbnails, takže tohle je
    jediný volně dostupný zdroj jejich obalů. Párování je stejně přísné jako u Steamu
    (přesná shoda nebo povolená reedice) — volnější shoda vrací úplně jiné hry."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        system = NINTENDO_SYSTEMS.get(slug)
        if not system:
            continue
        missing = [g for g in plat["games"] if not g.get("image")]
        if not missing:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"\n== {slug} - bez obrazku: {len(missing)} ==")
        for g in missing:
            total += 1
            time.sleep(0.3)
            base = P.re.sub(r"\([^)]*\)", " ", g["name"])
            base = base.split(" -ish")[0].split(" / ")[0].strip()
            hits = _nintendo_search(base, system)
            # _steam_pick očekává (id, title); tady je "id" rovnou URL obrázku
            pick = _steam_pick(base, [(url, title) for title, url in hits])
            if not pick:
                print(f"  [-] {g['name']}")
                continue
            url, title = pick
            try:
                img = http_get(url)
                if len(img) < 3000:
                    print(f"  [-] {g['name']} (maly soubor)")
                    continue
                (out / f"{g['slug']}.jpg").write_bytes(img)
                ok += 1
                print(f"  [OK] {g['name']}  <- eShop: {title}")
            except Exception as e:  # noqa
                print(f"  [x] {g['name']}: {e}")
    print(f"\nNintendo eShop: dohledano {ok}/{total} obrazku")


def _steam_screenshots(appid, limit=MAX_SNIMKU):
    """Vrátí URL prvních N screenshotů dané hry ze Steamu (veřejné appdetails API)."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&filters=screenshots"
    try:
        data = json.loads(http_get(url))
        shots = data[str(appid)]["data"]["screenshots"]
    except Exception:  # noqa
        return []
    out = []
    for sh in shots[:limit]:
        src = sh.get("path_full") or sh.get("path_thumbnail")
        if src:
            out.append(src)
    return out


# ---- GOG (bez API klice) ----
# Libretro ma jen tituly, ktere nekdo doplnil do RetroArch sady, a Steam zas
# nema starsi PC hry, ktere se na nej nikdy nedostaly. GOG stara PC vydani
# prodava dodnes a jeho katalog je verejny — pro DOSove a devadesatkove
# platformy je to nejlepsi zbyvajici zdroj.
_GOG_SEARCH = "https://catalog.gog.com/v1/catalog?limit=8&query=like:{q}&locale=en-US&countryCode=US&currencyCode=USD"
_GOG_PRODUCT = "https://api.gog.com/products/{pid}?expand=screenshots"
# poradi od nejvetsiho — chceme co nejvetsi snimek, ktery jeste existuje
_GOG_FORMATY = ("ggvgl_2x", "ggvgl", "ggvgm_2x", "ggvgm", "ggvgt_2x", "ggvgt")


def _gog_search(name, limit=8):
    """Hledani v katalogu GOG -> list (id, title)."""
    url = _GOG_SEARCH.format(q=urllib.parse.quote(name))
    try:
        data = json.loads(http_get(url))
    except Exception:  # noqa: BLE001
        return []
    out = []
    for p in (data.get("products") or [])[:limit]:
        if p.get("id") and p.get("title"):
            out.append((p["id"], p["title"]))
    return out


def _gog_pick(game_name, hits):
    """Vyber produkt, ktery je opravdu tataz hra.

    Hledani na GOG je velmi volne — dotaz "Fish Fillets" vrati "Warpaws"
    i "War Mechanic". Bez presne shody by se ke hre prilepil nahodny titul,
    takze plati stejna prisnost jako u Steamu: bud presna shoda, nebo jen
    povolena reedice ("Blade Runner - Enhanced Edition").
    """
    gnorm = P.norm_name(game_name)
    if len(gnorm) < 3:
        return None
    for pid, title in hits:
        if _steam_is_skippable(title):
            continue
        tnorm = P.norm_name(_steam_clean(title))
        if not tnorm:
            continue
        if tnorm == gnorm:
            return pid, title
        if tnorm.startswith(gnorm + " "):
            extra = tnorm[len(gnorm) + 1:].split()
            if extra and all(w in _STEAM_SUFFIX_OK for w in extra):
                return pid, title
            if extra and extra[-1] == "edition" and len(extra) <= 3:
                return pid, title
    return None


def _gog_images(pid, limit=MAX_SNIMKU):
    """Vrati (obal, [snimky]) pro produkt. Obal je svisly 'logo2x'."""
    try:
        d = json.loads(http_get(_GOG_PRODUCT.format(pid=pid)))
    except Exception:  # noqa: BLE001
        return None, []
    logo = ((d.get("images") or {}).get("logo2x") or "")
    if logo.startswith("//"):
        logo = "https:" + logo
    shots = []
    for sh in (d.get("screenshots") or []):
        podle = {x.get("formatter_name"): x.get("image_url")
                 for x in (sh.get("formatted_images") or [])}
        for f in _GOG_FORMATY:
            if podle.get(f):
                shots.append(podle[f])
                break
        if len(shots) >= limit:
            break
    return (logo or None), shots


def fetch_games_gog(only=None, shots_only=False):
    """Doplni obal a snimky ze hry z GOG.

    shots_only=False: hry BEZ obrazku (stahne obal i dva snimky).
    shots_only=True:  hry, ktere obal maji, ale nemaji snimky ze hry.
    """
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        # GOG prodava hry pro PC. Na jine platforme proto nabidne bud uplne
        # jinou verzi, nebo rovnou moderni remake pod puvodnim nazvem:
        # "Wizardry: Proving Grounds of the Mad Overlord" sedi presne, jenze
        # na Atari 800 vyslo roku 1981 a na GOG je remake z roku 2024. Stejne
        # tak Prince of Persia na C64 dostal snimky z 3D dilu a Cannon Fodder
        # na Amize verzi pro DOS. Rok platformy nestaci, protoze pc-dos i
        # pc-9x jsou stare a GOG je pro ne naopak nejlepsi zdroj — rozhoduje
        # tedy, jestli jde o PC linii.
        if slug not in GOG_OK:
            if wanted and slug in wanted:
                print(f"  [!] {slug}: GOG prodava verze pro PC, na tuto platformu se nepouziva")
            continue
        prubezna = plat.get("type") in ("web", "mobile")
        if shots_only:
            cile = [g for g in plat["games"]
                    if g.get("image") and len(g.get("gallery") or []) < 10]
        else:
            cile = [g for g in plat["games"] if not g.get("image")]
        if prubezna:
            cile = [g for g in cile
                    if str(g.get("year") or "0").isdigit()
                    and int(g["year"]) >= STEAM_MIN_PLATFORM_YEAR]
        if not cile:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"\n== {slug} — k doplneni: {len(cile)} ==")
        for g in cile:
            total += 1
            hit = _gog_pick(g["name"], _gog_search(g["name"]))
            if not hit:
                continue
            pid, title = hit
            logo, shots = _gog_images(pid)
            got = 0
            if not shots_only and logo:
                dest = out / f"{g['slug']}.jpg"
                if not dest.exists() and not dest.with_suffix(".webp").exists():
                    try:
                        dest.write_bytes(http_get(logo))
                        got += 1
                    except Exception:  # noqa: BLE001
                        pass
            # do prvni VOLNE pozice: kdyz uz hra jeden snimek ma, dalsi
            # musi jit do -snap2, ne se zahodit
            volne = volne_snimky(out, g["slug"])
            for jmeno, u in zip(volne, shots):
                dest = out / (jmeno + ".jpg")
                try:
                    dest.write_bytes(http_get(u))
                    got += 1
                except Exception:  # noqa: BLE001
                    pass
            if got:
                ok += 1
                print(f"  [OK] {g['name']}  <- gog:{pid} {title} ({got} obr.)")
    print(f"\nGOG: doplneno u {ok}/{total} her")


# ---- ZXDB / ZXInfo (bez API klice) ----
# Osmibitove Spectrum tituly nejsou ani na Steamu, ani na GOG a libretro sada
# je nekompletni. ZXDB je nejuplnejsi verejny katalog Spectra vubec.
_ZX_SEARCH = "https://api.zxinfo.dk/v3/search?query={q}&size=6&mode=compact"
_ZX_MEDIA = "https://zxinfo.dk/media"


def _zx_search(name):
    """Hledani v ZXDB -> list (title, [url snimku])."""
    try:
        d = json.loads(http_get(_ZX_SEARCH.format(q=urllib.parse.quote(name))))
    except Exception:  # noqa: BLE001
        return []
    out = []
    for h in ((d.get("hits") or {}).get("hits") or []):
        src = h.get("_source") or {}
        title = src.get("title")
        if not title:
            continue
        urls = []
        for sc in (src.get("screens") or []):
            u = sc.get("url")
            if u:
                urls.append(_ZX_MEDIA + u)
        if urls:
            out.append((title, urls))
    return out


def fetch_games_zxinfo(only=None):
    """Doplni hram na Spectru obal (loading screen) a snimky ze hry z ZXDB.

    ZXDB rozlisuje loading screen a in-game snimky jen nazvem souboru, takze
    prvni obrazek bereme jako titulni a dalsi dva do galerie. Parovani je
    stejne prisne jako u Steamu — hledani vraci i volne shody.
    """
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else {"zx-spectrum"}
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if slug not in wanted:
            continue
        cile = [g for g in plat["games"]
                if not g.get("image") or len(g.get("gallery") or []) < 2]
        if not cile:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print("\n== %s - k doplneni: %d ==" % (slug, len(cile)))
        for g in cile:
            total += 1
            gnorm = P.norm_name(g["name"])
            urls = None
            for title, u in _zx_search(g["name"]):
                if P.norm_name(_steam_clean(title)) == gnorm:
                    urls = u
                    break
            if not urls:
                continue
            got = 0
            # Snimky se ukladaji do prvni VOLNE pozice. Pozicni mapovani by
            # u hry, ktera uz obal a jeden snimek ma, zahodilo vse ostatni.
            volne = volne_snimky(out, g["slug"])
            # kdyz hra nema ani obal, prvni nalezeny obrazek slouzi jako obal
            if not any((out / (g["slug"] + e)).exists() for e in (".png", ".webp", ".jpg")):
                volne = [g["slug"]] + volne
            for jmeno, u in zip(volne, urls):
                dest = out / (jmeno + ".png")
                try:
                    dest.write_bytes(http_get(u))
                    got += 1
                except Exception:  # noqa: BLE001
                    pass
            if got:
                ok += 1
                print("  [OK] %s  <- zxdb (%d obr.)" % (g["name"], got))
    print("\nZXDB: doplneno u %d/%d her" % (ok, total))


def dedupe_game_images(only=None):
    """Smaze obrazky, ktere jsou u jedne hry ulozene dvakrat pod jinym jmenem.

    Porovnava se obsah souboru, ne nazev — stejny snimek muze prijit ze
    Steamu i z GOG, nebo se pri opakovanem behu s vyssim limitem ulozit
    znovu do volne pozice.

    POZOR NA PORADI: pousti se az PO 'optimize'. Cerstve stazeny JPEG a uz
    prevedeny WebP tehoz obrazku maji ruzne bajty, takze pred prevodem
    kontrola duplicitu neodhali — presne to se stalo u XCOM 2, kde snap
    a snap3 zustaly stejne. Ponechava se vzdy prvni vyskyt v poradi
    obal, -snap, -snap2 .. -snap9, -title.
    """
    import hashlib

    gdir = IMG / "games"
    wanted = set(only.split(",")) if only else None
    smazano = dotcenych = 0
    for pdir in sorted(gdir.iterdir()):
        if not pdir.is_dir() or (wanted and pdir.name not in wanted):
            continue
        # seskupit soubory podle hry
        podle_hry = {}
        for f in pdir.iterdir():
            if not f.is_file():
                continue
            zaklad = f.stem
            for suf in ["-title"] + [f"-snap{i}" for i in range(9, 1, -1)] + ["-snap"]:
                if zaklad.endswith(suf):
                    zaklad = zaklad[: -len(suf)]
                    break
            podle_hry.setdefault(zaklad, []).append(f)

        for gslug, soubory in podle_hry.items():
            poradi = [gslug, gslug + "-snap"] + [f"{gslug}-snap{i}" for i in range(2, 10)]
            poradi.append(gslug + "-title")
            klic = {p: i for i, p in enumerate(poradi)}
            soubory.sort(key=lambda f: klic.get(f.stem, 99))
            videne = {}
            for f in soubory:
                try:
                    h = hashlib.md5(f.read_bytes()).hexdigest()
                except Exception:  # noqa: BLE001
                    continue
                if h in videne:
                    f.unlink(missing_ok=True)
                    smazano += 1
                    dotcenych += 1
                else:
                    videne[h] = f
    print(f"\nDuplicity: smazano {smazano} souboru")


def fetch_games_steam_shots(only=None):
    """Doplní hrám, které UŽ MAJÍ obal, dva snímky ze hry ze Steamu.

    Retro platformy berou snímky z libretro (Named_Snaps / Named_Titles), jenže pro
    moderní konzole tam žádné nejsou — proto tam hry měly jediný obrázek. Ukládá se
    pod příponami -snap a -snap2 (oba jsou ze hry, Steam titulní obrazovky nemá),
    které parser skládá do galerie."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        # stejne jako u obalu: u webu a mobilu rozhoduje rok hry, ne platformy
        prubezna = plat.get("type") in ("web", "mobile")
        if plat["year"] < STEAM_MIN_PLATFORM_YEAR and not prubezna:
            if wanted and slug in wanted:
                print(f"  [!] {slug}: Steam se pro platformy před {STEAM_MIN_PLATFORM_YEAR} nepoužívá")
            continue
        # jen hry, které mají obal, ale ještě nemají snímky ze hry
        # galerie pobere deset polozek, takze dobirame i hry, ktere uz nejaky
        # snimek maji — fetcher existujici soubory preskoci, takze je to levne
        targets = [g for g in plat["games"] if g.get("image") and len(g.get("gallery") or []) < 10]
        if prubezna:
            targets = [g for g in targets
                       if str(g.get("year") or "0").isdigit()
                       and int(g["year"]) >= STEAM_MIN_PLATFORM_YEAR]
        if not targets:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"\n== {slug} - bez snimku: {len(targets)} ==")
        for g in targets:
            total += 1
            # Volne pozice pro snimky. Drive se preskocila cela hra, jakmile
            # existoval -snap, takze hra s jednim snimkem uz druhy nedostala.
            volne = volne_snimky(out, g["slug"])
            if not volne:
                continue
            time.sleep(0.35)
            base = P.re.sub(r"\([^)]*\)", " ", g["name"])
            base = base.split(" -ish")[0].split(" / ")[0].strip()
            hit = _steam_pick(base, _steam_search(base))
            if not hit:
                print(f"  [-] {g['name']}")
                continue
            appid, title = hit
            shots = _steam_screenshots(appid)
            if not shots:
                print(f"  [-] {g['name']} (bez screenshotu)")
                continue
            saved = 0
            for src, jmeno in zip(shots, volne):
                try:
                    img = http_get(src)
                    if len(img) < 3000:
                        continue
                    (out / f"{jmeno}.jpg").write_bytes(img)
                    saved += 1
                except Exception:  # noqa
                    pass
            if saved:
                ok += 1
                print(f"  [OK] {g['name']}  <- steam:{appid} ({saved} snimky)")
            else:
                print(f"  [x] {g['name']} (stazeni selhalo)")
    print(f"\nSteam screenshoty: doplneno u {ok}/{total} her")


def _nintendo_search_urls(name, system, limit=6):
    """Jako _nintendo_search, ale vrací (url_produktove_stranky, title)."""
    q = urllib.parse.urlencode({
        "q": name,
        "fq": f"type:GAME AND system_type:{system}*",
        "rows": str(limit),
        "wt": "json",
    })
    try:
        data = json.loads(http_get("https://search.nintendo-europe.com/en/select?" + q))
    except Exception:  # noqa
        return []
    out = []
    for doc in data.get("response", {}).get("docs", []):
        url, title = doc.get("url"), doc.get("title")
        if url and title:
            out.append(("https://www.nintendo.com/en-gb" + url if url.startswith("/") else url, title))
    return out


_NIN_SHOT_RE = None


def _nintendo_screenshots(page_url, limit=2):
    """Vytáhne z produktové stránky Nintenda odkazy na snímky ze hry.

    Nintendo je servíruje z cesty /06_screenshots/; varianty s '_TM_' jsou náhledy,
    ty přeskakujeme, ať v galerii nekončí rozmazané miniatury."""
    global _NIN_SHOT_RE
    if _NIN_SHOT_RE is None:
        _NIN_SHOT_RE = P.re.compile(r"https://\S+?/06_screenshots/\S+?\.(?:jpg|png)")
    try:
        html = http_get(page_url, headers={"User-Agent": _ITCH_UA}).decode("utf-8", "replace")
    except Exception:  # noqa
        return []
    seen, out = set(), []
    for m in _NIN_SHOT_RE.finditer(html):
        u = m.group(0)
        if "_TM_" in u or u in seen:
            continue
        seen.add(u)
        out.append(u)
        if len(out) >= limit:
            break
    return out


def fetch_games_nintendo_shots(only=None):
    """Doplní hrám s obalem, ale bez galerie, dva snímky ze hry z Nintendo eShopu.

    Nintendo exkluzivity nejsou na Steamu a libretro pro Switch nemá vůbec nic,
    takže tohle je jejich jediný volně dostupný zdroj snímků."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        system = NINTENDO_SYSTEMS.get(slug)
        if not system:
            continue
        # galerie pobere deset polozek, takze dobirame i hry, ktere uz nejaky
        # snimek maji — fetcher existujici soubory preskoci, takze je to levne
        targets = [g for g in plat["games"] if g.get("image") and len(g.get("gallery") or []) < 10]
        if not targets:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"\n== {slug} - bez snimku: {len(targets)} ==")
        for g in targets:
            total += 1
            if (out / f"{g['slug']}-snap.jpg").exists() or (out / f"{g['slug']}-snap.webp").exists():
                continue
            time.sleep(0.3)
            base = P.re.sub(r"\([^)]*\)", " ", g["name"])
            base = base.split(" -ish")[0].split(" / ")[0].strip()
            hits = _nintendo_search_urls(base, system)
            pick = _steam_pick(base, hits)  # (url_stranky, title) — stejne prisne parovani
            if not pick:
                print(f"  [-] {g['name']}")
                continue
            page_url, title = pick
            shots = _nintendo_screenshots(page_url)
            if not shots:
                print(f"  [-] {g['name']} (bez snimku na strance)")
                continue
            saved = 0
            for src, suffix in zip(shots, ("-snap", "-snap2")):
                try:
                    img = http_get(src, headers={"User-Agent": _ITCH_UA})
                    if len(img) < 3000:
                        continue
                    (out / f"{g['slug']}{suffix}.jpg").write_bytes(img)
                    saved += 1
                except Exception:  # noqa
                    pass
            if saved:
                ok += 1
                print(f"  [OK] {g['name']}  <- eShop ({saved} snimky)")
            else:
                print(f"  [x] {g['name']} (stazeni selhalo)")
    print(f"\nNintendo snimky: doplneno u {ok}/{total} her")


def _wiki_infobox_image(title):
    """Nazev souboru z pole |image= v infoboxu clanku (typicky obal hry).

    pageimages API nesvobodne soubory zasadne nevraci, proto se ctou primo
    wikitext a nazev souboru; samotny soubor uz pres imageinfo stahnout jde."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": title,
        "prop": "revisions", "rvprop": "content", "rvslots": "main", "redirects": "1",
    })
    try:
        data = json.loads(http_get("https://en.wikipedia.org/w/api.php?" + q))
    except Exception:  # noqa
        return None
    for page in data.get("query", {}).get("pages", {}).values():
        try:
            wt = page["revisions"][0]["slots"]["main"]["*"]
        except Exception:  # noqa
            continue
        for field in ("cover", "image"):
            m = P.re.search(r"\|\s*" + field + r"\s*=\s*([^\n|}]+)", wt)
            if not m:
                continue
            name = m.group(1).strip()
            # nekdy je hodnota zapsana jako [[File:Neco.png|...]]
            inner = P.re.search(r"File:([^|\]]+)", name)
            if inner:
                name = inner.group(1).strip()
            name = name.strip("[] ").strip()
            if name and "." in name:
                return name
    return None


def _wiki_file_url(filename, width=600):
    """URL nahledu souboru z Wikipedie (funguje i pro nesvobodne soubory)."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": f"File:{filename}",
        "prop": "imageinfo", "iiprop": "url", "iiurlwidth": str(width),
    })
    try:
        data = json.loads(http_get("https://en.wikipedia.org/w/api.php?" + q))
    except Exception:  # noqa
        return None
    for page in data.get("query", {}).get("pages", {}).values():
        ii = (page.get("imageinfo") or [{}])[0]
        return ii.get("thumburl") or ii.get("url")
    return None


def fetch_games_wiki_box(only=None):
    """Pro hry BEZ obrazku vezme obal z infoboxu clanku na anglicke Wikipedii.

    Posledni zdroj pro konzolove exkluzivity, ktere nejsou ani v libretro-thumbnails,
    ani na Steamu ci v eShopu (Uncharted, God of War, Killzone, Gran Turismo...).
    Overeni clanku je stejne prisne jako u fetch_games_wiki — kategorie musi
    obsahovat 'video game', jinak by se trefil stejnojmenny film nebo kniha."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else None
    ok = total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if wanted and slug not in wanted:
            continue
        missing = [g for g in plat["games"] if not g.get("image")]
        if not missing:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        used_files = {}
        print(f"\n== {slug} - bez obalu: {len(missing)} ==")
        for g in missing:
            total += 1
            # na hru pripadaji ctyri dotazy (hledani, kategorie, wikitext, soubor);
            # pri kratsi prodleve zacne Wikimedia odmitat a vypada to jako
            # "clanek nema obrazek", i kdyz ho ma
            time.sleep(1.5)
            base = P.re.sub(r"\([^)]*\)", " ", g["name"])
            base = base.split(" -ish")[0].split(" / ")[0].strip()
            # PRISNA shoda nazvu: volnejsi parovani napasovalo 'Killzone 2'
            # i 'inFamous 2' na clanek o PRVNIM dilu serie
            gnorm = P.norm_name(base)
            picked = None
            for query in (f"{base} video game", f"{base} {plat['short']} video game"):
                for title in _wiki_search(query):
                    # z nazvu clanku pryc rozlisovaci zavorka: 'Flower (video game)'
                    bare = P.re.sub(r"\([^)]*\)", " ", title).strip()
                    if P.norm_name(bare) != gnorm or not _wiki_is_videogame(title):
                        continue
                    picked = title
                    break
                if picked:
                    break
            if not picked:
                print(f"  [-] {g['name']}")
                continue
            fname = _wiki_infobox_image(picked)
            if not fname:
                print(f"  [-] {g['name']} (v infoboxu neni obrazek: {picked})")
                continue
            # kdyz stejny soubor sedne na vic her, je to spatna shoda (jiny dil serie)
            if fname in used_files:
                print(f"  [-] {g['name']} (obal uz pouzit u: {used_files[fname]})")
                continue
            used_files[fname] = g["name"]
            src = _wiki_file_url(fname)
            if not src:
                print(f"  [-] {g['name']} (soubor nedostupny: {fname})")
                continue
            try:
                img = http_get(src, headers={"User-Agent": _ITCH_UA})
                if len(img) < 3000:
                    print(f"  [-] {g['name']} (maly soubor)")
                    continue
                ext = os.path.splitext(urllib.parse.urlparse(src).path)[1].lower()
                if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
                    ext = ".jpg"
                (out / f"{g['slug']}{ext}").write_bytes(img)
                ok += 1
                print(f"  [OK] {g['name']}  <- WP:{picked} / {fname}")
            except Exception as e:  # noqa
                print(f"  [x] {g['name']}: {str(e)[:60]}")
    print(f"\nWikipedia obaly: dohledano {ok}/{total}")


def trim_platform_bg(only=None, base_thresh=250):
    """U fotek platforem s bilym pozadim udela z pozadi pruhlednost.

    Prah je zamerne vysoko (jen temer ciste bila). S nizsim se vypln prokouse do
    svetlych casti produktu — bily pasek PlayStation VR takhle prisel o kusy,
    protoze sedobila plocha jeste prosla jako pozadi.

    Fotky konzoli z Wikipedie jsou casto produktove snimky na bilem podkladu.
    Na karte pak vznikne bily obdelnik s tvrdym okrajem, ktery vedle vyrezu
    na tmavem gradientu vypada jako nalepena zaplata. Vyplnovy algoritmus
    zacina VYHRADNE od okraju obrazku, takze bile plochy uvnitr produktu
    (napr. bila konzole) zustanou — odstrani se jen pozadi spojite s ramem.

    only: carkou oddelene slugy; bez nich se vezmou platformy oznacene
    v platform_bg.json jako 'light'.
    """
    from PIL import Image
    from collections import deque

    pdir = IMG / "platforms"
    bg_file = ROOT / "src" / "data" / "platform_bg.json"
    if only:
        slugs = set(only.split(","))
    else:
        bg = json.loads(bg_file.read_text("utf-8")) if bg_file.exists() else {}
        slugs = ({k for k, v in bg.items() if v == "light"} | PLATFORM_CHROMA) - PLATFORM_TRIM_SKIP
    if not slugs:
        print("  zadne platformy se svetlym pozadim")
        return

    done = 0
    for slug in sorted(slugs):
        src = next((f for f in pdir.glob(f"{slug}.*") if f.suffix.lower() != ".svg"), None)
        if not src:
            print(f"  [-] {slug}: fotka nenalezena")
            continue
        try:
            im = Image.open(src).convert("RGBA")
        except Exception as e:  # noqa
            print(f"  [x] {slug}: {e}")
            continue
        w, h = im.size
        px = im.load()

        chroma = slug in PLATFORM_CHROMA
        thresh = PLATFORM_TRIM_THRESH.get(slug, base_thresh)

        def is_bg(x, y):
            r, g, b, a = px[x, y]
            if not a:
                return False
            if chroma:
                # Platno je syta zelen; bily plast (r~g~b) ani cerne polstrovani
                # ji nemaji.
                # Prah zamerne NEjde nize: tmava zelen uz je k nerozeznani od
                # cerne gumy se zelenym odleskem a vypln se do ni prokouse
                # (headset PSVR2 takhle prisel o polstrovani i pasek). Za cenu
                # toho ve snimku zustane jemny vrzeny stin.
                return g > 60 and g >= r + 28 and g >= b + 28
            return r >= thresh and g >= thresh and b >= thresh

        seen = bytearray(w * h)
        q = deque()
        for x in range(w):
            for y in (0, h - 1):
                if is_bg(x, y) and not seen[y * w + x]:
                    seen[y * w + x] = 1
                    q.append((x, y))
        for y in range(h):
            for x in (0, w - 1):
                if is_bg(x, y) and not seen[y * w + x]:
                    seen[y * w + x] = 1
                    q.append((x, y))

        cleared = 0
        while q:
            x, y = q.popleft()
            px[x, y] = (255, 255, 255, 0)
            cleared += 1
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and is_bg(nx, ny):
                    seen[ny * w + nx] = 1
                    q.append((nx, ny))

        ratio = cleared / (w * h)
        # Nektera fotka ma pozadi jen skoro bile (svetle sede studio). Prisny prah
        # ho nenajde, tak se zkusi jeste jednou mirneji — u platforem v
        # PLATFORM_TRIM_SKIP se to nedela, tam by se vypln prokousala do produktu.
        if ratio < 0.02 and not chroma and slug not in PLATFORM_TRIM_SKIP and thresh > 236:
            im = Image.open(src).convert("RGBA")
            px = im.load()
            seen = bytearray(w * h)
            q = deque()
            soft = 236

            def is_bg2(x, y):
                r, g, b, a = px[x, y]
                return a > 0 and r >= soft and g >= soft and b >= soft

            for x in range(w):
                for y in (0, h - 1):
                    if is_bg2(x, y) and not seen[y * w + x]:
                        seen[y * w + x] = 1
                        q.append((x, y))
            for y in range(h):
                for x in (0, w - 1):
                    if is_bg2(x, y) and not seen[y * w + x]:
                        seen[y * w + x] = 1
                        q.append((x, y))
            cleared = 0
            while q:
                x, y = q.popleft()
                px[x, y] = (255, 255, 255, 0)
                cleared += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and is_bg2(nx, ny):
                        seen[ny * w + nx] = 1
                        q.append((nx, ny))
            ratio = cleared / (w * h)
        # Vypln od okraju se nedostane do oblasti, kterou produkt uzavre do
        # smycky — u 3DO zustal bily ostrov uvnitr kabelu od ovladace a na
        # tmavem podkladu karty svitil jako zaplata. Zbyle ostrovy barvy pozadi,
        # ktere se nedotykaji ramu, jsou proto taky pozadi; velke se pro jistotu
        # nechavaji (to uz by nebyla dira, ale spatne rozpoznany produkt).
        ostrovy = 0
        limit = int(w * h * 0.08)
        for sy in range(h):
            for sx in range(w):
                if seen[sy * w + sx] or not is_bg(sx, sy):
                    continue
                komponenta, fronta, u_okraje = [], deque([(sx, sy)]), False
                seen[sy * w + sx] = 1
                while fronta:
                    x, y = fronta.popleft()
                    komponenta.append((x, y))
                    if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                        u_okraje = True
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and is_bg(nx, ny):
                            seen[ny * w + nx] = 1
                            fronta.append((nx, ny))
                if u_okraje or len(komponenta) > limit:
                    continue
                for x, y in komponenta:
                    px[x, y] = (255, 255, 255, 0)
                cleared += len(komponenta)
                ostrovy += 1
        if ostrovy:
            print(f"      uzavrenych ostrovu pozadi odmazano: {ostrovy}")

        if chroma and ratio >= 0.02:
            # Platno vrha na obrys produktu zeleny lem. Zbylym pixelum se zelena
            # slozka stlaci na uroven cerveno-modreho prumeru, cimz lem zesedne.
            for y in range(h):
                for x in range(w):
                    r, g, b, a = px[x, y]
                    if not a:
                        continue
                    cap = (r + b) // 2 + 10
                    if g > cap:
                        px[x, y] = (r, cap, b, a)

        # kdyz by zmizela vic nez tri ctvrtiny obrazku, je to spatne rozpoznany
        # snimek (svetly produkt splyva s pozadim) — nechame ho radeji bez zmeny
        if ratio > 0.75:
            print(f"  [-] {slug}: preskoceno, odmazalo by {ratio:.0%} obrazku")
            continue
        if ratio < 0.02:
            print(f"  [-] {slug}: bile pozadi u okraju nenalezeno")
            continue
        dst = src.with_suffix(".png")
        im.save(dst, "PNG", optimize=True)
        if dst != src:
            src.unlink()
        done += 1
        print(f"  [OK] {slug}: pozadi odmazano ({ratio:.0%} obrazku) -> {dst.name}")

    print(f"\nPruhledne pozadi: upraveno {done} fotek")
    print("Spust jeste 'classify' a parse_content.py, at se prekresli karty.")



# ---------------------------------------------------------------------------
# App Store — jediny zdroj, ktery u mobilnich her da obal i snimky ze hry
# ---------------------------------------------------------------------------
def _appstore_search(name, limit=8):
    """Verejne vyhledavaci API iTunes. Bez klice a bez registrace."""
    q = urllib.parse.urlencode({
        "term": name, "entity": "software", "country": "us",
        "limit": str(limit), "media": "software",
    })
    try:
        data = json.loads(http_get("https://itunes.apple.com/search?" + q))
    except Exception:  # noqa
        return []
    return data.get("results") or []


def _appstore_pick(name, results):
    """Vybere zaznam, ktery opravdu odpovida nazvu hry.

    App Store radi vysledky po svem — na dotaz "Monument Valley" vrati jako prvni
    "Monument Valley 3". Bez teto kontroly by kazdy dil serie dostal obal toho
    nejnovejsiho; je to presne ta chyba, kterou uz jednou udelalo parovani obalu
    z libretra u Tomb Raideru.
    """
    q_num = {w for w in P.norm_name(name).split() if w in _SEQUEL}
    for r in results:
        title = r.get("trackName") or ""
        if not title or not _plausible_match(name, title):
            continue
        # _plausible_match hlida cislo dilu jen kdyz je v DOTAZU. Tady je potreba
        # i opacny smer: na "Angry Birds" vraci obchod jako prvni "Angry Birds 2"
        # a jednicka by dostala obal dvojky.
        c_num = {w for w in P.norm_name(title).split() if w in _SEQUEL}
        if c_num - q_num:
            continue
        # Hlavni cast nazvu nesmi pridavat vyznamova slova navic. Puvodni
        # "Angry Birds" uz v obchode neni a bez tehle kontroly by misto nej
        # vysel obal "Angry Birds Friends". Podnazev za dvojteckou je v poradku
        # ("Cut the Rope: Physics Puzzle" je porad tataz hra).
        head = P.re.split(r"[:–—]", title)[0]
        extra = {w for w in P.norm_name(head).split() if len(w) >= 4} -                 {w for w in P.norm_name(name).split()}
        if extra:
            continue
        if r.get("primaryGenreName") not in ("Games", "Entertainment"):
            continue
        return r
    return None


def _appstore_big(url, size="1024x1024bb"):
    """Prepise rozmer v URL obrazku z App Storu na vetsi variantu."""
    return P.re.sub(r"/\d+x\d+bb(-\d+)?\.(jpg|png|webp)$", "/" + size + ".jpg", url)


def fetch_games_appstore(only=None):
    """Obaly a snimky ze hry z App Storu (vychozi platforma: mobil).

    Mobilni hra nema obal v klasickem smyslu — jeji "obal" je ikona aplikace,
    kterou lide znaji z plochy telefonu, takze se pouzije jako hlavni obrazek.
    Snimky se berou prednostne z iPadu: jsou na sirku a do galerie sednou lip
    nez uzke portretove snimky z telefonu.
    """
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    wanted = set(only.split(",")) if only else {"mobil"}
    ok_cover = ok_shots = total = 0

    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if slug not in wanted:
            continue
        out = IMG / "games" / slug
        out.mkdir(parents=True, exist_ok=True)
        targets = [g for g in plat["games"]
                   if (not g.get("image")) or len(g.get("gallery") or []) < 2]
        print("\n== " + slug + ": " + str(len(targets)) + " her bez obalu nebo bez snimku ==")

        for g in targets:
            total += 1
            gslug = g["slug"]
            ma_obal = bool(g.get("image"))
            ma_snimky = any((out / (gslug + "-snap" + x + ".jpg")).exists() for x in ("", "2"))
            if ma_obal and ma_snimky:
                continue
            time.sleep(0.35)
            hit = _appstore_pick(g["name"], _appstore_search(g["name"]))
            if not hit:
                print("  [-] " + g["name"])
                continue

            if not ma_obal:
                icon = hit.get("artworkUrl512") or hit.get("artworkUrl100")
                if icon:
                    try:
                        img = http_get(_appstore_big(icon))
                        if len(img) > 3000:
                            (out / (gslug + ".jpg")).write_bytes(img)
                            ok_cover += 1
                    except Exception:  # noqa
                        pass

            saved = 0
            if not ma_snimky:
                shots = (hit.get("ipadScreenshotUrls") or [])[:2] \
                    or (hit.get("screenshotUrls") or [])[:2]
                for src, suffix in zip(shots, ("-snap", "-snap2")):
                    try:
                        img = http_get(_appstore_big(src, "1200x1200bb"))
                        if len(img) < 3000:
                            continue
                        (out / (gslug + suffix + ".jpg")).write_bytes(img)
                        saved += 1
                    except Exception:  # noqa
                        pass
                if saved:
                    ok_shots += 1

            print("  [OK] " + g["name"] + "  <- " + str(hit.get("trackName")) +
                  " (" + str(saved) + " snimku)")

    print("\nApp Store: obalu " + str(ok_cover) + ", snimku u " + str(ok_shots) +
          " her (z " + str(total) + ")")

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "platforms"):
        print("=== PLATFORMY (Wikipedia) ===")
        fetch_platforms()
    if what in ("all", "games"):
        print("\n=== HRY (libretro-thumbnails) ===")
        fetch_games(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "optimize":
        print("=== OPTIMALIZACE ===")
        optimize_images()
    if what == "symlinks":
        print("=== SYMLINKY ===")
        resolve_symlinks()
    if what == "screenshots":
        print("=== SCREENSHOTY (Named_Snaps + Named_Titles) ===")
        fetch_screenshots(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "trim-bg":
        print("=== ODSTRANĚNÍ BÍLÉHO POZADÍ U FOTEK PLATFOREM ===")
        trim_platform_bg(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "classify":
        print("=== KLASIFIKACE POZADÍ PLATFOREM ===")
        classify_platform_bg()
    if what == "article-photos":
        print("=== DOPROVODNÉ FOTKY DO ČLÁNKŮ (Wikipedia) ===")
        fetch_article_photos()
    if what == "fallback-shots":
        print("=== FALLBACK OBRÁZKY HER (title/snap pro hry bez obalu) ===")
        fetch_fallback_shots(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-wiki":
        print("=== OBRÁZKY HER Z WIKIPEDIE (hry bez obrázku) ===")
        fetch_games_wiki(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-itch":
        print("=== OBRÁZKY HER Z ITCH.IO (homebrew/indie bez obrázku) ===")
        fetch_games_itch(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-steam":
        print("=== OBRÁZKY HER ZE STEAMU (portrétový box art, hry bez obrázku) ===")
        fetch_games_steam(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-nintendo":
        print("=== OBRÁZKY HER Z NINTENDO ESHOPU (hry bez obrázku) ===")
        fetch_games_nintendo(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-nintendo-shots":
        print("=== SNÍMKY ZE HRY Z NINTENDO ESHOPU (hry s obalem, ale bez galerie) ===")
        fetch_games_nintendo_shots(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-wiki-box":
        print("=== OBALY Z INFOBOXU NA WIKIPEDII (hry bez obrázku) ===")
        fetch_games_wiki_box(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-appstore":
        print("=== OBALY A SNÍMKY Z APP STORU (mobilní hry) ===")
        fetch_games_appstore(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-zxinfo":
        print("=== OBRAZKY ZE ZXDB (ZX Spectrum) ===")
        fetch_games_zxinfo(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "dedupe":
        print("=== ODSTRANENI DUPLICITNICH OBRAZKU U HER ===")
        dedupe_game_images(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-gog":
        print("=== OBALY A SNIMKY Z GOG (hry bez obrazku) ===")
        fetch_games_gog(sys.argv[2] if len(sys.argv) > 2 else None)
    if what == "games-gog-shots":
        print("=== SNIMKY ZE HRY Z GOG (hry s obalem, ale bez galerie) ===")
        fetch_games_gog(sys.argv[2] if len(sys.argv) > 2 else None, shots_only=True)
    if what == "games-steam-shots":
        print("=== SNÍMKY ZE HRY ZE STEAMU (hry s obalem, ale bez galerie) ===")
        fetch_games_steam_shots(sys.argv[2] if len(sys.argv) > 2 else None)
