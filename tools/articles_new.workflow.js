export const meta = {
  name: 'articles-new',
  description: 'Napise plne CZ clanky ke hram, ktere zadny clanek nemaji',
  phases: [{ title: 'Clanky', detail: 'davka her na agenta, vystup {slug: clanek}', model: 'sonnet' }],
}

phase('Clanky')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')

const RULES = `Uloha: napsat plny cesky clanek ke kazde hre ze vstupni davky.

Vstup je JSON pole objektu {slug, name, platform, year, studio, genre, delka, teaser}.
"teaser" je uz hotova uvodni veta — clanek s ni nesmi byt v rozporu, ale neopakuj ji doslova.

FORMAT KAZDEHO CLANKU:
- DELKA 1500-2000 znaku vcetne mezer. Kratsi nez 1300 je chyba.
- 3 odstavce oddelene prazdnym radkem, plynula ceska magazinova reportaz.
- Zadne nadpisy, zadne odrazky. Markdown jen pro **tucne** zvyrazneni nazvu hry v prvni vete.
- Na uplny konec pridej samostatny odstavec zacinajici presne "**Proč hrát:** " a za nim
  jednou vetou (90-260 znaku) rekni, KOMU a PROC se titul vyplati. Neni to shrnuti deje.
  Kdyz ma hra vyhradu (dnes uz nedostupna, agresivni monetizace, zestarla), zminy ji —
  doporuceni s vyhradou je uzitecnejsi nez chvalozpev.

O CEM PSAT (vyber, co k dane hre skutecne sedi):
- jak se hra hraje a jak se ovlada; u mobilnich her je dotykove ovladani podstatne
- proc vznikla a co znamenala v dobe vydani
- atmosfera, vytvarny styl, hudba
- vliv na zanr, pokracovani, dobove prijeti

U MOBILNICH HER navic ber v uvahu tri veci, ktere jinde neplati:
- ZPUSOB PLACENI je soucast hry, ne detail. Placena hra, free-to-play s reklamami,
  gacha, predplatne (Apple Arcade, Netflix Games) — napis to rovnou a bez prikraslovani.
  U gachy a agresivniho free-to-play to pojmenuj poctive, ale bez kazani.
- DOSTUPNOST. Rada mobilnich her uz ve storu NENI (Flappy Bird, Infinity Blade,
  Dragalia Lost a dalsi stazene tituly). Kdyz si jsty, ze hra skoncila, napis to.
- PORT vs. PUVODNI HRA. U portu velkych her rekni, jak se prevod povedl a jestli
  se to na dotyku da hrat; u puvodnich mobilnich her naopak, cim byly nove.

POZOR NA FAKTA: piš jen to, cim si jsi jisty. Radeji obecnejsi formulace nez vymysleny
detail. NIKDY si nevymysli jmena vyvojaru a skladatelu, cisla stazeni ani hodnoceni
v procentech. Nazvy her, konzoli a studii nechavej v originale, neprekladej je.

Vystup uloz nastrojem Write jako VALIDNI JSON objekt {"<slug>": "<clanek>", ...}
se VSEMI slugy ze vstupu. Odstavce oddeluj jako \\n\\n, uvozovky uvnitr escapuj jako \\".
Zadny text mimo JSON. Vrat kratke potvrzeni s poctem her a prumernou delkou.`

const jobs = Array.from({ length: batches }, (_, i) => ({
  i, in: `${base}/art_${pad(i)}.json`, out: `${base}/art_${pad(i)}_out.json`,
}))

log(`Clanky ke hram bez clanku: ${jobs.length} davek`)

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato davka ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON se vsemi
slugy ze vstupu, vrat jen: SKIP`
  return agent(prompt, { label: `clanek:${pad(j.i)}`, phase: 'Clanky', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
