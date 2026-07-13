// Lokalizace: čeština (výchozí, na /), angličtina (/en/), němčina (/de/).

export const LOCALES = ['cs', 'en', 'de'] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = 'cs';

export const LOCALE_NAME: Record<Locale, string> = {
  cs: 'Čeština',
  en: 'English',
  de: 'Deutsch',
};
export const LOCALE_FLAG: Record<Locale, string> = {
  cs: '🇨🇿',
  en: '🇬🇧',
  de: '🇩🇪',
};

/** Prefix cesty pro daný jazyk ('' pro CS, '/en', '/de'). */
export const localePrefix = (l: Locale): string => (l === DEFAULT_LOCALE ? '' : `/${l}`);

/** Připojí jazykový prefix na absolutní cestu ('/hry' -> '/en/hry'). */
export function localizePath(l: Locale, path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`;
  return (localePrefix(l) + p).replace(/\/$/, '') || '/';
}

/** Sekce webu, které už mají EN/DE varianty. Postupně přibývají (Fáze B).
 *  Root cesta sekce ('/', '/platformy', '/hry', …). */
export const LOCALIZED_SECTIONS = new Set<string>([
  '/', '/podporit', '/kontakt', '/platformy', '/studia',
]);

/** Root sekce z cesty: '/platformy/game-boy' -> '/platformy', '/' -> '/'. */
function sectionRoot(path: string): string {
  const seg = path.split('/').filter(Boolean)[0];
  return seg ? `/${seg}` : '/';
}

/** Odkaz respektující, zda cílová sekce už má překlad: pokud ano, lokalizuje,
 *  jinak vede na českou verzi (aby nevznikaly 404 před dokončením překladů). */
export function navHref(l: Locale, path: string): string {
  const root = path === '/' ? '/' : sectionRoot(path);
  return LOCALIZED_SECTIONS.has(root) ? localizePath(l, path) : path;
}

/** Zjistí jazyk z URL cesty. */
export function localeFromPath(pathname: string): Locale {
  const seg = pathname.split('/').filter(Boolean)[0];
  return (LOCALES as readonly string[]).includes(seg) ? (seg as Locale) : DEFAULT_LOCALE;
}

/** UI řetězce. Klíč -> překlad podle jazyka. */
type Dict = Record<string, Record<Locale, string>>;
const UI: Dict = {
  'nav.home': { cs: 'Domů', en: 'Home', de: 'Start' },
  'nav.platforms': { cs: 'Platformy', en: 'Platforms', de: 'Plattformen' },
  'nav.games': { cs: 'Hry', en: 'Games', de: 'Spiele' },
  'nav.studios': { cs: 'Studia', en: 'Studios', de: 'Studios' },
  'nav.hardware': { cs: 'Hardware', en: 'Hardware', de: 'Hardware' },
  'nav.about': { cs: 'O projektu', en: 'About', de: 'Über' },
  'nav.contact': { cs: 'Kontakt & přání', en: 'Contact & wishes', de: 'Kontakt & Wünsche' },
  'nav.support': { cs: 'Podpořit web ☕', en: 'Support the site ☕', de: 'Seite unterstützen ☕' },

  'theme.toggle': { cs: 'Přepnout denní/noční režim', en: 'Toggle day/night mode', de: 'Tag-/Nachtmodus umschalten' },
  'theme.dark': { cs: '🌙 Noční režim', en: '🌙 Dark mode', de: '🌙 Nachtmodus' },
  'theme.light': { cs: '☀️ Denní režim', en: '☀️ Light mode', de: '☀️ Tagmodus' },
  'nav.openMenu': { cs: 'Otevřít menu', en: 'Open menu', de: 'Menü öffnen' },
  'nav.closeMenu': { cs: 'Zavřít menu', en: 'Close menu', de: 'Menü schließen' },
  'nav.language': { cs: 'Jazyk', en: 'Language', de: 'Sprache' },

  'footer.tagline': {
    cs: 'Průvodce světem retro hraní — historie platforem, legendární hry a tipy pro handheldy jako Anbernic RG35XX Pro a R36S nebo Batocera na PC.',
    en: 'A guide to the world of retro gaming — platform history, legendary games and tips for handhelds like the Anbernic RG35XX Pro and R36S or Batocera on PC.',
    de: 'Ein Wegweiser durch die Welt des Retro-Gamings — Plattform-Geschichte, legendäre Spiele und Tipps für Handhelds wie Anbernic RG35XX Pro und R36S oder Batocera am PC.',
  },
  'footer.content': { cs: 'Obsah', en: 'Content', de: 'Inhalt' },
  'footer.community': { cs: 'Komunita', en: 'Community', de: 'Community' },
  'footer.aboutLink': { cs: 'O projektu & návod', en: 'About & guide', de: 'Über & Anleitung' },
  'footer.hardwareLink': { cs: 'Hardware & Batocera', en: 'Hardware & Batocera', de: 'Hardware & Batocera' },
  'footer.legal': {
    cs: 'Hry shánějte legálně — vlastní dumpy kazet a disků, nebo homebrew a freeware 🆓. Web žádné ROM soubory nenabízí.',
    en: 'Get games legally — your own cartridge/disc dumps, or homebrew and freeware 🆓. This site offers no ROM files.',
    de: 'Spiele legal beschaffen — eigene Dumps von Modulen/Discs oder Homebrew und Freeware 🆓. Diese Seite bietet keine ROM-Dateien an.',
  },
  'footer.built': { cs: 'postaveno s Astro', en: 'built with Astro', de: 'erstellt mit Astro' },
  'footer.data': { cs: 'Data: vlastní kurátorské podklady', en: 'Data: own curated sources', de: 'Daten: eigene kuratierte Quellen' },

  'games.count': { cs: 'her', en: 'games', de: 'Spiele' },
  'platforms.count': { cs: 'platforem', en: 'platforms', de: 'Plattformen' },

  // detail platformy / společné
  'detail.history': { cs: 'Historie & kontext', en: 'History & context', de: 'Geschichte & Kontext' },
  'detail.recommended': { cs: 'Doporučené hry', en: 'Recommended games', de: 'Empfohlene Spiele' },
  'detail.withComment': { cs: 's komentářem', en: 'with commentary', de: 'mit Kommentar' },
  'detail.year': { cs: 'Rok', en: 'Year', de: 'Jahr' },
  'filter.allGenres': { cs: 'Všechny žánry', en: 'All genres', de: 'Alle Genres' },
  'filter.emptyGenre': { cs: 'Žádná hra v tomto žánru.', en: 'No game in this genre.', de: 'Kein Spiel in diesem Genre.' },
  'pager.prevPlatform': { cs: '← Předchozí platforma', en: '← Previous platform', de: '← Vorherige Plattform' },
  'pager.nextPlatform': { cs: 'Další platforma →', en: 'Next platform →', de: 'Nächste Plattform →' },
  'pager.morePlatforms': { cs: 'Další platformy', en: 'More platforms', de: 'Weitere Plattformen' },
  'suggest.sub': { cs: 'Napiš mi ji — kurátorský výběr pořád rozšiřuju.', en: 'Tell me — I keep expanding the curated selection.', de: 'Schreib mir — ich erweitere die Auswahl laufend.' },
  'suggest.btn': { cs: '💡 Navrhnout hru', en: '💡 Suggest a game', de: '💡 Spiel vorschlagen' },
  'crumbs.games': { cs: 'Hry', en: 'Games', de: 'Spiele' },

  // studia
  'studios.title': { cs: 'Herní studia', en: 'Game studios', de: 'Spiele-Studios' },
  'studios.eyebrow': { cs: 'Tvůrci', en: 'Creators', de: 'Macher' },
  'studios.lead': {
    cs: 'Kdo stál za klasikami. Profily studií, jejich historie, proměny a hry, které tu máme.',
    en: 'Who was behind the classics. Studio profiles, their history, transformations and the games we have here.',
    de: 'Wer hinter den Klassikern stand. Studio-Profile, ihre Geschichte, Wandlungen und die Spiele, die wir hier haben.',
  },
  'studio.eyebrow': { cs: 'Herní studio', en: 'Game studio', de: 'Spiele-Studio' },
  'studio.inCatalog': { cs: 'her v katalogu', en: 'games in the catalogue', de: 'Spiele im Katalog' },
  'studio.gamesOf': { cs: 'Hry studia', en: 'Games by the studio', de: 'Spiele des Studios' },

  // hardware
  'hw.title': { cs: 'Hardware & emulace', en: 'Hardware & emulation', de: 'Hardware & Emulation' },
  'hw.eyebrow': { cs: 'Na čem hrát', en: 'What to play on', de: 'Worauf spielen' },
  'hw.lead': {
    cs: 'Handheldy, jednodeskové počítače, PC i mobil — na čem všem se dá rozjet retro a jak na to.',
    en: 'Handhelds, single-board computers, PC and mobile — everything you can run retro on and how to do it.',
    de: 'Handhelds, Einplatinencomputer, PC und Handy — worauf sich Retro betreiben lässt und wie.',
  },
  'hw.specs': { cs: 'Parametry', en: 'Specs', de: 'Technische Daten' },
  'hw.canPlay': { cs: 'Co utáhne', en: 'What it runs', de: 'Was es packt' },
  'hw.toc': { cs: 'V tomto průvodci', en: 'In this guide', de: 'In diesem Guide' },
  'hw.options': { cs: 'Rychlé tipy', en: 'Quick tips', de: 'Schnelle Tipps' },
  'hw.more': { cs: 'Další průvodci', en: 'More guides', de: 'Weitere Guides' },
  'hwlvl.ok': { cs: 'Plynule', en: 'Smoothly', de: 'Flüssig' },
  'hwlvl.most': { cs: 'Většinou', en: 'Mostly', de: 'Meistens' },
  'hwlvl.some': { cs: 'Vybrané tituly', en: 'Select titles', de: 'Ausgewählte Titel' },

  // katalog her — filtr
  'games.eyebrow': { cs: 'Herní katalog', en: 'Game catalogue', de: 'Spielekatalog' },
  'games.search': { cs: '🔍 Hledat hru…', en: '🔍 Search a game…', de: '🔍 Spiel suchen…' },
  'games.allPlatforms': { cs: 'Všechny platformy', en: 'All platforms', de: 'Alle Plattformen' },
  'games.multiplayer': { cs: '👥 Pro více hráčů', en: '👥 Multiplayer', de: '👥 Mehrspieler' },
  'games.commented': { cs: '📝 S komentářem', en: '📝 With commentary', de: '📝 Mit Kommentar' },
  'games.empty': { cs: 'Nic nenalezeno — zkus uvolnit filtry.', en: 'Nothing found — try relaxing the filters.', de: 'Nichts gefunden — lockere die Filter.' },
  'games.lead2': { cs: 'Hledej a filtruj.', en: 'Search and filter.', de: 'Suchen und filtern.' },

  // příznaky her
  'flag.homebrew': { cs: '🆓 Homebrew', en: '🆓 Homebrew', de: '🆓 Homebrew' },
  'flag.mustplay': { cs: '⭐ Must-play', en: '⭐ Must-play', de: '⭐ Must-play' },
  'flag.mature': { cs: '🔞 18+', en: '🔞 18+', de: '🔞 18+' },
  'flag.puzzle': { cs: '🧩 Logická', en: '🧩 Puzzle', de: '🧩 Logik' },

  // žánrové kategorie
  'genre.platformer': { cs: 'Plošinovky', en: 'Platformers', de: 'Jump ’n’ Runs' },
  'genre.action': { cs: 'Akční', en: 'Action', de: 'Action' },
  'genre.rpg': { cs: 'RPG / JRPG', en: 'RPG / JRPG', de: 'RPG / JRPG' },
  'genre.metroidvania': { cs: 'Metroidvanie', en: 'Metroidvania', de: 'Metroidvania' },
  'genre.fighting': { cs: 'Bojovky', en: 'Fighting', de: 'Beat ’em ups' },
  'genre.shooter': { cs: 'Střílečky', en: 'Shooters', de: 'Shooter' },
  'genre.racing': { cs: 'Závodní / auta', en: 'Racing', de: 'Rennspiele' },
  'genre.puzzle': { cs: 'Logické', en: 'Puzzle', de: 'Logik' },
  'genre.adventure': { cs: 'Adventury', en: 'Adventure', de: 'Adventures' },
  'genre.strategy': { cs: 'Strategie / Sim', en: 'Strategy / Sim', de: 'Strategie / Sim' },
  'genre.sport': { cs: 'Sport', en: 'Sports', de: 'Sport' },

  // homepage
  'home.eyebrow': { cs: '★ Insert coin · Press start', en: '★ Insert coin · Press start', de: '★ Insert coin · Press start' },
  'home.h1a': { cs: 'Svět', en: 'The world of', de: 'Die Welt des' },
  'home.h1b': { cs: 'retro hraní', en: 'retro gaming', de: 'Retro-Gamings' },
  'home.h1c': { cs: 'na jednom místě', en: 'in one place', de: 'an einem Ort' },
  'home.lead': {
    cs: 'Historie legendárních konzolí a počítačů, jejich nejlepší hry a tipy pro handheldy jako Anbernic RG35XX Pro, R36S a Batocera na starším PC.',
    en: 'The history of legendary consoles and computers, their best games and tips for handhelds like the Anbernic RG35XX Pro, R36S and Batocera on an older PC.',
    de: 'Die Geschichte legendärer Konsolen und Computer, ihre besten Spiele und Tipps für Handhelds wie Anbernic RG35XX Pro, R36S und Batocera auf älteren PCs.',
  },
  'home.ctaPlatforms': { cs: 'Prozkoumat platformy', en: 'Explore platforms', de: 'Plattformen entdecken' },
  'home.ctaGames': { cs: 'Procházet hry', en: 'Browse games', de: 'Spiele durchsuchen' },
  'home.images': { cs: 'obrázků', en: 'images', de: 'Bilder' },
  'home.hwEyebrow': { cs: 'Na čem hrát', en: 'What to play on', de: 'Worauf spielen' },
  'home.hwTitle': { cs: 'Hardware & emulace', en: 'Hardware & emulation', de: 'Hardware & Emulation' },
  'home.hwAll': { cs: 'Všichni průvodci →', en: 'All guides →', de: 'Alle Guides →' },
  'home.featEyebrow': { cs: '⭐ Must-play', en: '⭐ Must-play', de: '⭐ Must-play' },
  'home.featTitle': { cs: 'Moderní homebrew klenoty', en: 'Modern homebrew gems', de: 'Moderne Homebrew-Perlen' },
  'home.gamesAll': { cs: 'Všechny hry →', en: 'All games →', de: 'Alle Spiele →' },

  // typy platforem (sekce na homepage)
  'type.console.label': { cs: 'Herní konzole', en: 'Game consoles', de: 'Spielkonsolen' },
  'type.handheld.label': { cs: 'Kapesní konzole', en: 'Handhelds', de: 'Handhelds' },
  'type.computer.label': { cs: 'Domácí počítače', en: 'Home computers', de: 'Heimcomputer' },
  'type.arcade.label': { cs: 'Arkády', en: 'Arcades', de: 'Arcades' },
  'type.fantasy.label': { cs: 'Fantasy konzole', en: 'Fantasy consoles', de: 'Fantasy-Konsolen' },
  'type.console.tag': { cs: 'Stroje pod televizi, které definovaly herní generace.', en: 'Machines under the TV that defined gaming generations.', de: 'Geräte unterm Fernseher, die Gaming-Generationen prägten.' },
  'type.handheld.tag': { cs: 'Hraní do kapsy — srdce dnešních zařízení jako Anbernic.', en: 'Gaming in your pocket — the heart of today’s devices like Anbernic.', de: 'Gaming für die Tasche — das Herz heutiger Geräte wie Anbernic.' },
  'type.computer.tag': { cs: '8bitové a 16bitové počítače domácí éry.', en: '8-bit and 16-bit computers of the home era.', de: '8-Bit- und 16-Bit-Computer der Heim-Ära.' },
  'type.arcade.tag': { cs: 'Herny, mince a nekompromisní obtížnost.', en: 'Arcades, coins and uncompromising difficulty.', de: 'Spielhallen, Münzen und kompromisslose Schwierigkeit.' },
  'type.fantasy.tag': { cs: 'Moderní „virtuální" konzole s nostalgickými limity.', en: 'Modern “virtual” consoles with nostalgic limits.', de: 'Moderne „virtuelle" Konsolen mit nostalgischen Grenzen.' },
};

export function t(locale: Locale, key: string): string {
  const e = UI[key];
  if (!e) return key;
  return e[locale] ?? e[DEFAULT_LOCALE];
}
