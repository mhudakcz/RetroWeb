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
];

export const HW_LEVEL_LABEL: Record<'ok' | 'most' | 'some', string> = {
  ok: 'Plynule',
  most: 'Většinou',
  some: 'Vybrané tituly',
};

export const getHardware = (slug: string) => hardware.find((h) => h.slug === slug);
