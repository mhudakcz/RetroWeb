export const meta = {
  name: 'platform-article-photos',
  description: 'Vloží doprovodné fotky z Wikipedie do článků platforem s CZ popiskami',
  phases: [{ title: 'Vkládání fotek' }],
};

const slugs = (typeof args === 'string' ? JSON.parse(args) : args) || [];

phase('Vkládání fotek');

const PROMPT = (slug) => `Jsi editor retro-herního webu (česky). Vkládáš doprovodné fotky do článku o platformě "${slug}" do magazínového layoutu.

KROK 1 — fotky: otevři soubor \`tools/_article_photos.json\` a najdi klíč "${slug}". Je to pole objektů {file, src_name, desc} — fotky stažené z anglické Wikipedie této platformy (jsou tedy tematicky relevantní). Podle "src_name" (původní název souboru) a "desc" (popis z metadat) poznáš, co fotka zobrazuje.

KROK 2 — článek: přečti \`src/data/platform_articles/${slug}.md\` (Markdown; sekce začínají \`### \`).

ÚKOL:
1. Vyber 2 až 3 NEJLEPŠÍ a nejrůznorodější fotky (např. konzole + ovladač + varianta/reklama/periferie). Vynech ty, u kterých si podle názvu/popisu NEJSI jistý, co zobrazují, jsou redundantní (dvě skoro stejné konzole), nebo zobrazují jen základní desku/čip bez hodnoty pro čtenáře. Klidně použij jen 2. Pokud není vhodná žádná, nevkládej nic a napiš to.
2. Pro každou vybranou fotku napiš krátký český popisek (figcaption), 4–9 slov, věcný, bez fantazírování — drž se toho, co o fotce víš z názvu a popisu (např. „Ovladač NES s křížovým D-padem", „Japonský Famicom z roku 1983").
3. Fotky vlož do .md jako HTML bloky PŘESNĚ v tomto tvaru (každý na samostatném řádku, Markdown je propustí):
<figure class="article-photo"><img src="CESTA_Z_FILE" alt="POPISEK" loading="lazy"><figcaption>POPISEK</figcaption></figure>
4. Umísti každý <figure> TĚSNĚ PŘED některý nadpis sekce \`### \` tak, aby se fotka tematicky vázala k sekci (ovladač/periferie před „Propojení a periferie", varianta před „Modely a revize" apod.), nebo před vhodný odstavec uvnitř sekce. Nedávej dvě fotky vedle sebe; rozprostři je po článku. NEDÁVEJ fotku úplně na začátek (před první odstavec) ani úplně na konec článku.
5. Text článku jinak NEMĚŇ — jen vlož <figure> bloky. Zachovej diakritiku a uvozovky („").
6. Ulož upravený soubor zpět na \`src/data/platform_articles/${slug}.md\`.

Vrať jednu českou větu: kolik fotek jsi vložil a co zobrazují.`;

const results = await parallel(
  slugs.map((slug) => () => agent(PROMPT(slug), { label: slug, phase: 'Vkládání fotek' }))
);

return { platforem: slugs.length, vysledky: results.filter(Boolean) };
