export const meta = {
  name: 'series-intro',
  description: 'Napise pruvodni texty k hernim seriim rovnou ve ctyrech jazycich',
  phases: [{ title: 'Intra', detail: 'davka serii na agenta, vystup {slug: {cs,en,de,fr}}' }],
}

phase('Intra')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(2, '0')

log(`Pruvodni texty k seriim: ${batches.length} davek`)

const results = await parallel(batches.map((b, i) => () => {
  const out = `${base}/intro_${pad(i)}.json`
  const list = b.map((s) => `- ${s.name} (${s.count} her v katalogu, roky ${s.span}, platformy: ${s.platforms})`).join('\n')
  const slugs = b.map((s) => `"${s.slug}" = ${s.name}`).join(', ')
  const prompt = `Idempotentni uloha: pruvodni texty k hernim seriim, rovnou ve ctyrech jazycich.

KROK 1 - kontrola: Zkus nastrojem Read otevrit ${out}
Pokud EXISTUJE a je to VALIDNI JSON, kde ma kazdy slug vsechny ctyri jazyky (cs, en, de, fr),
jsi hotov — nic nezapisuj a vrat pouze: SKIP

KROK 2 - prace. Napis pruvodni text ke kazde z techto hernich serii:
${list}

Slugy pro vystup: ${slugs}

Text ke KAZDE serii:
- CILOVA DELKA 1100-1400 znaku v kazdem jazyce. Kratsi nez 1000 je chyba.
- 2 odstavce oddelene prazdnym radkem (\\n\\n). Zadne nadpisy ani odrazky.
- Obsah: cim serie zacala a kdy, co ji definuje (herni principy, atmosfera, cim se
  odlisuje), jak se vyvijela napric generacemi, ktere dily jsou povazovane za vrchol
  a proc, jaky mela vliv na zanr. Zminuj konkretni dily jmenem.
- POZOR NA FAKTA: piš jen to, cim si jsi jisty. NIKDY si nevymysli cisla prodeju,
  procentualni hodnoceni, jmena vyvojaru ani citace recenzi. Kdyz si necim nejsi jisty,
  napis to obecneji nebo vynech. Radeji strizlivy text nez vymysleny detail.
- Styl: plynula magazinova reportaz pro herni web, ne encyklopedicke heslo.
- Nazvy her, konzoli a studii nechavej v originale, neprekladej je.

Napis kazdy text ve VSECH ctyrech jazycich:
- "cs" = cestina (vychozi, piš ji jako prvni)
- "en" = anglictina
- "de" = nemcina (spravne prehlasky a ß)
- "fr" = francouzstina (spravne akcenty)
Nejde o otrocky preklad — v kazdem jazyce to ma znit prirozene, ale fakta i vyzneni
musi byt stejna.

Uloz nastrojem Write do ${out} VALIDNI JSON tvaru:
{"<slug>": {"cs": "...", "en": "...", "de": "...", "fr": "..."}, ...}
se VSEMI slugy z teto davky. Uvozovky uvnitr textu escapuj jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni.`
  return agent(prompt, { label: `serie:${pad(i)}`, phase: 'Intra', model: 'sonnet' })
}))

return { batches: batches.length, done: results.filter(Boolean).length }
