<div align="center">

# 🎮 RetroWeb

**Průvodce světem retro hraní** — historie herních platforem, jejich legendární hry
a hardware jako Anbernic RG35XX&nbsp;Pro, R36S a Batocera.

*A guide to the world of retro gaming — platform history, legendary games and hardware.*

`67 platforem` · `3279 her` · `99 % článků` · `90 % obrázků` · `🇨🇿 🇬🇧 🇩🇪 🇫🇷` · `Astro` · `static`

**🌐 Produkce (live):** [retrowebcz.netlify.app](https://retrowebcz.netlify.app) &nbsp;·&nbsp; **🧪 Náhled (GitHub Pages, noindex):** [mhudakcz.github.io/RetroWeb](https://mhudakcz.github.io/RetroWeb/)

</div>

---

## 🇨🇿 Česky

RetroWeb je statický web postavený v [Astro](https://astro.build), který z kurátorských
Markdown podkladů generuje přehledný katalog retro hraní:

- **Platformy** — 67 konzolí, handheldů a počítačů od Atari 2600 (1977) přes NES, Wii
  a PlayStation 2 až po PS5, Xbox Series a Switch 2, PC ve třech érách (DOS, Windows 9x,
  moderní), japonské počítače X68000 a PC-98 i kuriozity jako Virtual Boy, Vectrex,
  CD-i a fantasy konzole PICO-8 a TIC-80. Každá má dlouhý článek (technika, propojení, modely,
  klony vč. českých, dnešní scéna) prokládaný dobovými fotkami.
- **Jazyky** — kompletní obsah ve **čtyřech jazycích**: 🇨🇿 čeština, 🇬🇧 angličtina, 🇩🇪 němčina
  a 🇫🇷 francouzština. Přepínač v hlavičce i patičce, hreflang a lokalizovaná sitemap pro SEO.
- **Hry** — 3279 titulů, **99 % s magazínovým článkem** a jednou úvodní větou u každé (CZ). Žánr, délka hraní, počet
  hráčů 👥, obal/screenshoty. Katalog s hledáním a filtry (platforma, žánr, homebrew 🆓,
  must-play ⭐, logické 🧩, pro více hráčů). Postupné čtení (předchozí/další) u platforem i her.
- **Hardware & emulace** — průvodci pro Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS i konzole, vč. CRT filtrů, scrapingu obrázků a hraní ve více lidech (netplay).
- **Obrázky** — fotky konzolí z Wikimedia, obaly retro her z libretro-thumbnails (jako scrapuje
  Batocera), u moderních platforem ze Steamu a Nintendo eShopu; u konzolových exkluzivit,
  které nejsou nikde v obchodech, z infoboxu článku na Wikipedii.
  Kromě obalu má většina her i dva snímky ze hry; bez obalu se použije titulní obrazovka
  nebo emblém platformy. Vše optimalizované do WebP.
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
python tools/fetch_images.py games-steam # obaly moderních her (Steam, bez API klíče)
python tools/fetch_images.py games-nintendo    # obaly z Nintendo eShopu
python tools/fetch_images.py games-steam-shots # dva snímky ze hry ze Steamu
python tools/fetch_images.py games-wiki-box    # obaly z infoboxu na Wikipedii
python tools/fetch_images.py screenshots       # snímky z libretro (retro platformy)
python tools/fetch_images.py symlinks    # dořeší GitHub symlinky
python tools/fetch_images.py optimize    # zmenší + převede na WebP
```

Po úpravě podkladů spusť `npm run data` a `npm run build`.

### Struktura

```
Podklady/extracted/      zdrojové MD soubory (historie + hry)
tools/parse_content.py   parser MD → JSON (fuzzy párování her)
tools/fetch_images.py    stahování + optimalizace obrázků
src/data/                dataset.json + hardware.ts
src/components/           PlatformCard, GameCard, PlatformEmblem, HardwareArt …
src/pages/               domů, /platformy, /hry, /serie, /studia, /hardware, /zmeny
```

---

## 🇬🇧 English

RetroWeb is a static [Astro](https://astro.build) site that turns curated Markdown notes
into a browsable retro-gaming catalog:

- **Platforms** — 67 consoles, handhelds and computers from the Atari 2600 (1977) through the
  NES, Wii and PlayStation 2 to the PS5, Xbox Series and Switch 2, the PC across three eras
  (DOS, Windows 9x, modern), the Japanese X68000 and PC-98, oddities like the Virtual Boy,
  Vectrex and CD-i, and the PICO-8 / TIC-80 fantasy consoles, each with a long article (tech, links,
  models, clones, today's scene) interwoven with period photos.
- **Languages** — full content in **four languages**: 🇨🇿 Czech, 🇬🇧 English, 🇩🇪 German and
  🇫🇷 French. Switcher in header and footer, hreflang and a localized sitemap for SEO.
- **Games** — 3279 titles, **99 % with a magazine-style write-up** and a one-line summary each. Genre, play-length,
  player count 👥, box art / screenshots. Catalog with search and filters (platform, genre,
  homebrew 🆓, must-play ⭐, puzzle 🧩, multiplayer), plus prev/next reading navigation.
- **Hardware & emulation** — guides for Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS and consoles, incl. CRT shaders, artwork scraping and multiplayer (netplay).
- **Images** — console photos from Wikimedia, retro box art from libretro-thumbnails (the same
  source Batocera scrapes), modern-platform box art from Steam and the Nintendo eShop, and —
  for console exclusives carried by no store — the cover from the article infobox on Wikipedia. Most games also carry two in-game shots; those without a cover
  fall back to a title screen or the platform emblem. All optimized to WebP.

```bash
npm install && npm run dev      # dev server at http://localhost:4321
npm run build                   # static output to dist/
```

> Per-game articles, the localized UI and all four translations are done. Games for the
> newest platforms are still being written.

---

## ⚖️ Legálně / Legal

Web nenabízí žádné ROM soubory. Hry shánějte legálně — vlastní dumpy kazet a disků, nebo
homebrew/freeware (🆓). Fotografie konzolí pocházejí z Wikimedia Commons (volné licence);
obaly her z komunitní databáze libretro-thumbnails, z obchodů Steam a Nintendo eShop a u zbylých
titulů z Wikipedie — práva náleží příslušným vydavatelům a slouží zde jen k identifikaci her
ve fanouškovském katalogu.

*This site hosts no ROM files. Console photos are from Wikimedia Commons; box art from the
libretro-thumbnails community database, the Steam / Nintendo eShop stores and Wikipedia,
used for identification only — rights belong to the respective publishers.*

---

<div align="center">
<sub>Postaveno s Astro · Built with Astro · 🤖 vibe-coded with Claude Code</sub>
</div>
