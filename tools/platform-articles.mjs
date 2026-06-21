export const meta = {
  name: 'platform-articles',
  description: 'Dlouhe CZ clanky o platformach (~2 normostrany): technika, propojeni, revize, klony',
  phases: [{ title: 'Platformy' }],
}

let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const slugs = A.slugs || []
const inDir = A.inDir
const outDir = A.outDir
log('platforem=' + slugs.length)
if (!slugs.length || !inDir || !outDir) throw new Error('Chybi args: ' + JSON.stringify(args).slice(0, 200))

const STYLE = [
  'Jsi zkuseny redaktor herniho magazinu se znalosti retro hardwaru. Pises CESKY (se spravnou diakritikou; zadani je bez diakritiky jen kvuli kodovani).',
  'Napis pro zadanou platformu dlouhy, ctivy a FAKTICKY PRESNY clanek (cca 2 normostrany, tj. 600 az 800 slov).',
  'Struktura: kratky pritazlivy uvod (historie a vyznam), pak nekolik sekci oddelenych nadpisem "### Nazev sekce":',
  '  - "### Technika: grafika a zvuk" — rozliseni, barvy, sprity/scrolling, zvukovy cip a kanaly, cim to vynikalo nebo zaostavalo.',
  '  - "### Propojeni a periferie" — link kabel, multiplayer, myc/light gun/modem/pametove karty, TV/AV vystup atd. (jen co realne plati).',
  '  - "### Modely a revize" — hardwarove revize a varianty (napr. modely konzole, redesigny).',
  '  - "### Klony a varianty" — vyznamne klony; a kde to dava smysl, zminni i CESKOU/CESKOSLOVENSKOU stopu (napr. Didaktik = cs. klon ZX Spectra, famiclony/Pegasus u NES ve vychodnim bloku). NEVYMYSLEJ si; jen overitelne.',
  '  - "### Dnesni scena" — strucne emulace a homebrew.',
  'Sekce vol podle toho, co pro danou platformu dava smysl (u fantasy konzole napr. revize/klony vynech).',
  'PRESNOST: nevymyslej si cisla ani fakta. Pole "history" ber jako overeny zaklad a rozsiruj ho svou znalosti. Pole "sampleGames" jsou ukazky her na platforme.',
  'FORMAT: Markdown. Sekce pres "### ", duraz pres **tucne**. Zadny H1/H2 (ty doplni web). Odstavce oddeluj prazdnym radkem.',
].join('\n')

const results = await parallel(slugs.map((slug) => () => {
  const inFile = inDir + '/' + slug + '.json'
  const outFile = outDir + '/' + slug + '.md'
  const task = [
    STYLE,
    '',
    'UKOL:',
    '1) Precti vstup (JSON s metadaty platformy): ' + inFile,
    '   Pole: slug, name, maker, year, type, history, sampleGames.',
    '2) Napis dlouhy clanek dle stylu vyse (cesky, s diakritikou).',
    '3) Uloz CISTY MARKDOWN (ne JSON) do souboru: ' + outFile + ' (UTF-8).',
    '4) Vrat jen "OK ' + slug + '".',
  ].join('\n')
  return agent(task, { label: slug, phase: 'Platformy' })
}))

return { platforms: slugs.length, done: results.filter(Boolean).length }
