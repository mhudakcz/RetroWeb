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

## Stav k 5. 9. 2026 (PC se vypina)

Katalog: **77 platforem, 5910 her**. Vse zacommitovane a odeslane
na GitHub. Na produkci je jeste stav z 4. 9. — nove hry ani ucty tam nejsou.

Preklady: EN 5766, DE 5766, FR 5766 her.
Cim zacit: 800 doporuceni na 76 platformach.
Obrazky: bez obrazku 722 her, pod tremi 1693.

### Co pribylo naposledy
- 143 her na Nintendo DS (47 -> 106), 3DS (42 -> 101) a Wii (66 -> 91).
  Duvod: kanon byl pokryty, ale ze vzorku druhe vrstvy chybelo na 3DS 11 ze 14
  a na DS 10 ze 14. Rada kapesnich konzoli pritom po GBA (148) spadla na 47 a 42.
- 8 ceskych prohlizecovek (Samorost 1 a 2, Questionaut, Shy Dwarf, Osada,
  Stargate Online, Outspace Game, Obrana Ukrajiny) — vsechny s odkazem na hrani.
- Uzivatelske ucty pres Supabase (prihlaseni kodem, znacky u her, Muj seznam,
  administrace).

### KDE POKRACOVAT

**1. Dodelat novych 151 her** (143 Nintendo + 8 web) podle kontrolniho seznamu:

    python tools/teasers_prep.py .i18n-work/teasers5      # 151 her bez uvodni vety
    # workflow tools/teasers.workflow.js, pak --merge
    python tools/fetch_images.py games "nds,3ds,wii"
    python tools/fetch_images.py games-nintendo "nds,3ds,wii"
    python tools/fetch_images.py screenshots "nds,3ds,wii"
    python tools/fetch_images.py games-nintendo-shots "nds,3ds,wii"
    python tools/fetch_images.py optimize
    python tools/fetch_images.py dedupe      # POZOR: az PO optimize
    python tools/series_art.py; python tools/studio_art.py
    python tools/parse_content.py

**2. Preklady novych her** (EN, DE i FR chybi u ~151):

    python tools/i18n_gap.py .i18n-work/tr4 en,de,fr
    python tools/i18n_chunk.py .i18n-work/tr4 --games 8
    # workflow i18n_finish.workflow.js (EN+DE), pak i18n_fr.workflow.js (FR)
    python tools/i18n_merge.py .i18n-work/tr4

**3. Vyzkouset prihlaseni.** Schema v Supabase bezi a zabezpeceni je overene
(anonymni cteni prazdne, zapis odmitnut, statistiky jen pro adminy; admin
mhudak.cz@gmail.com je vlozeny). ZBYVA JEDNA VEC, bez ktere to nepujde:
sablona e-mailu musi obsahovat {{ .Token }}, jinak prijde odkaz misto kodu.
    https://supabase.com/dashboard/project/kcnfrihxmlvnhwroiriy/auth/templates
Prihlaseny pruchod nebyl otestovan — chybel k tomu e-mail uzivatele.

**4. Nasazeni na produkci** (uzivatel odsouhlasil, az budou preklady):

    npm run build          # ~20 minut, pres 25 tisic stranek
    git push origin main
    "/c/Users/Michal (admin)/AppData/Roaming/npm/netlify" deploy --prod --dir=dist

**5. Volitelne: Amiga +25 her.** Ze vzorku ji chybely 4 ze 14 a na svuj vyznam
ma jen 82 her. Ostatni 8/16bitove pocitace mezeru nemaji — Atari 800 a MSX
nechybelo nic, C64 jedna hra, Atari ST a Amstrad dve.

### Na co si dat pozor
- `dedupe` az PO `optimize` — pred prevodem porovnava JPEG proti WebP a nic nenajde.
- Vlastni `display` v CSS prebije atribut `hidden`; u novych komponent to bylo
  potreba osetrit natvrdo, jinak se ukazaly vsechny stavy naraz.
- Dlouhe davky poustet pres `tools/i18n_zbytek.py` — pri limitu relace spadnou
  naraz vsichni cekajici agenti, i ti, kteri meli jen vratit SKIP.
- GOG jen na PC linii (pc-dos, pc-9x, pc-modern, web, mobil); jinde nabizi jinou
  verzi nebo remake.
