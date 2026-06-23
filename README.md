<div align="center">

# 🎮 RetroWeb

**Průvodce světem retro hraní** — historie herních platforem, jejich legendární hry
a hardware jako Anbernic RG35XX&nbsp;Pro, R36S a Batocera.

*A guide to the world of retro gaming — platform history, legendary games and hardware.*

`38 platforem` · `1363 her` · `100 % článků` · `88 % obrázků` · `Astro` · `static`

</div>

---

## 🇨🇿 Česky

RetroWeb je statický web postavený v [Astro](https://astro.build), který z kurátorských
Markdown podkladů generuje přehledný katalog retro hraní:

- **Platformy** — 38 konzolí, handheldů a počítačů od Atari 2600 (1977) přes Nintendo DS
  po fantasy konzole PICO-8 a TIC-80. Každá má dlouhý článek (technika, propojení, modely,
  klony vč. českých, dnešní scéna) prokládaný dobovými fotkami.
- **Hry** — 1363 titulů, **100 % s magazínovým článkem** (CZ). Žánr, délka hraní, počet
  hráčů 👥, obal/screenshoty. Katalog s hledáním a filtry (platforma, žánr, homebrew 🆓,
  must-play ⭐, logické 🧩, pro více hráčů). Postupné čtení (předchozí/další) u platforem i her.
- **Hardware & emulace** — průvodci pro Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS i konzole, vč. CRT filtrů, scrapingu obrázků a hraní ve více lidech (netplay).
- **Obrázky** — fotky konzolí z Wikimedia, obaly her z libretro-thumbnails (jako scrapuje
  Batocera), u her bez obalu fallback na titulní obrazovku, vše optimalizované do WebP.
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
src/pages/               domů, /platformy, /hry, /hardware, /o-projektu
```

---

## 🇬🇧 English

RetroWeb is a static [Astro](https://astro.build) site that turns curated Markdown notes
into a browsable retro-gaming catalog:

- **Platforms** — 38 consoles, handhelds and computers from the Atari 2600 (1977) through the
  Nintendo DS to the PICO-8 / TIC-80 fantasy consoles, each with a long article (tech, links,
  models, clones, today's scene) interwoven with period photos.
- **Games** — 1363 titles, **100 % with a magazine-style write-up** (Czech). Genre, play-length,
  player count 👥, box art / screenshots. Catalog with search and filters (platform, genre,
  homebrew 🆓, must-play ⭐, puzzle 🧩, multiplayer), plus prev/next reading navigation.
- **Hardware & emulation** — guides for Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS and consoles, incl. CRT shaders, artwork scraping and multiplayer (netplay).
- **Images** — console photos from Wikimedia, game box art from libretro-thumbnails (the same
  source Batocera scrapes), with a title-screen fallback for boxart-less games, optimized to WebP.

```bash
npm install && npm run dev      # dev server at http://localhost:4321
npm run build                   # static output to dist/
```

> Per-game articles are done (100 %); a fully bilingual UI (CS/EN) is on the roadmap.

---

## ⚖️ Legálně / Legal

Web nenabízí žádné ROM soubory. Hry shánějte legálně — vlastní dumpy kazet a disků, nebo
homebrew/freeware (🆓). Fotografie konzolí pocházejí z Wikimedia Commons (volné licence);
obaly her z komunitní databáze libretro-thumbnails — práva náleží příslušným vydavatelům
a slouží zde jen k identifikaci her ve fanouškovském katalogu.

*This site hosts no ROM files. Console photos are from Wikimedia Commons; box art from the
libretro-thumbnails community database, used for identification only — rights belong to the
respective publishers.*

---

<div align="center">
<sub>Postaveno s Astro · Built with Astro · 🤖 vibe-coded with Claude Code</sub>
</div>
