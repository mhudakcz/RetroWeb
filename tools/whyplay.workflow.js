export const meta = {
  name: 'whyplay',
  description: 'Dopise clankum zaverecnou vetu "Proc hrat"',
  phases: [{ title: 'Proc hrat', detail: 'davka her na agenta, vystup {slug: veta}', model: 'sonnet' }],
}

phase('Proc hrat')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')

const RULES = `Uloha: napsat ke kazde hre ZAVERECNOU vetu clanku v CESTINE.

Clanek o hre konci shrnutim, ktere ctenari primo rekne, proc si titul pustit.
Na webu se zobrazi za tucnym "Proč hrát:", ktery UZ TAM JE — piš jen text za nim.

Ukazky stylu:
  "Pro nadcasovou SNES klasiku v kapesni podobe plus historicky prvni kooperativni
   Zeldu — dvojnasobna hodnota v jedne kazete."
  "Chytra mechanika stridani rocnich obdobi a unikatni propojeni s Oracle of Ages
   delaji z teto dvojice jednu z nejnapaditejsich kapitol cele serie Zelda."

Pravidla:
- DELKA 90-260 znaku. Jedna veta, nanejvys dve.
- Je to DOPORUCENI, ne shrnuti deje. Rekni, KOMU a PROC se hra vyplati.
- Vychazej ze "zaveru" — je to posledni odstavec uz hotoveho clanku. Neopakuj
  jeho vety doslova, ale nesmis si s nim protirecit.
- Kdyz ma hra vyhradu (kratka, tezka, zestarla), klidne ji zminy — doporuceni
  s vyhradou je uzitecnejsi nez chvalozpev.
- NEZACINEJ nazvem hry ani slovem "Hra". Zacni rovnou duvodem, klidne predlozkou
  ("Pro ...", "Kvuli ...", "Jestli ...").
- NEPREKLADEJ nazvy her, konzoli a studii.
- POZOR NA FAKTA: piš jen to, cim si jsi jisty. NIKDY si nevymysli jmena
  skladatelu a vyvojaru, cisla prodeju ani hodnoceni.

Vstup je JSON pole objektu {slug, name, platform, year, studio, genre, zaver}.

Vystup uloz nastrojem Write jako VALIDNI JSON objekt {"<slug>": "<veta>", ...}
se VSEMI slugy ze vstupu. Uvozovky uvnitr escapuj jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem her a prumernou delkou.`

const jobs = Array.from({ length: batches }, (_, i) => ({
  i, in: `${base}/why_${pad(i)}.json`, out: `${base}/why_${pad(i)}_out.json`,
}))

log(`Zaverecne vety: ${jobs.length} davek`)

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON, vrat jen: SKIP`
  return agent(prompt, { label: `proc:${pad(j.i)}`, phase: 'Proc hrat', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
