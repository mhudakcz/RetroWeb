export const meta = {
  name: 'i18n-new',
  description: 'Preklad noveho CS obsahu do EN+DE+FR naraz (Sonnet 5), idempotentni: hotove davky preskoci',
  phases: [{ title: 'Translate', detail: 'per-chunk: skip if out has en+de+fr, else translate', model: 'sonnet' }],
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

log(`Preklad noveho obsahu do EN+DE+FR: ${chunks.length} davek (Sonnet 5)`)

const results = await parallel(chunks.map((c, i) => () => {
  const prompt = `Idempotentni prekladova uloha do ANGLICTINY, NEMCINY a FRANCOUZSTINY.

KROK 1 – kontrola: Zkus nastrojem Read otevrit soubor: ${c.out}
Pokud soubor EXISTUJE a jeho obsah je VALIDNI JSON obsahujici VSECHNY tri klice "en", "de" i "fr", jsi hotov — NIC neprekladej, nic nezapisuj a vrat pouze slovo: SKIP

KROK 2 – preklad (jen kdyz out neexistuje nebo mu nektery jazyk chybi): Read ${c.in}
Je to JSON. ${STRUCT[c.type]}
Prelož VSECHNY textove hodnoty z cestiny do vsech tri jazyku:
- "en" = anglictina (prirozena, plynula, styl herniho magazinu)
- "de" = nemcina (spravne prehlasky a ß, spisovny styl herniho magazinu)
- "fr" = francouzstina (spravne akcenty é è à ç ê î ô û ù, spisovny styl herniho magazinu)

Pravidla: zachovej Markdown (## nadpisy, **tucne**, ### podnadpisy, odkazy) i strukturu 1:1; NEPREKLADEJ vlastni jmena (nazvy her, konzoli, cipu, studii, lidi, modelu); zachovej vsechny klice (slugy) i vnorene klice (teaser/detail/article/history) presne jako ve vstupu.

Uloz nastrojem Write do ${c.out} VALIDNI JSON tvaru:
{"en": <struktura s anglickymi texty>, "de": <struktura s nemeckymi texty>, "fr": <struktura s francouzskymi texty>}
Pozor na uvozovky uvnitr retezcu — escapuj je jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni.`
  return agent(prompt, { label: `xl8:${c.type}/${pad(i)}`, phase: 'Translate', model: 'sonnet' })
}))

return { chunks: chunks.length, done: results.filter(Boolean).length }
