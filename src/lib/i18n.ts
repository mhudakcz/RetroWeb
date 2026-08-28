// Lokalizace: čeština (výchozí, na /), angličtina (/en/), němčina (/de/).

export const LOCALES = ['cs', 'en', 'de', 'fr'] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = 'cs';

export const LOCALE_NAME: Record<Locale, string> = {
  cs: 'Čeština',
  en: 'English',
  de: 'Deutsch',
  fr: 'Français',
};
export const LOCALE_FLAG: Record<Locale, string> = {
  cs: '🇨🇿',
  en: '🇬🇧',
  de: '🇩🇪',
  fr: '🇫🇷',
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
  '/', '/podporit', '/kontakt', '/platformy', '/studia', '/hry', '/hardware', '/o-projektu',
  '/zmeny', '/serie',
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
  'nav.home': { cs: 'Domů', en: 'Home', de: 'Start', fr: 'Accueil' },
  'footer.changelog': { cs: 'Co je nového', en: "What's new", de: 'Was ist neu', fr: 'Quoi de neuf' },
  'nav.platforms': { cs: 'Platformy', en: 'Platforms', de: 'Plattformen', fr: 'Plateformes' },
  'nav.games': { cs: 'Hry', en: 'Games', de: 'Spiele', fr: 'Jeux' },
  'nav.studios': { cs: 'Studia', en: 'Studios', de: 'Studios', fr: 'Studios' },
  'nav.series': { cs: 'Série', en: 'Series', de: 'Reihen', fr: 'Séries' },
  'nav.hardware': { cs: 'Hardware', en: 'Hardware', de: 'Hardware', fr: 'Matériel' },
  'nav.about': { cs: 'O projektu', en: 'About', de: 'Über', fr: 'À propos' },
  'nav.contact': { cs: 'Kontakt & přání', en: 'Contact & wishes', de: 'Kontakt & Wünsche', fr: 'Contact & souhaits' },
  'nav.support': { cs: 'Podpořit web ☕', en: 'Support the site ☕', de: 'Seite unterstützen ☕', fr: 'Soutenir le site ☕' },

  'theme.toggle': { cs: 'Přepnout denní/noční režim', en: 'Toggle day/night mode', de: 'Tag-/Nachtmodus umschalten', fr: 'Basculer mode jour/nuit' },
  'theme.dark': { cs: '🌙 Noční režim', en: '🌙 Dark mode', de: '🌙 Nachtmodus', fr: '🌙 Mode nuit' },
  'theme.light': { cs: '☀️ Denní režim', en: '☀️ Light mode', de: '☀️ Tagmodus', fr: '☀️ Mode jour' },
  'nav.openMenu': { cs: 'Otevřít menu', en: 'Open menu', de: 'Menü öffnen', fr: 'Ouvrir le menu' },
  'nav.closeMenu': { cs: 'Zavřít menu', en: 'Close menu', de: 'Menü schließen', fr: 'Fermer le menu' },
  'nav.language': { cs: 'Jazyk', en: 'Language', de: 'Sprache', fr: 'Langue' },
  'search.placeholder': { cs: 'Hledat…', en: 'Search…', de: 'Suchen…', fr: 'Rechercher…' },
  'search.label': { cs: 'Hledat na webu', en: 'Search the site', de: 'Website durchsuchen', fr: 'Rechercher sur le site' },
  'search.empty': { cs: 'Nic nenalezeno', en: 'Nothing found', de: 'Nichts gefunden', fr: 'Aucun résultat' },
  'search.kind.g': { cs: 'Hra', en: 'Game', de: 'Spiel', fr: 'Jeu' },
  'search.kind.p': { cs: 'Platforma', en: 'Platform', de: 'Plattform', fr: 'Plateforme' },
  'search.kind.r': { cs: 'Série', en: 'Series', de: 'Reihe', fr: 'Série' },
  'search.kind.d': { cs: 'Studio', en: 'Studio', de: 'Studio', fr: 'Studio' },
  'games.allLetters': { cs: 'Vše', en: 'All', de: 'Alle', fr: 'Tout' },
  'series.jump': { cs: 'Přejít na písmeno', en: 'Jump to letter', de: 'Zum Buchstaben', fr: 'Aller à la lettre' },
  'shot.box': { cs: 'Obal', en: 'Box art', de: 'Verpackung', fr: 'Jaquette' },
  'shot.snap': { cs: 'Ze hry', en: 'In-game', de: 'Aus dem Spiel', fr: 'En jeu' },
  'shot.title': { cs: 'Titulní obrazovka', en: 'Title screen', de: 'Titelbildschirm', fr: 'Écran-titre' },
  'i18n.pending.title': {
    cs: 'Zatím bez překladu',
    en: 'Not translated yet',
    de: 'Noch nicht übersetzt',
    fr: 'Pas encore traduit',
  },
  'i18n.pending.body': {
    cs: 'Tento text je zatím jen v češtině. Na překladu pracujeme, zkuste se sem podívat později.',
    en: 'This text is still only in Czech. We are working on the translation — please check back later.',
    de: 'Dieser Text liegt bisher nur auf Tschechisch vor. Wir arbeiten an der Übersetzung — schauen Sie später wieder vorbei.',
    fr: 'Ce texte n’existe pour l’instant qu’en tchèque. La traduction est en cours — revenez plus tard.',
  },

  'footer.tagline': {
    cs: 'Průvodce světem retro hraní — historie platforem, legendární hry a tipy pro handheldy jako Anbernic RG35XX Pro a R36S nebo Batocera na PC.',
    en: 'A guide to the world of retro gaming — platform history, legendary games and tips for handhelds like the Anbernic RG35XX Pro and R36S or Batocera on PC.',
    de: 'Ein Wegweiser durch die Welt des Retro-Gamings — Plattform-Geschichte, legendäre Spiele und Tipps für Handhelds wie Anbernic RG35XX Pro und R36S oder Batocera am PC.',
    fr: "Un guide du monde du rétrogaming — l'histoire des plateformes, les jeux légendaires et des astuces pour les consoles portables comme l'Anbernic RG35XX Pro et la R36S ou Batocera sur PC.",
  },
  'footer.content': { cs: 'Obsah', en: 'Content', de: 'Inhalt', fr: 'Contenu' },
  'footer.community': { cs: 'Komunita', en: 'Community', de: 'Community', fr: 'Communauté' },
  'footer.aboutLink': { cs: 'O projektu & návod', en: 'About & guide', de: 'Über & Anleitung', fr: 'À propos & guide' },
  'footer.hardwareLink': { cs: 'Hardware & Batocera', en: 'Hardware & Batocera', de: 'Hardware & Batocera', fr: 'Matériel & Batocera' },
  'footer.legal': {
    cs: 'Hry shánějte legálně — vlastní dumpy kazet a disků, nebo homebrew a freeware 🆓. Web žádné ROM soubory nenabízí.',
    en: 'Get games legally — your own cartridge/disc dumps, or homebrew and freeware 🆓. This site offers no ROM files.',
    de: 'Spiele legal beschaffen — eigene Dumps von Modulen/Discs oder Homebrew und Freeware 🆓. Diese Seite bietet keine ROM-Dateien an.',
    fr: "Procurez-vous les jeux légalement — vos propres dumps de cartouches et disques, ou du homebrew et des freewares 🆓. Ce site ne propose aucun fichier ROM.",
  },
  'footer.built': { cs: 'postaveno s Astro', en: 'built with Astro', de: 'erstellt mit Astro', fr: 'conçu avec Astro' },
  'footer.data': { cs: 'Data: vlastní kurátorské podklady', en: 'Data: own curated sources', de: 'Daten: eigene kuratierte Quellen', fr: 'Données : sources sélectionnées maison' },

  'games.count': { cs: 'her', en: 'games', de: 'Spiele', fr: 'jeux' },
  'platforms.count': { cs: 'platforem', en: 'platforms', de: 'Plattformen', fr: 'plateformes' },

  // detail platformy / společné
  'detail.history': { cs: 'Historie & kontext', en: 'History & context', de: 'Geschichte & Kontext', fr: 'Histoire & contexte' },
  'detail.recommended': { cs: 'Doporučené hry', en: 'Recommended games', de: 'Empfohlene Spiele', fr: 'Jeux recommandés' },
  'detail.withComment': { cs: 's komentářem', en: 'with commentary', de: 'mit Kommentar', fr: 'avec commentaire' },
  'detail.year': { cs: 'Rok', en: 'Year', de: 'Jahr', fr: 'Année' },
  'filter.allGenres': { cs: 'Všechny žánry', en: 'All genres', de: 'Alle Genres', fr: 'Tous les genres' },
  'filter.emptyGenre': { cs: 'Žádná hra v tomto žánru.', en: 'No game in this genre.', de: 'Kein Spiel in diesem Genre.', fr: 'Aucun jeu dans ce genre.' },
  'pager.prevPlatform': { cs: '← Předchozí platforma', en: '← Previous platform', de: '← Vorherige Plattform', fr: '← Plateforme précédente' },
  'pager.nextPlatform': { cs: 'Další platforma →', en: 'Next platform →', de: 'Nächste Plattform →', fr: 'Plateforme suivante →' },
  'pager.morePlatforms': { cs: 'Další platformy', en: 'More platforms', de: 'Weitere Plattformen', fr: 'Plus de plateformes' },
  'suggest.sub': { cs: 'Napiš mi ji — kurátorský výběr pořád rozšiřuju.', en: 'Tell me — I keep expanding the curated selection.', de: 'Schreib mir — ich erweitere die Auswahl laufend.', fr: "Dites-le-moi — j'enrichis sans cesse la sélection." },
  'suggest.btn': { cs: '💡 Navrhnout hru', en: '💡 Suggest a game', de: '💡 Spiel vorschlagen', fr: '💡 Proposer un jeu' },
  'crumbs.games': { cs: 'Hry', en: 'Games', de: 'Spiele', fr: 'Jeux' },

  // série
  'series.title': { cs: 'Herní série', en: 'Game series', de: 'Spielereihen', fr: 'Séries de jeux' },
  'series.eyebrow': { cs: 'Značky', en: 'Franchises', de: 'Marken', fr: 'Franchises' },
  'series.lead': {
    cs: 'Velké herní značky napříč platformami a generacemi — od prvního dílu po ten poslední.',
    en: 'The big game franchises across platforms and generations — from the first entry to the latest.',
    de: 'Die großen Spielemarken über Plattformen und Generationen hinweg — vom ersten bis zum jüngsten Teil.',
    fr: 'Les grandes franchises du jeu, toutes plateformes et générations confondues — du premier au dernier épisode.',
  },
  'series.inCatalog': { cs: 'her v katalogu', en: 'games in the catalog', de: 'Spiele im Katalog', fr: 'jeux au catalogue' },
  'series.titles': { cs: 'titulů v katalogu', en: 'titles in the catalog', de: 'Titel im Katalog', fr: 'titres au catalogue' },
  'series.versions': { cs: 'verzí napříč platformami', en: 'versions across platforms', de: 'Fassungen über Plattformen', fr: 'versions toutes plateformes' },
  'series.games': { cs: 'Díly série', en: 'Entries in the series', de: 'Teile der Reihe', fr: 'Épisodes de la série' },
  'game.sameSeries': { cs: 'Ze stejné série', en: 'From the same series', de: 'Aus derselben Reihe', fr: 'De la même série' },
  'game.alsoOn': { cs: 'Tentýž titul jinde', en: 'The same title elsewhere', de: 'Derselbe Titel woanders', fr: 'Le même titre ailleurs' },
  'series.partOf': { cs: 'Součást série', en: 'Part of the series', de: 'Teil der Reihe', fr: 'Fait partie de la série' },

  // studia
  'studios.title': { cs: 'Herní studia', en: 'Game studios', de: 'Spiele-Studios', fr: 'Studios de jeux' },
  'studios.eyebrow': { cs: 'Tvůrci', en: 'Creators', de: 'Macher', fr: 'Créateurs' },
  'studios.lead': {
    cs: 'Kdo stál za klasikami. Profily studií, jejich historie, proměny a hry, které tu máme.',
    en: 'Who was behind the classics. Studio profiles, their history, transformations and the games we have here.',
    de: 'Wer hinter den Klassikern stand. Studio-Profile, ihre Geschichte, Wandlungen und die Spiele, die wir hier haben.',
    fr: "Qui se cache derrière les classiques. Profils des studios, leur histoire, leurs mutations et les jeux que nous avons ici.",
  },
  'studio.eyebrow': { cs: 'Herní studio', en: 'Game studio', de: 'Spiele-Studio', fr: 'Studio de jeux' },
  'studio.inCatalog': { cs: 'her v katalogu', en: 'games in the catalogue', de: 'Spiele im Katalog', fr: 'jeux au catalogue' },
  'studio.gamesOf': { cs: 'Hry studia', en: 'Games by the studio', de: 'Spiele des Studios', fr: 'Jeux du studio' },

  // hardware
  'hw.title': { cs: 'Hardware & emulace', en: 'Hardware & emulation', de: 'Hardware & Emulation', fr: 'Matériel & émulation' },
  'hw.eyebrow': { cs: 'Na čem hrát', en: 'What to play on', de: 'Worauf spielen', fr: 'Sur quoi jouer' },
  'hw.lead': {
    cs: 'Handheldy, jednodeskové počítače, PC i mobil — na čem všem se dá rozjet retro a jak na to.',
    en: 'Handhelds, single-board computers, PC and mobile — everything you can run retro on and how to do it.',
    de: 'Handhelds, Einplatinencomputer, PC und Handy — worauf sich Retro betreiben lässt und wie.',
    fr: "Consoles portables, ordinateurs monocartes, PC et mobile — tout ce sur quoi faire tourner le rétro et comment s'y prendre.",
  },
  'hw.specs': { cs: 'Parametry', en: 'Specs', de: 'Technische Daten', fr: 'Caractéristiques' },
  'hw.canPlay': { cs: 'Co utáhne', en: 'What it runs', de: 'Was es packt', fr: 'Ce qu\'il fait tourner' },
  'hw.toc': { cs: 'V tomto průvodci', en: 'In this guide', de: 'In diesem Guide', fr: 'Dans ce guide' },
  'hw.options': { cs: 'Rychlé tipy', en: 'Quick tips', de: 'Schnelle Tipps', fr: 'Astuces rapides' },
  'hw.more': { cs: 'Další průvodci', en: 'More guides', de: 'Weitere Guides', fr: 'Plus de guides' },
  'hwlvl.ok': { cs: 'Plynule', en: 'Smoothly', de: 'Flüssig', fr: 'Sans accroc' },
  'hwlvl.most': { cs: 'Většinou', en: 'Mostly', de: 'Meistens', fr: 'La plupart' },
  'hwlvl.some': { cs: 'Vybrané tituly', en: 'Select titles', de: 'Ausgewählte Titel', fr: 'Titres sélectionnés' },

  // katalog her — filtr
  'games.eyebrow': { cs: 'Herní katalog', en: 'Game catalogue', de: 'Spielekatalog', fr: 'Catalogue de jeux' },
  'games.search': { cs: '🔍 Hledat hru…', en: '🔍 Search a game…', de: '🔍 Spiel suchen…', fr: '🔍 Rechercher un jeu…' },
  'games.allPlatforms': { cs: 'Všechny platformy', en: 'All platforms', de: 'Alle Plattformen', fr: 'Toutes les plateformes' },
  'games.multiplayer': { cs: '👥 Pro více hráčů', en: '👥 Multiplayer', de: '👥 Mehrspieler', fr: '👥 Multijoueur' },
  'games.commented': { cs: '📝 S komentářem', en: '📝 With commentary', de: '📝 Mit Kommentar', fr: '📝 Avec commentaire' },
  'games.empty': { cs: 'Nic nenalezeno — zkus uvolnit filtry.', en: 'Nothing found — try relaxing the filters.', de: 'Nichts gefunden — lockere die Filter.', fr: 'Aucun résultat — essayez d\'assouplir les filtres.' },
  'games.lead2': { cs: 'Hledej a filtruj.', en: 'Search and filter.', de: 'Suchen und filtern.', fr: 'Recherchez et filtrez.' },

  // příznaky her
  'flag.homebrew': { cs: '🆓 Homebrew', en: '🆓 Homebrew', de: '🆓 Homebrew', fr: '🆓 Homebrew' },
  'flag.mustplay': { cs: '⭐ Must-play', en: '⭐ Must-play', de: '⭐ Must-play', fr: '⭐ Incontournable' },
  'flag.mature': { cs: '🔞 18+', en: '🔞 18+', de: '🔞 18+', fr: '🔞 18+' },
  'flag.puzzle': { cs: '🧩 Logická', en: '🧩 Puzzle', de: '🧩 Logik', fr: '🧩 Réflexion' },

  // detail hry
  'game.prev': { cs: '← Předchozí hra', en: '← Previous game', de: '← Vorheriges Spiel', fr: '← Jeu précédent' },
  'game.next': { cs: 'Další hra →', en: 'Next game →', de: 'Nächstes Spiel →', fr: 'Jeu suivant →' },
  'game.playOnline': { cs: '▶ Zahrát online v prohlížeči', en: '▶ Play online in browser', de: '▶ Online im Browser spielen', fr: '▶ Jouer en ligne dans le navigateur' },
  'game.official': { cs: '🔗 Oficiální stránka — kde hru legálně získat', en: '🔗 Official site — where to get it legally', de: '🔗 Offizielle Seite — wo man es legal bekommt', fr: '🔗 Site officiel — où se le procurer légalement' },
  'game.moreFrom': { cs: 'Další z', en: 'More from', de: 'Mehr von', fr: 'Plus de' },
  'game.all': { cs: 'všech', en: 'all', de: 'alle', fr: 'tous' },

  // žánrové kategorie
  'genre.platformer': { cs: 'Plošinovky', en: 'Platformers', de: 'Jump ’n’ Runs', fr: 'Plateforme' },
  'genre.action': { cs: 'Akční', en: 'Action', de: 'Action', fr: 'Action' },
  'genre.rpg': { cs: 'RPG / JRPG', en: 'RPG / JRPG', de: 'RPG / JRPG', fr: 'RPG / JRPG' },
  'genre.metroidvania': { cs: 'Metroidvanie', en: 'Metroidvania', de: 'Metroidvania', fr: 'Metroidvania' },
  'genre.fighting': { cs: 'Bojovky', en: 'Fighting', de: 'Beat ’em ups', fr: 'Combat' },
  'genre.shooter': { cs: 'Střílečky', en: 'Shooters', de: 'Shooter', fr: 'Tir' },
  'genre.racing': { cs: 'Závodní / auta', en: 'Racing', de: 'Rennspiele', fr: 'Course' },
  'genre.puzzle': { cs: 'Logické', en: 'Puzzle', de: 'Logik', fr: 'Réflexion' },
  'genre.adventure': { cs: 'Adventury', en: 'Adventure', de: 'Adventures', fr: 'Aventure' },
  'genre.strategy': { cs: 'Strategie / Sim', en: 'Strategy / Sim', de: 'Strategie / Sim', fr: 'Stratégie / Sim' },
  'genre.sport': { cs: 'Sport', en: 'Sports', de: 'Sport', fr: 'Sport' },

  // homepage
  'home.eyebrow': { cs: '★ Insert coin · Press start', en: '★ Insert coin · Press start', de: '★ Insert coin · Press start', fr: '★ Insert coin · Press start' },
  'home.h1a': { cs: 'Svět', en: 'The world of', de: 'Die Welt des', fr: 'Le monde du' },
  'home.h1b': { cs: 'retro hraní', en: 'retro gaming', de: 'Retro-Gamings', fr: 'rétrogaming' },
  'home.h1c': { cs: 'na jednom místě', en: 'in one place', de: 'an einem Ort', fr: 'en un seul endroit' },
  'home.lead': {
    cs: 'Historie legendárních konzolí a počítačů, jejich nejlepší hry a tipy pro handheldy jako Anbernic RG35XX Pro, R36S a Batocera na starším PC.',
    en: 'The history of legendary consoles and computers, their best games and tips for handhelds like the Anbernic RG35XX Pro, R36S and Batocera on an older PC.',
    de: 'Die Geschichte legendärer Konsolen und Computer, ihre besten Spiele und Tipps für Handhelds wie Anbernic RG35XX Pro, R36S und Batocera auf älteren PCs.',
    fr: "L'histoire des consoles et ordinateurs légendaires, leurs meilleurs jeux et des astuces pour les consoles portables comme l'Anbernic RG35XX Pro, la R36S et Batocera sur un PC plus ancien.",
  },
  'home.ctaPlatforms': { cs: 'Prozkoumat platformy', en: 'Explore platforms', de: 'Plattformen entdecken', fr: 'Explorer les plateformes' },
  'home.ctaGames': { cs: 'Procházet hry', en: 'Browse games', de: 'Spiele durchsuchen', fr: 'Parcourir les jeux' },
  'home.images': { cs: 'obrázků', en: 'images', de: 'Bilder', fr: 'images' },
  'home.hwEyebrow': { cs: 'Na čem hrát', en: 'What to play on', de: 'Worauf spielen', fr: 'Sur quoi jouer' },
  'home.hwTitle': { cs: 'Hardware & emulace', en: 'Hardware & emulation', de: 'Hardware & Emulation', fr: 'Matériel & émulation' },
  'home.hwAll': { cs: 'Všichni průvodci →', en: 'All guides →', de: 'Alle Guides →', fr: 'Tous les guides →' },
  'home.featEyebrow': { cs: '⭐ Must-play', en: '⭐ Must-play', de: '⭐ Must-play', fr: '⭐ Incontournable' },
  'home.featTitle': { cs: 'Moderní homebrew klenoty', en: 'Modern homebrew gems', de: 'Moderne Homebrew-Perlen', fr: 'Perles homebrew modernes' },
  'home.gamesAll': { cs: 'Všechny hry →', en: 'All games →', de: 'Alle Spiele →', fr: 'Tous les jeux →' },

  // typy platforem (sekce na homepage)
  'type.console.label': { cs: 'Herní konzole', en: 'Game consoles', de: 'Spielkonsolen', fr: 'Consoles de jeux' },
  'type.handheld.label': { cs: 'Kapesní konzole', en: 'Handhelds', de: 'Handhelds', fr: 'Consoles portables' },
  'type.computer.label': { cs: 'Domácí počítače', en: 'Home computers', de: 'Heimcomputer', fr: 'Ordinateurs familiaux' },
  'type.arcade.label': { cs: 'Arkády', en: 'Arcades', de: 'Arcades', fr: 'Arcades' },
  'type.vr.label': { cs: 'Virtuální realita', en: 'Virtual reality', de: 'Virtuelle Realität', fr: 'Réalité virtuelle' },
  'type.vr.tag': { cs: 'Headsety od kutilských devadesátek po dnešní samostatné brýle.', en: 'Headsets from the DIY nineties to today’s standalone goggles.', de: 'Headsets von den Bastel-Neunzigern bis zu heutigen Standalone-Brillen.', fr: 'Des casques des années 90 bricoleuses aux lunettes autonomes d’aujourd’hui.' },
  'type.fantasy.label': { cs: 'Fantasy konzole', en: 'Fantasy consoles', de: 'Fantasy-Konsolen', fr: 'Consoles fantasy' },
  'type.console.tag': { cs: 'Stroje pod televizi, které definovaly herní generace.', en: 'Machines under the TV that defined gaming generations.', de: 'Geräte unterm Fernseher, die Gaming-Generationen prägten.', fr: 'Des machines sous la télé qui ont défini des générations de jeu.' },
  'type.handheld.tag': { cs: 'Hraní do kapsy — srdce dnešních zařízení jako Anbernic.', en: 'Gaming in your pocket — the heart of today’s devices like Anbernic.', de: 'Gaming für die Tasche — das Herz heutiger Geräte wie Anbernic.', fr: "Le jeu dans la poche — le cœur des appareils actuels comme Anbernic." },
  'type.computer.tag': { cs: '8bitové a 16bitové počítače domácí éry.', en: '8-bit and 16-bit computers of the home era.', de: '8-Bit- und 16-Bit-Computer der Heim-Ära.', fr: "Les ordinateurs 8 bits et 16 bits de l'ère domestique." },
  'type.arcade.tag': { cs: 'Herny, mince a nekompromisní obtížnost.', en: 'Arcades, coins and uncompromising difficulty.', de: 'Spielhallen, Münzen und kompromisslose Schwierigkeit.', fr: 'Salles de jeux, pièces et difficulté sans concession.' },
  'type.fantasy.tag': { cs: 'Moderní „virtuální" konzole s nostalgickými limity.', en: 'Modern “virtual” consoles with nostalgic limits.', de: 'Moderne „virtuelle" Konsolen mit nostalgischen Grenzen.', fr: 'Des consoles « virtuelles » modernes aux limites nostalgiques.' },
};

export function t(locale: Locale, key: string): string {
  const e = UI[key];
  if (!e) return key;
  return e[locale] ?? e[DEFAULT_LOCALE];
}
