PICO-8 je v celém průvodci retro hardwarem tak trochu vetřelec — protože **žádný hardware není**. Je to takzvaná **fantasy konzole**: softwarové prostředí od novozélandského studia **Lexaloffle** (autor **Joseph White**, alias zep), které vyšlo v roce 2015. Místo aby simulovalo nějaký konkrétní dobový stroj, vymyslelo si vlastní, schválně přísná pravidla — málo barev, nízké rozlišení, drobounkou paměť — a tím napodobilo pocit programování a hraní na osmibitech 80. let. Jenže s moderním komfortem: editor kódu, grafiky, zvuku i map máte všechno v jednom okně a ke spuštění hry stačí napsat `run`.

Kouzlo spočívá právě v těch omezeních. Když nemůžete mít všechno, musíte být vynalézaví — a protože je tak snadné začít, vznikla kolem PICO-8 obrovská a aktivní komunita. Nejslavnější příběh je **Celeste**: vznikla jako čtyřdenní projekt na herním jamu v PICO-8 (pod názvem *Celeste Classic*) a později z ní byl jeden z nejuznávanějších moderních plošinovkových hitů. Původní PICO-8 verze je dodnes hratelná zdarma. To dokonale vystihuje, čím PICO-8 je: nostalgie po éře, kterou si mladší tvůrci často ani nezažili, přetavená v kreativní hřiště.

### Technika: grafika a zvuk

Specifikace si Lexaloffle stanovil pevně a programy je nemohou obejít. Obraz má rozlišení **128×128 pixelů** a pevnou **16barevnou paletu**. Ta paleta je ikonická — odstíny jako tmavě modrá, lososová, žlutozelená či světle béžová dávají hrám okamžitě rozpoznatelný „pico" vzhled. Novější verze přidaly takzvanou skrytou paletu dalších 16 barev, ze kterých lze základní šestnáctku přemapovat, takže tvůrci mají k dispozici širší rejstřík, byť stále jen 16 barev naráz.

Grafika stojí na **spritech 8×8 pixelů**: v sprite-sheetu jich je 256 (plus dalších 128 sdílených s mapou). Mapa pro úrovně má rozměr 128×32 dlaždic. Vykreslování běží na **30 nebo 60 snímcích za sekundu** podle toho, jestli použijete funkci `_update()` nebo `_update60()`.

Zvuk obstarává **4kanálový syntezátor**. Tvůrce má k dispozici 64 zvukových patternů a může skládat melodie i efekty pomocí několika základních tvarů vlny (čtvercová, pila, trojúhelník, šum a další), což zvukově odpovídá éře čipové hudby. Celý program — kód v jazyce **Lua**, grafika, mapa i hudba — se musí vejít do limitů „cartridge": kolem **32 kB** komprimovaných dat na kód a pevně dané sloty na grafiku a zvuk. Samotná cartridge je technická lahůdka: je to obyčejný **soubor PNG** o rozměru 160×205 pixelů, do jehož dat je hra ukrytá. Obrázek tak slouží zároveň jako ikona i jako nosič hry.

### Propojeni a periferie

Protože jde o software, „periferie" jsou ovládací schémata, ne fyzické krabičky. PICO-8 počítá se **dvěma virtuálními gamepady**, každý se šesti tlačítky: čtyřsměrový kříž plus dvě akční tlačítka (interně značená O a X). To je úmyslně minimalistické — mapuje se to snadno na klávesnici, herní pad i tlačítka retro handheldů. Některé hry využívají i **myš a klávesnici**, pokud to autor v cartridge povolí.

Zajímavostí je takzvaný **splore** — vestavěný prohlížeč, přes který si přímo v PICO-8 stáhnete a spustíte cartridge z online databáze BBS. Hry lze exportovat i jako samostatné HTML5 verze do webového prohlížeče nebo jako spustitelné soubory pro Windows, macOS a Linux. Pro lokální multiplayer je k dispozici sdílení gamepadů na jednom stroji.

### Klony a varianty

Fantasy konzole se mezitím rozrostly v celý žánr a PICO-8 je jeho vlajkou. Nejvýznamnější příbuznou je **TIC-80** (autor Vadim Grigoruk, 2017) — open-source a zdarma. Má o něco větší rozlišení **240×136 pixelů**, plnou 16barevnou paletu, podporuje víc programovacích jazyků (Lua, JavaScript, MoonScript, Wren a další) a hry v ní procházíte příkazem `surf`. Knihovna je menší než u PICO-8, ale filozofie je totožná.

Lexaloffle kromě PICO-8 vydal i **Voxatron** (3D fantasy konzole s voxely) a samostatný hudební nástroj. Mezi další projekty v žánru patří třeba **LIKO-12** nebo **WASM-4**. Přímou „českou stopu" tu — na rozdíl od ZX Spectra s Didaktikem nebo NES s Pegasusem — nehledejte: fantasy konzole jsou ryze internetový, globální fenomén poslední dekády a žádný dobový východoevropský klon u nich neexistuje.

### Dnesni scena

Tady je situace obrácená než u staré klasiky — žádná emulace minulosti, ale živá tvorba současnosti. PICO-8 je placený nástroj, ale výsledné hry bývají často zdarma a komunita jich vyprodukovala tisíce: od miniaturních metroidvanií přes logické hříčky po střílečky. Mimo *Celeste Classic* stojí za vyzkoušení třeba **Dank Tomb**, **Just One Boss**, **Hexagravity**, **Subsurface** nebo **Pico Racer**.

Pro retrohráče s handheldy je dobrá zpráva, že na Anbernicích s čipem **H700** (a podobných) PICO-8 běží přes vlastní core a TIC-80 nativně, byť graficky náročnější cartridge mohou na slabších kartách trochu zpomalit. Je to „nové retro" v nejčistší podobě — hry vyrobené dnes, ale s duší osmdesátek. Ideální volba, když chcete objevovat něco mimo dobové klasiky.
