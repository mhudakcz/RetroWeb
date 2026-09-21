export const meta = {
  name: 'hardware',
  description: 'Napise medailonky retro handheldu do hardware_extra.json',
  phases: [{ title: 'Zarizeni', detail: 'davka zarizeni na agenta, vystup = pole polozek' }],
}

phase('Zarizeni')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(2, '0')
const done = new Set(skip || [])

const RULES = `Uloha: medailonky kapesnich konzoli pro retro hrani.

Vstupni soubor je JSON pole objektu {slug, name, znacka}. Ke kazdemu zarizeni
napis jeden zaznam do katalogu hardwaru.

POZOR NA FAKTA — tohle je nejdulezitejsi pravidlo. U tehle techniky se snadno
vymysli cip, rozliseni nebo kapacita baterie, protoze modelu jsou desitky
a lisi se drobnostmi. Kdyz si u zarizeni NEJSI JISTY, ze existuje, nebo neznas
jeho parametry, VYNECH HO UPLNE — prazdny vystup je v poradku. Nikdy neuvadej
cenu (meni se) ani vymyslene udaje. Kdyz znas zarizeni, ale neznas nektery
parametr, ten radek ze "specs" vynech; nedoplnuj odhad.

Vrat pole objektu v tomto tvaru:
{
 "slug": "<slug ze vstupu>",
 "name": "<presny nazev zarizeni>",
 "kind": "Kapesni konzole · <rok uvedeni>",
 "tagline": "<jedna veta, 50-110 znaku — cim je tenhle model zajimavy>",
 "color": "<vyrazna barva v hex, napr. #ff3e7f>",
 "color2": "<tmava varianta tehoz odstinu, napr. #2a0f1d>",
 "art": "handheld-h nebo handheld-v (vodorovny vs. svisly tvar)",
 "intro": ["<odstavec 400-700 znaku: co to je a pro koho>"],
 "specs": [{"label": "Cip (SoC)", "value": "..."},
           {"label": "Displej", "value": "..."},
           {"label": "Pamet", "value": "..."},
           {"label": "Baterie", "value": "..."},
           {"label": "Uloziste", "value": "..."},
           {"label": "Systemy", "value": "..."}],
 "canPlay": [{"label": "NES, SNES, Mega Drive", "level": "ok"},
             {"label": "PlayStation (PS1)", "level": "ok"},
             {"label": "Nintendo 64, PSP", "level": "most"},
             {"label": "Dreamcast, PS2", "level": "some"}],
 "sections": [{"title": "<nadpis>", "body": ["<odstavec>", "<odstavec>"]},
              {"title": "<nadpis>", "body": ["<odstavec>"]}],
 "options": [{"title": "<kratky nadpis>", "text": "<jedna veta rady>"}]
}

"level" smi byt jen "ok" (plynule), "most" (vetsinou) nebo "some" (vybrane tituly).
Do "canPlay" pis skutecne moznosti daneho cipu — slabsi zarizeni na PS2 nestaci
a tvrdit opak je horsi nez to nenapsat.

"sections" jsou dva az tri oddily po 2-4 odstavcich: cim se model lisi od
sourozencu v rade, jak je na tom se systemy a komunitni podporou, pro koho se
hodi a pro koho ne. Pis strizlive a konkretne, ne reklamne — kde ma zarizeni
slabinu, napis ji.

"options" jsou dve az tri kratke rady (co k zarizeni dokoupit, jaky system zvolit).

Cely text pis CESKY. Nazvy zarizeni, cipu a systemu nechavej v originale.

Vystup uloz nastrojem Write jako VALIDNI JSON POLE. Kdyz si nejsi jisty ani
jednim zarizenim z davky, uloz prazdne pole []. Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem popsanych a vynechanych zarizeni.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `hw_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}_in.json`, out: `${base}/${name}_out.json` })
}

log(`Hardware: ${jobs.length} davek` + (skipped ? `, ${skipped} preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON pole,
vrat jen: SKIP`
  return agent(prompt, { label: `hw:${pad(j.i)}`, phase: 'Zarizeni', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
