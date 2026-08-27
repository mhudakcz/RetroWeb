export const meta = {
  name: 'studio-articles',
  description: 'Napise CZ clanky o hernich studiich, ktera je jeste nemaji',
  phases: [{ title: 'Studia', detail: 'davka studii na agenta, vystup .md soubory', model: 'sonnet' }],
}

phase('Studia')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(2, '0')

log(`Clanky o studiich: ${batches} davek`)

const jobs = Array.from({ length: batches }, (_, i) => ({ i, in: `${base}/stud_${pad(i)}.json` }))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `Idempotentni uloha: ceske clanky o hernich studiich.

KROK 1 - podklad: Read ${j.in}
Je to JSON pole objektu {slug, name, games}. "games" je vyber titulu daneho studia
z naseho katalogu ve tvaru {name, year, platform} — ber je jako oporu, ne jako
uplny seznam vseho, co studio kdy vydalo.

KROK 2 - kontrola: pro KAZDE studio zkus Read souboru
F:/__VibeCoding2026/RetroWeb/src/data/studio_articles/<slug>.md
Pokud uz existuje a neni prazdny, tohle studio PRESKOC.

KROK 3 - prace: ke kazdemu zbylemu studiu napis clanek v CESTINE a uloz ho
nastrojem Write do F:/__VibeCoding2026/RetroWeb/src/data/studio_articles/<slug>.md

Struktura souboru (presne v tomhle poradi, Markdown):
1. Uvodni odstavec BEZ nadpisu — kdo studio je, cim je pametihodne, jaky ma
   v herni historii vyznam. 500-800 znaku.
2. "## Historie" — jak studio vzniklo, ktere hry ho prosadily, jak se vyvijelo
   napric generacemi, pripadne zmeny vlastnika nebo zanik. 1200-1800 znaku.
3. "## Klicove osobnosti" — zakladatele a lidi, kteri urcovali smer, a cim
   konkretne. 500-900 znaku. Kdyz o lidech kolem studia nic bezpecne nevis,
   nadpis VYNECH cely a nevymysli si jmena.
4. "## Soucasnost" — co studio dela dnes, pripadne cim skoncilo. 500-900 znaku.

CILOVA DELKA celeho souboru 3500-5000 znaku.

POZOR NA FAKTA — tohle je nejdulezitejsi pravidlo:
- Piš jen to, cim si jsi jisty. NIKDY si nevymysli jmena zakladatelu a
  vyvojaru, roky zalozeni, cisla prodeju, procentualni hodnoceni ani citace.
- Kdyz si necim nejsi jisty, napis to obecneji nebo to vynech. Strizlivy text
  je lepsi nez vymysleny detail.
- Nazvy her, konzoli a firem nechavej v originale, neprekladej je.

Styl: plynula magazinova reportaz pro herni web, ne encyklopedicke heslo.
Zadne odrazky v souvislem textu, zadne tabulky.

Vrat kratke potvrzeni se seznamem zapsanych souboru a jejich delkami.`
  return agent(prompt, { label: `studio:${pad(j.i)}`, phase: 'Studia', model: 'sonnet' })
}))

return { batches, done: results.filter(Boolean).length }
