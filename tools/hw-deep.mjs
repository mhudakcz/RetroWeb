export const meta = {
  name: 'hw-deep-articles',
  description: 'Hluboké, obsáhlé CZ deep-research články pro hardware průvodce',
  phases: [{ title: 'HW články' }],
};

const A = typeof args === 'string' ? JSON.parse(args) : args;
const outDir = A.outDir;
const devices = A.devices; // [{slug, name, kind}]

phase('HW články');

const PROMPT = (d) => [
  'Jsi zkušený technologický redaktor a nadšenec do retro hraní. Píšeš CESKY (se správnou diakritikou).',
  `Napiš OPRAVDU OBSÁHLÝ, hloubkový průvodce (deep-research styl) pro hardware: "${d.name}" (kategorie: ${d.kind}).`,
  '',
  'POŽADAVKY NA OBSAH:',
  '- 9 až 13 sekcí. Každá sekce = nadpis + 2 až 4 ODSTAVCE bohatého, konkrétního textu.',
  '- Pokrytí (přizpůsob danému zařízení): co to je a komu je určené; historie a kontext na trhu; HARDWARE do detailu (čip/SoC, GPU, RAM, displej, baterie, porty, chlazení); SYSTÉMY a software (oficiální i komunitní, custom firmware); KOMPATIBILITA po platformách (co utáhne plynule / s kompromisy / vůbec); ovládání a ergonomie; obraz, zvuk, shadery/CRT; výdrž a napájení; příslušenství; NASTAVENÍ krok za krokem (instalace systému, hry, BIOS, scraping); modely/revize a varianty; časté problémy a jak je řešit; komunita a kde hledat pomoc; alternativy a srovnání s konkurencí; pro koho se hodí a pro koho ne.',
  '- Buď KONKRÉTNÍ a FAKTICKY PŘESNÝ (názvy čipů, systémů, emulátorů, postupů). Nevymýšlej si čísla; když si nejsi jistý přesným údajem, popiš věc obecně a pravdivě.',
  '- Piš VLASTNÍMI SLOVY (žádné kopírování odjinud). Čtivě, ale informačně nabité — cílem je, aby se čtenář dozvěděl hodně.',
  '- U handheldů zmiň i hraní více hráčů a TV výstup; u emulačních platforem i legální stránku (vlastní dumpy/legální zdroje, žádné pirátství).',
  '',
  'FORMÁT VÝSTUPU:',
  `- Ulož VALIDNÍ JSON do souboru: ${outDir}/${d.slug}.json`,
  '- Struktura: pole objektů [{"title": "Nadpis sekce", "body": ["odstavec 1", "odstavec 2", ...]}, ...]',
  '- V textu můžeš použít Markdown **tučně** pro klíčové pojmy. Escapuj uvozovky/lomítka, ať je JSON validní. UTF-8 s diakritikou.',
  '- Nadpisy sekcí krátké a výstižné (2–5 slov).',
  '',
  'Vrať jen "OK <pocet sekci>".',
].join('\n');

const results = await parallel(
  devices.map((d) => () => agent(PROMPT(d), { label: d.slug, phase: 'HW články' }))
);
return { devices: devices.length, done: results.filter(Boolean).length };
