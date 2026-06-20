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
  history: string | null;
  gameCount: number;
  games: Game[];
}

interface Dataset {
  platforms: Platform[];
  stats: { platforms: number; games: number; withDetail: number; withTeaser: number };
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

export const FLAG_LABEL: Record<GameFlag, string> = {
  homebrew: '🆓 Homebrew',
  mustplay: '⭐ Must-play',
  mature: '🔞 18+',
  puzzle: '🧩 Logická',
};

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
