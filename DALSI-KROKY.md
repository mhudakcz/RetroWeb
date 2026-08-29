# Kde jsme skončili (29. 8. 2026)

Poznámka pro příští sezení. Co je hotové, co běželo, a co dělat dál.

## Hotovo v tomto sezení

**Hardware — jak ukládat a vyskočit ze hry** (`d475e1b`, `a33f7f3`)
Nová sekce u R36S, RG35XX Pro, Androidu a iOS: rozdíl mezi herním savem a
save state, proč nevypínat konzoli natvrdo, tabulky zkratek (ArkOS, muOS,
Knulli, dotykový RetroArch, gesta Delty). Kombinace jsou z dokumentace
firmwarů, ne z hlavy.
Sekcím přibylo volitelné pole `keys` — tělo jde přes `marked.parseInline`,
takže blokový markdown (tabulky) v něm nefunguje.

**Nová platforma Mobil (iOS a Android)** (`6bf980f`, `16099ec`)
317 her, jedna platforma místo dvou (drtivá většina titulů vyšla na obojím).
Nový typ platformy `mobile` včetně popisků ve všech čtyřech jazycích.
Dlouhý článek `src/data/platform_articles/mobil.md` hotový.

**Nové nástroje**
- `tools/articles_prep.py` + `tools/articles_new.workflow.js` — píše PRVNÍ
  články ke hrám, které žádný nemají (dosavadní nástroje uměly jen rozšířit).
  Rovnou generuje i závěrečnou větu „Proč hrát".
- `tools/teasers_prep.py` umí `--platform`.
- `tools/magazine_issue.py` — rejstřík čísel magazínu, viz níže.

## Rozpracované — pokračovat tady

### 1. Mobil: teasery a články (nejbližší krok)
Hry mají jen jména a žánry, **texty chybí**. Dávky se generovaly do
scratchpadu, který se mezi sezeními maže — proto se prostě **připraví znovu**,
je to idempotentní:

```bash
python tools/teasers_prep.py .i18n-work/mobil --platform mobil --size 27
```
pak workflow `tools/teasers.workflow.js` s vypsanými args, po doběhnutí
`python tools/teasers_prep.py .i18n-work/mobil --merge` a `python tools/parse_content.py`.

Teprve potom články (teaser je pro ně vstup):
```bash
python tools/articles_prep.py .i18n-work/mobil-art --platform mobil --size 12
```
workflow `tools/articles_new.workflow.js`, merge s `--prefix mobil-01`.

**Pozor:** všechna generovací workflow musí mít `model: 'sonnet'`, jinak
zdědí model sezení.

### 2. Nedokončený požadavek: „Ty platformy dej do tagů hry"
Uživatel to napsal ke sloučené mobilní platformě. Dvě možná čtení, **zeptat
se**, které platí:
- (a) U mobilních her ukázat tagy `iOS` / `Android` podle toho, kde hra
  skutečně vyšla. Mechanika by šla jako `src/data/game_os.json` po vzoru
  `game_players.json`, tag se přidá do řádku v `GameDetail.astro` (ř. 104–115).
  Riziko: u 317 her nejde exkluzivitu spolehlivě určit z hlavy — u většiny
  platí obojí, ale výjimky (Infinity Blade, Device 6, Apple Arcade tituly,
  Death Stranding) by chtěly ověřit.
- (b) U každé hry ukázat tagy všech platforem z katalogu. Tohle už ale
  částečně existuje jako sekce „Také na" (`sameGameElsewhere`), takže spíš (a).

### 3. Magazín — vzorové číslo
Uživatel schválil **plný magazín** (editorial, téma čísla, žebříček, „co se
chystá") a **nejdřív ukázat návrh** — postavit jedno vzorové číslo (1994),
teprve pak zbytek.

`tools/magazine_issue.py` je hotový: z katalogu vychází **186 čísel**
(1977–2025, ~26 her na číslo). Klíčové pravidlo je v docstringu — obsah
vydaného čísla se nikdy nemění, nové hry zakládají nová čísla.

Zbývá: texty čísla (workflow), stránka `/magazin/<rok>-<cislo>`, přehled
ročníků, obálka.

## Fronta ostatních věcí

- **Články na mobil nejsou přeložené** — nová hardwarová sekce o ukládání je
  zatím jen česky (v EN/DE/FR se nezobrazí, protože lokalizovaný soubor má
  vlastní seznam sekcí). Stejně tak celá platforma Mobil.
- **Batch „whyplay" se ztratil** — agenti psali do kořene scratchpadu místo
  do pracovní složky a ta se smazala. Znovu přes `whyplay_prep.py`.
- **Batch „strategie"** (Hearts of Iron, Civilization III/V/VI, SimCity,
  Silent Hill) doběhl, ale nikdy se nesloučil — a data jsou pryč. Znovu.
- Rozšířit arkády (83 her), +50 na GBA/GB/GBC/Mega Drive/SNES/NES,
  dotáhnout Switch, Saturn, Dreamcast, Master System na 150.
- Úvodní texty sérií na 2200–2800 znaků u zbývajících ~80 sérií.
- Lightbox / galerie u obrázků (dnes strop 480 px).
- Hodnocení her — Metacritic nemá API a zakazuje scraping; procenta ze Steamu
  fungují, ale pokrývají hlavně moderní PC.
- Multiplayer info (lokální/online, počet hráčů).
- ~486 her bez obrázků; Virtuality a Cardboard prakticky bez obrázků.
- Build má 996 MB, což je přesně strop GitHub Pages — proto je náhled na
  Pages jen v češtině (`ONLY_CS=1`). Produkce na Netlify staví všechny jazyky.

## Provozní poznámky

- Deploy na produkci **jen na vyzvání**, přes `netlify.cmd` (`.ps1` blokuje
  Execution Policy). CLI 25–40 minut mlčí, to je normální.
- Pracovní dávky patří do `.i18n-work/` (gitignored, přežije sezení), **ne**
  do session scratchpadu — ten se mezi sezeními maže a padly tím už tři dávky
  (whyplay, strategie, teasery k mobilu).
