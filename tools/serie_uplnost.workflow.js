export const meta = {
  name: 'serie-uplnost',
  description: 'Najde dily serii, ktere v katalogu uplne chybi',
  phases: [{ title: 'Uplnost', detail: 'davka serii na agenta, vystup = chybejici tituly' }],
}

phase('Uplnost')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')
const done = new Set(skip || [])

const RULES = `Uloha: u kazde herni serie zjistit, ktere jeji dily v katalogu CHYBI.

Vstupni soubor je JSON pole objektu {serie, mame}, kde "mame" je seznam nazvu,
ktere uz v katalogu jsou (napric vsemi platformami, bez opakovani).

Vrat tituly, ktere do serie patri a v seznamu NEJSOU.

CO SE POCITA JAKO CHYBEJICI DIL:
- samostatne vydana hra serie, vcetne spin-offu a handheldovych odbocek
- datadisk, ktery vysel jako samostatny produkt (Call of Duty: United Offensive)
- remake nebo remaster pod VLASTNIM nazvem (Diablo II: Resurrected) — je to
  samostatny titul, ne jen dalsi vydani

CO NEVRACET:
- tentyz titul pod jinym regionalnim nazvem, kdyz uz jednu podobu mame
  (mame "Final Fantasy VI (FFIII US)" -> nevracej "Final Fantasy III")
- pouhe porty a edice teze hry na dalsi platformy (to resi jiny nastroj)
- ohlasene hry, ktere jeste nevysly
- sberatelske kompilace a "trilogy" balicky bez noveho obsahu
- mobilni free-to-play odbocky, pokud to neni vyznamny titul serie

POZOR NA FAKTA: vracej jen tituly, kterymi si jsi JISTY, ze existuji a ze do
serie patri. Vymysleny dil je horsi nez zadny — objevi se na webu jako hra,
ktera nikdy nevysla. Kdyz si u serie nejsi jisty nicim, vrat pro ni prazdny
seznam. Neni cilem neco najit za kazdou cenu.

U kazdeho titulu uved rok prvniho vydani a platformy, na kterych vysel; pouzivej
jen tyto slugy: pc-modern, pc-9x, pc-dos, ps2, ps3, ps4, ps5, playstation, xbox,
xbox-360, xbox-one, xbox-series, switch, gamecube, wii, wii-u, nds, 3ds, n64,
snes, nes, mega-drive, master-system, game-boy, game-boy-color,
game-boy-advance, psp, ps-vita, dreamcast, saturn, amiga, atari-st, c64, mobil,
arcade. Kdyz hra vysla nekde jinde, tu platformu vynech.

Vystup uloz nastrojem Write jako VALIDNI JSON pole objektu
{"serie": "<nazev serie>", "name": "<presny nazev hry>", "year": "<rok>",
 "platforms": ["<slug>", ...]}
Kdyz nechybi nic, uloz prazdne pole []. Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem serii a poctem nalezenych chybejicich dilu.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `uplnost_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}_in.json`, out: `${base}/${name}_out.json` })
}

log(`Uplnost serii: ${jobs.length} davek` + (skipped ? `, ${skipped} preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON pole,
vrat jen: SKIP`
  return agent(prompt, { label: `uplnost:${pad(j.i)}`, phase: 'Uplnost', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
