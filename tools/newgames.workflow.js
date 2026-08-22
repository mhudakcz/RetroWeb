export const meta = {
  name: 'new-games',
  description: 'Vygeneruje dalsi hry na modernich platformach vcetne plnych CZ clanku',
  phases: [{ title: 'Generate', detail: 'agent na kazdy tematicky okruh dane platformy' }],
}

phase('Generate')
const { base, plan } = typeof args === 'string' ? JSON.parse(args) : args

const total = plan.reduce((n, p) => n + p.slices.length, 0)
log(`Generovani her: ${plan.length} platforem, ${total} okruhu`)

const jobs = []
for (const p of plan) {
  p.slices.forEach((slice, i) => {
    jobs.push({ ...p, slice, i, out: `${base}/out_${p.slug}_${String(i).padStart(2, '0')}.json` })
  })
}

const results = await parallel(jobs.map((j) => () => {
  const prompt = `Idempotentni uloha: navrh her do katalogu retro webu vcetne plnych ceskych clanku.

KROK 1 – kontrola: Zkus nastrojem Read otevrit ${j.out}
Pokud EXISTUJE a je to VALIDNI JSON pole s alespon ${j.count} polozkami, jsi hotov — nic nezapisuj a vrat pouze: SKIP

KROK 2 – prace.
Platforma: ${j.platform} (slug "${j.slug}")
Tematicky okruh: ${j.slice}

Nejdriv si nactri Read ${base}/existing_${j.slug}.txt — je to seznam her, ktere uz v katalogu JSOU. Zadnou z nich neopakuj (ani jinou jazykovou variantu tehoz nazvu).

Navrhni ${j.count} DALSICH her, ktere na teto platforme SKUTECNE vysly a spadaji do zadaneho okruhu. Vybirej vyznamne, dobre zname nebo kriticky cenene tituly — ne obskurni vyplne. NEVYMYSLEJ si hry ani porty, ktere neexistuji; kdyz si u titulu nejsi jisty, radeji ho vynech.

Pro KAZDOU hru vrat objekt:
{
 "name": "presny anglicky nazev, jak vysel",
 "genre": "zanr cesky nebo bezne uzivanym anglickym terminem (napr. \\"Akcni adventura\\", \\"JRPG\\", \\"Shmup\\", \\"Zavodni\\", \\"Plosinovka\\", \\"Strategie\\")",
 "length": "S | M | L | XL (odhad delky hrani: S do 5 h, M 5-15 h, L 15-40 h, XL 40+ h)",
 "year": "rok vydani na teto platforme, jako retezec",
 "studio": "vyvojarske studio",
 "flags": [],
 "article": "cesky clanek"
}

Pole "flags" muze obsahovat jen tyto hodnoty (a klidne zustat prazdne):
 "mustplay" = zasadni, doporucene i dnes | "puzzle" = logicka hra
 "mature" = pro dospele (nasili, horor) | "homebrew" = neoficialni/komunitni titul

Clanek ("article"):
- CILOVA DELKA 1800–2000 znaku vcetne mezer. Kratsi nez 1750 je chyba.
- Cesky, plynula magazinova reportaz, 2–3 odstavce oddelene prazdnym radkem (\\n\\n).
- Obsah: o cem hra je a jak se hraje, herni mechaniky, technicke provedeni na dane platforme, atmosfera a hudba, dobove prijeti, vliv na zanr, jak pusobi dnes.
- POZOR NA FAKTA: piš jen to, co si o hre skutecne jisty. NIKDY si nevymysli jmena vyvojaru, cisla prodeju, procentualni hodnoceni ani citace recenzi. Radeji obecnejsi formulace nez vymysleny detail.
- Zadne nadpisy ani odrazky. Nazvy her, konzoli a studii nechavej v originale.
- Prvni veta necht obsahuje nazev hry v **tucnem**.

Uloz nastrojem Write do ${j.out} VALIDNI JSON pole techto objektu (${j.count} polozek).
Uvozovky uvnitr textu escapuj jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem her.`
  return agent(prompt, { label: `hry:${j.slug}/${j.i}`, phase: 'Generate', model: 'sonnet' })
}))

return { jobs: jobs.length, done: results.filter(Boolean).length }
