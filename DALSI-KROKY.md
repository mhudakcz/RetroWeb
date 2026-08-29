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

## Fronta

- **Překlady**: platforma Mobil, magazín a nová hardwarová sekce o ukládání
  jsou zatím jen česky. Magazín se schválně nedává do cizojazyčné navigace.
- **Batch „whyplay"** se ztratil (psalo se do scratchpadu). Znovu přes
  `whyplay_prep.py` — týká se ~3 100 článků bez závěrečné věty.
- Rozšířit arkády (83 her), +50 na GBA/GB/GBC/Mega Drive/SNES/NES,
  dotáhnout Switch, Saturn, Dreamcast, Master System na 150.
- Úvodní texty sérií na 2200–2800 znaků u zbývajících ~80 sérií.
- Lightbox / galerie u obrázků (dnes strop 480 px).
- Hodnocení her — Metacritic nemá API a zakazuje scraping; procenta ze Steamu
  fungují, ale pokrývají hlavně moderní PC.
- Multiplayer info (lokální/online, počet hráčů).
- ~140 mobilních her bez obalu (free-to-play tituly, volný zdroj neexistuje).

## Provozní poznámky

- Deploy na produkci **jen na vyzvání**, přes `netlify.cmd`. Náhled na Pages
  se staví sám po `git push` (~2,5 min).
- Pracovní dávky patří do `.i18n-work/` (gitignored, přežije sezení), **ne**
  do session scratchpadu — ten se mezi sezeními maže a padly tím už dvě dávky.
- Všechna generovací workflow musí mít `model: 'sonnet'`.
- Články ke hrám bez článku: `articles_prep.py --platform <slug>` +
  `articles_new.workflow.js`, merge s `--prefix`. Teasery napřed, jsou vstup.
