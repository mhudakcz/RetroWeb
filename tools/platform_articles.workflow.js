export const meta = {
  name: 'platform-articles',
  description: 'Napise dlouhe CZ clanky o platformach do src/data/platform_articles/<slug>.md',
  phases: [{ title: 'Articles', detail: 'jeden agent na platformu, predloha = existujici clanek' }],
}

phase('Articles')
const { platforms } = typeof args === 'string' ? JSON.parse(args) : args
const DIR = 'F:/__VibeCoding2026/RetroWeb/src/data/platform_articles'

log(`Clanky o platformach: ${platforms.length}`)

const results = await parallel(platforms.map((p) => () => {
  const prompt = `Idempotentni uloha: cesky clanek o herni platforme.

KROK 1 - kontrola: Zkus nastrojem Read otevrit ${DIR}/${p.slug}.md
Pokud EXISTUJE a ma aspon 4000 znaku, jsi hotov — nic nezapisuj a vrat pouze: SKIP

KROK 2 - prace. Nejdriv si precti predlohu: ${DIR}/${p.ref}.md
Tvuj text musi kopirovat jeji styl, strukturu i delku.

Napis clanek o platforme **${p.name}** do ${DIR}/${p.slug}.md

POZADAVKY:
- Delka 5000-6000 znaku. Cestina, plynula magazinova reportaz, Markdown.
- Struktura: 2-3 odstavce uvodu BEZ nadpisu, pak sekce s ### nadpisy ve stejnem duchu
  jako predloha (typicky: Technika: grafika a zvuk / Propojeni a periferie /
  Modely a revize / Klony a varianty / Dnesni scena). Presne zneni nadpisu prevezmi
  z predlohy vcetne toho, jestli maji diakritiku.
- NEVKLADEJ zadne <figure class="article-photo"> bloky.
- Klicove pojmy **tucne**. Nazvy her, konzoli, cipu a studii nechavej v originale.

OPORNE BODY (piš jen to, cim si jsi jisty; nic si nevymyslej — zadna vymyslena
cisla prodeju, jmena vyvojaru ani citace):
${p.brief}

Rozsir je o dalsi fakta, ktera o platforme bezpecne vis: typicke hry, dobovy kontext,
konkurenci, cim si ji lide pamatuji a jak se k ni da dostat dnes (emulace, Batocera,
legalni zdroje her). Kdyz si necim nejsi jisty, napis to obecneji nebo vynech.

Uloz nastrojem Write. Vrat kratke potvrzeni s poctem znaku.`
  return agent(prompt, { label: `clanek:${p.slug}`, phase: 'Articles' })
}))

return { platforms: platforms.length, done: results.filter(Boolean).length }
