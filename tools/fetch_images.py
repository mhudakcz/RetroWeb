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
}

# ---- platforma -> libretro-thumbnails repo (boxarty) ----
LIBRETRO = {
    "game-boy": "Nintendo_-_Game_Boy",
    "game-boy-color": "Nintendo_-_Game_Boy_Color",
    "game-boy-advance": "Nintendo_-_Game_Boy_Advance",
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
    # game-watch / pico-8 / tic-80: bez libretro boxartů -> emblém zůstane
}

# regiony, které preferujeme při výběru z více variant boxartu
REGION_PREF = ["(USA)", "(World)", "(USA, Europe)", "(Europe)", "(Japan, USA)", "(Japan)"]


def http_get(url, headers=None, retries=3, timeout=40):
    """Stažení přes curl (používá Windows cert store; Python urllib má prošlý CA bundle)."""
    cmd = ["curl", "-sL", "--fail", "--max-time", str(timeout), "-A", UA]
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


# ----------------------------------------------------------------- hry
def list_boxarts(repo):
    """Vrátí list názvů souborů (bez .png) ve složce Named_Boxarts daného repa."""
    for branch in ("master", "main"):
        # zkus rekurzivní strom
        try:
            tree = gh_api(f"/repos/libretro-thumbnails/{repo}/git/trees/{branch}?recursive=1")
            if not tree.get("truncated"):
                files = [
                    os.path.basename(t["path"])[:-4]
                    for t in tree.get("tree", [])
                    if t["path"].startswith("Named_Boxarts/") and t["path"].endswith(".png")
                ]
                if files:
                    return files
        except Exception:  # noqa
            pass
        # fallback: root -> Named_Boxarts sha -> jeho strom
        try:
            root = gh_api(f"/repos/libretro-thumbnails/{repo}/git/trees/{branch}")
            sha = next(
                (t["sha"] for t in root.get("tree", []) if t["path"] == "Named_Boxarts"), None
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
        jobs = []
        for g in games:
            fn = best_boxart(g["name"], names, idx)
            if fn:
                jobs.append((g["slug"], fn))
        grand_total += len(games)

        def dl(job):
            gslug, fn = job
            dest = out / f"{gslug}.png"
            if dest.exists() and dest.stat().st_size > 2048:
                return True  # už staženo
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


def resolve_symlinks():
    """Některé položky v libretro repech jsou symlinky: stažený 'soubor' obsahuje
    jen cílový název .png. Dořeší je: stáhne skutečný obrázek a převede na WebP."""
    from PIL import Image

    gdir = IMG / "games"
    leftovers = list(gdir.rglob("*.png"))
    print(f"Symlink kandidátů (.png): {len(leftovers)}")
    fixed = dropped = 0
    for p in leftovers:
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
