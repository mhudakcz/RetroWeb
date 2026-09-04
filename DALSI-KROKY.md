# Kde jsme skončili (29. 8. 2026)

Poznámka pro příští sezení. Co je hotové, co běželo, a co dělat dál.

## Hotovo v tomto sezení

**Hardware — jak ukládat a vyskočit ze hry** (`d475e1b`, `a33f7f3`)
Nová sekce u R36S, RG35XX Pro, Androidu a iOS: rozdíl mezi herním savem a
save state, proč nevypínat konzoli natvrdo, tabulky zkratek (ArkOS, muOS,
Knulli, dotykový RetroArch, gesta Delty). Sekcím přibylo volitelné pole
`keys` — tělo jde přes `marked.parseInline`, kde blokový markdown nefunguje.

**Platforma Mobil (iOS a Android)** — hotová
316 her, teasery, plné české články se závěrečnou větou „Proč hrát",
175 obalů (Steam + infoboxy Wikipedie), tagy iOS/Android u her, obrázek
platformy, dlouhý článek o platformě.

**Náhled na Pages je teď opravdu jen česky** (`f3f3a4a`)
`ONLY_CS` existoval, ale nefungoval dvakrát: dynamické stránky měly jazyky
natvrdo a Astro nepouští holé env do `import.meta.env`. Teď přes
`vite.define`. Výsledek: 5 475 stránek a 469 MB místo 20 tisíc a 996 MB.

**Magazín — vzorový ročník 1994** (`d77c954`)
7 čísel s editorialem, tématem, žebříčkem a rubrikou „příště". Stránky
`/magazin` a `/magazin/<rok>-<číslo>`, odkaz v hlavičce (jen CZ).

**Chybějící díly strategických řad** (`8e38431`)
30 titulů: celý Paradox (Hearts of Iron chyběl úplně), Civilization III/V/VI
na PC, SimCity 3000/4/2013, Cities: Skylines, Total War, Silent Hill
Homecoming a Downpour.

## Čeká na rozhodnutí

**Magazín: pustit zbytek?** Vzorový ročník 1994 je na webu k prohlédnutí.
Z celého katalogu vychází **186 čísel**. Až to uživatel schválí:
```bash
python tools/magazine_issue.py --write        # rejstřík pro všechny roky
python tools/magazine_prep.py .i18n-work/magazin
```
a workflow `tools/magazine.workflow.js`. Obsah vydaného čísla se nikdy
nemění — nové hry zakládají nová čísla.

## Fronta — změřeno 29. 8. 2026, katalog má 4 915 her

**1. Závěrečná věta „Proč hrát" chybí u 3 191 her (64 %).** Největší díra
v obsahu. Dávka `whyplay` se ztratila (psalo se do scratchpadu). Znovu:
`python tools/whyplay_prep.py .i18n-work/why --size 25` → workflow
`whyplay.workflow.js` → `--merge`. Zhruba 128 dávek.

**2. Snímky ze hry chybí u 826 her, které mají obal.** App Store se u mobilu
osvědčil; pro ostatní platformy existují `games-steam-shots` a
`games-nintendo-shots`, které se dosud pustily jen zčásti.

**3. 609 her (12 %) nemá žádný obrázek.** Nejhůř PC moderní (75), PC 9x (58),
Xbox 360 (49), PS3 (46), Mobil (43 — stažené tituly, nedohledatelné),
PS Vita (27), Xbox Series (24).

**4. Překlady stojí na 66 %.** 1 640 her bez cizojazyčného článku a navíc celá
platforma Mobil, magazín a hardwarová sekce o ukládání. Postup viz
[[retroweb-obsah-workflow]] — `i18n_gap.py` → `i18n_new.workflow.js` → merge.

**5. Úvody sérií jsou krátké — medián 1 191 znaků, žádný nepřesahuje 1 553.**
Cíl 2 200–2 800 nebyl nikdy splněn, dřívější poznámka o hotových 10 sériích
byla mylná (nesloučilo se). Týká se všech 155 sérií.

**6. 155 her nemá rok vydání.** Kromě detailu hry to kazí i magazín, kam se
takové hry zařazují jen odhadem podle roku platformy.

**7. Drobnosti:** 33 her bez článku, 15 bez úvodní věty.

**Malé platformy** (kdyby se chtělo rozšiřovat): Amiga CD32 10, Intellivision
11, Jaguar 11, Atari 5200 11, 32X 13, SG-1000 13, Virtual Boy 13, CD-i 13,
Vectrex 13, Atari 7800 14, ColecoVision 16, Atari 2600 jen 34, Master System
38, PC Engine 38. Arkády mají 83.

**Nedodělané funkce:** lightbox/galerie u obrázků (dnes strop 480 px),
hodnocení her (Metacritic nemá API a zakazuje scraping; procenta ze Steamu
fungují, ale pokrývají hlavně moderní PC), multiplayer info (lokální/online,
počet hráčů).

**Magazín** je pozastavený — uživatel 29. 8. 2026 řekl, že to chce udělat
„malinko jinak". Ročník 1994 (7 čísel) zůstává na webu jako ukázka.

## Provozní poznámky

- Deploy na produkci **jen na vyzvání**, přes `netlify.cmd`. Náhled na Pages
  se staví sám po `git push` (~2,5 min).
- Pracovní dávky patří do `.i18n-work/` (gitignored, přežije sezení), **ne**
  do session scratchpadu — ten se mezi sezeními maže a padly tím už dvě dávky.
- Všechna generovací workflow musí mít `model: 'sonnet'`.
- Články ke hrám bez článku: `articles_prep.py --platform <slug>` +
  `articles_new.workflow.js`, merge s `--prefix`. Teasery napřed, jsou vstup.

## Stav k 4. 9. 2026 (preruseno na vyzadani)

Katalog: **77 platforem, 5759 her**. Kazda ma clanek, uvodni vetu
i zaverecne "Proc hrat"; zadny clanek neni kratsi nez 1400 znaku.

Obrazky: bez obrazku 571 her, pod tremi 1542,
pet a vic 1404. Galerie pobere deset polozek,
na strance jsou videt dva snimky a znacka +N.

Preklady: EN 5527, DE 5527, FR 4488 her z 5759.
"Cim zacit": 768 doporuceni na 76 platformach.

Vsechno je zacommitovane. Na produkci zatim NENI nic z teto davky —
uzivatel nasazeni odsouhlasil, ale az budou preklady vcetne FR.

## KDE POKRACOVAT

### 1. Francouzstina (rozdelana, 120 z 296 davek)
Prace je v `.i18n-work/fr2`, hotove davky se preskoci. Aby se nespoustelo
296 agentu kvuli zbytku (pri limitu relace spadnou naraz vsichni cekajici):

    python tools/i18n_zbytek.py .i18n-work/fr2 .i18n-work/fr2-zbytek
    # workflow tools/i18n_fr.workflow.js s args, ktere skript vypise
    python tools/i18n_zbytek.py .i18n-work/fr2 .i18n-work/fr2-zbytek --zpet
    python tools/i18n_merge.py .i18n-work/fr2

### 2. Dorovnat EN a DE
Chybi u ~230 nejnovejsich her (pribyly az po extrakci):

    python tools/i18n_gap.py .i18n-work/tr3 en,de
    python tools/i18n_chunk.py .i18n-work/tr3 --games 8
    # workflow tools/i18n_finish.workflow.js
    python tools/i18n_merge.py .i18n-work/tr3

### 3. "Cim zacit" podle zebricku z Vimm's Lair
Pripraveno, jeste nespusteno. 143 her je v zebriccich a chybi mezi
doporucenimi:

    python tools/picks_prep.py .i18n-work/picks5 --zebricek .i18n-work/vimm/report.json
    # workflow tools/picks.workflow.js
    python tools/picks_prep.py .i18n-work/picks5 --merge

### 4. Nasazeni na produkci (odsouhlaseno, az budou preklady)

    npm run build                      # ~16 minut, 24 tisic stranek
    git push origin main
    "/c/Users/Michal (admin)/AppData/Roaming/npm/netlify" deploy --prod --dir=dist

### Zdroje obrazku
libretro (obaly i snimky) | Steam | Nintendo eShop | App Store | GOG (jen PC
linie: pc-dos, pc-9x, pc-modern, web, mobil — jinde nabizi jinou verzi nebo
remake) | ZXDB (Spectrum) | itch.io | Wikipedia infobox.

POZOR NA PORADI: `dedupe` se pousti az PO `optimize`. Pred prevodem porovnava
cerstvy JPEG proti uz prevedenemu WebP a duplicity neodhali — v jednom behu
takhle proslo 1866 duplicitnich souboru.

Zdroje jsou uz vycerpane: posledni sweep dal 28 obalu z Wikipedie, Nintendo
eShop k 157 hram nic. Co zbyva bez obrazku, volny zdroj nepokryva — Java
a Symbian, PICO-8 (zije na lexaloffle BBS) a konzolove exkluzivity na PS3
a Xbox 360; na ty by byl potreba klic k RAWG nebo IGDB.

### Limity relace
Pri limitu spadnou naraz vsichni cekajici agenti, i ti, kteri meli vratit SKIP.
Limit se resetuje v celou hodinu (hlaska rika kterou). Proto `i18n_zbytek.py`.
