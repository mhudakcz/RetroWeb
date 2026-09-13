export const meta = {
  name: 'serie',
  description: 'Posoudi kandidaty na herni serii a vrati definice do series.json',
  phases: [{ title: 'Serie', detail: 'davka skupin na agenta, vystup je pole definic' }],
}

phase('Serie')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')
const done = new Set(skip || [])

const RULES = `Uloha: posoudit skupiny her, ktere maji podobny nazev, a rozhodnout,
ktere z nich jsou opravdu jedna herni serie.

Vstup je JSON pole objektu {klic, hry:[{slug, name, platform, year}]}.
Skupiny vznikly strojove podle spolecneho zacatku nazvu, takze cast z nich
jsou PLANE SHODY — ty se musi zahodit:

- "Alien 3" a "Alien 8" spolu nesouviseji (filmova licence vs. britska hra pro ZX)
- "Bust-A-Move" a "Bust-A-Groove" jsou dve ruzne serie
- "Mario Kart" a "Mario Party" jsou ruzne serie, i kdyz obe zacinaji "Mario"
- tentyz titul na peti platformach neni serie, jen pet vydani jedne hry

Serie je posloupnost RUZNYCH her, ktere k sobe patri vydavatelem a znackou.

Pro kazdou skupinu, ktera serii JE, vrat definici:
{
  "slug": "kratky-slug-s-pomlckami",
  "name": "Nazev serie, jak ji lide znaji",
  "match": ["retezec", "dalsi retezec"],
  "exclude": ["nepatri sem"]
}

"match" jsou retezce, ktere se hledaji v nazvu hry na hranicich slov
(mala pismena, bez diakritiky se nemeni). Musi chytit vsechny dily serie
a zaroven NESMI chytit hry, ktere do ni nepatri. Kdyz hrozi zamena,
pouzij "exclude" — podretezec, po jehoz nalezeni se hra vyradi.
"exclude" uvadej jen kdyz je potreba, jinak klic vynech.

Priklad: skupina "alien" obsahuje Alien 3, Alien: Isolation a Alien 8.
Spravna odpoved je jedna serie {"slug":"alien","name":"Alien","match":["alien"],
"exclude":["alien 8"]} — Alien 8 do ni nepatri.

POZOR NA FAKTA: kdyz si u skupiny NEJSI JISTY, jestli jde o serii, VYNECH ji.
Prazdny vystup je v poradku. Falesna serie se projevi na webu jako stranka,
ktera slucuje nesouvisejici hry, coz je horsi nez zadna stranka.

Vystup uloz nastrojem Write jako VALIDNI JSON POLE definic (muze byt prazdne).
Zadny text mimo JSON. Vrat kratke potvrzeni s poctem prijatych a zahozenych skupin.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `serie_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}.json`, out: `${base}/${name}_out.json` })
}

log(`Serie: ${jobs.length} davek` + (skipped ? `, ${skipped} hotovych preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON, vrat jen: SKIP`
  return agent(prompt, { label: `serie:${pad(j.i)}`, phase: 'Serie', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
