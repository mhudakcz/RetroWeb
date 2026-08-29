export const meta = {
  name: 'magazine',
  description: 'Napise redakcni obsah cisla magazinu: editorial, tema, zebricek, upoutavku',
  phases: [{ title: 'Cisla', detail: 'jedno cislo na agenta', model: 'sonnet' }],
}

phase('Cisla')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(3, '0')

const RULES = `Uloha: napsat redakcni obsah jednoho cisla retro herniho magazinu, CESKY.

Web ma katalog her rozdeleny do "cisel" podle roku vydani — jako kdyby v te dobe
vychazel casopis. Ty pises to, co v takovem casopise stoji kolem recenzi: uvodnik,
hlavni tema a zebricek. Nepises recenze samotne, ty uz na webu jsou.

DULEZITE — PIS Z POHLEDU DOBY. Cislo 1994-2 mluvi o roce 1994 jako o pritomnosti:
"letos", "cerstve", "prave dorazil". Nesmis odkazovat na nic, co se stalo POZDEJI —
zadne "o rok pozdeji vyslo", "dnes uz vime", "zpetne vzato". Ctenar toho cisla je
v roce, o kterem cislo je. Jedina vyjimka je rubrika "chystame", ktera smi upoutat
na obsah PRISTIHO cisla.

Vstup je JSON s poli: id, rok, cislo, platformy (nove stroje toho cisla), hry
(nazev, platforma, zanr, studio, teaser, mustplay) a "dalsi" (obsah pristiho cisla).

Vystup je JSON objekt s temito klici:

"titulek" — kratky poutak na obalku, 3-7 slov, bez uvozovek. Vystihuje, cim je cislo
  zajimave. Priklad: "Rok, kdy dorazily disky".

"editorial" — uvodnik sefredaktora, 2 odstavce oddelene \\n\\n, dohromady 700-1100
  znaku. Vychazi z toho, CO v cisle skutecne je. Kdyz cislo uvadi nove platformy,
  je to hlavni udalost. Ma to byt osobni a mit nazor, ne vycet.

"tema" — objekt {"nadpis": "...", "text": "..."}. Hlavni tema cisla: neco, co
  spojuje vic her z tohoto cisla — zanr, ktery zrovna vybuchl, technologie, studio,
  trend. Nadpis 2-6 slov. Text 900-1400 znaku, 2-3 odstavce oddelene \\n\\n.
  Vybirej tema, ktere v datech cisla OPRAVDU je; nevymysli si trend, na ktery
  v seznamu nejsou hry.

"zebricek" — pole 5 objektu {"slug": "...", "text": "..."}, serazene od nejlepsi.
  Slug MUSI byt presne jeden ze slugu ve vstupnim poli "hry" — nic jineho.
  Text je 100-220 znaku, jedna dve vety: proc si tenhle titul zaslouzi mistp.
  Vybirej podle skutecne kvality a vyznamu, ne podle poradi ve vstupu.

"chystame" — upoutavka na dalsi cislo, 200-400 znaku, podle pole "dalsi".
  Kdyz je "dalsi" null, napis misto toho kratke rozlouceni s rocnikem.

POZOR NA FAKTA: piš jen to, cim si jsi jisty. NIKDY si nevymysli jmena vyvojaru,
cisla prodeju, hodnoceni ani citace. Nazvy her, konzoli a studii nechavej v originale.
Kdyz si nejsi jisty datem nebo detailem, napis to obecneji.

Uloz nastrojem Write VALIDNI JSON. Klic "id" ve vystupu musi byt stejny jako ve vstupu.
Uvozovky uvnitr textu escapuj jako \\". Zadny text mimo JSON.
Vrat kratke potvrzeni s id cisla a nazvem tematu.`

const jobs = Array.from({ length: batches }, (_, i) => ({
  i, in: `${base}/mag_${pad(i)}.json`, out: `${base}/mag_${pad(i)}_out.json`,
}))

log(`Magazin: ${jobs.length} cisel`)

const results = await parallel(jobs.map((j) => () => {
  const prompt = `${RULES}

--- toto cislo ---
Vstupni soubor:  ${j.in}
Vystupni soubor: ${j.out}
Nejdriv zkus Read vystupniho souboru — kdyz uz existuje a je validni JSON se vsemi
klici, vrat jen: SKIP`
  return agent(prompt, { label: `cislo:${pad(j.i)}`, phase: 'Cisla', model: 'sonnet' })
}))

return { batches: jobs.length, done: results.filter(Boolean).length }
