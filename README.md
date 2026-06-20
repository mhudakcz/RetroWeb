# 🎮 RetroWeb

Web o retro hraní — historie herních platforem, jejich legendární hry a tipy pro
handheldy (**Anbernic RG35XX Pro**, **R36S**) a **Batoceru** na PC.

Postaveno v [Astro](https://astro.build). Obsah pochází z kurátorských Markdown podkladů
ve složce `Podklady/`, které parser převádí na strukturovaný dataset.

## Struktura

```
Podklady/extracted/      zdrojové MD soubory (historie platforem + hry)
tools/parse_content.py   parser MD → JSON (registr platforem + fuzzy párování her)
src/data/dataset.json    vygenerovaný dataset (27 platforem, 943 her)
src/lib/data.ts          načtení dat + typy + helpery + render markdownu
src/components/          Header, Footer, PlatformEmblem, PlatformCard, GameCard
src/pages/
  index.astro            domovská stránka (hero + platformy dle typu + must-play)
  platformy/             přehled + detail platformy (historie + seznam her)
  hry/                   katalog s filtrováním + detail hry
  o-projektu.astro       o webu + právní poznámka
```

## Příkazy

```bash
npm install          # instalace závislostí
npm run data         # přegenerování datasetu z Podklady/ (vyžaduje Python 3)
npm run dev          # vývojový server na http://localhost:4321
npm run build        # statický build do dist/
npm run preview      # náhled buildu
```

> Po úpravě Markdown podkladů spusť `npm run data` a poté `npm run build`.

## Obrázky

```bash
python tools/fetch_images.py platforms   # fotky konzolí z Wikipedie -> public/images/platforms
python tools/fetch_images.py games       # boxarty z libretro-thumbnails -> public/images/games
python tools/fetch_images.py optimize    # zmenší/převede na WebP (nutné po stažení)
python tools/parse_content.py            # doplní cesty k obrázkům do datasetu
```

Skript přeskakuje již stažené soubory. Pro vyšší limit GitHub API nastav `GH_TOKEN`.
Cesty k obrázkům se do datasetu dostanou podle existence souborů v `public/images/`.

## Datový tok

`parse_content.py` segmentuje 4 MD soubory podle nadpisů platforem, vytahuje hry
(žánr, délka, flagy 🆓⭐🔞🧩, rok, studio, komentáře) a **fuzzy párováním**
spojuje záznamy napříč soubory v rámci každé platformy. Akceptační pravidlo brání
falešným shodám sourozeneckých titulů (stejná série, jiný díl).

## Plánováno (část 2)

Průvodce sestavením ROM setu na SD kartu (struktura složek pro Batocera/EmulationStation,
BIOS, box-art a metadata, výkon na čipu H700). Jen postupy a nástroje — **žádné herní soubory**.

## Legálně

Web nenabízí ROM soubory. Hry shánět legálně: vlastní dumpy kazet/disků nebo homebrew/freeware (🆓).
