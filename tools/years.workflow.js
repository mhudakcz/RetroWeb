export const meta = {
  name: 'years',
  description: 'Dohleda rok vydani hram, ktere ho v katalogu nemaji',
  phases: [{ title: 'Roky', detail: 'davka her na agenta, vystup {slug: "rok"}' }],
}

phase('Roky')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')
const done = new Set(skip || [])

const RULES = `Uloha: doplnit rok vydani hram, ktere ho v katalogu nemaji.

Vstup je JSON pole objektu {slug, name, platform, platform_years, studio}.

Pro KAZDOU hru vrat rok, kdy vysla NA TETO KONKRETNI PLATFORME — ne rok
arkadoveho originalu, ne rok pozdejsiho portu jinam. U her, ktere na dane
platforme vysly v ruznych regionech v jinych letech, uved rok PRVNIHO vydani.

Priklady toho, na cem se nejcasteji chybuje:
- "Space Harrier" na Master Systemu vysel 1986, prestoze arkada je z roku 1985
- "Doom" na Sega 32X vysel 1994, prestoze DOSova verze je z roku 1993
- "Out Run" na Mega Drive vysel 1991, arkada 1986

POZOR NA FAKTA: kdyz si rokem NEJSI JISTY, hru z vystupu VYNECH. Prazdny
zaznam je v poradku; vymysleny rok je horsi nez zadny, protoze se pak dostane
na casovou osu i do provazani verzi. Netipuj podle roku platformy.

Vystup uloz nastrojem Write jako VALIDNI JSON objekt {"<slug>": "<rok>", ...},
kde rok je ctyrmistne cislo jako retezec, napriklad "1991". Uved jen hry,
kterymi si jsi jisty — nemusis pokryt cely vstup. Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem doplnenych a vynechanych her.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `years_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}.json`, out: `${base}/${name}_out.json` })
}

log(`Roky vydani: ${jobs.length} davek` + (skipped ? `, ${skipped} hotovych preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON, vrat jen: SKIP`
  return agent(prompt, { label: `roky:${pad(j.i)}`, phase: 'Roky', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
