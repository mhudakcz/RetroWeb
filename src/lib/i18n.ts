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

/** Cesty, které už mají EN/DE variantu (Fáze A). Ostatní zatím padají na češtinu. */
export const LOCALIZED_ROUTES = new Set<string>(['/', '/podporit', '/kontakt']);

/** Odkaz do navigace: lokalizuje jen cesty, které EN/DE variantu mají,
 *  jinak vede na českou verzi (aby nevznikaly 404 před dokončením překladů). */
export function navHref(l: Locale, path: string): string {
  return LOCALIZED_ROUTES.has(path) ? localizePath(l, path) : path;
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
