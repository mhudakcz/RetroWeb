// Obsah o hardwaru: retro handheldy a Batocera.
// Strukturováno tak, aby šlo později snadno přeložit (cs/en) – zatím čeština.

export interface HardwareSpec {
  label: string;
  value: string;
}

export interface HardwareItem {
  slug: string;
  name: string;
  kind: string; // typový štítek
  tagline: string;
  color: string;
  color2: string;
  art: 'handheld-h' | 'handheld-v' | 'batocera';
  intro: string[]; // odstavce
  specs: HardwareSpec[];
  canPlay: { label: string; level: 'ok' | 'most' | 'some' }[]; // co utáhne
  options: { title: string; text: string }[]; // možnosti / software / tipy
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
      'RG35XX Pro je vylepšená, „horizontální" varianta populární řady RG35XX od čínského výrobce Anbernic. Oproti původnímu svislému modelu přidává výkonnější čip **Allwinner H700** (čtyřjádrové ARM Cortex-A53), pohodlnější rozložení ovládacích prvků, dva analogové sticky a lepší výdrž.',
      'Displej je 3,5" IPS s poměrem stran **4:3** a rozlišením 640×480 — přesně to, co retro hrám sedí, protože většina konzolí a počítačů do éry PS1 používala právě tento poměr. Obraz je ostrý a barevný, takže i osmibitové hry vypadají skvěle.',
      'Síla RG35XX Pro je v poměru cena/výkon a v komunitní podpoře. Běží na něm celá řada operačních systémů a emulace je vyladěná tak, že většinu retro knihovny zvládne plynule.',
    ],
    specs: [
      { label: 'Čip (SoC)', value: 'Allwinner H700, 4× Cortex-A53' },
      { label: 'Displej', value: '3,5" IPS, 640×480 (4:3)' },
      { label: 'Paměť', value: '1 GB DDR4' },
      { label: 'Baterie', value: '~3300 mAh (cca 5–8 h hraní)' },
      { label: 'Úložiště', value: 'microSD (systém + hry)' },
      { label: 'Systémy', value: 'muOS, Knulli, Batocera, stock Linux' },
    ],
    canPlay: [
      { label: 'NES, SNES, Mega Drive, GB/GBC/GBA', level: 'ok' },
      { label: 'PlayStation (PS1)', level: 'ok' },
      { label: 'Nintendo 64, PSP', level: 'most' },
      { label: 'Dreamcast', level: 'some' },
    ],
    options: [
      {
        title: 'Operační systémy',
        text: 'Kromě dodávaného systému je oblíbený **muOS** (rychlý, čistý), **Knulli** (z rodiny Batocera/EmulationStation) a samotná **Batocera**. Mění se jen obraz na SD kartě — zařízení tím nijak neutrpí.',
      },
      {
        title: 'Dvě SD karty',
        text: 'Pro má dva sloty: do prvního patří systém, do druhého hry (ROM set). Hry tak můžeš přenášet mezi zařízeními a systém kdykoli přeinstalovat bez ztráty knihovny.',
      },
      {
        title: 'Tipy na výkon',
        text: 'Čip H700 utáhne 8/16bit, GBA i PS1 bez kompromisů. U N64 a PSP vybírej tituly (2D a lehčí 3D jedou, náročné 3D ne). Dreamcast je hraniční — funguje, ale ne vše.',
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
      'R36S je levný „klon" v duchu starších Anbernic RG351 — svislý (vertikální) handheld s 3,5" IPS displejem 640×480. Pohání ho starší čip **Rockchip RK3326** (čtyřjádrové Cortex-A35), takže výkonově je pod RG35XX Pro, zato je velmi levný a má skvělou komunitní podporu.',
      'Právě otevřenost je jeho silná stránka: dodává se s předinstalovaným systémem, ale komunita pro něj připravila vyladěné distribuce jako **ArkOS**, **JELOS** nebo **Batocera**, které z hardwaru vymáčknou maximum.',
      'Je to ideální „první" retro handheld — za málo peněz zahraješ obrovskou knihovnu 8/16bit her, GBA a většinu PS1. Na náročnější systémy už ale nestačí.',
    ],
    specs: [
      { label: 'Čip (SoC)', value: 'Rockchip RK3326, 4× Cortex-A35' },
      { label: 'Displej', value: '3,5" IPS, 640×480 (4:3)' },
      { label: 'Paměť', value: '1 GB DDR3L' },
      { label: 'Baterie', value: '~3200 mAh (cca 4–6 h)' },
      { label: 'Úložiště', value: 'microSD' },
      { label: 'Systémy', value: 'ArkOS, JELOS, Batocera, stock' },
    ],
    canPlay: [
      { label: 'NES, SNES, Mega Drive, GB/GBC/GBA', level: 'ok' },
      { label: 'PlayStation (PS1)', level: 'most' },
      { label: 'Nintendo 64', level: 'some' },
      { label: 'Dreamcast, PSP', level: 'some' },
    ],
    options: [
      {
        title: 'Vyladěné systémy',
        text: '**ArkOS** je nejpopulárnější (stabilní, svižný). **JELOS** a **Batocera** nabídnou modernější frontend. Stačí nahrát obraz na SD kartu.',
      },
      {
        title: 'Pozor na verze',
        text: 'R36S existuje v mnoha výrobních verzích s různými čipy a obrazovkami. Při výběru systému se vyplatí ověřit, jaký panel a SoC máš, aby seděl správný image.',
      },
      {
        title: 'Realistická očekávání',
        text: 'Do PS1 jede skvěle. N64 a PSP jen vybrané tituly. Dreamcast spíš ne. Pro 8/16bit éru je to ale dělník bez chyby.',
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
      'Batocera je svobodná (open-source) linuxová distribuce zaměřená výhradně na retro hraní. Funguje na principu „**plug & play**": nainstaluješ ji na SD kartu nebo USB disk, nabootuješ z ní a máš okamžitě hotový herní systém — bez instalace, beze změny svého počítače.',
      'O ovládání se stará frontend **EmulationStation**: krásné, ovladačem ovladatelné menu, kde procházíš systémy a hry, vidíš box-art, popisy a videa. Pod kapotou běží **RetroArch** a desítky dalších emulátorů, které Batocera spravuje za tebe.',
      'Obrovská výhoda je univerzálnost — stejnou filozofii a uspořádání použiješ na starém PC, na Raspberry Pi i na podporovaných handheldech. Tvůj ROM set a nastavení tak fungují všude stejně.',
    ],
    specs: [
      { label: 'Typ', value: 'Linuxová distribuce (zdarma, open-source)' },
      { label: 'Frontend', value: 'EmulationStation' },
      { label: 'Jádra', value: 'RetroArch + samostatné emulátory' },
      { label: 'Zařízení', value: 'PC (x86), Raspberry Pi, handheldy' },
      { label: 'Instalace', value: 'image na SD/USB (nemění interní disk)' },
      { label: 'Systémy', value: '100+ konzolí, počítačů a arkád' },
    ],
    canPlay: [
      { label: 'Vše 8/16bit, GB/GBA, PS1', level: 'ok' },
      { label: 'N64, Dreamcast, PSP, Saturn', level: 'most' },
      { label: 'PS2, GameCube, Wii (silné PC)', level: 'some' },
    ],
    options: [
      {
        title: 'Jak začít',
        text: 'Stáhni image pro své zařízení z **batocera.org**, zapiš ho na SD/USB (např. nástrojem Balena Etcher) a nabootuj. Hry pak nakopíruješ do složek podle systému (`roms/snes`, `roms/psx`, …).',
      },
      {
        title: 'Box-art a metadata (scraping)',
        text: 'Batocera umí automaticky stáhnout obaly, popisy a videa ke hrám (tzv. scraping). Výsledkem je galerie, která vypadá jako profesionální herní knihovna — přesně ty obaly používá i tento web.',
      },
      {
        title: 'BIOS soubory',
        text: 'Některé systémy (PS1, Saturn, Dreamcast…) vyžadují originální BIOS soubory, které Batocera nesmí distribuovat. Patří do složky `bios/`. Bez nich daný emulátor nenastartuje.',
      },
      {
        title: 'Uložení a ovladače',
        text: 'Podporuje pozice uložení (save states), bezdrátové i drátové ovladače (Xbox, PlayStation, 8BitDo) a po síti i streamování či sdílení knihovny.',
      },
    ],
  },
];

export const HW_LEVEL_LABEL: Record<'ok' | 'most' | 'some', string> = {
  ok: 'Plynule',
  most: 'Většinou',
  some: 'Vybrané tituly',
};
