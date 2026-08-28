import type { APIRoute } from 'astro';
import { platforms, series, studios } from '../lib/data';

/**
 * Index pro naseptavac v hlavicce.
 *
 * Generuje se jako staticky soubor pri buildu a v prohlizeci se nacte az pri
 * prvnim pouziti hledani — bezna navsteva ho nestahuje vubec.
 *
 * Bere se PRIMO ze stejnych exportu, ze kterych se generuji stranky. Kdyby se
 * seznam skladal zvlast, index by odkazoval na studia a serie pod prahem
 * STUDIO_MIN / SERIES_MIN, ktere vlastni stranku nemaji, a hledani by vodilo
 * na 404.
 *
 * Nazvy se neprekladaji: hry i studia jsou vlastni jmena a u platforem a serii
 * staci ceska podoba, protoze se hleda podle znacky ("PlayStation", "Zelda").
 * URL si klient sestavi sam podle jazykove predpony.
 */

/** Bez diakritiky a interpunkce, aby "pokemon" naslo "Pokémon". */
const fold = (s: string): string =>
  s
    .normalize('NFKD')
    .replace(/\p{M}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();

type Row = { t: 'g' | 'p' | 'r' | 'd'; s: string; n: string; x: string; f: string };

export const GET: APIRoute = () => {
  const rows: Row[] = [];
  const push = (t: Row['t'], s: string, n: string, x = '') =>
    rows.push({ t, s, n, x, f: fold(n) });

  for (const p of platforms) {
    push('p', p.slug, p.name, p.short);
    // u hry se veze zkratka platformy, at jde odlisit stejnojmenne zaznamy
    for (const g of p.games) push('g', g.slug, g.name, p.short);
  }
  for (const s of series) push('r', s.slug, s.name);
  for (const s of studios) push('d', s.slug, s.name);

  return new Response(JSON.stringify(rows), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
