import { marked } from 'marked';
import dataset from '../data/dataset.json';

marked.setOptions({ gfm: true, breaks: false });

// ---------------------------------------------------------------- typy
export type PlatformType = 'handheld' | 'console' | 'computer' | 'arcade' | 'fantasy';
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
  rating: string | null;
}

export interface Platform {
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
}

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

const studioMap = new Map<string, Studio>();
for (const g of allGames) {
  const raw = (g.studio || '').trim();
  if (!raw) continue;
  const slug = studioSlug(raw);
  if (STUDIO_SKIP.has(slug)) continue;
  let s = studioMap.get(slug);
  if (!s) {
    s = { slug, name: raw, games: [], gameCount: 0, article: studioArticles[slug] ?? null };
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
export const TYPE_ORDER: PlatformType[] = ['console', 'handheld', 'computer', 'arcade', 'fantasy'];

export const TYPE_LABEL: Record<PlatformType, string> = {
  console: 'Herní konzole',
  handheld: 'Kapesní konzole',
  computer: 'Domácí počítače',
  arcade: 'Arkády',
  fantasy: 'Fantasy konzole',
};

export const TYPE_TAGLINE: Record<PlatformType, string> = {
  console: 'Stroje pod televizi, které definovaly herní generace.',
  handheld: 'Hraní do kapsy — srdce dnešních zařízení jako Anbernic.',
  computer: '8bitové a 16bitové počítače domácí éry.',
  arcade: 'Herny, mince a nekompromisní obtížnost.',
  fantasy: 'Moderní „virtuální“ konzole s nostalgickými limity.',
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
export const mdInline = (s: string | null | undefined): string => (s ? (marked.parseInline(s) as string) : '');
