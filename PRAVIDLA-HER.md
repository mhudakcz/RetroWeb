# Pravidla pro přidávání her

Co musí mít každá hra, než se dá považovat za hotovou. Vzniklo z chyb, které
se při dávkovém přidávání opakovaly — proto je u většiny bodů napsané i **jak
se pozná, že chybí**, ne jen co má být.

Kontrolu pustí `python tools/kontrola_her.py`; vypíše, co kterému titulu chybí.

---

## 1. Obrázky — ideálně tři a víc

Minimum je obal. Cílem jsou **aspoň tři obrázky** (obal + dva snímky ze hry),
strop je deset — nad to se galerie stává nepřehlednou.

Zdroje se doplňují, každý pokrývá jinou část katalogu:

| zdroj | na co |
|---|---|
| libretro | obaly i snímky pro retro platformy |
| Steam | moderní konzole a PC |
| Nintendo eShop | Nintendo platformy |
| App Store | **jen platforma mobil** |
| GOG | **jen PC linie** (pc-dos, pc-9x, pc-modern, web, mobil) |
| ZXDB | ZX Spectrum |
| itch.io | prohlížečovky a homebrew |
| Wikipedia infobox | co nemá nikdo jiný |

**App Store nesmí na java-mobil ani jinam.** Prodává dnešní iOS verze, takže
na javovou éru vrátí moderní port pod stejným názvem — Doom takhle dostal
reklamní banner k 25. výročí místo snímku z hry pro tehdejší telefony.

**GOG nesmí na jiné platformy než PC.** Prodává verze pro PC, takže na konzoli
nabídne buď jinou verzi, nebo rovnou moderní remake pod původním názvem —
Wizardry na Atari 800 takhle dostalo snímky z remaku z roku 2024.

Obecně: **každý obchod prodává svoji verzi.** Než se zdroj pustí na novou
platformu, ověřit na jedné hře, že nevrací remake nebo port odjinud.

**Pořadí kroků: `dedupe` až PO `optimize`.** Před převodem porovnává čerstvý
JPEG proti už převedenému WebP, což jsou u téhož obrázku různé bajty, a hlásí
nulu. Jednou takhle prošlo 1866 duplicitních souborů.

## 2. Úvodní věta

Jedna věta, 40–90 znaků, ve stylu ostatních platforem. Není to shrnutí děje,
ale důvod, proč si té hry všimnout.

## 3. Text správné délky

Článek 1500–2000 znaků, tři odstavce. **Slučovací skript zahazuje články pod
limitem bez varování** — v jednom kole takhle vypadlo 15 z 71 her. Po každé
dávce proto porovnat, kolik titulů se přijalo proti kolika zadaným, a zbytek
dopsat; jinak to vypadá hotově a přitom chybí třetina.

## 4. Závěrečná věta „Proč hrát"

Na konci článku, za tučným `**Proč hrát:**`. Řekne přímo, komu a proč se hra
vyplatí — ne opakování toho, co už je v textu.

## 5. Zařazení v čase

Rok vydání u každé hry. Když vyšla na víc platforem v různých letech, platí rok
pro **tuto** platformu, ne rok prvního vydání série.

## 6. Série

Podívat se, jestli hra nepatří do série, kterou už vedeme — a když ano, zařadit
ji tam. Když jde o dva a víc dílů, které sérii zatím nemají, **novou sérii
založit**. Po změnách přegenerovat koláže: `python tools/series_art.py`.

---

## Co k tomu ještě patří

### 7. Kontrola duplicit proti jinému zápisu

Nestačí porovnat přesný název. Tytéž hry vedeme často jinak:

- `1943` vs `1943: The Battle of Midway` — podtitul
- `Street Fighter 2 Champion Edition` vs `Street Fighter II': Champion Edition`
- `Donkey Kong Junior` vs `Donkey Kong Jr.`
- `Pokémon Blue` vs `Pokémon Red / Blue / Yellow` — sloučený záznam
- `Jet Grind Radio` vs `Jet Set Radio` — regionální přejmenování

Poslední případ řetězcově dohledat **nejde**; u známých her se to musí ověřit
znalostí. Bez téhle kontroly vznikají dvojité záznamy — takhle vzniklo `1941`
vedle `1941: Counter Attack`.

### 8. Ostatní pole

Žánr, studio, délka hraní (S/M/L/XL), počet hráčů, příznaky
(`mustplay`, `homebrew`, `puzzle`, `mature`).

### 9. Odkaz na hraní

U webových her, které dodnes běží, doplnit `game_play.json`. **Každou adresu
ověřit dotazem** — mrtvý odkaz je horší než žádný.

### 10. Překlady

EN, DE i FR. Francouzština má vlastní workflow (`i18n_fr.workflow.js`), zbytek
`i18n_finish.workflow.js`.

### 11. „Čím začít"

Když přibude na platformě hodně her, projít výběr doporučení — nové silné
tituly do něj patří.

### 12. Záznam do „Co je nového“

Každé nasazení na produkci musí dostat záznam v `src/data/changelog.json` —
a to **ve všech čtyřech jazycích**, stejně jako zbytek webu. Týká se to obojího:
přidaných her i nových funkcí a jejich úprav.

**Datum je datum nasazení, ne commitu.** Čtenář na webu vidí jen to, co je na
produkci; kdyby změny nabíhaly dřív, než jsou vidět, byl by ten přehled matoucí.
Co je hotové v repozitáři, ale ještě nenasazené, se do changelogu nepíše —
přidá se, až to půjde ven.

Formát jednoho vydání:

```json
{
  "version": "2026.09.12",
  "date": "2026-09-12",
  "title": { "cs": "…", "en": "…", "de": "…", "fr": "…" },
  "entries": [
    { "tag": "games", "text": { "cs": "…", "en": "…", "de": "…", "fr": "…" } }
  ]
}
```

Značky, které stránka umí vykreslit: `games`, `platform`, `images`, `content`,
`i18n`, `feature`, `fix`. Novou značku je potřeba nejdřív přidat do `TAGS`
v `ChangelogPage.astro`, jinak se u položky nezobrazí popisek.

Text píšeme tak, aby dával smysl čtenáři, ne vývojáři: co na webu přibylo a co
z toho má, ne názvy skriptů a souborů.

---

## Pasti, které stály čas

**Staré výstupy v pracovním adresáři.** Agenti vracejí SKIP, když výstupní
soubor existuje — i když patří úplně jiným hrám. Vždy ověřit, že slugy ve
výstupu odpovídají vstupu, ne jen že soubor je. Jednou tak 50 her zůstalo bez
úvodní věty a workflow hlásilo hotovo.

**Limit relace.** Při jeho dosažení spadnou naráz všichni čekající agenti,
včetně těch, kteří měli jen vrátit SKIP. U velkých sad pouštět jen chybějící
práci přes `tools/i18n_zbytek.py`.

**Dávka, která nic nepřidala, vypadá stejně jako dávka, která uspěla.**
Zdroje vracejí snímky vždy od začátku seznamu. Když hra už dva snímky má,
uloží se do volných pozic tytéž dva znovu a `dedupe` je zase smaže — výpis
přitom hlásí stovky doplněných her. Po každé obrázkové dávce proto porovnat
`dataset.json` proti předchozí verzi (kolika hrám opravdu přibyl obrázek),
ne věřit číslu z výpisu. Jednou takhle skončilo 2404 stažených souborů v koši.

**Počet her v katalogu nevypovídá o pokrytí.** Výběr je kurátorský: N64 má
v katalogu desítky her a kánon je celý, zatímco 3DS jich mělo 42 a chybělo
11 ze 14 ze vzorku. Mezeru hledat sondou na konkrétní tituly, ne podle počtu.

**Agent radši vynechá, než vymyslí.** Když u platformy dodá míň her, než bylo
zadáno, bývá to správně — u PICO-8 nebo okrajových arkád reálný katalog na
zadaný počet nestačí. Nenutit doplnit počet za každou cenu.
