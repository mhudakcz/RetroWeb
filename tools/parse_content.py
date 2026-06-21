# -*- coding: utf-8 -*-
"""
Parser podkladových Markdown souborů -> strukturovaný JSON dataset pro web.

Vstup (Podklady/extracted/):
  - retro-hry-batocera.md        : kanonický seznam her dle platforem (žánr, délka, flagy)
  - retro-hry-pruvodce-plus.md   : detailní komentář (žánr · rok · studio + odstavec)
  - retro-hry-pruvodce.md        : krátký teaser
  - retro-platformy-pruvodce.md  : historie platforem

Výstup: src/data/dataset.json
"""
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Podklady" / "extracted"
OUT = ROOT / "src" / "data" / "dataset.json"
PUBLIC_IMG = ROOT / "public" / "images"
ARTICLES_DIR = ROOT / "src" / "data" / "articles"
PLATFORM_ARTICLES_DIR = ROOT / "src" / "data" / "platform_articles"


def platform_long_article(slug):
    """Dlouhý článek o platformě (přepíše historii z MD), pokud existuje."""
    f = PLATFORM_ARTICLES_DIR / f"{slug}.md"
    if f.exists():
        txt = f.read_text(encoding="utf-8").strip()
        if txt:
            return txt
    return None
IMG_EXTS = (".webp", ".jpg", ".jpeg", ".png", ".gif", ".svg")


def load_articles():
    """Načte dlouhé „magazínové" články ze src/data/articles/*.json (slug -> markdown)."""
    out = {}
    if ARTICLES_DIR.exists():
        for f in sorted(ARTICLES_DIR.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                for slug, md in data.items():
                    if md and md.strip():
                        out[slug] = md.strip()
            except Exception as e:  # noqa
                print(f"  [x] článek {f.name}: {e}")
    return out


def find_image(subdir, stem):
    """Vrátí veřejnou cestu /images/... pokud obrázek se zadaným jménem existuje."""
    d = PUBLIC_IMG / subdir
    for ext in IMG_EXTS:
        if (d / f"{stem}{ext}").exists():
            return f"/images/{subdir}/{stem}{ext}".replace("\\", "/")
    return None

# ---------------------------------------------------------------------------
# Registr platforem: slug, název, metadata, barvy a aliasy nadpisů (z obou souborů).
# Pořadí = pořadí na webu. type: handheld | console | computer | arcade | fantasy
# ---------------------------------------------------------------------------
PLATFORMS = [
    dict(slug="game-boy", name="Nintendo Game Boy", short="GB", maker="Nintendo",
         year=1989, type="handheld", color="#7e8f2d", color2="#1c2a10",
         aliases=["Nintendo Game Boy (GB)"]),
    dict(slug="game-boy-color", name="Game Boy Color", short="GBC", maker="Nintendo",
         year=1998, type="handheld", color="#8e54b0", color2="#3a1f52",
         aliases=["Nintendo Game Boy Color (GBC)"]),
    dict(slug="game-boy-advance", name="Game Boy Advance", short="GBA", maker="Nintendo",
         year=2001, type="handheld", color="#5b4fd6", color2="#241f63",
         aliases=["Nintendo Game Boy Advance (GBA)"]),
    dict(slug="nes", name="Nintendo NES", short="NES", maker="Nintendo",
         year=1983, type="console", color="#b8302a", color2="#3a1413",
         aliases=["Nintendo NES / Famicom", "Nintendo Entertainment System (NES / Famicom)"]),
    dict(slug="snes", name="Super Nintendo", short="SNES", maker="Nintendo",
         year=1990, type="console", color="#5b4b9e", color2="#272040",
         aliases=["Super Nintendo / Super Famicom (SNES)", "Super Nintendo (SNES / Super Famicom)"]),
    dict(slug="mega-drive", name="SEGA Mega Drive", short="MD", maker="SEGA",
         year=1988, type="console", color="#d23030", color2="#1a1a1a",
         aliases=["SEGA Mega Drive / Genesis"]),
    dict(slug="master-system", name="SEGA Master System", short="SMS", maker="SEGA",
         year=1985, type="console", color="#b62a2a", color2="#2a1010",
         aliases=["SEGA Master System"]),
    dict(slug="game-gear", name="SEGA Game Gear", short="GG", maker="SEGA",
         year=1990, type="handheld", color="#2f76b8", color2="#15263a",
         aliases=["SEGA Game Gear"]),
    dict(slug="atari-lynx", name="Atari Lynx", short="Lynx", maker="Atari",
         year=1989, type="handheld", color="#e6a417", color2="#3a2a08",
         aliases=["Atari Lynx"]),
    dict(slug="saturn", name="SEGA Saturn", short="Saturn", maker="SEGA",
         year=1994, type="console", color="#3f47a0", color2="#1c1f44",
         aliases=["SEGA Saturn"]),
    dict(slug="playstation", name="Sony PlayStation", short="PS1", maker="Sony",
         year=1994, type="console", color="#4a4f70", color2="#1f2130",
         aliases=["Sony PlayStation (PS1)"]),
    dict(slug="psp", name="Sony PSP", short="PSP", maker="Sony",
         year=2004, type="handheld", color="#3a6fd6", color2="#161b2e",
         aliases=["Sony PSP"]),
    dict(slug="n64", name="Nintendo 64", short="N64", maker="Nintendo",
         year=1996, type="console", color="#3b9c5a", color2="#163a23",
         aliases=["Nintendo 64"]),
    dict(slug="arcade", name="Arcade", short="MAME", maker="různí (MAME / FBNeo)",
         year=1979, type="arcade", color="#e3357a", color2="#3a0f24",
         aliases=["Arcade (MAME / FBNeo)"]),
    dict(slug="neogeo", name="SNK Neo Geo", short="Neo Geo", maker="SNK",
         year=1990, type="arcade", color="#e0b53d", color2="#2e2406",
         aliases=[]),
    dict(slug="cps", name="Capcom CPS", short="CPS", maker="Capcom",
         year=1988, type="arcade", color="#2f7ad6", color2="#0f2540",
         aliases=[]),
    dict(slug="pc-engine", name="PC Engine / TurboGrafx-16", short="PCE", maker="NEC",
         year=1987, type="console", color="#e8731e", color2="#3a1d08",
         aliases=["TurboGrafx-16 / PC Engine (+ CD)", "NEC TurboGrafx-16 / PC Engine"]),
    dict(slug="dreamcast", name="SEGA Dreamcast", short="DC", maker="SEGA",
         year=1998, type="console", color="#e85d1a", color2="#2a1408",
         aliases=["SEGA Dreamcast"]),
    dict(slug="zx81", name="Sinclair ZX81", short="ZX81", maker="Sinclair",
         year=1981, type="computer", color="#9aa0b4", color2="#16181f",
         aliases=[]),
    dict(slug="zx-spectrum", name="ZX Spectrum", short="ZX", maker="Sinclair",
         year=1982, type="computer", color="#d11e2a", color2="#2a0a0c",
         aliases=["ZX Spectrum"]),
    dict(slug="amstrad-cpc", name="Amstrad CPC", short="CPC", maker="Amstrad",
         year=1984, type="computer", color="#2f63a8", color2="#13243a",
         aliases=["Amstrad CPC"]),
    dict(slug="msx", name="MSX / MSX2", short="MSX", maker="MSX standard",
         year=1983, type="computer", color="#cc2b2b", color2="#2a0e0e",
         aliases=["MSX / MSX2"]),
    dict(slug="colecovision", name="ColecoVision", short="Coleco", maker="Coleco",
         year=1982, type="console", color="#2f50a0", color2="#141d3a",
         aliases=["ColecoVision"]),
    dict(slug="intellivision", name="Intellivision", short="INTV", maker="Mattel",
         year=1979, type="console", color="#b8862a", color2="#2e2208",
         aliases=[]),
    dict(slug="jaguar", name="Atari Jaguar", short="Jaguar", maker="Atari",
         year=1993, type="console", color="#c0392b", color2="#2a100c",
         aliases=[]),
    dict(slug="amiga-cd32", name="Amiga CD32", short="CD32", maker="Commodore",
         year=1993, type="console", color="#b03a5b", color2="#2a0f1a",
         aliases=[]),
    dict(slug="atari-2600", name="Atari 2600", short="2600", maker="Atari",
         year=1977, type="console", color="#c0532f", color2="#3a1a0e",
         aliases=["Atari 2600 / 7800"]),
    dict(slug="atari-5200", name="Atari 5200", short="5200", maker="Atari",
         year=1982, type="console", color="#b0481f", color2="#33140a",
         aliases=[]),
    dict(slug="atari-7800", name="Atari 7800", short="7800", maker="Atari",
         year=1986, type="console", color="#cf6033", color2="#3a1a0e",
         aliases=[]),
    dict(slug="atari-8bit", name="Atari 800 / 8-bit", short="A800", maker="Atari",
         year=1979, type="computer", color="#2f76b0", color2="#142a3a",
         aliases=["Atari 800 / 8-bit (XL/XE)"]),
    dict(slug="vic20", name="Commodore VIC-20", short="VIC-20", maker="Commodore",
         year=1980, type="computer", color="#6a8ad0", color2="#1f2747",
         aliases=[]),
    dict(slug="c64", name="Commodore 64", short="C64", maker="Commodore",
         year=1982, type="computer", color="#5a72c0", color2="#1f2747",
         aliases=["Commodore 64 (C64)"]),
    dict(slug="amiga", name="Commodore Amiga", short="Amiga", maker="Commodore",
         year=1985, type="computer", color="#c0392b", color2="#2a100c",
         aliases=["Commodore Amiga"]),
    dict(slug="atari-st", name="Atari ST", short="ST", maker="Atari",
         year=1985, type="computer", color="#2f76b0", color2="#142a3a",
         aliases=[]),
    dict(slug="game-watch", name="Nintendo Game & Watch", short="G&W", maker="Nintendo",
         year=1980, type="handheld", color="#b0902a", color2="#332808",
         aliases=["Nintendo Game & Watch"]),
    dict(slug="pico-8", name="PICO-8", short="PICO-8", maker="Lexaloffle (fantasy konzole)",
         year=2015, type="fantasy", color="#ff004d", color2="#3a0013",
         aliases=["PICO-8 (fantasy konzole)", "Fantasy konzole — PICO-8 a TIC-80",
                  "Fantasy konzole — PICO-8 & TIC-80"]),
    dict(slug="tic-80", name="TIC-80", short="TIC-80", maker="Nesbox (fantasy konzole)",
         year=2017, type="fantasy", color="#e23b6d", color2="#3a0f1d",
         aliases=["TIC-80 (fantasy konzole)", "Fantasy konzole — PICO-8 a TIC-80",
                  "Fantasy konzole — PICO-8 & TIC-80"]),
]

# Přeřazení her z původní (sloučené) platformy na novou (po rozdělení).
# Klíč = původní slug hry, hodnota = cílová platforma.
REASSIGN = {
    # Arcade -> Neo Geo (SNK)
    "arcade__metal-slug-1-x-3": "neogeo",
    "arcade__king-of-fighters-98-2002": "neogeo",
    "arcade__garou-mark-of-wolves": "neogeo",
    "arcade__samurai-shodown-ii": "neogeo",
    "arcade__last-blade-2": "neogeo",
    "arcade__money-puzzle-exchanger": "neogeo",
    "arcade__magical-drop-ii-iii": "neogeo",
    "arcade__aero-fighters-2": "neogeo",
    "arcade__neo-turf-masters": "neogeo",
    "arcade__windjammers": "neogeo",
    "arcade__shock-troopers": "neogeo",
    "arcade__puzzle-bobble-bust-move": "neogeo",
    # Arcade -> Capcom CPS
    "arcade__street-fighter-iii-3rd-strike": "cps",
    "arcade__street-fighter-alpha-3": "cps",
    "arcade__marvel-vs-capcom": "cps",
    "arcade__x-men-children-of-atom": "cps",
    "arcade__capcom-vs-snk-2": "cps",
    "arcade__cadillacs-and-dinosaurs": "cps",
    "arcade__alien-vs-predator": "cps",
    "arcade__punisher": "cps",
    "arcade__dungeons-and-dragons-shadow-over-mystara": "cps",
    "arcade__final-fight": "cps",
    "arcade__captain-commando": "cps",
    "arcade__knights-of-round": "cps",
    "arcade__street-fighter-ii-world-warrior": "cps",
    "arcade__street-fighter-ii-hyper-fighting": "cps",
    "arcade__alien-progear": "cps",
    # Atari 2600 -> 7800
    "atari-2600__ninja-golf": "atari-7800",
    "atari-2600__food-fight": "atari-7800",
    "atari-2600__galaga": "atari-7800",
}


def slugs_for_heading(heading):
    """Vrátí všechny slugy platforem, jejichž alias odpovídá nadpisu (kvůli sdíleným sekcím)."""
    return [p["slug"] for p in PLATFORMS if heading in p["aliases"]]

FLAG_MAP = {
    "🆓": "homebrew",   # legálně zdarma
    "⭐": "mustplay",   # moderní must-play
    "🔞": "mature",     # dospělejší
    "🧩": "puzzle",     # logická
}
FLAG_CHARS = "".join(FLAG_MAP.keys())


# ---------------------------------------------------------------------------
# Pomocné funkce
# ---------------------------------------------------------------------------
def read(name):
    return (SRC / name).read_text(encoding="utf-8")


def strip_emoji(s):
    return "".join(ch for ch in s if ch not in FLAG_CHARS).strip()


def norm_name(s):
    """Normalizace názvu hry pro párování."""
    s = strip_emoji(s)
    s = s.replace("’", "'").replace("`", "'")
    # odstranit závorky a jejich obsah
    s = re.sub(r"\([^)]*\)", " ", s)
    # diakritika -> ascii
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    # sjednotit oddělovače
    s = s.replace("&", " and ")
    s = re.sub(r"[/:+\-–—.,!?'\"]", " ", s)
    s = re.sub(r"\b(the|a|an)\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokens(s):
    return set(norm_name(s).split())


def match_metrics(a, b):
    """Vrátí (score, contain, jac, seq) pro dvojici názvů."""
    na, nb = norm_name(a), norm_name(b)
    if not na or not nb:
        return 0.0, False, 0.0, 0.0
    if na == nb:
        return 1.0, True, 1.0, 1.0
    contain = na in nb or nb in na
    ta, tb = tokens(a), tokens(b)
    jac = len(ta & tb) / len(ta | tb) if (ta and tb) else 0.0
    seq = SequenceMatcher(None, na, nb).ratio()
    score = 0.93 if contain else max(jac, seq)
    return score, contain, jac, seq


def similarity(a, b):
    return match_metrics(a, b)[0]


def acceptable(a, b):
    """Brání falešným shodám sourozeneckých titulů (stejná série, jiný díl).
    Přijmi jen containment, slušný token-overlap, nebo velmi vysoké seq."""
    _, contain, jac, seq = match_metrics(a, b)
    return contain or jac >= 0.5 or seq >= 0.82


def split_sections(text):
    """Rozdělí MD na sekce dle '## ' nadpisů. Vrátí list (heading, body)."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    # parts[0] = preambule; pak střídavě heading, body
    out = []
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1]))
    return out


# ---------------------------------------------------------------------------
# Parsování jednotlivých souborů do mezistruktur dle platformy
# ---------------------------------------------------------------------------
def parse_batocera():
    """slug -> list her: {name, genre, length, flags, order}"""
    text = read("retro-hry-batocera.md")
    result = {}
    line_re = re.compile(r"^\d+\.\s+(.*)$")
    for heading, body in split_sections(text):
        slugs = slugs_for_heading(heading)
        if not slugs:
            continue
        games = []
        for line in body.splitlines():
            m = line_re.match(line.strip())
            if not m:
                continue
            entry = m.group(1).strip()
            # rozdělit "Název [flagy] — *Žánr* · ⏱ X"
            # oddělovač název/zbytek je " — " (em dash) nebo " - "
            name_part, sep, rest = entry.partition(" — ")
            if not sep:
                name_part, sep, rest = entry.partition(" – ")
            flags = [FLAG_MAP[c] for c in name_part if c in FLAG_MAP]
            name = strip_emoji(name_part)
            genre = None
            length = None
            gm = re.search(r"\*([^*]+)\*", rest)
            if gm:
                genre = gm.group(1).strip()
            lm = re.search(r"⏱\s*(XL|L|M|S)", rest)
            if lm:
                length = lm.group(1)
            if name:
                games.append(dict(name=name, genre=genre, length=length,
                                  flags=flags, order=len(games)))
        for slug in slugs:
            if games:
                result.setdefault(slug, []).extend(games)
    return result


def parse_plus():
    """slug -> list {name, genre, year, studio, detail, est}"""
    text = read("retro-hry-pruvodce-plus.md")
    result = {}
    # hlavička: **Název** — *Žánr · rok · studio* — odstavec ... *(⏱ cca X)*
    line_re = re.compile(r"^\*\*(.+?)\*\*\s*[—–-]\s*(.*)$")
    for heading, body in split_sections(text):
        slugs = slugs_for_heading(heading)
        if not slugs:
            continue
        games = []
        for line in body.splitlines():
            line = line.strip()
            m = line_re.match(line)
            if not m:
                continue
            name = m.group(1).strip()
            rest = m.group(2).strip()
            genre = year = studio = None
            est = None
            meta_m = re.match(r"\*([^*]+)\*\s*[—–-]?\s*(.*)$", rest)
            detail = rest
            if meta_m:
                meta = meta_m.group(1).strip()
                detail = meta_m.group(2).strip()
                # meta = "Žánr · rok · studio"
                bits = [b.strip() for b in re.split(r"·", meta)]
                if bits:
                    genre = bits[0]
                if len(bits) >= 2:
                    year = bits[1]
                if len(bits) >= 3:
                    studio = " · ".join(bits[2:])
            em = re.search(r"\*\(⏱([^)]*)\)\*", detail)
            if em:
                est = em.group(1).replace("cca", "").strip()
                detail = detail[:em.start()].strip()
            games.append(dict(name=name, genre=genre, year=year, studio=studio,
                              detail=detail, est=est))
        for slug in slugs:
            if games:
                result.setdefault(slug, []).extend(games)
    return result


def parse_short():
    """slug -> list {name, teaser}"""
    text = read("retro-hry-pruvodce.md")
    result = {}
    line_re = re.compile(r"^-\s+\*\*(.+?)\*\*\s*[—–-]\s*(.*)$")
    for heading, body in split_sections(text):
        slugs = slugs_for_heading(heading)
        if not slugs:
            continue
        games = []
        for line in body.splitlines():
            m = line_re.match(line.strip())
            if not m:
                continue
            games.append(dict(name=m.group(1).strip(), teaser=m.group(2).strip()))
        for slug in slugs:
            if games:
                result.setdefault(slug, []).extend(games)
    return result


def parse_platform_history():
    """slug -> historie (markdown odstavce)"""
    text = read("retro-platformy-pruvodce.md")
    result = {}
    for heading, body in split_sections(text):
        slugs = slugs_for_heading(heading)
        if not slugs:
            continue
        history = body.strip()
        # odstranit koncové '---'
        history = re.sub(r"\n-{3,}\s*$", "", history).strip()
        for s in slugs:
            result[s] = history
    return result


def best_match(name, candidates, used, threshold=0.62):
    """Najde nejlepší dosud nepoužitý kandidát."""
    best_i, best_score = -1, 0.0
    for i, c in enumerate(candidates):
        if i in used:
            continue
        sc = similarity(name, c["name"])
        if sc > best_score:
            best_score, best_i = sc, i
    if best_i >= 0 and best_score >= threshold and acceptable(name, candidates[best_i]["name"]):
        return best_i, best_score
    return -1, 0.0


# ---------------------------------------------------------------------------
# Sestavení datasetu
# ---------------------------------------------------------------------------
def slugify_game(platform_slug, name, idx):
    # jen bezpečné znaky pro URL i názvy složek (Windows)
    base = re.sub(r"[^a-z0-9]+", "-", norm_name(name)).strip("-") or f"hra-{idx}"
    return f"{platform_slug}__{base}"


def build():
    bato = parse_batocera()
    plus = parse_plus()
    short = parse_short()
    history = parse_platform_history()
    articles = load_articles()
    bg_file = ROOT / "src" / "data" / "platform_bg.json"
    platform_bg = json.loads(bg_file.read_text(encoding="utf-8")) if bg_file.exists() else {}
    extra_file = ROOT / "src" / "data" / "extra_games.json"
    extra = json.loads(extra_file.read_text(encoding="utf-8")) if extra_file.exists() else {}
    links_file = ROOT / "src" / "data" / "game_links.json"
    game_links = json.loads(links_file.read_text(encoding="utf-8")) if links_file.exists() else {}
    play_file = ROOT / "src" / "data" / "game_play.json"
    game_play = json.loads(play_file.read_text(encoding="utf-8")) if play_file.exists() else {}

    platforms_out = []
    total_games = 0
    matched_detail = 0
    matched_teaser = 0

    # surové hry per platforma (batocera + doplňkové)
    raw_by_platform = {}
    for p in PLATFORMS:
        slug = p["slug"]
        lst = list(bato.get(slug, []))
        for eg in extra.get(slug, []):
            lst.append(dict(name=eg["name"], genre=eg.get("genre"),
                            length=eg.get("length"), flags=eg.get("flags", []),
                            order=len(lst)))
        raw_by_platform[slug] = lst

    # přeřazení her na nové platformy (rozdělení Arcade/Atari) + remap slugů
    slug_remap = {}
    for src_slug in list(raw_by_platform.keys()):
        keep = []
        for g in raw_by_platform[src_slug]:
            old = slugify_game(src_slug, g["name"], g["order"])
            tgt = REASSIGN.get(old)
            if tgt and tgt in raw_by_platform:
                g = dict(g, order=len(raw_by_platform[tgt]))
                raw_by_platform[tgt].append(g)
                slug_remap[old] = slugify_game(tgt, g["name"], g["order"])
            else:
                keep.append(g)
        raw_by_platform[src_slug] = keep

    # přemapuj články a odkazy na nové slugy
    for old, new in slug_remap.items():
        if old in articles:
            articles[new] = articles[old]
        if old in game_links:
            game_links[new] = game_links[old]
        if old in game_play:
            game_play[new] = game_play[old]
    (ROOT / "src" / "data" / "slug_remap.json").write_text(
        json.dumps(slug_remap, ensure_ascii=False, indent=2), encoding="utf-8")

    for p in PLATFORMS:
        slug = p["slug"]
        games_raw = raw_by_platform.get(slug, [])
        plus_list = plus.get(slug, [])
        short_list = short.get(slug, [])
        used_plus, used_short = set(), set()

        games = []
        seen_gslugs = {}
        for g in games_raw:
            pi, _ = best_match(g["name"], plus_list, used_plus)
            si, _ = best_match(g["name"], short_list, used_short)
            detail = year = studio = est = teaser = None
            genre = g["genre"]
            if pi >= 0:
                used_plus.add(pi)
                pd = plus_list[pi]
                detail = pd["detail"] or None
                year = pd["year"]
                studio = pd["studio"]
                est = pd["est"]
                if not genre and pd["genre"]:
                    genre = pd["genre"]
                matched_detail += 1
            if si >= 0:
                used_short.add(si)
                teaser = short_list[si]["teaser"] or None
                matched_teaser += 1

            gslug = slugify_game(slug, g["name"], g["order"])
            if gslug in seen_gslugs:
                seen_gslugs[gslug] += 1
                gslug = f"{gslug}-{seen_gslugs[gslug]}"
            else:
                seen_gslugs[gslug] = 1

            sub = f"games/{slug}"
            gallery = []
            for suffix, label, kind in (("", "Obal", "box"),
                                        ("-snap", "Ze hry", "snap"),
                                        ("-title", "Titulní obrazovka", "title")):
                src = find_image(sub, f"{gslug}{suffix}")
                if src:
                    gallery.append(dict(src=src, label=label, kind=kind))

            games.append(dict(
                slug=gslug, name=g["name"], genre=genre, length=g["length"],
                flags=g["flags"], year=year, studio=studio, est=est,
                teaser=teaser, detail=detail,
                article=articles.get(gslug),
                image=find_image(sub, gslug),
                gallery=gallery,
                link=game_links.get(gslug),
                playUrl=game_play.get(gslug),
            ))
            total_games += 1

        platforms_out.append(dict(
            slug=slug, name=p["name"], short=p["short"], maker=p["maker"],
            year=p["year"], type=p["type"], color=p["color"], color2=p["color2"],
            image=find_image("platforms", slug),
            photoBg=platform_bg.get(slug, "dark"),
            history=platform_long_article(slug) or history.get(slug),
            gameCount=len(games), games=games,
        ))

    games_with_img = sum(1 for po in platforms_out for g in po["games"] if g["image"])
    plats_with_img = sum(1 for po in platforms_out if po["image"])
    games_with_article = sum(1 for po in platforms_out for g in po["games"] if g["article"])
    dataset = dict(
        platforms=platforms_out,
        stats=dict(
            platforms=len(platforms_out),
            games=total_games,
            withDetail=matched_detail,
            withTeaser=matched_teaser,
            withArticle=games_with_article,
            platformImages=plats_with_img,
            gameImages=games_with_img,
        ),
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")

    # report
    print(f"Platforem: {len(platforms_out)}")
    print(f"Her celkem: {total_games}")
    print(f"  s detailním komentářem: {matched_detail} ({100*matched_detail//max(1,total_games)} %)")
    print(f"  s krátkým teaserem:     {matched_teaser}")
    print(f"  obrázky platforem: {plats_with_img}/{len(platforms_out)}")
    print(f"  obrázky her:       {games_with_img}/{total_games}")
    print("\nPokrytí detailem dle platformy:")
    for po in platforms_out:
        no_detail = [g["name"] for g in po["games"] if not g["detail"]]
        if po["gameCount"]:
            pct = 100 * (po["gameCount"] - len(no_detail)) // po["gameCount"]
            print(f"  {po['slug']:16s} {po['gameCount']:3d} her, detail {pct:3d}%")
    print(f"\nULOŽENO: {OUT}")


if __name__ == "__main__":
    build()
