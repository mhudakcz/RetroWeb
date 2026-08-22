export const meta = {
  name: 'expand-short',
  description: 'Rozsiri prilis kratke CZ clanky ke hram na plnou magazinovou delku (~1800-2000 znaku)',
  phases: [{ title: 'Expand', detail: 'per-chunk: skip if out exists, else rewrite articles longer' }],
}

phase('Expand')
const { base, chunks: n } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (i) => String(i).padStart(3, '0')

log(`Rozsireni kratkych clanku: ${n} davek po 20 hrach`)

const jobs = Array.from({ length: n }, (_, i) => ({
  in: `${base}/chunks/exp_${pad(i)}.json`,
  out: `${base}/chunks/exp_${pad(i)}_out.json`,
  i,
}))

const results = await parallel(jobs.map((c) => () => {
  const prompt = `Idempotentni uloha: rozsireni ceskych clanku o retro hrach na plnou magazinovou delku.

KROK 1 – kontrola: Zkus nastrojem Read otevrit ${c.out}
Pokud EXISTUJE a je to VALIDNI JSON objekt {slug: text} s neprazdnymi texty, jsi hotov — nic nezapisuj a vrat pouze: SKIP

KROK 2 – prace: Read ${c.in}
Je to JSON pole objektu {slug, platform, name, year, studio, genre, current}. "current" je STAVAJICI cesky clanek, ktery je prilis kratky (cca 1150–1600 znaku).

Pro KAZDOU hru napis ROZSIRENOU verzi clanku v CESTINE:
- CILOVA DELKA 1800–2000 znaku (vcetne mezer). Kratsi nez 1750 je chyba, delsi nez 2200 taky.
- Vychazej z "current" — zachovej jeho fakta, hodnoceni i vyzneni, nic si neprotirec. Text rozsiruj, neprepisuj od nuly.
- Cim rozsirit (vyber, co k dane hre skutecne sedi): konkretni herni mechaniky a jak se hra ovlada; technicke reseni a jak vypadala na dobovem hardwaru; atmosfera, hudba, vytvarny styl; dobove prijeti a prodeje; vliv na zanr a pokracovani serie; jak hra pusobi dnes.
- POZOR NA FAKTA: piš jen to, co si o hre skutecne jisty. Radeji obecnejsi formulace nez vymysleny detail. NIKDY si nevymysli jmena vyvojaru, presna cisla prodeju, hodnoceni v procentech ani citace recenzi.
- Styl: plynula ceska magazinova reportaz, 2–3 odstavce oddelene prazdnym radkem. Zadne nadpisy, zadne odrazky, zadny Markdown krome pripadneho **tucneho** zvyrazneni nazvu hry v prvni vete.
- Nazvy her, konzoli, studii a cipu nechavej v originale.

Uloz nastrojem Write do ${c.out} VALIDNI JSON objekt {"<slug>": "<rozsireny clanek>", ...} se VSEMI slugy z ${c.in}.
Odstavce oddeluj jako \\n\\n. Uvozovky uvnitr textu escapuj jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem her a prumernou delkou.`
  return agent(prompt, { label: `exp:${pad(c.i)}`, phase: 'Expand', model: 'sonnet' })
}))

return { chunks: n, done: results.filter(Boolean).length }
