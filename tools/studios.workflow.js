export const meta = {
  name: 'studios',
  description: 'Dohleda vyvojarske studio hram, ktere ho v katalogu nemaji',
  phases: [{ title: 'Studia', detail: 'davka her na agenta, vystup {slug: "studio"}' }],
}

phase('Studia')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')
const done = new Set(skip || [])

const RULES = `Uloha: doplnit VYVOJARSKE STUDIO hram, ktere ho v katalogu nemaji.

Vstup je JSON pole objektu {slug, name, platform, year, genre}.

Pro KAZDOU hru vrat jmeno studia, ktere hru VYVINULO — ne vydavatele.
U portu na konkretni platformu plati studio, ktere delalo TUHLE verzi, kdyz
se lisi od autora originalu.

Priklady toho, na cem se nejcasteji chybuje:
- "Sonic the Hedgehog" vyvinulo Sonic Team, Sega je vydavatel
- "GoldenEye 007" vyvinulo Rare, Nintendo je vydavatel
- "Aladdin" na Mega Drive delalo Virgin Games, na SNES Capcom — jina hra, jine studio
- japonske hry uvadej pod jmenem, pod kterym studio vystupovalo tehdy
  (Squaresoft, ne Square Enix, kdyz jde o hru z devadesatek)

Jmeno pis jako bezne jmeno studia bez pravni formy a bez dovetku:
"Konami", ne "Konami Co., Ltd."; "Team17", ne "Team17 Digital Limited".

POZOR NA FAKTA: kdyz si studiem NEJSI JISTY, hru z vystupu VYNECH. Prazdny
zaznam je v poradku; vymyslene studio je horsi nez zadne, protoze se pak
objevi na strance vyvojare a v prehledu "od stejneho studia".
Nepis zastupne hodnoty jako "neznamy", "ruzni" nebo "homebrew".

Vystup uloz nastrojem Write jako VALIDNI JSON objekt {"<slug>": "<studio>", ...}.
Uved jen hry, kterymi si jsi jisty — nemusis pokryt cely vstup. Zadny text
mimo JSON. Vrat kratke potvrzeni s poctem doplnenych a vynechanych her.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `studios_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}.json`, out: `${base}/${name}_out.json` })
}

log(`Studia: ${jobs.length} davek` + (skipped ? `, ${skipped} hotovych preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON, vrat jen: SKIP`
  return agent(prompt, { label: `studia:${pad(j.i)}`, phase: 'Studia', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
