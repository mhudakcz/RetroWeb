Zlom mezi „starým" a „moderním" PC nemá jediné datum, ale má jasné znaky. Někdy kolem roku 2001 přestalo být herní PC krabicí, do níž se cpe co nejrychlejší procesor, a stalo se strojem, kde hlavní práci odvádí **programovatelná grafická karta**. Krátce nato se přidala druhá revoluce: v roce 2003 uvedlo AMD procesor **Athlon 64** a s ním architekturu **x86-64**, tedy 64bitové rozšíření, které — na rozdíl od exotických slepých uliček — zůstalo plně zpětně kompatibilní se vším, co do té doby vzniklo. Intel ji po počátečním odporu převzal také a x86-64 se stalo společným jazykem celého odvětví, včetně herních konzolí.

Třetí pilíř éry přišel s **vícejádrovými procesory**. Frekvence narazily na fyzikální strop a místo dalších gigahertzů začaly přibývat jádra, což donutilo herní studia přepsat způsob, jakým své enginy staví. Od poloviny dekády tak vývoj her přestal být otázkou jediné rychlé smyčky a stal se disciplínou paralelního programování — s odděleným vláknem pro fyziku, zvuk, streamování dat i vykreslování.

A nad tím vším se odehrála změna, která hráče zasáhla víc než jakýkoli křemík: **digitální distribuce**. Krabice z regálu vystřídal účet, knihovna a stahování na pozadí. PC se z platformy, kterou konzoloví hráči v půlce nultých let odepisovali, stalo tou nejotevřenější a nejrozsáhlejší herní platformou vůbec.

### Technika: grafika a zvuk

Klíčovým okamžikem byly **programovatelné shadery**. Do té doby grafické karty uměly jen pevně danou sadu operací; s **DirectX 8** a kartou **GeForce 3** (2001) mohli vývojáři poprvé psát vlastní krátké programy běžící přímo na GPU pro každý vrchol a každý pixel. **DirectX 9** a **ATI Radeon 9700** (2002) posunuly hranici dál a výsledek byl vidět na první pohled: skutečné odlesky na mokrém asfaltu, vlnící se voda, měkké stíny, kůže a látky, které vypadaly jako kůže a látky. Hry jako Half-Life 2 nebo Far Cry ukázaly, co to znamená v praxi.

Další krok přinesly **unifikované shadery** — namísto oddělených jednotek pro vrcholy a pixely nastoupila univerzální pole výpočetních jader, která se dala využít i na obecné výpočty. Na to navázaly **DirectX 11** s tesselací a výpočetními shadery, později **DirectX 12** a otevřený **Vulkan**, jež daly vývojářům přístup blíž k hardwaru a snížily režii ovladače.

Souběžně rostla i „hrubá" čísla. Od rozlišení 1024×768 se hraní posunulo přes 1080p a 1440p ke **4K**, obnovovací frekvence z 60 Hz na 144 Hz i výš, **antialiasing** vyhladil zubaté hrany a **HDR** rozšířil rozsah jasu a barev. Poslední velkou kapitolou je **ray tracing** — výpočet odrazů, stínů a osvětlení sledováním paprsků, tedy postupem, jakým se dřív renderoval film přes noc. Protože je stále náročný, doprovázejí ho **upscalovací techniky** jako **DLSS** od Nvidie a **FSR** od AMD, které obraz počítají v nižším rozlišení a dopočítávají ho do plné velikosti.

### Propojeni a periferie

Základem zůstala **klávesnice a myš**, dvojice, kterou žádná konzole nikdy nepřekonala v přesnosti míření a v počtu okamžitě dostupných příkazů. Vedle ní ale PC získalo plnou podporu **gamepadů**: ovladač Xboxu se stal de facto standardem, hry ho poznají samy a zobrazují jeho ikony, takže plošinovky a závody se hrají stejně pohodlně jako na konzoli.

Přibyly i periferie, které konzole nemají — **VR headsety**, vysokofrekvenční monitory, volanty i páky pro simulátory. Na straně paměti se prostřídaly generace **DDR** až po DDR5, ale největší praktický rozdíl udělalo úložiště: přechod z pevných disků na **SSD** a dál na **NVMe** disky připojené přes PCI Express zkrátil načítací obrazovky z desítek sekund na jednotky a umožnil hrám streamovat obrovské otevřené světy za běhu.

### Digitální distribuce a služby

**Steam** spustil Valve v roce **2003** a hráči ho zpočátku upřímně nenáviděli — hlavně proto, že bez něj v roce 2004 nešlo spustit Half-Life 2, tehdy zcela nevídaná podmínka. Během několika let se ale z nutného zla stal nejpohodlnější způsob, jak hry kupovat, aktualizovat a mít je navždy dostupné. Následovaly **GOG.com** se hrami bez ochran a s péčí o staré tituly, **Epic Games Store** i předplatné **Game Pass**.

Změnil se tím celý životní cyklus hry. Skončily krabice i představa, že hra je po vylisování hotová — nastoupilo pravidelné **patchování**, dodatečný obsah, **Steam Workshop** pro snadnou distribuci modifikací a **předběžný přístup**, kdy hráči kupují titul rozpracovaný a sledují, jak roste. Pro malá studia to byl zásadní obrat: cesta na trh přestala vést přes vydavatele a distributora.

### Modding, indie a otevřenost

Právě otevřenost je vlastnost, kterou PC nikdo nevzal. **Modding** se z okrajové zábavy stal fenoménem — **Skyrim** má po letech tisíce modifikací měnících grafiku, mechaniky i celé nové kraje, **Minecraft** vybudoval kolem úprav vlastní kulturu a nejedna dnešní samostatná hra vznikla původně jako mod cizího titulu.

Souběžně vyrostla **indie scéna**. Digitální distribuce jí dala pult a nástroje jako **Unity** nebo open source **Godot** výrobu; hry, které by v éře krabic neprošly schvalováním, si najednou našly statisíce hráčů. A do třetice je PC domovem **emulace** — právě tady vznikají a běží emulátory konzolí od osmibitů po nedávné generace.

### Dnesni scena

Poslední roky přinesly něco, co by na začátku éry znělo jako protimluv: **přenosné herní PC**. **Steam Deck** od Valve a stroje jako **ROG Ally** vypadají jako handheldy, ale uvnitř je běžné x86-64 PC. Deck navíc běží na Linuxu a hry pro Windows spouští přes kompatibilní vrstvu **Proton**, která fungovala natolik dobře, že z knihovny nakoupených her udělala prakticky přenositelný majetek napříč systémy i zařízeními.

Tím se kruh uzavírá. PC dnes není jen platforma s nejnovějšími hrami — je to jediné místo, kde se dá naráz hrát prakticky celá historie hraní: dnešní blockbustery v ray tracingu, indie klenoty, staré klasiky z GOG.com i emulované tituly z konzolí všech generací. Moderní PC je zároveň nejvýkonnějším herním strojem současnosti a nejlepším muzeem, jaké hraní má.
