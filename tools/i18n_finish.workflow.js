export const meta = {
  name: 'i18n-finish',
  description: 'Idempotentní dojezd překladů: přeloží jen chybějící dávky (hotové přeskočí)',
  phases: [{ title: 'Translate', detail: 'per-chunk: skip if valid out exists, else translate' }],
}

phase('Translate')
const { base, counts } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')

const STRUCT = {
  games: 'Objekt {slug: {teaser?, detail?, article?}} — hodnoty jsou český text (teaser krátký, detail/article Markdown).',
  platforms: 'Objekt {slug: {history}} — history je dlouhý český Markdown článek.',
  studios: 'Objekt {slug: "..."} — hodnota je celý český Markdown článek o studiu.',
  hardware_sections: 'Objekt {slug: [{title, body: [odstavce]}]} — pole sekcí, každá má title a body (pole českých odstavců).',
  hardware_meta: 'Objekt {slug: {kind, tagline, intro:[odstavce], specs:[{label,value}], canPlay:[{label,level}], options:[{title,text}]}}. Přelož kind, tagline, intro, specs.label, specs.value (kromě technických zkratek/čísel/názvů modelů, ty ponech), canPlay.label, options.title, options.text. DŮLEŽITÉ: hodnotu canPlay.level (ok/most/some) NEMĚŇ.',
}

// pořadí: nejdřív malé sekce (rychlé, ať se stihnou před dennim limitem), pak hry
const ORDER = ['hardware_meta', 'hardware_sections', 'studios', 'platforms', 'games']
const chunks = []
for (const type of ORDER) {
  const n = counts[type] || 0
  for (let i = 0; i < n; i++) {
    chunks.push({ type, in: `${base}/chunks/${type}_${pad(i)}.json`, out: `${base}/chunks/${type}_${pad(i)}_out.json` })
  }
}

const results = await parallel(chunks.map((c) => () => {
  const prompt = `Idempotentní překladová úloha.

KROK 1 – kontrola: Zkus nástrojem Read otevřít soubor: ${c.out}
Pokud soubor EXISTUJE a jeho obsah je VALIDNÍ JSON obsahující klíče "en" i "de", jsi hotov — NIC nepřekládej, nic nezapisuj a vrať pouze slovo: SKIP

KROK 2 – překlad (jen když out neexistuje nebo je poškozený): Read ${c.in}
Je to JSON. ${STRUCT[c.type]}
Přelož VŠECHNY textové hodnoty z češtiny do ANGLIČTINY a NĚMČINY.
Pravidla: zachovej Markdown (## nadpisy, **tučné**, odkazy) i strukturu 1:1; NEPŘEKLÁDEJ vlastní jména (názvy her, konzolí, studií, lidí); překládej přirozeně; zachovej všechny klíče (slugy).
Ulož nástrojem Write do ${c.out} VALIDNÍ JSON tvaru {"en": <struktura s EN texty>, "de": <struktura s DE texty>}. Pozor na uvozovky uvnitř řetězců (escapuj \\" nebo použij české „").
Vrať krátké potvrzení.`
  return agent(prompt, { label: `${c.type}/${pad(0)}`.replace('000', c.in.split('/').pop()), phase: 'Translate' })
}))

return { chunks: chunks.length, done: results.filter(Boolean).length }
