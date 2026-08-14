export const meta = {
  name: 'i18n-fr',
  description: 'Plny FR preklad existujiciho obsahu (Sonnet 5), idempotentni: hotove davky preskoci',
  phases: [{ title: 'Translate', detail: 'per-chunk: skip if valid FR out exists, else translate to French', model: 'sonnet' }],
}

phase('Translate')
const { base, counts } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')

const STRUCT = {
  games: 'Objekt {slug: {teaser?, detail?, article?}} — hodnoty jsou cesky text (teaser kratky, detail/article Markdown).',
  platforms: 'Objekt {slug: {history}} — history je dlouhy cesky Markdown clanek.',
  studios: 'Objekt {slug: "..."} — hodnota je cely cesky Markdown clanek o studiu.',
  hardware_sections: 'Objekt {slug: [{title, body: [odstavce]}]} — pole sekci, kazda ma title a body (pole ceskych odstavcu).',
}

// poradi: nejdriv male sekce (rychle), pak hry
const ORDER = ['hardware_sections', 'studios', 'platforms', 'games']
const chunks = []
for (const type of ORDER) {
  const n = counts[type] || 0
  for (let i = 0; i < n; i++) {
    chunks.push({ type, in: `${base}/chunks/${type}_${pad(i)}.json`, out: `${base}/chunks/${type}_${pad(i)}_out.json` })
  }
}

log(`FR preklad: ${chunks.length} davek (Sonnet 5)`)

const results = await parallel(chunks.map((c, i) => () => {
  const prompt = `Idempotentni prekladova uloha do FRANCOUZSTINY.

KROK 1 – kontrola: Zkus nastrojem Read otevrit soubor: ${c.out}
Pokud soubor EXISTUJE a jeho obsah je VALIDNI JSON obsahujici klic "fr", jsi hotov — NIC neprekladej, nic nezapisuj a vrat pouze slovo: SKIP

KROK 2 – preklad (jen kdyz out neexistuje nebo je poskozeny): Read ${c.in}
Je to JSON. ${STRUCT[c.type]}
Prelož VSECHNY textove hodnoty z cestiny do FRANCOUZSTINY (francais). Pouzivej spravne akcenty (é è à ç ê î ô û ù). Prirozena, plynula, spisovna francouzstina vhodna pro herni magazin.
Pravidla: zachovej Markdown (## nadpisy, **tucne**, ### podnadpisy, odkazy) i strukturu 1:1; NEPREKLADEJ vlastni jmena (nazvy her, konzoli, cipu, studii, lidi, modelu); zachovej vsechny klice (slugy) i vnorene klice.
Uloz nastrojem Write do ${c.out} VALIDNI JSON tvaru {"fr": <struktura s francouzskymi texty>}. Pozor na uvozovky uvnitr retezcu — escapuj je jako \\".
Vrat kratke potvrzeni.`
  return agent(prompt, { label: `fr:${c.type}/${pad(i)}`, phase: 'Translate', model: 'sonnet' })
}))

return { chunks: chunks.length, done: results.filter(Boolean).length }
