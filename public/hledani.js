/**
 * Vyhledavani nad indexem /search.json — sdilene napovedou v hlavicce
 * a strankou s vysledky.
 *
 * Zamerne obycejny skript v public/, ne modul: hlavicka ho pouziva v bloku
 * is:inline, ktery se nebalikuje, a duplikovat bodovani na dvou mistech by
 * znamenalo, ze se jednou zmeni a podruhe ne.
 */
(function (global) {
  'use strict';

  /** Bez diakritiky a interpunkce — musi odpovidat fold() v search.json.ts */
  function fold(s) {
    return String(s).normalize('NFKD').replace(/[̀-ͯ]/g, '')
      .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }

  /* Vzdalenost dvou slov s horni mezi — kdyz je vetsi nez max, vratime max+1
     a dal nepocitame. Pri sesti tisicich zaznamech se to vola casto, takze
     pouzivame jen dva radky matice misto cele. */
  function blizko(a, b, max) {
    if (a === b) return 0;
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var prev = [], cur = [], i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur[0] = i;
      var nejlepsi = i;
      for (j = 1; j <= b.length; j++) {
        var cena = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + cena);
        if (cur[j] < nejlepsi) nejlepsi = cur[j];
      }
      if (nejlepsi > max) return max + 1;  // cely radek uz je za limitem
      for (j = 0; j <= b.length; j++) prev[j] = cur[j];
    }
    return prev[b.length];
  }

  /* Kolik preklepu slovu odpustime. U kratkych slov zadny — jinak by
     "mario" naslo "maria" i "mari" a nabidka by byla k nicemu. */
  function tolerance(slovo) {
    if (slovo.length <= 3) return 0;
    if (slovo.length <= 6) return 1;
    return 2;
  }

  /* Skore zaznamu proti dotazu; 0 znamena "neodpovida".
     Vyssi je lepsi. Poradi urovni:
       100  cely dotaz od zacatku nazvu     "super mario" -> Super Mario Bros.
        80  cely dotaz nekde v nazvu        "mario bros" -> Super Mario Bros.
        60  vsechna slova jako zacatek slov "zelda ocarina" -> Zelda: Ocarina of Time
        40  vsechna slova kdekoliv
        20  vsechna slova s preklepem       "residnt evil" -> Resident Evil */
  function skore(r, f, slova) {
    var at = r.f.indexOf(f);
    if (at === 0) return 100;
    if (at > 0) return 80;

    var casti = r.f.split(' ');
    var vsechnyZacatky = true, vsechnyKdekoliv = true, vsechnySPreklepem = true;
    for (var i = 0; i < slova.length; i++) {
      var w = slova[i];
      var zacatek = false, kdekoliv = false, preklep = false;
      for (var j = 0; j < casti.length; j++) {
        var c = casti[j];
        if (c.indexOf(w) === 0) { zacatek = true; kdekoliv = true; preklep = true; break; }
        if (c.indexOf(w) > 0) { kdekoliv = true; preklep = true; }
      }
      if (!kdekoliv) {
        var max = tolerance(w);
        if (max > 0) {
          for (var k = 0; k < casti.length; k++) {
            if (blizko(w, casti[k], max) <= max) { preklep = true; break; }
          }
        }
      }
      if (!zacatek) vsechnyZacatky = false;
      if (!kdekoliv) vsechnyKdekoliv = false;
      if (!preklep) { vsechnySPreklepem = false; break; }
    }
    if (vsechnyZacatky) return 60;
    if (vsechnyKdekoliv) return 40;
    if (vsechnySPreklepem) return 20;
    return 0;
  }

  /**
   * Vrati serazene zaznamy indexu odpovidajici dotazu.
   * limit 0 = bez omezeni (pouziva stranka s vysledky).
   */
  function hledej(index, dotaz, limit) {
    var f = fold(dotaz);
    if (!f || !index) return [];
    var slova = f.split(' ');
    var out = [];
    for (var i = 0; i < index.length; i++) {
      var r = index[i];
      var sk = skore(r, f, slova);
      if (sk) out.push({ r: r, sk: sk });
    }
    // typy krome her jdou napred — je jich malo a hleda se na ne cileneji
    out.sort(function (a, b) {
      if (a.sk !== b.sk) return b.sk - a.sk;
      var ra = a.r.t === 'g' ? 1 : 0, rb = b.r.t === 'g' ? 1 : 0;
      return ra - rb || a.r.n.length - b.r.n.length;
    });
    var vysledek = [];
    var strop = limit || out.length;
    for (var m = 0; m < out.length && m < strop; m++) vysledek.push(out[m].r);
    return vysledek;
  }

  global.RWHledani = { fold: fold, hledej: hledej, skore: skore };
})(window);
