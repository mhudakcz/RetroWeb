export const meta = {
  name: 'teasers',
  description: 'Doplni hram uvodni shrnujici vetu ve stylu starsich platforem',
  phases: [{ title: 'Teasery', detail: 'davka her na agenta, vystup {slug: veta}', model: 'sonnet' }],
}

phase('Teasery')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')
const done = new Set(skip || [])

// Staticka cast je schvalne prvni, promenne az za ni.
const RULES = `Uloha: napsat ke kazde hre JEDNU uvodni shrnujici vetu (teaser) v CESTINE.

Tenhle web uz teasery ma u starsich platforem a novy musi znit STEJNE. Ukazky stylu:
  Streets of Rage 2 — "Mozna nejlepsi 2D beat 'em up vubec; legendarni soundtrack od Yuza Koshira."
  Tetris (Game Boy) — "Pack-in titul, ktery prodal Game Boy. Mozna nejdokonalejsi puzzle vsech dob."
  Metroid II — "Temna, klaustrofobni lovecka vyprava. Atmosferou predbehla dobu."
  Wario Land — "Pomalejsi, prozkoumavaci protipol Maria. Sbirani pokladu a hledani tajnych vychodu je navykove."
  Kid Dracula — "Odlehceny, vtipny Castlevania spin-off. Skryty poklad Konami."

Pravidla:
- DELKA 40-90 znaku. To je tvrdy limit — je to jednoradkovy popisek, ne odstavec.
- Jedna az dve uderne vety. Klidne oddelene teckou nebo strednikem.
- Ma to byt VERDIKT plus jeden konkretni detail, ktery hru odlisuje: cim je slavna,
  co v ni bylo poprve, kdo delal hudbu, v cem je jina nez konkurence.
- Piš s nazorem ("mozna nejlepsi", "skryty poklad"), ne encyklopedicky.
- NEZACINEJ nazvem hry — ten je na strance hned nad tim. Zadne "Tato hra je...".
- NEPREKLADEJ nazvy her, konzoli a studii.
- POZOR NA FAKTA: piš jen to, cim si jsi jisty. NIKDY si nevymysli jmena skladatelu
  a vyvojaru, cisla prodeju ani hodnoceni. Kdyz o hre nic konkretniho bezpecne nevis,
  napis strizlivejsi vetu o zanru a tom, jak se hraje — to je vzdy lepsi nez vymysl.
- Nepis, na jake platforme hra vysla, pokud to prave neni ta pointa (napr. povedeny
  port na slabsi hardware nebo naopak verze, ktera je nejlepsi z celeho seznamu).

Vstup je JSON pole objektu {slug, name, platform, genre, year, studio, uryvek}.
"uryvek" je zacatek uz hotoveho ceskeho clanku o hre — ber z nej fakta, neopisuj vety.

Vystup uloz nastrojem Write jako VALIDNI JSON objekt {"<slug>": "<veta>", ...}
se VSEMI slugy ze vstupu. Uvozovky uvnitr escapuj jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem her a prumernou delkou vety.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `teaser_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}.json`, out: `${base}/${name}_out.json` })
}

log(`Teasery: ${jobs.length} davek` + (skipped ? `, ${skipped} hotovych preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON, vrat jen: SKIP`
  return agent(prompt, { label: `teaser:${pad(j.i)}`, phase: 'Teasery', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
