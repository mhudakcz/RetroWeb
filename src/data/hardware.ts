// Obsah o hardwaru: retro handheldy a Batocera — dlouhé samostatné články.

export interface HardwareSpec {
  label: string;
  value: string;
}

export interface HardwareSection {
  title: string;
  body: string[]; // odstavce (markdown inline)
}

export interface HardwareItem {
  slug: string;
  name: string;
  kind: string;
  tagline: string;
  color: string;
  color2: string;
  art: 'handheld-h' | 'handheld-v' | 'batocera';
  intro: string[];
  photo?: { src: string; caption: string };
  specs: HardwareSpec[];
  canPlay: { label: string; level: 'ok' | 'most' | 'some' }[];
  sections: HardwareSection[];
  options: { title: string; text: string }[];
}

export const hardware: HardwareItem[] = [
  {
    slug: 'rg35xx-pro',
    name: 'Anbernic RG35XX Pro',
    kind: 'Kapesní konzole · 2024',
    tagline: 'Horizontální handheld s čipem H700 — sladké místo mezi cenou a výkonem.',
    color: '#ff3e7f',
    color2: '#2a0f1d',
    art: 'handheld-h',
    intro: [
      'RG35XX Pro je horizontální vrchol populární řady RG35XX od čínského výrobce Anbernic. Spojuje příjemnou velikost do kapsy, ostrý 4:3 displej a čip Allwinner H700, který utáhne drtivou většinu retro knihovny až po PlayStation. Za svou cenu nabízí poměr výkonu, výdrže a komunitní podpory, jaký jen tak něco netrumfne.',
    ],
    specs: [
      { label: 'Čip (SoC)', value: 'Allwinner H700, 4× Cortex-A53 @ ~1,5 GHz' },
      { label: 'Grafika', value: 'Mali-G31 MP2' },
      { label: 'Displej', value: '3,5" IPS, 640×480 (4:3)' },
      { label: 'Paměť', value: '1 GB LPDDR4' },
      { label: 'Baterie', value: '~3300 mAh (cca 5–8 h hraní)' },
      { label: 'Úložiště', value: '2× microSD (systém + hry)' },
      { label: 'Konektivita', value: 'Wi-Fi, HDMI výstup, USB-C' },
      { label: 'Systémy', value: 'muOS, Knulli, Batocera, ROCKNIX, stock' },
    ],
    canPlay: [
      { label: 'NES, SNES, Mega Drive, Master System, PC Engine', level: 'ok' },
      { label: 'Game Boy / GBC / GBA', level: 'ok' },
      { label: 'PlayStation (PS1)', level: 'ok' },
      { label: 'Nintendo 64, PSP', level: 'most' },
      { label: 'Dreamcast, Saturn', level: 'some' },
    ],
    sections: [
      {
        title: 'Odkud se vzal',
        body: [
          'Anbernic je dnes prakticky synonymem pro retro handheldy — čínská firma chrlí nové modely tempem, kterému se dá těžko stačit, a řada RG35XX patří k jejím nejúspěšnějším. Začalo to skromným svislým RG35XX, který okouzlil cenou a 4:3 displejem; pak přišel RG35XX Plus s výkonnějším čipem H700 a nakonec **RG35XX Pro**, který stejný čip zabalil do pohodlnějšího horizontálního „gameboyovského" těla s ramennímí tlačítky a dvěma analogovými sticky.',
          'Právě horizontální layout je důvod, proč si Pro oblíbili hráči, kteří víc než svislé „kapesní" tělo ocení ergonomii klasického ovladače. Anbernic na stejném čipu postavil i další modely (RG40XX, RG CubeXX), ale Pro zůstává nejvyváženější volbou pro toho, kdo chce jedno zařízení na všechno.',
        ],
      },
      {
        title: 'Čip H700 a kam až sahá výkon',
        body: [
          'Srdcem je **Allwinner H700** — čtyřjádrové ARM Cortex-A53 s grafikou Mali-G31. Na papíře to nezní jako trhák, ale pro emulaci 8bitových a 16bitových systémů je to víc než dost: NES, SNES, Mega Drive, Master System, PC Engine i celá řada Game Boyů běží na plné obrátky, bez zpomalení, s plynulým zvukem.',
          'Strop je zhruba u **PlayStationu 1**, který jede výborně, a u lehčích **PSP** a **Nintenda 64** titulů. U N64 a PSP ale platí, že každá hra je jiná — 2D a méně náročné 3D zvládne, technicky nejnáročnější tituly se zadrhávají nebo mají grafické chyby. **Dreamcast a Saturn** jsou na hraně: některé hry rozběhnete, ale nečekejte zázraky. Je to klasický kompromis levného ARM čipu — a v praxi pokryje 90 % toho, co většina lidí na retru chce hrát.',
        ],
      },
      {
        title: 'Displej, ovládání a zpracování',
        body: [
          'Displej je 3,5" IPS s rozlišením 640×480 a poměrem stran **4:3** — a to je klíčové. Drtivá většina konzolí a počítačů do éry PS1 používala 4:3, takže obraz vyplní celou plochu bez černých pruhů a každý pixel sedí. Panel je jasný, kontrastní a barevný; osmibitové hry na něm vypadají skoro líp než na dobové televizi.',
          'Tělo působí překvapivě kvalitně — pevná konstrukce, příjemné membránové i mikrospínačové varianty tlačítek (podle revize) a dva analogové sticky pro 3D tituly. Výdrž baterie se pohybuje kolem 5–8 hodin podle náročnosti emulace a jasu. Navíc je tu **HDMI výstup**, takže handheld připojíte k televizi a hrajete s bezdrátovým ovladačem jako na malé konzoli.',
        ],
      },
      {
        title: 'Operační systémy — srdce zážitku',
        body: [
          'Z výroby běží na vlastním Linuxu od Anbernicu, ale skutečné kouzlo je v **komunitních systémech**, které jen nahrajete na SD kartu — zařízení tím nijak neutrpí a kdykoli se vrátíte zpět. Nejoblíbenější jsou:',
          '**muOS** — rychlý, čistý a přehledný systém, dnes asi nejdoporučovanější volba pro H700. **Knulli** (z rodiny Batocera/EmulationStation) — krásný frontend s box-artem a scrapingem. **Batocera** — stejná univerzální distribuce jako na PC. **ROCKNIX** (nástupce JELOS) — výkonná a stabilní alternativa. Každý má trochu jinou filozofii; vyplatí se vyzkoušet dva tři a zůstat u toho, který vám sedne.',
        ],
      },
      {
        title: 'Pro koho to je a co zvážit',
        body: [
          'RG35XX Pro je ideální „jedno zařízení na všechno" pro někoho, kdo chce hrát klasiku do PS1 v kapse, nechce řešit drahý high-end handheld a ocení živou komunitu, návody a aktualizace. Pokud toužíte hlavně po N64, Dreamcastu nebo PSP ve plné parádě, sáhněte po výkonnějším (a dražším) zařízení s čipem řady Snapdragon.',
          'Při koupi pozor na **revize** a varianty (existují modely s mírně odlišnými tlačítky a sticky) a počítejte s tím, že druhou SD kartu na hry si nejspíš dokoupíte. Kvalitní rychlá karta se vyplatí — pomalá karta se projeví delším načítáním a trhanějším procházením velkých knihoven.',
        ],
      },
      {
        title: 'Ovládání: ukládání, menu a přepínání',
        body: [
          'Hraje se jako na klasické konzoli — D-pad nebo stick, tlačítka A/B/X/Y, ramena L/R. Srdcem pohodlí je vyhrazené tlačítko **Function (Fn / Menu)**, kterým se přímo ve hře dostaneš k funkcím emulátoru.',
          'Nejdůležitější jsou **save states** — uložení přesného stavu hry kdykoli (nejen na ukládacích místech). Na systémech postavených nad RetroArchem (muOS, Batocera, ROCKNIX) platí podobné **hotkeye**: **Fn + R1 = uložit stav**, **Fn + L1 = načíst stav**, **Fn + Start = ukončit hru**, **Fn + Select/X = menu emulátoru** (převíjení, změna jádra, nastavení). Kombinace si můžeš předefinovat.',
          'Mezi hrami přepínáš ukončením do seznamu (Fn + Start) a výběrem další. Uložené pozice i save states zůstávají na SD kartě, takže po vypnutí pokračuješ přesně tam, kde jsi skončil.',
        ],
      },
    ],
    options: [
      {
        title: 'Dvě SD karty',
        text: 'Do prvního slotu patří systém, do druhého tvoje hry. Knihovnu tak přenášíš mezi zařízeními a systém kdykoli přeinstaluješ bez ztráty her.',
      },
      {
        title: 'Vyplatí se rychlá karta',
        text: 'U velkých knihoven (hlavně s box-artem) dělá kvalitní microSD rozdíl v rychlosti procházení i načítání. Nešetři na ní.',
      },
      {
        title: 'HDMI na televizi',
        text: 'Přes HDMI výstup z handheldu uděláš malou konzoli pod televizi — stačí bezdrátový ovladač.',
      },
    ],
  },
  {
    slug: 'r36s',
    name: 'R36S',
    kind: 'Kapesní konzole · 2023',
    tagline: 'Cenově dostupný klon s vertikálním displejem a otevřeným systémem.',
    color: '#36e2ff',
    color2: '#0f2a30',
    art: 'handheld-v',
    intro: [
      'R36S je levný „lidový" handheld v duchu starších Anbernic RG351 — svislé tělo, 3,5" IPS displej a otevřený systém, pro který komunita připravila skvělé vyladěné distribuce. Výkonem nepatří mezi špičku, ale jako vstupní brána do retro hraní za pár stovek je těžko k překonání. Háček je v tom, že existuje v záplavě variant a klonů, takže při koupi je dobré vědět, do čeho jdete.',
    ],
    specs: [
      { label: 'Čip (SoC)', value: 'Rockchip RK3326, 4× Cortex-A35 @ ~1,3 GHz' },
      { label: 'Grafika', value: 'Mali-G31' },
      { label: 'Displej', value: '3,5" IPS, 640×480 (4:3)' },
      { label: 'Paměť', value: '1 GB DDR3L' },
      { label: 'Baterie', value: '~3200 mAh (cca 4–6 h)' },
      { label: 'Úložiště', value: 'microSD (často 2 sloty)' },
      { label: 'Systémy', value: 'ArkOS, ROCKNIX/JELOS, Batocera, stock' },
    ],
    canPlay: [
      { label: 'NES, SNES, Mega Drive, GB/GBC/GBA', level: 'ok' },
      { label: 'PC Engine, Master System, arkády (lehčí)', level: 'ok' },
      { label: 'PlayStation (PS1)', level: 'most' },
      { label: 'Nintendo 64, DOS, ScummVM', level: 'some' },
      { label: 'Dreamcast, PSP', level: 'some' },
    ],
    sections: [
      {
        title: 'Fenomén levného klonu',
        body: [
          'R36S vznikl jako cenově ostrá odpověď na dražší značkové handheldy. Tvarem i vnitřnostmi navazuje na osvědčenou školu Anbernic RG351 — stejný čip Rockchip RK3326, podobný 4:3 displej — ale prodává se za zlomek ceny. Díky tomu se stal jedním z nejprodávanějších „prvních" retro handheldů a fenoménem hlavně mezi začátečníky.',
          'Jeho největší devízou je otevřenost. Komunita kolem RK3326 je obrovská (vznikla už kolem RG351) a připravila pro něj vyladěné systémy, které z levného hardwaru dostanou maximum. To, co by jinak byl bezejmenný klon, se tak mění v plnohodnotnou retro mašinu s pěkným frontendem.',
        ],
      },
      {
        title: 'Hardware RK3326 — realistická očekávání',
        body: [
          'Čtyřjádrový **Rockchip RK3326** (Cortex-A35) je o generaci pozadu za H700 v RG35XX Pro. Pro éru 8/16 bitů a kapesní konzole je to ale pořád skvělý dělník: NES, SNES, Mega Drive, Master System, PC Engine, Game Boy i GBA jedou plynule. **PlayStation 1** většinou rozběhnete dobře, jen u náročnějších 3D titulů narazíte na limit.',
          '**Nintendo 64, Dreamcast a PSP** berte jako bonus — zahrajete vybrané, spíš 2D nebo nenáročné kousky, ale nečekejte plnou kompatibilitu. Naopak skvěle si sedne s DOSem, ScummVM adventurami a domácími počítači (C64, Amiga…), kde výkon nehraje takovou roli a 4:3 displej je ideál.',
        ],
      },
      {
        title: 'Operační systémy',
        body: [
          'Z krabice přichází R36S s předinstalovaným systémem (zpravidla fork ArkOS) na SD kartě. Pravá síla je ale ve výměně za komunitní distribuci: **ArkOS** je nejpopulárnější — stabilní, svižný, jednoduchý. **ROCKNIX** (dříve JELOS) nabízí modernější frontend a dobrou údržbu. **Batocera** přináší stejné prostředí jako na PC.',
          'Instalace je jako u všech těchto zařízení otázkou zapsání obrazu na microSD — interní paměť se nemění a původní kartu si můžete schovat jako zálohu.',
        ],
      },
      {
        title: 'Na co si dát pozor při koupi',
        body: [
          'R36S je proslulý **záplavou variant a klonů**. Pod stejným jménem se prodávají kusy s různými výrobními revizemi, různými displeji (kvalita panelu se liší — tzv. „screen lottery") a dokonce i s odlišnými čipy. Existují i přímé padělky a příbuzné modely (R36H, R35S a další).',
          'Praktický důsledek: než nahrajete nějaký komunitní systém, ověřte si, **jaký panel a SoC vaše konkrétní jednotka má**, ať zvolíte správný obraz — jinak vám může obraz vyjít převrácený nebo s mizernými barvami. Kupujte od prodejců s recenzemi a počítejte s tím, že u nejlevnějších kusů je kvalita zpracování loterie.',
        ],
      },
      {
        title: 'Ovládání: ukládání, menu a přepínání',
        body: [
          'Ovládáš ho jako klasickou konzoli; navíc má vyhrazené tlačítko **Function (F)**, kterým se ve hře dostaneš k funkcím emulátoru. Na ArkOS, ROCKNIX i Batoceře platí podobné **hotkeye**: **F + R = uložit stav**, **F + L = načíst stav**, **F + Start = ukončit hru**, **F + Select/X = menu emulátoru**.',
          'Nejpohodlnější ukládání jsou **save states** — uložíš kdykoli a okamžitě se vrátíš; klasické herní uložení (do paměti hry) funguje samozřejmě taky. Vše zůstává na SD kartě, takže po vypnutí pokračuješ, kde jsi přestal.',
          'Mezi hrami se přepínáš ukončením do seznamu a výběrem další. Kombinace tlačítek si lze v nastavení systému předefinovat.',
        ],
      },
    ],
    options: [
      {
        title: 'Ověř si verzi',
        text: 'Před nahráním systému zjisti, jaký displej a čip tvůj kus má — na to navazuje správný image (jinak hrozí převrácený obraz nebo špatné barvy).',
      },
      {
        title: 'Ideál na 8/16 bit a počítače',
        text: 'Do PS1 jede dobře, ale srdcem je éra 8/16 bitů, DOS, ScummVM a domácí počítače. Na náročné 3D systémy sáhni po výkonnějším zařízení.',
      },
      {
        title: 'Nech si původní kartu',
        text: 'Systém vyměníš na SD kartě. Tu původní si schovej jako zálohu pro případ návratu.',
      },
    ],
  },
  {
    slug: 'batocera',
    name: 'Batocera.linux',
    kind: 'Systém pro retro hraní',
    tagline: 'Linuxová distribuce, ze které uděláš retro konzoli z čehokoli — PC, Raspberry Pi i handheldu.',
    color: '#ffd23e',
    color2: '#2a2308',
    art: 'batocera',
    intro: [
      'Batocera je svobodná linuxová distribuce zaměřená výhradně na retro hraní. Funguje jako „plug & play": nainstalujete ji na SD kartu nebo USB disk, nabootujete a máte hotový herní systém — bez instalace na pevný disk a beze změny svého počítače. O zážitek se stará nádherný frontend EmulationStation, pod kapotou desítky emulátorů. Tytéž principy a uspořádání použijete na starém PC, na Raspberry Pi i na podporovaných handheldech.',
    ],
    specs: [
      { label: 'Typ', value: 'Linuxová distribuce (zdarma, open-source)' },
      { label: 'Frontend', value: 'EmulationStation' },
      { label: 'Jádra', value: 'RetroArch + samostatné emulátory' },
      { label: 'Zařízení', value: 'PC (x86-64), Raspberry Pi, ARM handheldy' },
      { label: 'Instalace', value: 'image na SD/USB (nemění interní disk)' },
      { label: 'Systémy', value: '100+ konzolí, počítačů a arkád' },
      { label: 'Ovladače', value: 'Xbox, PlayStation, 8BitDo, Switch Pro…' },
    ],
    canPlay: [
      { label: 'Vše 8/16bit, GB/GBA, PS1, domácí počítače', level: 'ok' },
      { label: 'N64, Dreamcast, PSP, Saturn (slušné PC/RPi5)', level: 'most' },
      { label: 'PS2, GameCube, Wii, 3DS (jen výkonné PC)', level: 'some' },
    ],
    sections: [
      {
        title: 'Co je Batocera a jak funguje',
        body: [
          'Batocera není program, který si nainstalujete do Windows — je to celý **operační systém** postavený na Linuxu, vyladěný jen na jednu věc: hrát retro hry. Spustíte ji přímo z SD karty nebo USB disku, takže váš počítač zůstane netknutý; po vypnutí a vyndání média je všechno jako předtím.',
          'Po startu vás přivítá **EmulationStation** — frontend ovladatelný gamepadem, kde procházíte systémy a hry jako v elegantním menu, s box-artem, popisy a videoukázkami. Když hru spustíte, Batocera na pozadí sáhne po správném emulátoru: většinou přes **RetroArch** (sjednocené rozhraní s tzv. jádry), u náročnějších systémů po samostatných emulátorech. Tu složitost ale řeší za vás — vy jen vyberete hru a hrajete.',
        ],
      },
      {
        title: 'Na čem Batocera běží',
        body: [
          'Univerzálnost je hlavní devíza. Stejnou filozofii rozjedete na **starém PC** (ideální druhý život pro vyřazený notebook či kancelářskou bednu), na **Raspberry Pi** (oblíbená levná krabička pod televizi) i na řadě **ARM handheldů** včetně zařízení Anbernic.',
          'Výkon určuje, kam až se dostanete. Slabší Raspberry a staré PC pohodlně zvládnou éru do PlayStationu 1. Silnější Raspberry Pi 5 a běžné moderní PC přidají N64, Dreamcast, PSP, Saturn. Na **PS2, GameCube, Wii nebo 3DS** už ale potřebujete pořádné herní PC — emulace těchto systémů je náročná bez ohledu na frontend.',
        ],
      },
      {
        title: 'Instalace krok za krokem',
        body: [
          '1) Na **batocera.org** stáhnete obraz (image) pro své zařízení. 2) Zapíšete ho na SD kartu nebo USB disk — nejčastěji nástrojem **Balena Etcher** (vybrat image, vybrat médium, „Flash"). 3) Z média **nabootujete** (na PC přes boot menu, na Raspberry prostě zasunete kartu). 4) Hry nakopírujete do složek podle systému — `roms/snes`, `roms/megadrive`, `roms/psx` a tak dál. Po restartu se objeví v menu.',
          'Žádná instalace do systému, žádné mazání disku. Když chcete zpět ke svým Windows, jen vypnete a vyndáte médium. To z Batocery dělá bezrizikový způsob, jak si retro hraní vyzkoušet.',
        ],
      },
      {
        title: 'Box-art, BIOS a ovladače',
        body: [
          '**Scraping** je funkce, díky které Batocera ke hrám automaticky stáhne obaly, popisy, žánry i videoukázky a z holého seznamu udělá galerii vypadající jako profesionální herní knihovna — přesně tytéž obaly z komunitní databáze libretro používá i tento web.',
          'Některé systémy (PlayStation, Saturn, Dreamcast a další) potřebují ke spuštění **BIOS soubory**, které Batocera ze zákona nesmí distribuovat — patří do složky `bios/` a bez nich daný emulátor nenastartuje. Co se ovládání týče, Batocera rozezná drtivou většinu **ovladačů** (Xbox, PlayStation, 8BitDo, Switch Pro) drátově i bezdrátově; nastavíte je jednou a fungují všude.',
        ],
      },
      {
        title: 'Save states, netplay, témata a údržba',
        body: [
          'Kromě klasického ukládání umí Batocera **save states** (uložení přesného stavu hry kdykoli), **převíjení** (rewind) i **rychlé přetáčení**. Přes síť zvládne **netplay** — kooperaci nebo souboj po internetu — a streamování.',
          'Vzhled celého prostředí změníte **tématy** (od minimalistických po věrné napodobeniny dobových menu), takže si EmulationStation naladíte přesně podle svého. Aktualizace systému i jader řešíte přímo z menu. A protože je všechno na vyměnitelném médiu, je velmi snadné mít víc karet s různými konfiguracemi nebo zálohovat celou knihovnu.',
        ],
      },
      {
        title: 'Batocera vs. ostatní',
        body: [
          'Batocera není jediná hra na trhu. **Recalbox** je podobně přívětivá a začátečnicky laděná alternativa; **Lakka** je čistý RetroArch bez nadstavby (lehká, ale méně „hezká"); **RetroBat** běží přímo nad Windows, pokud nechcete samostatný systém. Na handheldech jsou pak silní hráči **Knulli** (přímo z rodiny Batocera) a **ROCKNIX**.',
          'Pro většinu lidí je Batocera nejlepší výchozí volbou: obrovská podpora systémů, krásný frontend, velká komunita a stejné prostředí napříč zařízeními. Pokud vám něco nesedne, přechod na alternativu je otázkou zapsání jiného obrazu na kartu.',
        ],
      },
      {
        title: 'Spuštění z USB (i bez instalace)',
        body: [
          'Batoceru nemusíš nikam instalovat — rozjedeš ji **přímo z USB flashky nebo disku**. Postup: image zapíšeš nástrojem **Balena Etcher** na USB, při startu počítače otevřeš **boot menu** (obvykle klávesa F12, F10, F8 nebo Esc hned po zapnutí) a vybereš spuštění z USB. Pevný disk i Windows zůstanou nedotčené.',
          'Je to ideální způsob, jak retro nezávazně vyzkoušet, nebo jak nosit svůj setup s sebou — flashku zasuneš do jiného počítače a hraješ se stejnou knihovnou. Pro plynulost ber **USB 3.0** disk; pomalá flashka zdržuje načítání. (Tip: kdybys chtěl bootovat z USB i na novějším PC, možná bude potřeba v BIOSu vypnout Secure Boot.)',
        ],
      },
      {
        title: 'Adresářová struktura: kam patří hry a BIOS',
        body: [
          'Batocera má jednotné, logické uspořádání. Na médiu je složka **`roms/`** a v ní podsložka pro každý systém — hru prostě nakopíruješ do té správné: `roms/nes`, `roms/snes`, `roms/megadrive`, `roms/gba`, `roms/psx`, `roms/n64`, `roms/dreamcast`, `roms/arcade`… Po restartu nebo „aktualizaci her" v menu se objeví v seznamu.',
          'Soubory **BIOS** patří do složky **`bios/`** (např. `bios/scph5501.bin` pro PlayStation). Když nějaký chybí, Batocera ti to u daného systému přímo vypíše. Obaly, popisy a videa ze scrapingu se ukládají k hrám (do `media`), takže celá knihovna zůstává přenosná.',
          'Tahle struktura je v zásadě stejná i na handheldech s Batocerou/Knulli a velmi podobná i v RetroPie a Recalboxu — pochopíš ji jednou a využiješ všude.',
        ],
      },
    ],
    options: [
      {
        title: 'Začni na starém PC nebo Raspberry',
        text: 'Vyřazený notebook nebo levné Raspberry Pi je ideální základ. Stačí image na SD/USB a bootnout — interní disk zůstává netknutý.',
      },
      {
        title: 'Nezapomeň na BIOS',
        text: 'PS1, Saturn, Dreamcast a další chtějí originální BIOS soubory ve složce bios/. Bez nich emulátor nenastartuje.',
      },
      {
        title: 'Zapni scraping',
        text: 'Necháš Batoceru stáhnout obaly, popisy a videa — z holého seznamu se stane vizuálně bohatá knihovna.',
      },
      {
        title: 'Více karet, více setupů',
        text: 'Díky vyměnitelnému médiu můžeš mít víc karet s různými konfiguracemi a snadno zálohovat celou knihovnu.',
      },
    ],
  },
  {
    slug: 'raspberry-pi',
    name: 'Raspberry Pi & spol.',
    kind: 'Jednodeskový počítač',
    tagline: 'Levná krabička velikosti karetní krabičky, ze které uděláš retro konzoli pod televizi.',
    color: '#c51a4a',
    color2: '#2a0a16',
    art: 'pi',
    intro: [
      'Raspberry Pi je malý jednodeskový počítač (SBC), který se stal legendou domácího kutilství — a v retro hraní hraje první ligu. Za pár stovek až tisícovku dostaneš tichou, úspornou krabičku, kterou připojíš k televizi, nahraješ na ni hotový systém a máš retro konzoli na míru. Kolem Pi navíc existuje obří komunita a hotová řešení, takže rozjezd je otázkou chvíle.',
    ],
    photo: { src: '/images/hardware/raspberry-pi.png', caption: 'Raspberry Pi 4 Model B — celá „konzole" se vejde do dlaně' },
    specs: [
      { label: 'Doporučené modely', value: 'Pi 4 (4 GB) nebo Pi 5; Pi Zero 2 W pro 8/16bit' },
      { label: 'Výstup', value: 'HDMI (Pi 4/5: až 4K), 3,5mm zvuk přes adaptér' },
      { label: 'Úložiště', value: 'microSD (Pi 5 i NVMe přes HAT)' },
      { label: 'Systémy', value: 'Batocera, RetroPie, Recalbox, Lakka' },
      { label: 'Napájení', value: 'USB-C (Pi 5 doporučuje 27W zdroj)' },
      { label: 'Ovladače', value: 'Bluetooth i USB (Xbox, 8BitDo, PS…)' },
    ],
    canPlay: [
      { label: 'NES, SNES, Mega Drive, GB/GBA, PS1, PC Engine', level: 'ok' },
      { label: 'Nintendo 64, PSP, Saturn (hlavně Pi 5)', level: 'most' },
      { label: 'Dreamcast (Pi 5)', level: 'most' },
      { label: 'PS2, GameCube (jen Pi 5, vybrané)', level: 'some' },
    ],
    sections: [
      {
        title: 'Proč zrovna Raspberry Pi',
        body: [
          'Pi je levné, tiché, žere minimum proudu a vejde se za televizi nebo do tištěné krabičky vedle konzolí. Na rozdíl od handheldu ho hraješ na velké obrazovce s plnohodnotným ovladačem — je to klasický „pod televizi" setup. A protože je to plnohodnotný počítač s Linuxem, máš k dispozici tytéž vyspělé systémy jako jinde.',
          'Druhá výhoda je komunita: návodů, hotových obrazů a témat jsou tisíce. Když něco nevíš, někdo to už vyřešil před tebou.',
        ],
      },
      {
        title: 'Který model vybrat',
        body: [
          '**Raspberry Pi 5** je dnes nejlepší volba — utáhne i Dreamcast a Saturn a u náročnějších systémů jede svižně. **Pi 4 (4 GB)** je levnější a pohodlně zvládne vše do PS1 plus většinu N64/PSP. **Pi Zero 2 W** je drobeček ideální do mini buildů a na 8/16bit éru, ale na 3D nečekej zázraky.',
          'K čemukoli nad Pi 4 počítej s **chlazením** (pasivní heatsink nebo aktivní větráček) — emulace procesor zahřeje a bez chlazení se výkon přiškrtí.',
        ],
      },
      {
        title: 'Systémy: Batocera, RetroPie, Recalbox, Lakka',
        body: [
          'Na Pi se nainstaluje systém zapsáním obrazu na microSD (nástrojem Raspberry Pi Imager nebo Balena Etcher). Na výběr máš: **Batocera** (univerzální, krásný frontend, plug & play), **RetroPie** (klasika postavená na Raspbianu, hodně možností ladění), **Recalbox** (přívětivá a jednoduchá) a **Lakka** (čistý RetroArch, lehká).',
          'Pro začátek doporučuju Batoceru nebo Recalbox — nejmenší tření. RetroPie oceníš, když si chceš hrát s detailním nastavením.',
        ],
      },
      {
        title: 'Jak začít krok za krokem',
        body: [
          '1) Stáhni **Raspberry Pi Imager** a zapiš vybraný systém na microSD. 2) Kartu vlož do Pi, připoj HDMI do televize, ovladač a napájení. 3) Po startu projdeš úvodním nastavením (jazyk, ovladač, Wi-Fi). 4) Hry nahraješ do složek podle systému — buď po síti (Pi se objeví jako sdílená složka), nebo přímo na kartu na PC. 5) Některé systémy chtějí **BIOS** soubory do složky `bios/`.',
          'Po restartu se hry objeví v menu, kde k nim necháš stáhnout obaly a popisy (scraping). Hotovo — máš domácí retro konzoli.',
        ],
      },
      {
        title: 'Příslušenství a alternativy',
        body: [
          'Vyplatí se **krabička s chlazením**, kvalitní **napájení** (podvýživa zlobí) a rychlá microSD. Ovladač klidně bezdrátový — 8BitDo, Xbox i DualShock fungují.',
          'Pi není jediný SBC. Podobně poslouží **Odroid** (N2+, výkonný), **Orange Pi** nebo **Radxa Rock**; existují i levná **mini PC** (x86), která rozjedou Batoceru jako PC a nabídnou víc výkonu za podobné peníze. Pi má ale největší komunitu a podporu, takže pro začátek je nejjistější.',
        ],
      },
    ],
    options: [
      { title: 'Chlazení není luxus', text: 'U Pi 4/5 pořiď heatsink nebo větráček — bez chlazení se výkon při emulaci přiškrtí.' },
      { title: 'Kvalitní zdroj', text: 'Slabé napájení způsobuje pády a zlobení. Pi 5 chce 27W USB-C zdroj.' },
      { title: 'Hry po síti', text: 'Pi se v síti objeví jako sdílená složka — ROMy a BIOS nakopíruješ pohodlně z PC bez vyndávání karty.' },
    ],
  },
  {
    slug: 'android',
    name: 'Android (boxy, TV i telefony)',
    kind: 'Mobilní platforma',
    tagline: 'Telefon, TV box nebo Android TV — emulátor stáhneš z obchodu a hraješ během minut.',
    color: '#3ddc84',
    color2: '#0e2a1b',
    art: 'android',
    intro: [
      'Android je možná nejdostupnější cesta k retru — zařízení už nejspíš máš v kapse nebo pod televizí. Emulátory se instalují jako běžné aplikace, ovladač spáruješ přes Bluetooth a můžeš hrát na telefonu, tabletu, levném TV boxu i v Android TV. Výkon kolísá od skromných boxů po vlajkové telefony, které zvládnou i náročné konzole.',
    ],
    specs: [
      { label: 'Zařízení', value: 'telefon, tablet, TV box, Android TV' },
      { label: 'Ovladač', value: 'Bluetooth (8BitDo, Xbox, DualSense) nebo USB-OTG' },
      { label: 'Výstup', value: 'obrazovka zařízení nebo TV (box / HDMI / cast)' },
      { label: 'Klíčové appky', value: 'RetroArch + samostatné emulátory' },
      { label: 'Výkon', value: 'dle čipu — od PS1 po PS2/GameCube' },
    ],
    canPlay: [
      { label: 'NES, SNES, Mega Drive, GB/GBA, PS1, PSP', level: 'ok' },
      { label: 'Nintendo 64, DS, Dreamcast', level: 'most' },
      { label: 'PS2, GameCube, Wii, 3DS (silné telefony)', level: 'some' },
    ],
    sections: [
      {
        title: 'Telefon vs. TV box vs. Android TV',
        body: [
          '**Telefon/tablet** je nejvýkonnější (vlajkové čipy utáhnou i PS2 nebo GameCube) a máš ho po ruce — stačí dokoupit ovladač s držákem. **Android TV** (v televizi nebo jako klacek) je pohodlná cesta hrát rovnou na velké obrazovce. **Levné TV boxy** jsou nejlevnější, ale výkonem slabší a je u nich potřeba opatrnost (viz níže).',
          'Společné mají všechny jedno: instalace je jako u kterékoli appky a hraní na velké obrazovce vyřeší ovladač přes Bluetooth.',
        ],
      },
      {
        title: 'Které aplikace',
        body: [
          'Univerzální základ je **RetroArch** (zdarma, desítky jader pod jednou střechou). Pro náročnější systémy se ale vyplatí **samostatné emulátory**, které bývají výkonnější a pohodlnější: **DuckStation** (PS1), **PPSSPP** (PSP), **Dolphin** (GameCube/Wii), **melonDS** / DraStic (DS), **Redream** / Flycast (Dreamcast), **Citra-nástupci** (3DS).',
          'Pro 8/16bit éru a handheldy stačí RetroArch nebo jednoúčelové appky — rozdíl ve výkonu tam nehraje roli.',
        ],
      },
      {
        title: 'Jak začít',
        body: [
          '1) Z obchodu (Google Play, případně APK z oficiálního zdroje) nainstaluj RetroArch nebo zvolený emulátor. 2) Nahraj hry do složky v úložišti (např. `Roms/`) — z PC kabelem nebo přes cloud. 3) V appce nastav cestu ke hrám; někdy je potřeba **BIOS** (PS1, DS…). 4) Spáruj **ovladač** přes Bluetooth a namapuj tlačítka.',
          'Hotovo. Na telefonu doporučuju ovladač s držákem (telefon „zaklapneš" doprostřed), na TV boxu klasický gamepad.',
        ],
      },
      {
        title: 'Pozor na levné TV boxy',
        body: [
          'Trh s levnými Android boxy je plný kousků s **nadhodnocenými parametry** a starou verzí Androidu. Klidně inzerují „8 GB RAM / 8K", ale realita je jiná a emulace náročnějších systémů drhne. Před koupí čti recenze a ber údaje s rezervou.',
          'Pokud chceš jistotu výkonu na velké obrazovce, je často lepší **herní telefon / tablet** připojený k TV, nebo rovnou Raspberry Pi či mini PC.',
        ],
      },
    ],
    options: [
      { title: 'Ovladač je základ', text: 'Bez fyzického ovladače je hraní utrpení. 8BitDo, Xbox i DualSense fungují přes Bluetooth.' },
      { title: 'Samostatné emulátory pro 3D', text: 'Na PS1/PSP/GC/DS bývají samostatné appky (DuckStation, PPSSPP, Dolphin) výkonnější než RetroArch jádra.' },
      { title: 'Hraj na telefonu na TV', text: 'Přes kabel, HDMI adaptér nebo cast pošleš obraz z telefonu na televizi a hraješ na velkém.' },
    ],
  },
  {
    slug: 'pc-emulace',
    name: 'Emulace na PC',
    kind: 'Návod & emulátory',
    tagline: 'Nejvýkonnější a nejflexibilnější cesta — od 8 bitů až po PS2, GameCube a 3DS.',
    color: '#6e8bff',
    color2: '#141a33',
    art: 'pc',
    intro: [
      'PC je králem emulace: největší výkon, nejpřesnější emulátory a nejvíc možností ladění. Rozjedeš na něm prakticky cokoli — od Atari 2600 až po PlayStation 2, GameCube, Wii nebo 3DS, pokud máš dost výkonný stroj. Můžeš jít cestou jednoho sjednoceného programu (RetroArch), nebo pro každou platformu použít špičkový samostatný emulátor; nejlepší výsledky dává kombinace obojího.',
    ],
    photo: { src: '/images/hardware/pc-emulace.png', caption: 'RetroArch — jedno rozhraní, desítky systémů pod jednou střechou' },
    specs: [
      { label: 'Systém', value: 'Windows, Linux i macOS' },
      { label: 'Výkon', value: 'silné jednovlákno CPU; GPU s Vulkan/OpenGL pro 3D' },
      { label: 'Univerzál', value: 'RetroArch (jádra) + EmulationStation/EmuDeck' },
      { label: 'Ovladače', value: 'Xbox, DualSense, 8BitDo (XInput plug & play)' },
      { label: 'Frontendy', value: 'EmuDeck, LaunchBox, Playnite, ES-DE' },
    ],
    canPlay: [
      { label: 'Vše 8/16bit, handheldy, PS1, arkády, počítače', level: 'ok' },
      { label: 'N64, PSP, Saturn, Dreamcast, DS', level: 'ok' },
      { label: 'PS2, GameCube, Wii, 3DS, Wii U/Switch (výkonné PC)', level: 'most' },
    ],
    sections: [
      {
        title: 'RetroArch — jeden program pro vše',
        body: [
          '**RetroArch** je sjednocené rozhraní, do kterého si stáhneš tzv. **jádra** (cores) — každé jádro je emulátor jednoho systému. Výhoda: jedno ovládání, jeden vzhled, jedny save states a shadery (např. CRT filtr) napříč všemi systémy. Je zdarma a běží i na všech ostatních zařízeních z tohoto webu, takže co se naučíš na PC, použiješ i na handheldu, Pi nebo Androidu.',
          'Pro 8/16bit éru, handheldy i PS1 je RetroArch ideální. U technicky náročných konzolí (PS2, GameCube…) ale často sáhneš po samostatném emulátoru.',
        ],
      },
      {
        title: 'Samostatné emulátory podle platformy',
        body: [
          'Když chceš nejvyšší kompatibilitu a vychytávky (upscaling, widescreen hacky), jdou cestou samostatných programů. Osvědčená volba podle systému:',
          '**PlayStation 1** → DuckStation · **PlayStation 2** → PCSX2 · **PSP** → PPSSPP · **Nintendo 64** → simple64 / RMG · **GameCube & Wii** → Dolphin · **Nintendo DS** → melonDS · **3DS** → nástupci Citry (Lime3DS / Azahar) · **Saturn** → Mednafen / Kronos · **Dreamcast** → Flycast (nebo Redream) · **Arkády** → MAME, FinalBurn Neo.',
          'Pro počítače: **Amiga** → WinUAE / FS-UAE · **C64** → VICE · **Atari ST** → Hatari · **DOS** → DOSBox. Samostatné emulátory jednotlivých 8/16bit konzolí (Mesen pro NES, Snes9x/bsnes pro SNES, mGBA pro GBA) jsou skvělé na přesnost, ale v RetroArchi je máš taky.',
        ],
      },
      {
        title: 'Jak začít krok za krokem',
        body: [
          '1) **Stáhni** RetroArch (z oficiálního webu / Steamu) nebo konkrétní emulátor. 2) V RetroArchi přes **Online Updater** stáhni jádra systémů, které chceš. 3) Některé systémy vyžadují **BIOS** soubory (PS1, PS2, Saturn, DS…) — patří do složky `system/`. 4) Přidej složky s hrami a nech naskenovat knihovnu. 5) Připoj ovladač a hraj.',
          'Chceš to mít hezké a pohodlné jako na konzoli? Nasaď nad emulátory **frontend**: **EmuDeck** (skvělý zejména na Steam Decku a Windows, nastaví vše za tebe), **LaunchBox** nebo **Playnite** udělají z knihovny elegantní galerii s obaly.',
        ],
      },
      {
        title: 'Ovladače a jejich nastavení',
        body: [
          'PC rozumí **XInput** ovladačům (Xbox) okamžitě — připojíš a funguje. Bezdrátově fungují i **DualSense/DualShock** (přes Bluetooth nebo kabel) a oblíbené **8BitDo** padlety, které navíc umí přepínat režimy (XInput/DirectInput). RetroArch i samostatné emulátory mají vlastní **mapování tlačítek**: jednou nastavíš, co je „A/B/X/Y", a uloží se to.',
          'Tip: pro autentický pocit existují repliky dobových ovladačů (SNES, Mega Drive, N64) s USB/Bluetooth od 8BitDo a dalších. A pokud chceš jeden ovladač na všechno, Xbox nebo 8BitDo Pro 2 jsou sázka na jistotu.',
        ],
      },
      {
        title: 'Legálně',
        body: [
          'Emulátory samotné jsou **legální software**. Co řeší zákon, jsou herní soubory (ROM/ISO) a BIOS — ty si pořiď legálně: vlastní dumpy svých kazet, disků a konzolí, nebo homebrew a freeware tituly. Tenhle web žádné takové soubory nenabízí.',
        ],
      },
      {
        title: 'Kam dávat hry a BIOS (struktura složek)',
        body: [
          'Na PC nejsou hry vázané na pevnou strukturu jako na konzoli — složku s ROMy si uděláš kdekoli (např. `D:\\Roms\\snes`, `D:\\Roms\\psx`) a v emulátoru na ni jen ukážeš. Přehlednosti pomáhá držet schéma **jedna složka = jeden systém**, ať to později snadno napojíš na frontend.',
          '**RetroArch** má vlastní složky: jádra v `cores/`, **BIOS v `system/`** (sem patří např. PS1/Saturn/DS BIOS), uložení v `saves/` a `states/`. **Samostatné emulátory** mají každý svoje: DuckStation, PCSX2 i Dolphin si BIOS/klíče a paměťovky drží ve svých datových složkách (obvykle v Dokumentech nebo vedle programu). Když nasadíš **frontend** (EmuDeck, LaunchBox), ten ti složky pomůže sjednotit a uklidit.',
        ],
      },
    ],
    options: [
      { title: 'Začni RetroArchem', text: 'Pro 8/16bit, handheldy a PS1 je sjednocený RetroArch ideál. Na PS2/GC sáhni po PCSX2/Dolphin.' },
      { title: 'EmuDeck ušetří čas', text: 'Na Windows i Steam Decku ti EmuDeck nastaví emulátory, složky i frontend skoro na jeden klik.' },
      { title: 'BIOS do system/', text: 'PS1, PS2, Saturn nebo DS chtějí originální BIOS. Bez něj jádro nenastartuje.' },
      { title: 'Jeden ovladač na vše', text: 'Xbox nebo 8BitDo Pro 2 fungují všude přes XInput; dobové repliky přidají autentický pocit.' },
    ],
  },
  {
    slug: 'ios',
    name: 'iOS (iPhone & iPad)',
    kind: 'Mobilní platforma',
    tagline: 'Od roku 2024 jdou emulátory i na iPhone a iPad — přímo z App Storu.',
    color: '#9aa0b4',
    color2: '#1a1c24',
    art: 'mobile',
    intro: [
      'Dlouho byla emulace na iPhonu a iPadu spíš pro otrlé (přes složité postupy), ale to se v roce 2024 změnilo: Apple povolil retro herní emulátory **přímo v App Storu**. Dnes si tak appku stáhneš jedním klepnutím jako kteroukoli jinou a hraješ. iPady s čipy řady M jsou navíc tak výkonné, že zvládnou i náročnější konzole.',
    ],
    specs: [
      { label: 'Zařízení', value: 'iPhone, iPad (ideálně s čipem A15+/M)' },
      { label: 'Klíčové appky', value: 'Delta, RetroArch, PPSSPP, DuckStation, Provenance' },
      { label: 'Ovladač', value: 'Bluetooth (Xbox, DualSense, 8BitDo, Backbone)' },
      { label: 'Hry', value: 'přes aplikaci Soubory, iCloud nebo AirDrop' },
      { label: 'Výstup', value: 'obrazovka, nebo TV přes AirPlay / USB-C' },
    ],
    canPlay: [
      { label: 'NES, SNES, N64, GB/GBC/GBA, DS (Delta)', level: 'ok' },
      { label: 'PlayStation (PS1), PSP', level: 'ok' },
      { label: 'Dreamcast, Saturn', level: 'most' },
      { label: 'GameCube, Wii, PS2 (iPad M, přes sideload)', level: 'some' },
    ],
    sections: [
      {
        title: 'Co se v roce 2024 změnilo',
        body: [
          'Apple roky emulátory v App Storu nepovoloval, takže jediná cesta vedla přes komplikované „sideloady" a developerské certifikáty. Na jaře 2024 ale pravidla uvolnil a emulátory retro konzolí jsou teď oficiálně povolené. Pro běžného uživatele to znamená jediné: appku najdeš v App Storu a nainstaluješ stejně snadno jako na Androidu.',
        ],
      },
      {
        title: 'Které aplikace',
        body: [
          'Hvězdou je **Delta** — elegantní emulátor nintendovských systémů (NES, SNES, N64, Game Boy/GBC/GBA, DS) od autora populárního GBA4iOS. Univerzál **RetroArch** pokryje desítky dalších systémů. Pro náročnější tituly jsou skvělé samostatné appky: **PPSSPP** (PSP), **DuckStation** (PS1), **Provenance** (multi-systémový balík).',
          'Pro nejtěžší konzole (GameCube, Wii, PS2) na výkonném iPadu existují emulátory jako DolphiniOS, ale ty se zatím obvykle instalují mimo App Store (přes AltStore/sideload) — je to o krok náročnější.',
        ],
      },
      {
        title: 'Jak začít a nahrát hry',
        body: [
          '1) Z App Storu nainstaluj **Delta** (nebo RetroArch/PPSSPP podle systému). 2) Hry dostaneš do zařízení přes appku **Soubory** (z iCloud Drive, přes AirDrop z Macu, nebo z počítače kabelem) a v emulátoru je naimportuješ. 3) Některé systémy chtějí **BIOS** (PS1, DS…) — přidáš je stejnou cestou. 4) Spáruj **ovladač** přes Bluetooth a hraj.',
        ],
      },
      {
        title: 'Ovladače a iPad jako mini konzole',
        body: [
          'iOS bez problémů spáruje **Xbox**, **DualSense (PS5)** i **8BitDo** ovladače přes Bluetooth — stačí v nastavení Bluetooth a hraješ. Populární jsou i „klipsy" jako **Backbone** nebo GameSir, do kterých telefon zasuneš a vznikne z něj handheld.',
          'iPad s čipem M je sám o sobě malá herní stanice: přes **AirPlay** nebo **USB-C** pošleš obraz na televizi, připojíš ovladač a máš plnohodnotný retro setup na velké obrazovce.',
        ],
      },
    ],
    options: [
      { title: 'Začni Deltou', text: 'Pro nintendovské systémy (NES–DS) je Delta nejpohodlnější. Na zbytek RetroArch nebo samostatné appky.' },
      { title: 'Ovladač přes Bluetooth', text: 'Xbox, DualSense i 8BitDo se spárují za pár vteřin; klipsy Backbone/GameSir z telefonu udělají handheld.' },
      { title: 'Hry přes Soubory/iCloud', text: 'ROMy a BIOS dostaneš do appky přes Soubory, iCloud Drive nebo AirDrop. Sháněj je legálně.' },
    ],
  },
  {
    slug: 'konzole-emulace',
    name: 'Emulace na konzolích (PS, Xbox, Switch)',
    kind: 'Návod — homebrew scéna',
    tagline: 'I z PlayStationu, Xboxu nebo Switche jde udělat retro stroj — přes jejich homebrew scénu.',
    color: '#b06bff',
    color2: '#1e1430',
    art: 'console',
    intro: [
      'Moderní herní konzole mají pod kapotou hodně výkonu — a komunita ho umí využít i k emulaci. Přes tzv. homebrew (neoficiální software) se z PlayStationu, Xboxu i Switche dá udělat plnohodnotná retro mašina s RetroArchem. Je to o úroveň pokročilejší než handheld nebo Raspberry: záleží na konkrétním modelu a verzi firmwaru, někdy hrozí ztráta záruky nebo ban v online službách. Tady je přehled, co která rodina umí.',
    ],
    specs: [
      { label: 'Princip', value: 'homebrew / úprava firmwaru daného modelu' },
      { label: 'Software', value: 'většinou RetroArch (port na danou konzoli)' },
      { label: 'Závisí na', value: 'modelu a verzi firmwaru (důležité!)' },
      { label: 'Ovladač', value: 'rovnou ovladač dané konzole' },
      { label: 'Riziko', value: 'ztráta záruky, u online i ban — na vlastní odpovědnost' },
    ],
    canPlay: [
      { label: 'PS Vita, original Xbox, Switch: 8/16bit–PS1, PSP', level: 'ok' },
      { label: 'PS3 / Xbox 360 / Switch: N64, DC, PSP, Saturn', level: 'most' },
      { label: 'Switch / Series: GameCube, Wii, PS2 (vybrané)', level: 'some' },
    ],
    sections: [
      {
        title: 'Než začneš: jak to funguje a legálně',
        body: [
          'Konzole z výroby spouští jen podepsaný software. „Homebrew" scéna hledá způsoby, jak na konkrétním modelu spustit i neoficiální aplikace (mezi nimi RetroArch). Postup se liší konzoli od konzole a hlavně podle **verze firmwaru** — proto vždy nejdřív zjisti, co tvůj konkrétní kus a jeho firmware umožňuje.',
          'Důležité varování: úprava může **zrušit záruku**, při chybě konzoli dočasně znefunkčnit a v online službách (hlavně Switch) hrozí **ban**. Dělej to na vlastní odpovědnost, ideálně na zařízení, které není připojené k online účtu. A jako všude jinde — hry sháněj legálně (vlastní dumpy).',
        ],
      },
      {
        title: 'PlayStation',
        body: [
          'Klasické **PS1 a PS2** rozběhne homebrew z paměťové karty (na PS2 legendární FreeMcBoot) a poslouží jako solидní emulátor 8/16bit a starších systémů. **PS3** se přes HEN/CFW dostane k RetroArchi a zvládne i náročnější systémy. Skutečným klenotem pro retro je ale **PS Vita** — po úpravě (HENkaku) je to skvělý kapesní RetroArch stroj, ideální až po PS1/PSP.',
          'Novější **PS4/PS5** jdou upravit jen na starších, zranitelných verzích firmwaru a možnosti jsou omezenější — pro retro je rozumnější sáhnout po starší konzoli nebo handheldu.',
        ],
      },
      {
        title: 'Xbox',
        body: [
          'Původní **Xbox (2001)** je po „softmodu" pověstná retro mašina — díky výkonu a velkému disku z něj uděláš elegantní emulační centrum (RetroArch, MAME, dobové frontendy). **Xbox 360** se otevírá složitěji (RGH).',
          'Skvělá zpráva je u **Xbox One a Series X|S**: stačí zdarma zapnout **Dev Mode** (vývojářský režim) a nainstalovat **RetroArch oficiálně** — bez jailbreaku a bez ztráty záruky. Je to asi nejjednodušší legální cesta, jak z moderní konzole udělat výkonný retro stroj (klidně až po Dreamcast, PSP a víc).',
        ],
      },
      {
        title: 'Nintendo Switch',
        body: [
          'Switch je výkonný handheld, takže láká i na emulaci. Jde to přes homebrew (custom firmware Atmosphère) a následně **RetroArch** — Switch pak zvládne retro až po náročnější systémy (N64, Dreamcast, PSP, vybrané GameCube/Wii). Hraní v ruce i na televizi je obrovská výhoda.',
          'Velké ALE: homebrew jde jen na **starších, hardwarově zranitelných** kusech (novější revize a Lite/OLED většinou ne) a **online ban je tu reálné riziko** — proto se to dělá na konzoli odpojené od Nintenda. Zvaž, jestli ti to za to stojí; jinak je čistší cesta dedikovaný handheld nebo Raspberry.',
        ],
      },
    ],
    options: [
      { title: 'Nejdřív zjisti firmware', text: 'Možnosti i postup stojí a padají s modelem a verzí firmwaru. Ověř si svůj kus, než cokoli uděláš.' },
      { title: 'Nejjednodušší: Xbox Series Dev Mode', text: 'Zapneš vývojářský režim a nainstaluješ RetroArch oficiálně — bez jailbreaku a ztráty záruky.' },
      { title: 'PS Vita = skvělý retro handheld', text: 'Po úpravě je z Vity vynikající kapesní RetroArch stroj až po PS1/PSP.' },
      { title: 'Pozor na bany a záruku', text: 'U Switche hrozí online ban; obecně riskuješ záruku. Dělej to odpojené od účtu a na vlastní odpovědnost.' },
    ],
  },
];

export const HW_LEVEL_LABEL: Record<'ok' | 'most' | 'some', string> = {
  ok: 'Plynule',
  most: 'Většinou',
  some: 'Vybrané tituly',
};

export const getHardware = (slug: string) => hardware.find((h) => h.slug === slug);
