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
    "n64": "Nintendo 64",
    "arcade": "Arcade cabinet",
    "pc-engine": "TurboGrafx-16",
    "dreamcast": "Dreamcast",
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
    "intellivision": "Intellivision",
    "jaguar": "Atari Jaguar",
    "amiga-cd32": "Amiga CD32",
}

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
    "n64": "Nintendo_-_Nintendo_64",
    "arcade": "MAME",
    "pc-engine": "NEC_-_PC_Engine_-_TurboGrafx_16",
    "dreamcast": "Sega_-_Dreamcast",
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
            src = wiki_image(title)
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


def best_boxart(game_name, names, idx):
    key = P.norm_name(game_name)
    if key in idx:
        return idx[key]
    # fuzzy přes všechny názvy
    best, best_sc = None, 0.0
    for n in names:
        sc = P.match_metrics(game_name, n)[0]
        if sc > best_sc:
            best_sc, best = sc, n
    if best and best_sc >= 0.78 and P.acceptable(game_name, best):
        return best
    return None


def fetch_games():
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    plat_games = {p["slug"]: p["games"] for p in dataset["platforms"]}

    grand_total = grand_ok = 0
    for slug, repo in LIBRETRO.items():
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


def fetch_screenshots():
    """Stáhne in-game screenshot (Named_Snaps) a title screen (Named_Titles) pro hry,
    které mají boxart. Stejné názvy souborů jako boxarty. Ukládá jako <slug>-snap.png / -title.png."""
    dataset = json.loads((ROOT / "src" / "data" / "dataset.json").read_text("utf-8"))
    plat_games = {p["slug"]: p["games"] for p in dataset["platforms"]}
    grand = {"snap": 0, "title": 0}
    for slug, repo in LIBRETRO.items():
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
    grand = 0
    for slug, repo in LIBRETRO.items():
        if only and slug != only:
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

    # --- hry: PNG -> WebP 480px ---
    gdir = IMG / "games"
    pngs = list(gdir.rglob("*.png"))
    before = sum(p.stat().st_size for p in pngs)
    conv = 0
    for p in pngs:
        try:
            im = Image.open(p)
            im.thumbnail((480, 480), Image.LANCZOS)
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA")
            webp = p.with_suffix(".webp")
            im.save(webp, "WEBP", quality=80, method=6)
            p.unlink()
            conv += 1
        except Exception as e:  # noqa
            print(f"  [x] {p.name}: {e}")
    after = sum(f.stat().st_size for f in gdir.rglob("*.webp"))
    print(f"Hry: {conv} obrázků -> WebP, {before//1024//1024} MB -> {after//1024//1024} MB")

    # --- platformy: zmenšit velké (mimo gif kvůli animaci) ---
    pdir = IMG / "platforms"
    pcount = 0
    for p in list(pdir.iterdir()):
        if p.suffix.lower() == ".gif":
            continue
        try:
            im = Image.open(p)
            if max(im.size) > 900:
                im.thumbnail((900, 900), Image.LANCZOS)
                im.save(p)
                pcount += 1
        except Exception as e:  # noqa
            print(f"  [x] {p.name}: {e}")
    print(f"Platformy: zmenšeno {pcount} velkých obrázků")


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
    ok = 0
    total = 0
    for plat in dataset["platforms"]:
        slug = plat["slug"]
        if only and slug != only:
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


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "platforms"):
        print("=== PLATFORMY (Wikipedia) ===")
        fetch_platforms()
    if what in ("all", "games"):
        print("\n=== HRY (libretro-thumbnails) ===")
        fetch_games()
    if what == "optimize":
        print("=== OPTIMALIZACE ===")
        optimize_images()
    if what == "symlinks":
        print("=== SYMLINKY ===")
        resolve_symlinks()
    if what == "screenshots":
        print("=== SCREENSHOTY (Named_Snaps + Named_Titles) ===")
        fetch_screenshots()
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
