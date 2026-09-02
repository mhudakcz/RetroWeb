export const meta = {
  name: 'picks',
  description: 'Vybere ke kazde platforme hry, kterymi ma ctenar zacit',
  phases: [{ title: 'Vyber', detail: 'jedna platforma na agenta', model: 'sonnet' }],
}

phase('Vyber')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')

const RULES = `Uloha: vybrat ke konkretni herni platforme hry, kterymi ma ctenar zacit.

Ctenar prijde na stranku platformy, vidi sto her v abecednim seznamu a nevi,
cim zacit. Tenhle vyber je odpoved — nekolik titulu, ktere na te platforme
nema minout, s jednou vetou, PROC prave ony.

Vstup je JSON: {slug, platform, rok, pocet, hry}. "hry" je cely katalog dane
platformy — objekty {slug, name, year, genre, mustplay, teaser}.

PRAVIDLA VYBERU:
- Vyber presne "pocet" her, serazene od nejdulezitejsi.
- Vybirej VYHRADNE ze slugu ve vstupu. Nic jineho neuvadej — hra, ktera
  v katalogu neni, by vedla na neexistujici stranku.
- Priznak "mustplay" je voditko, ne pravidlo; na nekterych platformach neni
  rozdany vubec, jinde je u vic her, nez kolik jich mas vybrat.
- Miř na SIRKU, ne na jeden zanr: platforma se ma ukazat z vic stran. Kdyz na
  ni vysla legendarni plosinovka, RPG i zavodni hra, at jsou ve vyberu vsechny.
- ZANROVA PESTROST je pozadavek, ne doporuceni: pri osmi a vic titulech musi byt
  zastoupeno aspon PET ruznych zanru. Sedm plosinovek za sebou je spatny vyber,
  i kdyby to bylo sedm nejlepsich her platformy.
- Poradi michej tak, aby hned za sebou nesly dve hry tehoz zanru.
- Prednost maji tituly, ktere jsou pro platformu urcujici — bud protoze se na
  ni proslavily, nebo protoze ukazuji, co ten stroj umel.
- U kapesnich konzoli a domacich pocitacu ber ohled i na to, co se na nich
  hraje dobre dnes.

VETA "why" ke kazde hre:
- DELKA 40-220 znaku, jedna veta.
- Rekni, PROC prave tahle hra na teto platforme. Ne shrnuti deje.
- Neopakuj doslova teaser, ktery uz ve vstupu je.
- NEZACINEJ nazvem hry — ten se vypise vedle.
- POZOR NA FAKTA: nevymyslej si jmena vyvojaru, cisla prodeju ani hodnoceni.

Vystup uloz nastrojem Write jako VALIDNI JSON:
{"slug": "<slug platformy ze vstupu>", "vyber": [{"slug": "...", "why": "..."}]}
Zadny text mimo JSON. Vrat kratke potvrzeni s nazvem platformy a poctem her.`

const jobs = Array.from({ length: batches }, (_, i) => ({
  i, in: `${base}/picks_${pad(i)}.json`, out: `${base}/picks_${pad(i)}_out.json`,
}))

log(`Vyber her: ${jobs.length} platforem`)

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- tato platforma ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON
s neprazdnym polem "vyber", vrat jen: SKIP`
  return agent(prompt, { label: `vyber:${pad(j.i)}`, phase: 'Vyber', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
