export const meta = {
  name: 'series-intro',
  description: 'Napise pruvodni texty k hernim seriim rovnou ve ctyrech jazycich',
  phases: [{ title: 'Intra', detail: 'davka serii na agenta, vystup {slug: {cs,en,de,fr}}' }],
}

phase('Intra')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')
const done = new Set(skip || [])

const RULES = `Uloha: pruvodni texty k hernim seriim, rovnou ve ctyrech jazycich.

Vstupni soubor je JSON pole objektu
{slug, name, count, span, platforms, pasmo, min, max, odstavcu}.

Text ke KAZDE serii ze vstupu:
- DELKA JE U KAZDE SERIE JINA — je to pole "min" a "max" (znaku v KAZDEM jazyce).
  Ridi se vahou znacky: serie s desitkami dilu napric generacemi unese vic nez
  serie o dvou dilech. Text kratsi nez "min" je chyba, stejne jako text
  nafouknuty vatou na "max".
- Pocet odstavcu je v poli "odstavcu". Oddeluj je prazdnym radkem (\\n\\n).
  Zadne nadpisy ani odrazky.
- Delsi text NENI tyz text rozredeny. Kdyz je prostoru vic, napis toho vic
  vecne: jednotlive dily a cim se lisily, odbocky serie a spin-offy, zmeny
  studia nebo vydavatele, obdobi utlumu a navraty, prijeti u hracu.
- Obsah: cim serie zacala a kdy, co ji definuje (herni principy, atmosfera, cim
  se odlisuje), jak se vyvijela napric generacemi, ktere dily jsou povazovane za
  vrchol a proc, jaky mela vliv na zanr. Zminuj konkretni dily jmenem.
- POZOR NA FAKTA: piš jen to, cim si jsi jisty. NIKDY si nevymysli cisla prodeju,
  procentualni hodnoceni, jmena vyvojaru ani citace recenzi. Kdyz si necim nejsi
  jisty, napis to obecneji nebo vynech. Radeji strizlivy text nez vymysleny detail.
  Delka NENI duvod neco si vymyslet — kdyz o serii neni co rici, drz se spodni
  hranice rozsahu.
- Styl: plynula magazinova reportaz pro herni web, ne encyklopedicke heslo.
- Nazvy her, konzoli a studii nechavej v originale, neprekladej je.

Napis kazdy text ve VSECH ctyrech jazycich:
- "cs" = cestina (vychozi, piš ji jako prvni)
- "en" = anglictina
- "de" = nemcina (spravne prehlasky a ß)
- "fr" = francouzstina (spravne akcenty)
Nejde o otrocky preklad — v kazdem jazyce to ma znit prirozene, ale fakta
i vyzneni musi byt stejna, vcetne delky.

Vystup uloz nastrojem Write jako VALIDNI JSON tvaru
{"<slug>": {"cs": "...", "en": "...", "de": "...", "fr": "..."}, ...}
se VSEMI slugy ze vstupu. Uvozovky uvnitr textu escapuj jako \\". Zadny text
mimo JSON. Vrat kratke potvrzeni s poctem serii a delkami ceskych textu.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `intro_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}_in.json`, out: `${base}/${name}.json` })
}

log(`Pruvodni texty k seriim: ${jobs.length} davek` + (skipped ? `, ${skipped} preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje, je validni JSON, ma
vsechny slugy ze vstupu a kazdy ve vsech ctyrech jazycich v pozadovane delce,
vrat jen: SKIP`
  return agent(prompt, { label: `serie:${pad(j.i)}`, phase: 'Intra', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
