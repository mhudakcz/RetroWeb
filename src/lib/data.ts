import { marked } from 'marked';
import dataset from '../data/dataset.json';

marked.setOptions({ gfm: true, breaks: false });

// ---------------------------------------------------------------- typy
export type PlatformType = 'handheld' | 'console' | 'computer' | 'arcade' | 'fantasy' | 'vr' | 'mobile';
export type GameLength = 'S' | 'M' | 'L' | 'XL';
export type GameFlag = 'homebrew' | 'mustplay' | 'mature' | 'puzzle';

export interface Game {
  slug: string;
  name: string;
  genre: string | null;
  length: GameLength | null;
  flags: GameFlag[];
  year: string | null;
  studio: string | null;
  est: string | null;
  teaser: string | null;
  detail: string | null;
  article: string | null;
  image: string | null;
  gallery: { src: string; label: string; kind: string }[];
  link: string | null;
  playUrl: string | null;
  players: string | null;
  /** Obchody, ve kterych hra na mobilu opravdu vysla. Jinde nez na 'mobil' null. */
  os?: string[] | null;
  rating: string | null;
  /** Pole, ktera v teto jazykove mutaci jeste nejsou prelozena a ukazuji cesky
   *  original. V ceske mutaci je pole vzdy prazdne. */
  fallback?: ('teaser' | 'detail' | 'article')[];
}

export interface Platform {
  /** Historie platformy jeste neni v teto mutaci prelozena, ukazuje se cesky. */
  historyFallback?: boolean;
  slug: string;
  name: string;
  short: string;
  maker: string;
  year: number;
  type: PlatformType;
  color: string;
  color2: string;
  image: string | null;
  photoBg: 'light' | 'dark';
  history: string | null;
  gameCount: number;
  games: Game[];
}

interface Dataset {
  platforms: Platform[];
  stats: { platforms: number; games: number; withDetail: number; withTeaser: number; withArticle: number; gameImages: number; platformImages: number };
}

const data = dataset as unknown as Dataset;

// ---------------------------------------------------------------- data
export const platforms: Platform[] = data.platforms;
export const stats = data.stats;

const platformMap = new Map(platforms.map((p) => [p.slug, p]));
export const getPlatform = (slug: string) => platformMap.get(slug);

// hru identifikujeme dvojicí (platforma, hra); slug hry je už globálně unikátní
export interface GameWithPlatform extends Game {
  platform: Platform;
}

export const allGames: GameWithPlatform[] = platforms.flatMap((p) =>
  p.games.map((g) => ({ ...g, platform: p }))
);

const gameMap = new Map(allGames.map((g) => [g.slug, g]));
export const getGame = (slug: string) => gameMap.get(slug);

// ---------------------------------------------------------------- studia
export interface Studio {
  slug: string;
  name: string;
  games: GameWithPlatform[];
  gameCount: number;
  article: string | null;
  /** koláž z obalů her studia, generuje tools/studio_art.py */
  image: string | null;
}

// existující koláže; studia s málo obaly ji prostě nemají
const studioArtFiles = import.meta.glob('../../public/images/studios/*.webp', { eager: true });
const studioArt = new Set(
  Object.keys(studioArtFiles).map((p) => p.split('/').pop()!.replace(/\.webp$/, '')),
);
const studioImage = (slug: string): string | null =>
  studioArt.has(slug) ? `/images/studios/${slug}.webp` : null;

export const studioSlug = (name: string): string =>
  name
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');

// studia, která nejsou skutečné firmy (nelinkujeme)
const STUDIO_SKIP = new Set(['komunita', 'various', 'ruzni', 'ruzne', '']);
// minimální počet her, aby studio dostalo vlastní stránku
export const STUDIO_MIN = 3;

// dlouhé články o studiích (markdown), načtené ze souborů
const studioArticleFiles = import.meta.glob('../data/studio_articles/*.md', {
  eager: true,
  query: '?raw',
  import: 'default',
}) as Record<string, string>;
const studioArticles: Record<string, string> = {};
for (const [path, raw] of Object.entries(studioArticleFiles)) {
  const slug = path.split('/').pop()!.replace(/\.md$/, '');
  studioArticles[slug] = raw;
}

/** Normalizace názvu hry pro párování téhož titulu napříč platformami.
 *  Odpovídá norm_name() v tools/parse_content.py. */
/** Prvni pismeno pro abecedni razeni. Diakritika se odstranuje — ceska serie
 *  zacinajici na „Č“ patri ctenari pod C, ne do zvlastni skupiny na konci
 *  abecedy. Co nezacina pismenem (cislice, symbol) jde pod „#“. */
export function alphaLetter(name: string): string {
  const c = name.normalize('NFD').replace(/\p{M}/gu, '').charAt(0).toUpperCase();
  return /[A-Z]/.test(c) ? c : '#';
}

/** Seradi polozky podle nazvu a rozdeli je do skupin po prvnim pismenu.
 *  Vraci i poradi pismen, ve kterem se maji vypsat — „#“ az na konci. */
export function groupByLetter<T extends { name: string }>(
  items: T[],
): { letters: string[]; groups: Map<string, T[]> } {
  const groups = new Map<string, T[]>();
  for (const it of [...items].sort((a, b) => a.name.localeCompare(b.name, 'cs'))) {
    const k = alphaLetter(it.name);
    const arr = groups.get(k);
    if (arr) arr.push(it);
    else groups.set(k, [it]);
  }
  const letters = [...groups.keys()].sort((a, b) =>
    a === '#' ? 1 : b === '#' ? -1 : a.localeCompare(b, 'cs'),
  );
  return { letters, groups };
}

/** Kotva pro skupinu pismene — „#“ nesmi skoncit v URL jako fragment. */
export const alphaAnchor = (letter: string): string =>
  `pismeno-${letter === '#' ? 'ostatni' : letter}`;

export function normGameName(s: string): string {
  let x = s.replace(/[’`]/g, "'").replace(/\([^)]*\)/g, ' ');
  x = x.normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
  x = x.replace(/&/g, ' and ').replace(/[/:+\-–—.,!?'"]/g, ' ');
  x = x.replace(/\b(the|a|an)\b/g, ' ').replace(/\s+/g, ' ').trim();
  return x;
}

export interface Series {
  slug: string;
  name: string;
  games: GameWithPlatform[];
  gameCount: number;
  intro: string | null;
  /** koláž z obalů dílů, generuje tools/series_art.py */
  image: string | null;
}

interface SeriesDef {
  slug: string;
  name: string;
  match: string[];
  /** názvy, které vzor chytí omylem — „Tower of Doom" není díl Doomu */
  exclude?: string[];
  /** výslovný seznam slugů — pro kolekce, které nespojuje název, ale něco jiného
   *  (třeba původ: české a slovenské hry). Použije se místo `match`. */
  games?: string[];
  intro?: Record<string, string>;
}
import seriesDefsRaw from '../data/series.json';
const seriesDefs = seriesDefsRaw as SeriesDef[];

/** Minimální počet her, aby série dostala vlastní stránku. */
export const SERIES_MIN = 4;

// koláže z obalů dílů (tools/series_art.py) — u série bez obalů prostě nejsou
const seriesArtFiles = import.meta.glob('../../public/images/series/*.webp', { eager: true });
const seriesArt = new Set(
  Object.keys(seriesArtFiles).map((p) => p.split('/').pop()!.replace(/\.webp$/, '')),
);

// koláže z obalů her platformy (tools/platform_art.py) — u PC řekne víc než
// fotka béžové skříně; existují jen pro platformy, kde se vyrobily
const platArtFiles = import.meta.glob('../../public/images/platforms/extra/*-games.webp', { eager: true });
const platArt = new Set(
  Object.keys(platArtFiles).map((p) => p.split('/').pop()!.replace(/-games\.webp$/, '')),
);
/** Pás obalů her dané platformy, pokud existuje. */
export const platformGamesArt = (slug: string): string | null =>
  platArt.has(slug) ? `/images/platforms/extra/${slug}-games.webp` : null;

/** Párování na hranice slov — podřetězcem by „Ys" chytlo „Days" a „Ultima" chytla „Ultimate". */
const RX_SPECIAL = /[.*+?^${}()|[\]\\]/g;
const seriesPatterns = seriesDefs.map((d) => ({
  def: d,
  rx: d.match.map((m) => {
    const lit = m.toLowerCase().replace(RX_SPECIAL, '\\$&');
    return new RegExp('(?<![a-z0-9])' + lit + '(?![a-z0-9])');
  }),
}));

function buildSeries(source: GameWithPlatform[], locale: string): Map<string, Series> {
  const map = new Map<string, Series>();
  for (const { def, rx } of seriesPatterns) {
    const skip = (def.exclude || []).map((e) => e.toLowerCase());
    const explicit = def.games ? new Set(def.games) : null;
    const games = explicit
      ? source.filter((g) => explicit.has(g.slug))
      : source.filter((g) => {
          const n = g.name.toLowerCase();
          if (skip.some((e) => n.includes(e))) return false;
          return rx.some((r) => r.test(n));
        });
    games.sort((a, b) => (parseInt(a.year || '0') || 0) - (parseInt(b.year || '0') || 0));
    map.set(def.slug, {
      slug: def.slug,
      name: def.name,
      games,
      gameCount: games.length,
      intro: def.intro?.[locale] ?? def.intro?.cs ?? null,
      image: seriesArt.has(def.slug) ? `/images/series/${def.slug}.webp` : null,
    });
  }
  return map;
}

const seriesMap = buildSeries(allGames, 'cs');
/** Série s vlastní stránkou (≥ SERIES_MIN her), seřazené dle počtu her. */
export const series: Series[] = [...seriesMap.values()]
  .filter((s) => s.gameCount >= SERIES_MIN)
  .sort((a, b) => b.gameCount - a.gameCount);
export const getSeries = (slug: string) => seriesMap.get(slug);

/** Série, do kterých hra patří (pro prolinkování z detailu hry). */
export function seriesOfGame(name: string, all: Series[] = series, slug?: string): Series[] {
  const n = name.toLowerCase();
  return all.filter((s) => {
    const def = seriesPatterns.find((p) => p.def.slug === s.slug);
    if (!def) return false;
    if (def.def.games) return slug ? def.def.games.includes(slug) : false;
    return def.rx.some((r) => r.test(n));
  });
}

const studioMap = new Map<string, Studio>();
for (const g of allGames) {
  const raw = (g.studio || '').trim();
  if (!raw) continue;
  const slug = studioSlug(raw);
  if (STUDIO_SKIP.has(slug)) continue;
  let s = studioMap.get(slug);
  if (!s) {
    s = { slug, name: raw, games: [], gameCount: 0, article: studioArticles[slug] ?? null, image: studioImage(slug) };
    studioMap.set(slug, s);
  }
  s.games.push(g);
}
for (const s of studioMap.values()) {
  s.gameCount = s.games.length;
  // seřaď hry studia podle roku
  s.games.sort((a, b) => (parseInt(a.year || '0') || 0) - (parseInt(b.year || '0') || 0));
}

/** Studia s vlastní stránkou (≥ STUDIO_MIN her), seřazená dle počtu her. */
export const studios: Studio[] = [...studioMap.values()]
  .filter((s) => s.gameCount >= STUDIO_MIN)
  .sort((a, b) => b.gameCount - a.gameCount);

const linkableStudios = new Set(studios.map((s) => s.slug));
export const getStudio = (slug: string) => studioMap.get(slug);
/** Vrátí slug studia, pokud má vlastní stránku (jinak null) – pro prolinkování. */
export const studioLink = (name: string | null): string | null => {
  if (!name) return null;
  const slug = studioSlug(name.trim());
  return linkableStudios.has(slug) ? slug : null;
};

// ---------------------------------------------------------------- skupiny / popisky
export const TYPE_ORDER: PlatformType[] = ['console', 'handheld', 'computer', 'arcade', 'mobile', 'vr', 'fantasy'];

export const TYPE_LABEL: Record<PlatformType, string> = {
  console: 'Herní konzole',
  handheld: 'Kapesní konzole',
  computer: 'Domácí počítače',
  arcade: 'Arkády',
  vr: 'Virtuální realita',
  fantasy: 'Fantasy konzole',
  mobile: 'Mobil',
};

export const TYPE_TAGLINE: Record<PlatformType, string> = {
  console: 'Stroje pod televizi, které definovaly herní generace.',
  handheld: 'Hraní do kapsy — srdce dnešních zařízení jako Anbernic.',
  computer: '8bitové a 16bitové počítače domácí éry.',
  arcade: 'Herny, mince a nekompromisní obtížnost.',
  vr: 'Headsety od kutilských devadesátek po dnešní samostatné brýle.',
  fantasy: 'Moderní „virtuální“ konzole s nostalgickými limity.',
  mobile: 'Hry, které se vešly do telefonu — a předělaly herní trh.',
};

export const LENGTH_LABEL: Record<GameLength, string> = {
  S: 'Krátká · do ~3 h',
  M: 'Střední · ~3–10 h',
  L: 'Dlouhá · ~10–30 h',
  XL: 'Velmi dlouhá · 30+ h',
};

export const LENGTH_WORD: Record<GameLength, string> = {
  S: 'Krátká',
  M: 'Střední',
  L: 'Dlouhá',
  XL: 'Velmi dlouhá',
};

/** Jeden text délky hraní – kombinuje kategorii a konkrétní odhad bez duplicity. */
export function playtimeLabel(length: GameLength | null, est: string | null): string | null {
  if (est) {
    const cleaned = est.replace(/^cca\s*/i, '').trim();
    return length ? `${LENGTH_WORD[length]} · cca ${cleaned}` : `cca ${cleaned}`;
  }
  return length ? LENGTH_LABEL[length] : null;
}

export const FLAG_LABEL: Record<GameFlag, string> = {
  homebrew: '🆓 Homebrew',
  mustplay: '⭐ Must-play',
  mature: '🔞 18+',
  puzzle: '🧩 Logická',
};

// Žánrové kategorie pro filtr (klíč, popisek, vzor proti poli genre).
// Sdílené mezi katalogem her a sekcí her na stránce platformy.
export const GENRE_CATS: [string, string, RegExp][] = [
  ['platformer', 'Plošinovky', /platform/i],
  ['action', 'Akční', /action|run & gun|beat|hack|shinobi/i],
  ['rpg', 'RPG / JRPG', /rpg|role/i],
  ['metroidvania', 'Metroidvanie', /metroidvania/i],
  ['fighting', 'Bojovky', /fighting/i],
  ['shooter', 'Střílečky', /shoot|shmup|stříleč|gun|run & gun/i],
  ['racing', 'Závodní / auta', /racing|závod|driving|kart|racer/i],
  ['puzzle', 'Logické', /puzzle|logick|sokoban|match/i],
  ['adventure', 'Adventury', /adventure|point/i],
  ['strategy', 'Strategie / Sim', /strateg|\bsim\b|sim |tactic|management|tycoon|budování/i],
  ['sport', 'Sport', /sport|tennis|golf|soccer|fotbal|skat|fishing|bowling/i],
];

export const genreCats = (genre: string | null): string[] =>
  genre ? GENRE_CATS.filter(([, , re]) => re.test(genre)).map(([k]) => k) : [];

// Pořadí platforem pro „postupné čtení" (dle skupin a roku) + sousedé
export function orderedPlatforms(): Platform[] {
  return platformsByType().flatMap((g) => g.items);
}

export function platformNeighbors(slug: string): { prev: Platform | null; next: Platform | null } {
  const arr = orderedPlatforms();
  const i = arr.findIndex((p) => p.slug === slug);
  return {
    prev: i > 0 ? arr[i - 1] : null,
    next: i >= 0 && i < arr.length - 1 ? arr[i + 1] : null,
  };
}

// poznámky, čím se lišily verze téhož titulu na jednotlivých platformách
// (tools/version_notes.workflow.js), klíč = normalizovaný název hry
import versionNotesRaw from '../data/version_notes.json';
import editionsRaw from '../data/game_editions.json';
const versionNotes = versionNotesRaw as Record<string, Record<string, string>>;

/** Text o rozdílech mezi verzemi téhož titulu, nebo null. */
export function versionNote(name: string, locale = 'cs'): string | null {
  const n = versionNotes[normGameName(name)];
  if (!n) return null;
  return n[locale] ?? n.cs ?? null;
}

/** Kolik let smí být mezi vydáními, aby šlo o verze TÉŽE hry.
 *  Bez toho by se Doom z roku 1993 spojil s rebootem z roku 2016 —
 *  stejný název, ale jiná hra. */
const SAME_GAME_YEARS = 6;

/** Ruční skupiny vydání. Heuristika „stejný název + blízký rok“ neustojí dva
 *  případy: starý titul vydaný znovu po desetiletích (Doom z roku 1993 se
 *  na PS5 dostal až v roce 2019) a reboot se stejným názvem (Doom 2016).
 *  Slug uvedený ve skupině se páruje jen v jejím rámci a rok se neřeší. */
const editionOf = new Map<string, string>();
for (const [id, slugs] of Object.entries(
  (editionsRaw as { groups: Record<string, string[]> }).groups,
)) {
  for (const slug of slugs) editionOf.set(slug, id);
}

const releaseYear = (g: GameWithPlatform): number =>
  parseInt(g.year || '') || g.platform.year;

/** Přípony, kterými vydavatelé značí pozdější vydání téhož titulu.
 *  „Cave Story+“ nebo „Burnout Paradise Remastered“ jsou tatáž hra jako
 *  originál, jen pod delším jménem — bez tohohle by se nespárovaly.
 *  Schválně sem NEpatří „Classic“ (Celeste Classic je jiná, starší hra)
 *  ani „Remake“ (předělávka bývá samostatný titul). */
const EDITION_SUFFIX =
  /\s*(?:[-–—:]\s*)?\b(?:enhanced|complete|definitive|special|ultimate|deluxe|premium|anniversary|legendary|redux|remaster(?:ed)?|hd|goty|game of the year|director's cut|gold|platinum)\b[\w' ]*$/i;

/** Název bez edicní přípony. Vrací i příznak, jestli se něco odřízlo —
 *  jen tehdy totiž smíme prominout odstup let (remaster vychází i po dekádě). */
function editionKey(name: string): { key: string; suffixed: boolean } {
  let x = name;
  let suffixed = false;
  for (let i = 0; i < 3; i++) {
    const y = x.replace(EDITION_SUFFIX, '').trim();
    if (y === x || !y) break;
    x = y;
    suffixed = true;
  }
  // „Cave Story+“ — plus se do přípony výše nevejde, ale znamená totéž
  const plus = x.replace(/\s*\+$/, '').trim();
  if (plus && plus !== x) {
    x = plus;
    suffixed = true;
  }
  return { key: normGameName(x), suffixed };
}

/** Tentýž titul na jiných platformách (párování podle normalizovaného názvu
 *  a blízkého roku vydání). Seřazeno chronologicky, aby šlo číst vývoj verzí. */
export function sameGameElsewhere(
  game: GameWithPlatform,
  all: GameWithPlatform[],
): GameWithPlatform[] {
  const byName = (list: GameWithPlatform[]) =>
    list.sort(
      (a, b) => releaseYear(a) - releaseYear(b) || a.platform.name.localeCompare(b.platform.name),
    );

  const edition = editionOf.get(game.slug);
  if (edition) {
    return byName(all.filter((g) => g.slug !== game.slug && editionOf.get(g.slug) === edition));
  }

  const me = editionKey(game.name);
  if (!me.key) return [];
  const y = releaseYear(game);
  return byName(
    all.filter((g) => {
      if (g.slug === game.slug) return false;
      // hra zařazená do skupiny se páruje jen uvnitř ní, ať se sem
      // klasický Doom nepřilepí k rebootu jen proto, že roky vyšly
      if (editionOf.has(g.slug)) return false;
      const other = editionKey(g.name);
      if (other.key !== me.key) return false;
      // Odstup let hlídá jen shodné názvy — tam totiž může jít o reboot.
      // Když je jedna strana označená jako pozdější edice, je vztah jistý.
      if (me.suffixed || other.suffixed) return true;
      return Math.abs(releaseYear(g) - y) <= SAME_GAME_YEARS;
    }),
  );
}

export function gameNeighbors(platform: Platform, slug: string): { prev: Game | null; next: Game | null } {
  const arr = platform.games;
  const i = arr.findIndex((g) => g.slug === slug);
  return {
    prev: i > 0 ? arr[i - 1] : null,
    next: i >= 0 && i < arr.length - 1 ? arr[i + 1] : null,
  };
}

export function platformsByType(): { type: PlatformType; label: string; tagline: string; items: Platform[] }[] {
  return TYPE_ORDER.map((type) => ({
    type,
    label: TYPE_LABEL[type],
    tagline: TYPE_TAGLINE[type],
    // seřazeno podle časové osy (rok vydání vzestupně)
    items: platforms.filter((p) => p.type === type).sort((a, b) => a.year - b.year),
  })).filter((g) => g.items.length > 0);
}

// ---------------------------------------------------------------- markdown
export const mdBlock = (s: string | null | undefined): string => (s ? (marked.parse(s) as string) : '');

/** Nadpisy `### …` z markdownu + jejich id, na obsah dlouhého článku.
 *  Články o platformách mají pět sekcí a bez rozcestníku je čtenář v textu nenajde. */
export function mdHeadings(src: string | null | undefined): { id: string; text: string }[] {
  if (!src) return [];
  const out: { id: string; text: string }[] = [];
  const seen = new Set<string>();
  for (const m of src.matchAll(/^###\s+(.+)$/gm)) {
    const text = m[1].replace(/[*_`]/g, '').trim();
    let id = text
      .normalize('NFKD')
      .replace(/\p{M}/gu, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');
    if (!id) continue;
    let uniq = id;
    let i = 2;
    while (seen.has(uniq)) uniq = `${id}-${i++}`;
    seen.add(uniq);
    out.push({ id: uniq, text });
  }
  return out;
}

/** Doplní `id` k `<h3>` v už vyrenderovaném HTML, aby na ně vedly odkazy z obsahu. */
export function mdBlockAnchored(src: string | null | undefined): string {
  const html = mdBlock(src);
  const ids = mdHeadings(src).map((h) => h.id);
  let i = 0;
  return html.replace(/<h3>/g, () => (i < ids.length ? `<h3 id="${ids[i++]}">` : '<h3>'));
}
export const mdInline = (s: string | null | undefined): string => (s ? (marked.parseInline(s) as string) : '');

// ---------------------------------------------------------------- lokalizace obsahu (EN/DE)
// Překladové překryvy: src/data/i18n/<locale>/<type>.json
const i18nFiles = import.meta.glob('../data/i18n/*/*.json', { eager: true, import: 'default' }) as Record<
  string,
  unknown
>;
const i18nData: Record<string, Record<string, unknown>> = {};
for (const [path, data0] of Object.entries(i18nFiles)) {
  const m = path.match(/i18n\/([a-z]{2})\/([a-z_]+)\.json$/);
  if (m) ((i18nData[m[1]] ||= {}) as Record<string, unknown>)[m[2]] = data0;
}
const trMap = (locale: string, type: string): Record<string, any> =>
  (i18nData[locale]?.[type] as Record<string, any>) || {};

export interface LocaleBundle {
  platforms: Platform[];
  allGames: GameWithPlatform[];
  getPlatform: (slug: string) => Platform | undefined;
  getGame: (slug: string) => GameWithPlatform | undefined;
  studios: Studio[];
  getStudio: (slug: string) => Studio | undefined;
  series: Series[];
  getSeries: (slug: string) => Series | undefined;
}

const bundleCache = new Map<string, LocaleBundle>();

/** Vrátí data (platformy, hry, studia) s obsahem přeloženým do daného jazyka
 *  (fallback na češtinu tam, kde překlad chybí). */
export function localeData(locale: string): LocaleBundle {
  if (locale === 'cs') {
    return { platforms, allGames, getPlatform, getGame, studios, getStudio, series, getSeries };
  }
  const cached = bundleCache.get(locale);
  if (cached) return cached;

  const gT = trMap(locale, 'games');
  const pT = trMap(locale, 'platforms');
  const sT = trMap(locale, 'studios');

  const locPlatforms: Platform[] = platforms.map((p) => {
    const ph = pT[p.slug];
    const games = p.games.map((g) => {
      const o = gT[g.slug];
      // Chybejici preklad neznamena prazdnou stranku — vypise se cesky original.
      // Aby to ctenar poznal, drzi si hra seznam poli, ktera takhle propadla.
      const fallback: ('teaser' | 'detail' | 'article')[] = [];
      if (g.teaser && !o?.teaser) fallback.push('teaser');
      if (g.detail && !o?.detail) fallback.push('detail');
      if (g.article && !o?.article) fallback.push('article');
      return o
        ? { ...g, teaser: o.teaser ?? g.teaser, detail: o.detail ?? g.detail, article: o.article ?? g.article, fallback }
        : { ...g, fallback };
    });
    return { ...p, history: ph?.history ?? p.history, historyFallback: !!p.history && !ph?.history, games };
  });

  const pMap = new Map(locPlatforms.map((p) => [p.slug, p]));
  const locGames: GameWithPlatform[] = locPlatforms.flatMap((p) => p.games.map((g) => ({ ...g, platform: p })));
  const gMap = new Map(locGames.map((g) => [g.slug, g]));

  // studia znovu poskládaná z lokalizovaných her + přeložený článek
  const sMap = new Map<string, Studio>();
  for (const g of locGames) {
    const raw = (g.studio || '').trim();
    if (!raw) continue;
    const slug = studioSlug(raw);
    if (STUDIO_SKIP.has(slug)) continue;
    let s = sMap.get(slug);
    if (!s) {
      s = { slug, name: raw, games: [], gameCount: 0, article: sT[slug] ?? studioArticles[slug] ?? null, image: studioImage(slug) };
      sMap.set(slug, s);
    }
    s.games.push(g);
  }
  for (const s of sMap.values()) {
    s.gameCount = s.games.length;
    s.games.sort((a, b) => (parseInt(a.year || '0') || 0) - (parseInt(b.year || '0') || 0));
  }
  const locStudios = [...sMap.values()].filter((s) => s.gameCount >= STUDIO_MIN).sort((a, b) => b.gameCount - a.gameCount);

  const serMap = buildSeries(locGames, locale);
  const locSeries = [...serMap.values()]
    .filter((s) => s.gameCount >= SERIES_MIN)
    .sort((a, b) => b.gameCount - a.gameCount);

  const bundle: LocaleBundle = {
    platforms: locPlatforms,
    allGames: locGames,
    getPlatform: (slug) => pMap.get(slug),
    getGame: (slug) => gMap.get(slug),
    studios: locStudios,
    getStudio: (slug) => sMap.get(slug),
    series: locSeries,
    getSeries: (slug) => serMap.get(slug),
  };
  bundleCache.set(locale, bundle);
  return bundle;
}

/** Lokalizované HW sekce (deep články) pro daný jazyk; fallback na češtinu. */
export function hardwareSectionsLoc(locale: string): Record<string, { title: string; body: string[] }[]> {
  return trMap(locale, 'hardware_sections') as Record<string, { title: string; body: string[] }[]>;
}

/** Lokalizovaná statická pole HW průvodců (kind, tagline, intro, specs, canPlay, options). */
export function hardwareMetaLoc(locale: string): Record<string, any> {
  return trMap(locale, 'hardware_meta');
}

/** Platformy seskupené dle typu pro daný jazyk (kvůli lokalizovanému indexu). */
export function platformsByTypeLoc(locale: string): { type: PlatformType; items: Platform[] }[] {
  const ps = localeData(locale).platforms;
  return TYPE_ORDER.map((type) => ({
    type,
    items: ps.filter((p) => p.type === type).sort((a, b) => a.year - b.year),
  })).filter((g) => g.items.length > 0);
}

/** České skloňování počtu: 1 hra, 2–4 hry, 5+ her. */
export function plural(n: number, one: string, few: string, many: string): string {
  return `${n} ${n === 1 ? one : n >= 2 && n <= 4 ? few : many}`;
}

// ---------------------------------------------------------------- magazín
// Katalog rozdělený do „čísel“ podle roku vydání — jako kdyby v té době
// vycházel časopis. Rejstřík (magazine.json) říká, co v kterém čísle je, a je
// záměrně neměnný: přidání hry zakládá nové číslo, nepřeskládá stará.
import magazineLedger from '../data/magazine.json';
import magazineText from '../data/magazine_text.json';

export interface MagazineIssue {
  id: string;
  rok: number;
  cislo: number;
  titulek: string;
  editorial: string;
  tema: { nadpis: string; text: string } | null;
  zebricek: { game: GameWithPlatform; text: string }[];
  chystame: string;
  platformy: Platform[];
  hry: GameWithPlatform[];
  /** Hry, u kterých rok neznáme a zařadily se podle roku platformy. */
  odhad: Set<string>;
  prev: string | null;
  next: string | null;
}

const magTexts = magazineText as Record<string, any>;

/** Čísla, která mají hotový redakční text — jen ta se na webu ukazují. */
export const magazineIssues: MagazineIssue[] = (() => {
  const raw = (magazineLedger as any).vydani as any[];
  const vydana = raw.filter((v) => magTexts[v.id]);
  return vydana.map((v, i) => {
    const t = magTexts[v.id];
    return {
      id: v.id,
      rok: v.rok,
      cislo: v.cislo,
      titulek: t.titulek || '',
      editorial: t.editorial,
      tema: t.tema ?? null,
      zebricek: (t.zebricek || [])
        .map((z: any) => ({ game: getGame(z.slug), text: z.text }))
        .filter((z: any) => z.game),
      chystame: t.chystame || '',
      platformy: (v.platformy as string[]).map(getPlatform).filter(Boolean) as Platform[],
      hry: (v.hry as string[]).map(getGame).filter(Boolean) as GameWithPlatform[],
      odhad: new Set<string>(v.odhad_roku || []),
      prev: i > 0 ? vydana[i - 1].id : null,
      next: i + 1 < vydana.length ? vydana[i + 1].id : null,
    };
  });
})();

export const getMagazineIssue = (id: string) => magazineIssues.find((v) => v.id === id);

/** Čísla po ročnících, nejnovější ročník nahoře. */
export function magazineByYear(): { rok: number; issues: MagazineIssue[] }[] {
  const by = new Map<number, MagazineIssue[]>();
  for (const v of magazineIssues) {
    if (!by.has(v.rok)) by.set(v.rok, []);
    by.get(v.rok)!.push(v);
  }
  return [...by.entries()]
    .sort((a, b) => b[0] - a[0])
    .map(([rok, issues]) => ({ rok, issues }));
}
