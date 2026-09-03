export const meta = {
  name: 'titles',
  description: 'Napise zaznamy ke hram ze zadaneho seznamu nazvu',
  phases: [{ title: 'Zaznamy', detail: 'jedna davka nazvu na agenta', model: 'sonnet' }],
}

phase('Zaznamy')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')

const RULES = `Uloha: napsat zaznamy do katalogu retro her k PREDEM DANEMU seznamu nazvu.

Vstup je JSON: {slug, platform, tituly, uz_mame}. "tituly" je seznam nazvu her,
ktere na te platforme vysly a v katalogu chybi. "uz_mame" jsou hry, ktere uz
v katalogu na te platforme jsou.

DULEZITE — na rozdil od jinych davek si tituly NEVYBIRAS. Zpracuj ty ze
seznamu "tituly" a zadne jine.

KDY TITUL VYNECHAT (a je to spravne, ne selhani):
- Kdyz si nejsi jisty, ze hra na TETO platforme opravdu vysla.
- Kdyz je to jen jina regionalni verze nebo reedice hry, ktera uz je
  v "uz_mame" (napr. "Rockman & Forte" je japonsky nazev "Mega Man & Bass").
- Kdyz jde o kompilaci nebo o titul, ktery uz "uz_mame" pokryva jako serii.
Radeji vynech, nez abys napsal zaznam k necemu, co neexistuje. Do odpovedi
napis, ktere tituly jsi vynechal a proc.

KE KAZDEMU ZPRACOVANEMU TITULU:
{
 "name": "presny anglicky nazev, jak vysel",
 "genre": "zanr cesky (napr. Akcni plosinovka, JRPG, Zavodni hra)",
 "length": "S | M | L | XL",
 "year": "rok vydani na teto platforme",
 "studio": "vyvojar",
 "flags": [],
 "detail": "cesky clanek"
}
flags: "mustplay" = zasadni titul platformy | "puzzle" = logicka hra |
"mature" = pro dospele | "homebrew" = neoficialni titul. Bezne prazdne pole.

CLANEK ("detail"):
- DELKA 1500-2000 znaku vcetne mezer.
- 3 odstavce oddelene prazdnym radkem, plynula ceska magazinova reportaz.
- Prvni zminka nazvu hry **tucne**.
- Posledni odstavec konci samostatnym radkem: "**Proč hrát:** <jedna veta>".
- POZOR NA FAKTA: nevymyslej si jmena vyvojaru, cisla prodeju ani hodnoceni.
  Kdyz rok nebo studio nevis jiste, napis, co vis, a zbytek vynech.

Vystup uloz nastrojem Write jako VALIDNI JSON pole techto objektu.
Zadny text mimo JSON v souboru.`

const jobs = Array.from({ length: batches }, (_, i) => ({
  i, in: `${base}/tit_${pad(i)}.json`, out: `${base}/tit_${pad(i)}_out.json`,
}))

log(`Zaznamy k zadanym titulum: ${jobs.length} davek`)

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON
s neprazdnym polem, vrat jen: SKIP`
  return agent(prompt, { label: `tituly:${pad(j.i)}`, phase: 'Zaznamy', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
