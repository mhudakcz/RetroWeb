export const meta = {
  name: 'series-expand',
  description: 'Rozsiri stavajici pruvodni texty k seriim na delsi a bohatsi verzi ve 4 jazycich',
  phases: [{ title: 'Rozsireni', detail: 'davka serii na agenta, vystup {slug: {cs,en,de,fr}}' }],
}

phase('Rozsireni')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(2, '0')

log(`Rozsireni uvodu k seriim: ${batches.length} davek`)

const results = await parallel(batches.map((b, i) => () => {
  const out = `${base}/exp_${pad(i)}.json`
  const list = b
    .map((s) => `- "${s.slug}" = ${s.name} (${s.count} her v katalogu, roky ${s.span}, platformy: ${s.platforms})`)
    .join('\n')

  const prompt = `Idempotentni uloha: rozsireni pruvodnich textu k hernim seriim.

KROK 1 - kontrola: Zkus nastrojem Read otevrit ${out}
Pokud EXISTUJE a je to VALIDNI JSON, kde ma kazdy slug vsechny ctyri jazyky (cs, en, de, fr)
a cesky text ma aspon 2000 znaku, jsi hotov — nic nezapisuj a vrat pouze: SKIP

KROK 2 - podklad. Nactri nastrojem Read soubor ${base}/current_${pad(i)}.json.
Je to {"<slug>": {"cs": ..., "en": ..., "de": ..., "fr": ...}} se STAVAJICIMI texty
techto serii:
${list}

KROK 3 - prace. Kazdy text prepis na DELSI a BOHATSI verzi.

Stavajici texty maji kolem 1200 znaku a jsou prilis strucne — projdou serii jen letmo.
Nova verze ma CILOVOU DELKU 2200-2800 znaku v kazdem jazyce, ve TRECH az CTYRECH
odstavcich oddelenych prazdnym radkem (\\n\\n).

Neni to preklad ani prepis jinymi slovy — text ma opravdu PRIBYT na obsahu:
- konkretni dily jmenem, roky a studia, ktera je delala
- v cem se jednotlivé generace lisily a proc — herni principy, technologie, tempo
- ktery dil je povazovan za vrchol serie a co presne za tim stoji
- co serie prinesla zanru a co po ni prevzali ostatni
- kde serie naopak selhala nebo se stocila jinam, kdyz se to o ni bezne rika
- drobnost, ktera se hodi vedet: prezdivka, technicka kuriozita, spor s vydavatelem

Cim NEplytvat: obecnymi frazemi ("kultovni klasika", "nezapomenutelny zazitek"),
opakovanim tehoz jinymi slovy, vycty her bez komentare.

POZOR NA FAKTA: piš jen to, cim si jsi jisty. NIKDY si nevymysli cisla prodeju,
procentualni hodnoceni, jmena vyvojaru ani citace recenzi. Kdyz si necim nejsi jisty,
napis to obecneji nebo vynech. Radeji strizlivy text nez vymysleny detail.
Kdyz stavajici text obsahuje neco, cim si nejsi jisty, do nove verze to nepretahuj.

Styl: plynula magazinova reportaz pro herni web, ne encyklopedicke heslo.
Nazvy her, konzoli a studii nechavej v originale, neprekladej je.

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
Vrat kratke potvrzeni s pocty znaku ceskych textu.`

  return agent(prompt, { label: `serie-exp:${pad(i)}`, phase: 'Rozsireni', model: 'sonnet' })
}))

return { batches: batches.length, done: results.filter(Boolean).length }
