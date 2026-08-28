export const meta = {
  name: 'platform-ports',
  description: 'Doplni hry na dalsi platformy, kde take vysly',
  phases: [{ title: 'Porty', detail: 'davka titulu na agenta, vystup vcetne cilove platformy', model: 'sonnet' }],
}

phase('Porty')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(2, '0')

log(`Doplneni portu: ${batches} davek`)

const SLUGS = 'pc-modern, pc-9x, pc-dos, ps2, ps3, ps4, ps5, playstation, xbox, xbox-360, xbox-one, xbox-series, switch, gamecube, wii, wii-u, nds, psp, ps-vita, dreamcast, saturn, n64, snes, mega-drive'

const jobs = Array.from({ length: batches }, (_, i) => ({
  i,
  in: `${base}/ports_${pad(i)}.json`,
  out: `${base}/ports_${pad(i)}_out.json`,
}))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `Idempotentni uloha: doplneni her na platformy, kde take vysly.

KROK 1 - kontrola: Zkus nastrojem Read otevrit ${j.out}
Pokud EXISTUJE a je to VALIDNI JSON pole, jsi hotov — nic nezapisuj a vrat pouze: SKIP

KROK 2 - podklad: Read ${j.in}
Je to JSON pole objektu {name, year, have}. "have" jsou platformy, na kterych titul
v katalogu UZ JE.

KROK 3 - prace. U kazdeho titulu zvaz, na kterych DALSICH platformach skutecne vysel,
a pro kazdou takovou vydanou verzi vrat jeden zaznam.

TOHLE JE NEJDULEZITEJSI PRAVIDLO: pridavej jen vydani, kterym si jsi JISTY.
Rada her je zamerne exkluzivni — Wii Sports vyslo jen na Wii, Resistance jen na
PlayStationu, Blue Dragon jen na Xboxu 360. U takovych titulu nevrat NIC.
Vymyslený port je horsi nez zadny, protoze na webu bude stat, ze hra na dane
konzoli vysla, i kdyz nevysla. Kdyz si nejsi jisty, titul VYNECH.

Nepridavej:
- pozdejsi remastery a remaky pod jinym nazvem (ty jsou samostatny titul)
- verze pro cloudove sluzby a zpetnou kompatibilitu
- platformu, ktera uz je v "have"

Pro KAZDE doplnene vydani vrat objekt:
{
 "platform": "<slug cilove platformy>",
 "name": "<presny nazev, jak vysel na teto platforme>",
 "genre": "zanr cesky nebo bezne uzivanym anglickym terminem",
 "length": "S | M | L | XL",
 "year": "rok vydani NA TETO PLATFORME jako retezec",
 "studio": "vyvojarske studio",
 "flags": [],
 "article": "cesky clanek, 1800-2100 znaku, 2-3 odstavce oddelene \\n\\n"
}

Povolene slugy platforem: ${SLUGS}

Clanek pis o hre jako takove, ale VZDY zminuj, cim se prave tato verze lisila —
vykon, ovladani, obsah navic nebo naopak chybejici, doba vydani oproti ostatnim
verzim. Kdyz se verze prakticky nelisila, napis to primo; to je taky informace.

POZOR NA FAKTA: nevymyslej si jmena vyvojaru, cisla prodeju ani hodnoceni.

Uloz nastrojem Write do ${j.out} VALIDNI JSON POLE techto objektu. Kdyz nemas
co doplnit, uloz prazdne pole []. Uvozovky uvnitr textu escapuj jako \\".
Vrat kratke potvrzeni s poctem doplnenych vydani.`
  return agent(prompt, { label: `porty:${pad(j.i)}`, phase: 'Porty', model: 'sonnet' })
}))

return { batches, done: results.filter(Boolean).length }
