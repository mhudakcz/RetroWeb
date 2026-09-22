# Fronta práce — na příští spuštění

Stav k 22. 9. 2026. Postup a pasti jsou v `PRAVIDLA-HER.md`; tady je jen to,
co je rozdělané a v jakém pořadí na to navázat.

---

## 1. Dokončit nové hry (nutné před nasazením)

Do katalogu přibylo **555 chybějících dílů sérií** (celkem 6 860 her), ale
nesplňují pravidla — chybí jim úvodní věta a závěrečné „Proč hrát". Vzniklo to
tím, že se generovaly zadáním, které o ně ještě nežádalo.

```
python tools/kontrola_her.py
```

| co chybí | kolik her |
|---|---|
| bez úvodní věty | 700 |
| bez závěrečné věty | 236 |
| bez obrázku | 1 045 |
| bez studia | 402 |
| bez roku | 244 |

Úvodní věty a „Proč hrát" doplní `tools/teasers.workflow.js`
a `tools/whyplay.workflow.js` (přípravy `teasers_prep.py`, `whyplay_prep.py`).

**Bez tohohle kroku nenasazovat** — 700 her by na webu bylo bez věty v přehledu.

## 2. Obrázky pro nové hry

`tools/fetch_images.py` postupně: `games-steam` → `games-msstore` →
`games-wiki-box`, pak **`optimize` a teprve potom `dedupe`** (na pořadí záleží,
viz pravidla). Nové snímky se rovnou ukládají i ve velké verzi pro lightbox.

## 3. Překlady

555 nových her je jen česky.

```
python tools/i18n_gap.py .i18n-work/prekladyX en,de,fr
python tools/i18n_chunk.py .i18n-work/prekladyX --games 8
```
pak `i18n_finish.workflow.js` a `i18n_merge.py`.

## 4. Chybějící platformy u her, které už máme

Největší zbývající kus: **2 695 titulů, 337 dávek** v `.i18n-work/porty_vse`.

```
python tools/porty_kontrola.py .i18n-work/porty_vse
```

Pouštět po vlnách po 30 dávkách přes `from`, **vždy jen jednu instanci nad
adresářem** (dvě si přepíšou výsledky). Po každé vlně kontrola, pak
`ports_verify.workflow.js` a teprve pak `porty_prep.py --merge`.

Staré výstupy z doby před pravidlem o významných verzích leží
v `porty_vse_stare_zadani` — nepoužívat, jsou příliš štědré.

## 5. Nasazení

```
npm run build
git push origin main
netlify deploy --prod --dir=dist --no-build
```

`--no-build` je podstatné: `netlify.toml` má `command = "npm run build"`, takže
bez něj CLI staví web podruhé a nasazení trvá hodinu místo devíti minut.

Do `src/data/changelog.json` patří záznam **s datem nasazení** ve všech čtyřech
jazycích (pravidlo 13).

---

## Menší věci

- **Osm handheldů** se nepodařilo ověřit: Black Hawk X9 a X20, S36R, R36 Max,
  Anbernic RG CubeXX a RG ARC-D, Powkiddy X55, GKD Pixel. Agenti si nebyli jistí,
  že pod těmi názvy existují. Doplnit ručně, až budou podklady.
- **Starší obrázky** jsou jen v 480 px a lightbox je roztahuje. Nové už se
  ukládají ve dvou velikostech; převod zbytku znamená stáhnout je znovu
  (~1,5 GB navíc). Uživatel odložil.
- **Dvě série bez textu** z 240 — `stalker` a `metro`, založené později než
  proběhla dávka. `series_intro_prep.py --chybejici`.
- **Indexace na Googlu**: 958 z 28 300 stránek. Není to chyba webu (ověřeno:
  canonical, hreflang i robots.txt sedí). Největší páka je vlastní doména místo
  `netlify.app`.
