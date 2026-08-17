<div align="center">

# 🎮 RetroWeb

**Průvodce světem retro hraní** — historie herních platforem, jejich legendární hry
a hardware jako Anbernic RG35XX&nbsp;Pro, R36S a Batocera.

*A guide to the world of retro gaming — platform history, legendary games and hardware.*

`48 platforem` · `2508 her` · `99 % článků` · `86 % obrázků` · `🇨🇿 🇬🇧 🇩🇪 🇫🇷` · `Astro` · `static`

**🌐 Produkce (live):** [retrowebcz.netlify.app](https://retrowebcz.netlify.app) &nbsp;·&nbsp; **🧪 Náhled (GitHub Pages, noindex):** [mhudakcz.github.io/RetroWeb](https://mhudakcz.github.io/RetroWeb/)

</div>

---

## 🇨🇿 Česky

RetroWeb je statický web postavený v [Astro](https://astro.build), který z kurátorských
Markdown podkladů generuje přehledný katalog retro hraní:

- **Platformy** — 48 konzolí, handheldů a počítačů od Atari 2600 (1977) přes Nintendo DS,
  PlayStation 2, GameCube a Xbox až po PS3/PS4, Xbox 360/One, Nintendo Switch, PS Vita
  a fantasy konzole PICO-8 a TIC-80. Každá má dlouhý článek (technika, propojení, modely,
  klony vč. českých, dnešní scéna) prokládaný dobovými fotkami.
- **Jazyky** — 🇨🇿 čeština, 🇬🇧 angličtina a 🇩🇪 němčina pokrývají obsah kompletně,
  🇫🇷 francouzština zatím zhruba z třetiny (zbytek dojíždí, mezitím se zobrazí čeština).
  Přepínač v hlavičce i patičce, hreflang a lokalizovaná sitemap pro SEO.
- **Hry** — 2508 titulů, **99 % s magazínovým článkem** (CZ). Žánr, délka hraní, počet
  hráčů 👥, obal/screenshoty. Katalog s hledáním a filtry (platforma, žánr, homebrew 🆓,
  must-play ⭐, logické 🧩, pro více hráčů). Postupné čtení (předchozí/další) u platforem i her.
- **Hardware & emulace** — průvodci pro Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS i konzole, vč. CRT filtrů, scrapingu obrázků a hraní ve více lidech (netplay).
- **Obrázky** — fotky konzolí z Wikimedia, obaly retro her z libretro-thumbnails (jako scrapuje
  Batocera), u moderních platforem ze Steamu (libretro pro ně obaly nemá), u her bez obalu
  fallback na titulní obrazovku nebo emblém platformy, vše optimalizované do WebP.
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

- **Platforms** — 48 consoles, handhelds and computers from the Atari 2600 (1977) through the
  Nintendo DS, PlayStation 2, GameCube and Xbox to the PS3/PS4, Xbox 360/One, Nintendo Switch,
  PS Vita and the PICO-8 / TIC-80 fantasy consoles, each with a long article (tech, links,
  models, clones, today's scene) interwoven with period photos.
- **Languages** — 🇨🇿 Czech, 🇬🇧 English and 🇩🇪 German cover the content in full; 🇫🇷 French is
  roughly a third done (the rest falls back to Czech for now). Switcher in header and footer,
  hreflang and a localized sitemap for SEO.
- **Games** — 2508 titles, **99 % with a magazine-style write-up**. Genre, play-length,
  player count 👥, box art / screenshots. Catalog with search and filters (platform, genre,
  homebrew 🆓, must-play ⭐, puzzle 🧩, multiplayer), plus prev/next reading navigation.
- **Hardware & emulation** — guides for Anbernic RG35XX Pro, R36S, Batocera, Raspberry Pi,
  Android, PC, iOS and consoles, incl. CRT shaders, artwork scraping and multiplayer (netplay).
- **Images** — console photos from Wikimedia, retro box art from libretro-thumbnails (the same
  source Batocera scrapes) and modern-platform box art from Steam (libretro has none for those),
  with a title-screen or platform-emblem fallback for boxart-less games, optimized to WebP.

```bash
npm install && npm run dev      # dev server at http://localhost:4321
npm run build                   # static output to dist/
```

> Per-game articles and the localized UI are done; finishing the French translation
> and box art for console exclusives that Steam doesn't carry are what's left.

---

## ⚖️ Legálně / Legal

Web nenabízí žádné ROM soubory. Hry shánějte legálně — vlastní dumpy kazet a disků, nebo
homebrew/freeware (🆓). Fotografie konzolí pocházejí z Wikimedia Commons (volné licence);
obaly her z komunitní databáze libretro-thumbnails a z obchodu Steam — práva náleží
příslušným vydavatelům a slouží zde jen k identifikaci her ve fanouškovském katalogu.

*This site hosts no ROM files. Console photos are from Wikimedia Commons; box art from the
libretro-thumbnails community database and the Steam store, used for identification only —
rights belong to the respective publishers.*

---

<div align="center">
<sub>Postaveno s Astro · Built with Astro · 🤖 vibe-coded with Claude Code</sub>
</div>
