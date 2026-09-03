<div align="center">

# 🎮 RetroWeb

**Průvodce světem retro hraní** — historie herních platforem, jejich legendární hry
a hardware jako Anbernic RG35XX&nbsp;Pro, R36S a Batocera.

*A guide to the world of retro gaming — platform history, legendary games and hardware.*

`77 platforem` · `5520 her` · `100 % článků` · `90 % obrázků` · `🇨🇿 🇬🇧 🇩🇪 🇫🇷` · `Astro` · `static`

**🌐 Produkce (live):** [retrowebcz.netlify.app](https://retrowebcz.netlify.app) &nbsp;·&nbsp; **🧪 Náhled (GitHub Pages, noindex):** [mhudakcz.github.io/RetroWeb](https://mhudakcz.github.io/RetroWeb/)

</div>

---

## 🇨🇿 Česky

RetroWeb je statický web postavený v [Astro](https://astro.build), který z kurátorských
Markdown podkladů generuje přehledný katalog retro hraní:

- **Platformy** — 77 konzolí, handheldů a počítačů od Atari 2600 (1977) přes NES, Wii
  a PlayStation 2 až po PS5, Xbox Series a Switch 2, PC ve třech érách (DOS, Windows 9x,
  moderní), japonské počítače X68000 a PC-98 i kuriozity jako Virtual Boy, Vectrex,
  CD-i a fantasy konzole PICO-8 a TIC-80. Vedle strojů pokrývá i tři platformy bez krabice:
  **hry v prohlížeči** (Flash, portály, `.io` hry), **Java a Symbian** na tlačítkových
  telefonech a **mobil** (iOS a Android) od prvních App Store titulů po gachu.
  Každá platforma má dlouhý článek (technika, propojení, modely, klony vč. českých,
  dnešní scéna) prokládaný dobovými fotkami.
- **Čím začít** — u každé platformy výběr her, kterými má čtenář začít, s jednou větou proč
  právě ony. Celkem 768 doporučení na 76 platformách; velké platformy jich mají 18–20,
  malé čtyři. Výběr je zapuštěný přímo do článku o platformě.
- **Jazyky** — obsah ve **čtyřech jazycích**: 🇨🇿 čeština, 🇬🇧 angličtina, 🇩🇪 němčina
  a 🇫🇷 francouzština. Přepínač v hlavičce i patičce, hreflang a lokalizovaná sitemap pro SEO.
  Čeština je kompletní, překlady jsou hotové zhruba ze dvou třetin a průběžně dobíhají.
- **Hry** — 5520 titulů, **každý s magazínovým článkem**, úvodní větou a závěrečným
  „Proč hrát" (CZ). Žánr, délka hraní, počet hráčů 👥, obal a snímky ze hry. Katalog
  s hledáním a filtry (platforma, žánr, homebrew 🆓, must-play ⭐, logické 🧩, pro více
  hráčů). Postupné čtení (předchozí/další) u platforem i her, na mobilu i swipem.
- **Galerie** — jedna lightbox galerie na hru přes všechny její obrázky: šipky, miniatury,
  swipe na dotykových zařízeních a celočíselné zvětšování u pixel artu, aby nebyl rozmazaný.
- **Hraní v prohlížeči** — u webových her, které dodnes běží, přímý odkaz „Zahrát si online"
  (Wordle, 2048, Slither.io, Cookie Clicker, QWOP, RuneScape a další).
- **Hardware & emulace** — průvodci pro Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS i konzole, vč. CRT filtrů, scrapingu obrázků, hraní ve více lidech
  (netplay) a tabulek zkratek pro ukládání postupu a vyskočení ze hry.
- **Obrázky** — fotky konzolí z Wikimedia; obaly retro her z libretro-thumbnails (jako scrapuje
  Batocera), u moderních platforem ze Steamu a Nintendo eShopu, u mobilních z App Store.
  Chybějící tituly dohledávají **GOG** (stará PC vydání, která na Steamu nikdy nebyla),
  **ZXDB** (ZX Spectrum, které nevede žádný obchod), **itch.io** (prohlížečovky a homebrew)
  a infobox článku na Wikipedii. Většina her má kromě obalu i dva snímky ze hry; bez obalu
  se použije titulní obrazovka nebo emblém platformy. Vše optimalizované do WebP.
- **SEO** — sitemap, robots, kanonická doména, ověřená Google Search Console.

### Spuštění

```bash
npm install      # závislosti
npm run dev      # vývojový server → http://localhost:4321
npm run build    # statický web do dist/
```

### Obsah a obrázky

```bash
npm run data                             # MD podklady → dataset (Python 3)
python tools/fetch_images.py platforms   # fotky konzolí (Wikipedia)
python tools/fetch_images.py games       # obaly her (libretro-thumbnails)
python tools/fetch_images.py screenshots       # snímky z libretro (retro platformy)
python tools/fetch_images.py games-steam       # obaly moderních her (Steam, bez API klíče)
python tools/fetch_images.py games-steam-shots # dva snímky ze hry ze Steamu
python tools/fetch_images.py games-nintendo    # obaly z Nintendo eShopu
python tools/fetch_images.py games-appstore    # obaly a snímky mobilních her (App Store)
python tools/fetch_images.py games-gog         # obaly a snímky ze staršího PC (GOG)
python tools/fetch_images.py games-zxinfo      # ZX Spectrum (ZXDB / api.zxinfo.dk)
python tools/fetch_images.py games-itch        # itch.io (prohlížečovky, homebrew)
python tools/fetch_images.py games-wiki-box    # obaly z infoboxu na Wikipedii
python tools/fetch_images.py fallback-shots    # titulní obrazovka pro hry bez obalu
python tools/fetch_images.py symlinks    # dořeší GitHub symlinky
python tools/fetch_images.py optimize    # zmenší + převede na WebP
```

Po úpravě podkladů spusť `npm run data` a `npm run build`.

Zdroje se doplňují — každý pokrývá jinou část katalogu a jméno hry páruje přísně
(přesná shoda nebo povolená reedice), aby se ke hře nepřilepil cizí obrázek.

### Struktura

```
Podklady/extracted/      zdrojové MD soubory (historie + hry)
tools/parse_content.py   parser MD → JSON (fuzzy párování her)
tools/fetch_images.py    stahování + optimalizace obrázků
tools/picks_prep.py      výběr „Čím začít" pro platformy
tools/i18n_*.py          extrakce, dávkování a slučování překladů
src/data/                dataset.json + hardware.ts + platform_picks.json
src/components/          PlatformCard, GameCard, Lightbox, SwipeNav, HardwareArt …
src/pages/               domů, /platformy, /hry, /serie, /studia, /hardware, /zmeny
```

---

## 🇬🇧 English

RetroWeb is a static [Astro](https://astro.build) site that turns curated Markdown notes
into a browsable retro-gaming catalog:

- **Platforms** — 77 consoles, handhelds and computers from the Atari 2600 (1977) through the
  NES, Wii and PlayStation 2 to the PS5, Xbox Series and Switch 2, the PC across three eras
  (DOS, Windows 9x, modern), the Japanese X68000 and PC-98, oddities like the Virtual Boy,
  Vectrex and CD-i, and the PICO-8 / TIC-80 fantasy consoles. Alongside the machines it also
  covers three platforms that never came in a box: **browser games** (Flash, portals, `.io`
  games), **Java and Symbian** on pre-smartphone handsets, and **mobile** (iOS and Android)
  from the first App Store hits to gacha. Each platform has a long article (tech, links,
  models, clones, today's scene) interwoven with period photos.
- **Where to start** — every platform carries a shortlist of games to begin with and one line
  on why each one. 768 picks across 76 platforms: 18–20 for the big libraries, four for the
  smallest, set inside the platform article itself.
- **Languages** — content in **four languages**: 🇨🇿 Czech, 🇬🇧 English, 🇩🇪 German and
  🇫🇷 French. Switcher in header and footer, hreflang and a localized sitemap for SEO.
  Czech is complete; the translations are roughly two thirds done and still running.
- **Games** — 5520 titles, **every one with a magazine-style write-up**, a one-line summary
  and a closing "why play it". Genre, play-length, player count 👥, box art and in-game shots.
  Catalog with search and filters (platform, genre, homebrew 🆓, must-play ⭐, puzzle 🧩,
  multiplayer), plus prev/next reading navigation, by swipe on touch devices.
- **Gallery** — one lightbox per game across all of its images: arrows, thumbnails, swipe,
  and integer scaling for pixel art so it stays sharp.
- **Play in the browser** — web games that still run link straight to where to play them
  (Wordle, 2048, Slither.io, Cookie Clicker, QWOP, RuneScape and others).
- **Hardware & emulation** — guides for Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS and consoles, incl. CRT shaders, artwork scraping, multiplayer (netplay)
  and hotkey tables for saving progress and exiting a game.
- **Images** — console photos from Wikimedia; retro box art from libretro-thumbnails (the same
  source Batocera scrapes), modern-platform art from Steam and the Nintendo eShop, mobile from
  the App Store. The gaps are filled by **GOG** (older PC releases that never reached Steam),
  **ZXDB** (ZX Spectrum, carried by no store), **itch.io** (browser games and homebrew) and the
  article infobox on Wikipedia. Most games also carry two in-game shots; those without a cover
  fall back to a title screen or the platform emblem. All optimized to WebP.

```bash
npm install && npm run dev      # dev server at http://localhost:4321
npm run build                   # static output to dist/
```

> Czech content is complete: every game has an article, a summary line and a closing
> recommendation. Translations into English, German and French cover about two thirds of the
> catalog and are still being generated. Roughly one game in four has fewer than three images —
> mostly console exclusives no free source carries.

---

## ⚖️ Legálně / Legal

Web nenabízí žádné ROM soubory. Hry shánějte legálně — vlastní dumpy kazet a disků, nebo
homebrew/freeware (🆓). Fotografie konzolí pocházejí z Wikimedia Commons (volné licence);
obaly her z komunitní databáze libretro-thumbnails, z obchodů Steam, Nintendo eShop, App Store
a GOG, z databáze ZXDB, z itch.io a u zbylých titulů z Wikipedie — práva náleží příslušným
vydavatelům a slouží zde jen k identifikaci her ve fanouškovském katalogu.

*This site hosts no ROM files. Console photos are from Wikimedia Commons; box art from the
libretro-thumbnails community database, the Steam / Nintendo eShop / App Store / GOG stores,
the ZXDB database, itch.io and Wikipedia, used for identification only — rights belong to the
respective publishers.*

---

<div align="center">
<sub>Postaveno s Astro · Built with Astro · 🤖 vibe-coded with Claude Code</sub>
</div>
