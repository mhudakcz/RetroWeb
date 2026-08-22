export const meta = {
  name: 'version-notes',
  description: 'Napise k titulum vydanym na vic retro platformach poznamku, cim se verze lisily',
  phases: [{ title: 'Verze', detail: 'davka titulu na agenta, vystup {key: {cs,en,de,fr}}', model: 'sonnet' }],
}

phase('Verze')
const { base, batches, skip } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')
const done = new Set(skip || [])

const RULES = `Uloha: ke kazdemu titulu napsat poznamku, CIM SE LISILY jeho verze na jednotlivych platformach.

Tohle je klicova vec, kterou dnesni hrac uz nezna: v 8bitove a 16bitove ere byl "tentyz"
titul na kazdem stroji casto jina hra — jiny pocet barev, jina hudba, jiny scrolling,
vystrizene urovne, jinde zas verze nejlepsi z celeho seznamu.

Pravidla:
- DELKA 500-800 znaku v kazdem jazyce. Jeden odstavec, zadne nadpisy ani odrazky.
- Zminuj KONKRETNI platformy jmenem a rekni, v cem byla ta ktera verze lepsi nebo horsi:
  barvy a plynulost, zvukovy cip a hudba, velikost urovni, rychlost, ovladani,
  co se muselo vypustit. Kde je jedna verze povazovana za nejlepsi, napis to.
- Piš pro cloveka, ktery uvazuje, kterou verzi si dnes pustit — at z toho ma uzitek.
- POZOR NA FAKTA. Tohle je oblast, kde se snadno vymysli. Piš jen rozdily, kterymi si
  jsi SKUTECNE jisty. Kdyz o konkretnich rozdilech nic bezpecneho nevis, napis
  strizlive a obecne (napr. ze arkadni original prekonaval domaci konverze vykonem
  a ze osmibitove verze musely ubrat na barvach a plynulosti) — to je vzdy lepsi
  nez vymysleny detail. NIKDY si nevymysli jmena programatoru konverzi ani hodnoceni.
- NEPREKLADEJ nazvy her, konzoli a cipu.
- Nezacinej nazvem hry, ten je na strance nad tim.

Napis text ve VSECH ctyrech jazycich: "cs" (cestina, piš ji prvni), "en", "de"
(spravne prehlasky a ß), "fr" (spravne akcenty). Fakta i vyzneni musi byt stejna.

Vstup je JSON pole objektu {key, title, versions:[{platform, slug, year, genre, uryvek}]}.
"uryvek" je zacatek clanku o dane verzi — ber z nej fakta.

Vystup uloz nastrojem Write jako VALIDNI JSON objekt
{"<key>": {"cs":"...", "en":"...", "de":"...", "fr":"..."}, ...}
se VSEMI klici ze vstupu (pouzij presne hodnotu pole "key"). Uvozovky escapuj jako \\".
Zadny text mimo JSON. Vrat kratke potvrzeni.`

const jobs = []
let skipped = 0
for (let i = 0; i < batches; i++) {
  const name = `ver_${pad(i)}`
  if (done.has(name)) { skipped++; continue }
  jobs.push({ i, in: `${base}/${name}.json`, out: `${base}/${name}_out.json` })
}

log(`Poznamky k verzim: ${jobs.length} davek` + (skipped ? `, ${skipped} hotovych preskoceno` : ''))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON se vsemi
ctyrmi jazyky u kazdeho klice, vrat jen: SKIP`
  return agent(prompt, { label: `verze:${pad(j.i)}`, phase: 'Verze', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
