<div align="center">

# 🎮 RetroWeb

**Průvodce světem retro hraní** — historie herních platforem, jejich legendární hry
a hardware jako Anbernic RG35XX&nbsp;Pro, R36S a Batocera.

*A guide to the world of retro gaming — platform history, legendary games and hardware.*

`27 platforem` · `943 her` · `816 obalů` · `Astro` · `static`

</div>

---

## 🇨🇿 Česky

RetroWeb je statický web postavený v [Astro](https://astro.build), který z kurátorských
Markdown podkladů generuje přehledný katalog retro hraní:

- **Platformy** — 27 konzolí, handheldů a počítačů od Atari 2600 (1977) po fantasy konzole
  PICO-8 a TIC-80, každá s historií, kontextem a fotografií.
- **Hry** — 943 titulů s žánrem, délkou hraní a u 443 z nich detailním komentářem; katalog
  s fulltextovým hledáním a filtry (homebrew 🆓, must-play ⭐, logické 🧩).
- **Hardware & Batocera** — co retro handheldy a Batocera umí, co utáhnou a jak je nastavit.
- **Obrázky** — fotky konzolí z Wikipedie, obaly her z libretro-thumbnails (stejné, co
  scrapuje Batocera), optimalizované do WebP.

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

- **Platforms** — 27 consoles, handhelds and computers from the Atari 2600 (1977) to the
  PICO-8 / TIC-80 fantasy consoles, each with history, context and a photo.
- **Games** — 943 titles with genre, play-length and a detailed write-up for 443 of them;
  a catalog with full-text search and filters (homebrew 🆓, must-play ⭐, puzzle 🧩).
- **Hardware & Batocera** — what the retro handhelds and Batocera can do and how to set them up.
- **Images** — console photos from Wikipedia, game box art from libretro-thumbnails (the same
  source Batocera scrapes), optimized to WebP.

```bash
npm install && npm run dev      # dev server at http://localhost:4321
npm run build                   # static output to dist/
```

> A bilingual UI (CS/EN) and longer per-game articles are on the roadmap.

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
