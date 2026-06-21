Existuje celá kategorie herních platforem, které nikdy nedostaly plastovou krabičku, čip ani konektor do televize — a přesto se chovají, jako by je měly. **TIC-80** je jednou z nich. Jde o takzvanou **fantasy konzoli**: čistě softwarové prostředí, které si dobrovolně nasadilo přísná omezení 8bitové éry (málo barev, nízké rozlišení, skromnou paměť), aby v tvůrci probudilo stejný pocit, jaký kdysi měli programátoři na strojích jako ZX Spectrum, Commodore 64 nebo NES. Není to emulace žádného existujícího počítače — je to vymyšlený stroj, který by klidně mohl pocházet z roku 1985, ale narodil se až v roce 2017.

Autorem TIC-80 je **Vadim Grigoruk** (vystupující pod značkou Nesbox) a od počátku ho pojal jako **open-source a zdarma šiřitelný** projekt. Tím se vymezil vůči svému slavnějšímu vzoru, komerční konzoli **PICO-8** od studia Lexaloffle (2015). Zatímco PICO-8 sází na uzavřenost a vyladěnou jednoduchost, TIC-80 nabízí o něco velkorysejší rozlišení, otevřený kód a volbu z více programovacích jazyků. Filozofie je ale stejná: omezení je tvůrčí palivo. Kolem obou konzolí se rozrostly komunity, které vyrábějí stovky až tisíce malých, chytrých her — plošinovky, puzzle, střílečky i miniaturní metroidvanie. Je to „nové retro" v nejčistší podobě: hry dělané dnes, ale s duší osmdesátek.

### Technika: grafika a zvuk

Srdcem TIC-80 je obrazovka o rozlišení **240×136 pixelů** a paleta **16 barev**. To je zhruba dvojnásobek plochy oproti PICO-8 (128×128) a právě tahle drobná velkorysost dává tvůrcům o něco víc prostoru pro detail a text. Paleta je editovatelná — patnáct barev plus jedna průhledná, takže si autor může výchozí sadu přebarvit podle vkusu hry. Grafika se skládá z **8×8 pixelových dlaždic a spritů**; konzole má banky pro sprity i pro mapu, po kterých se vykresluje pozadí a scrolling.

Zvuk řeší **čtyři kanály** s programovatelnými vlnami. TIC-80 nabízí editor wavetable, takže si tvůrce může nakreslit vlastní tvar vlny, k tomu sekvencer pro skladby a sadu efektů. Výsledek zní typicky „chiptune" — bzučivé, syrové, ale překvapivě muzikální. Celá hra včetně kódu, grafiky, map a hudby se ukládá do jediné **cartridge** (soubor `.tic`), což krásně odkazuje na dobové herní moduly, jen v podobě jednoho malého souboru.

### Programování a nástroje

Tady TIC-80 vyniká nejvíc. Je to v podstatě **celé vývojové prostředí v jednom okně**: přímo v konzoli najdeš editor kódu, editor spritů, editor map, zvukový editor i hudební sekvencer. Nemusíš instalovat nic dalšího — otevřeš konzoli a tvoříš.

Velkou předností oproti PICO-8 je **podpora více programovacích jazyků**. Vedle výchozího **Lua** umí TIC-80 i **MoonScript, JavaScript, Wren, Fennel, Squirrel** a další (sada se postupem verzí rozšiřovala). Hru spustíš příkazem `run`, hotové cartridge z internetové databáze procházíš a hraješ přímo v konzoli přes **`surf`** — listuješ nabídkou jako v jukeboxu a tituly rovnou spouštíš. Hry lze také exportovat do samostatných spustitelných souborů nebo do HTML, takže běží i v prohlížeči.

### Varianty a verze

Protože TIC-80 není hardware, „modely a revize" tu nahrazují **verze programu** a varianty distribuce. Základní edice je zdarma a open-source (kód je veřejně dostupný). Autor zároveň nabízí placenou **PRO** verzi, která přidává hlavně pohodlí pro vývojáře — třeba ukládání cartridge v textové podobě vhodné pro verzování v Gitu nebo víc paměťových bank pro větší projekty. Sám engine je **multiplatformní**: běží na Windows, macOS, Linuxu, na webu přes prohlížeč a díky otevřenému kódu byl portován i na řadu dalších zařízení.

### Klony a varianty

Mluvit o „klonech" u fantasy konzole je trochu paradox — TIC-80 sám je v jistém smyslu otevřenou odpovědí na PICO-8. Celý žánr fantasy konzolí je dnes pestrý: vedle PICO-8 a TIC-80 existují třeba **PixelVision8**, **WASM-4** nebo **LIKO-12**, přičemž LIKO-12 je přímo navržený jako otevřená obdoba PICO-8. Každá si volí trochu jiná omezení a jiný „dobový charakter".

Pro hráče na **Anbernicích** a podobných handheldech je důležité, že TIC-80 díky open-source kódu běží **nativně** přímo na zařízení (na čipech jako H700 sice plynule, ale u náročnějších cartridge se na slabších kartách může zadrhávat). PICO-8 se na stejných strojích typicky spouští přes samostatný core. Pro retrohráče to znamená přístup k obrovské zásobě malých, často zcela zdarma dostupných her mimo dobové klasiky.

### Dnešní scéna

TIC-80 je svým způsobem „věčně živá" platforma — je to současně nástroj i herna. Komunita kolem něj stále vydává nové cartridge, pořádají se game jamy a webová databáze her roste. Mezi tituly, na které lze narazit, patří třeba **Bombic**, **ESCAPE**, **Sumico**, **RobomanIA**, **Bunny Maze**, **Knight's Quest**, **Tic Tank** nebo recesistická **ASCII Game**. Žádný z nich nestál ani korunu na licencích a většinu si zahraješ v prohlížeči během pár vteřin. Pokud tě láká retro pocit, ale nechceš jen dokola hrát čtyřicet let staré hity, je TIC-80 ideální brána do světa, kde se osmdesátá léta vyrábějí znovu — dnes, s láskou a otevřeným kódem.
