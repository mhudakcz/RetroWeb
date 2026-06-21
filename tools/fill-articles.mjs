export const meta = {
  name: 'fill-articles',
  description: 'Dogeneruje CZ magazinove clanky ke hram bez clanku',
  phases: [{ title: 'Clanky' }],
}

let A = args
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
A = A || {}
const chunkDir = A.chunkDir
const chunkCount = A.chunkCount
const outDir = A.outDir
const prefix = A.prefix || 'fill'
log('chunkCount=' + chunkCount + ', dir=' + chunkDir)
if (!chunkCount || !chunkDir || !outDir) {
  throw new Error('Chybi args: ' + JSON.stringify(args).slice(0, 200))
}

const STYLE = [
  'Jsi zkuseny redaktor popularniho herniho magazinu (styl Score / Level / IGN retro). Pises CESKY.',
  'Pro KAZDOU hru v zadanem souboru napis poutavy clanek:',
  '- 400 az 550 slov, 4 az 6 odstavcu. Silny uvodni hook, ctive a se stavou, ale FAKTICKY PRESNE.',
  '- Zapracuj: herni mechaniky a cim vynika; vyvojovy kontext (studio, doba); kulturni vyznam; a pokud to SKUTECNE a overitelne znas: oceneni, prodeje, zebricky, trivia, porty/pokracovani.',
  '- PRESNOST: nevymyslej si fakta. U mene znamych nebo homebrew titulu (vc. PICO-8/TIC-80 a Game & Watch), kde nemas overena data, je NEUVADEJ; pis o zanru, hernich pocitech, kontextu platformy a tom, co je overitelne. Radsi obecneji nez nepravdive. Pole "teaser" a "detail" ber jako overena fakta, "platform" je platforma.',
  '- Pis ale CESKY a se spravnou diakritikou (tohle zadani je bez diakritiky jen kvuli kodovani).',
  '- Zakonci samostatnym radkem ve tvaru: **Proc hrat:** <jedna az dve vety>.',
  '- Markdown (**tucne**), ZADNE nadpisy, ZADNA zanrova hlavicka. Odstavce oddeluj prazdnym radkem.',
].join('\n')

const idxs = Array.from({ length: chunkCount }, (_, i) => i)

const results = await parallel(idxs.map((i) => () => {
  const num = String(i).padStart(3, '0')
  const inFile = chunkDir + '/chunk_' + num + '.json'
  const outFile = outDir + '/' + prefix + '-' + num + '.json'
  const task = [
    STYLE,
    '',
    'UKOL:',
    '1) Precti soubor (JSON pole her, max 8): ' + inFile,
    '2) Zpracuj VSECHNY hry. Pole: slug, name, platform, genre, year, studio, teaser, detail.',
    '3) Pro kazdou napis clanek dle stylu vyse (cesky, s diakritikou).',
    '4) Uloz jako VALIDNI JSON do: ' + outFile,
    '   - Objekt kde klic = PRESNE hodnota "slug" a hodnota = clanek jako jeden string. Zahrn VSECHNY hry ze vstupu.',
    '   - Odstavce v clanku oddeluj sekvenci backslash-n backslash-n. Escapuj uvozovky a lomitka, at je JSON validni. UTF-8.',
    '5) Vrat jen "OK <pocet>".',
  ].join('\n')
  return agent(task, { label: 'chunk ' + num, phase: 'Clanky' })
}))

return { chunkCount, done: results.filter(Boolean).length }
