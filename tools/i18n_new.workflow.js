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
// Hotove davky se daji predat v `skip` (seznam nazvu jako "games_007").
// Bez toho se pri navazovani nastartuje agent i pro kazdou hotovou davku
// jen aby precetl soubor a vratil SKIP — pri desitkach davek zbytecna rezie.
const skip = new Set(
  (typeof args === 'string' ? JSON.parse(args) : args).skip || [],
)

const chunks = []
let skipped = 0
for (const type of ORDER) {
  const n = counts[type] || 0
  for (let i = 0; i < n; i++) {
    const name = `${type}_${pad(i)}`
    if (skip.has(name)) { skipped++; continue }
    chunks.push({ type, name, in: `${base}/chunks/${name}.json`, out: `${base}/chunks/${name}_out.json` })
  }
}

log(`Preklad do EN+DE+FR: ${chunks.length} davek k prekladu` +
    (skipped ? `, ${skipped} uz hotovych preskoceno bez agenta` : ''))

// Staticka cast promptu je u vsech davek totozna a je schvalne PRVNI —
// promenne cesty jsou az na konci, takze se spolecny prefix da nacachovat
// napric desitkami agentu misto opakovaneho posilani.
const RULES = `Idempotentni prekladova uloha do ANGLICTINY, NEMCINY a FRANCOUZSTINY.

Postup:
1. KONTROLA: Zkus nastrojem Read otevrit vystupni soubor (cesta nize).
   Pokud EXISTUJE a je to VALIDNI JSON obsahujici VSECHNY tri klice "en", "de" i "fr",
   jsi hotov — NIC neprekladej, nic nezapisuj a vrat pouze slovo: SKIP
2. PREKLAD (jen kdyz vystup neexistuje nebo mu nektery jazyk chybi):
   Read vstupni soubor a preloz VSECHNY textove hodnoty z cestiny do vsech tri jazyku:
   - "en" = anglictina (prirozena, plynula, styl herniho magazinu)
   - "de" = nemcina (spravne prehlasky a ß, spisovny styl herniho magazinu)
   - "fr" = francouzstina (spravne akcenty é è à ç ê î ô û ù, spisovny styl herniho magazinu)

Pravidla: zachovej Markdown (## nadpisy, **tucne**, ### podnadpisy, odkazy) i strukturu 1:1;
NEPREKLADEJ vlastni jmena (nazvy her, konzoli, cipu, studii, lidi, modelu);
zachovej vsechny klice (slugy) i vnorene klice (teaser/detail/article/history) presne jako ve vstupu.

Vystup uloz nastrojem Write jako VALIDNI JSON tvaru:
{"en": <struktura s anglickymi texty>, "de": <struktura s nemeckymi texty>, "fr": <struktura s francouzskymi texty>}
Pozor na uvozovky uvnitr retezcu — escapuj je jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni.`

const results = await parallel(chunks.map((c, i) => () => {
  const prompt = `${RULES}

--- tato davka ---
Struktura vstupu: ${STRUCT[c.type]}
Vstupni soubor:  ${c.in}
Vystupni soubor: ${c.out}`
  return agent(prompt, { label: `xl8:${c.type}/${pad(i)}`, phase: 'Translate', model: 'sonnet' })
}))

return { chunks: chunks.length, done: results.filter(Boolean).length }
