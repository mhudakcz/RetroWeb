/**
 * Uzivatelsky ucet a znacky u her — klient bezici v prohlizeci.
 *
 * Zamerne bez knihovny @supabase/supabase-js: web ma pres 25 tisic statickych
 * stranek a SDK by se pribalilo ke kazde. Potrebujeme z nej stejne jen prihlaseni
 * odkazem z e-mailu a ctyri dotazy na tabulku, coz je par desitek radku pres fetch.
 *
 * Publikovatelny klic patri do stranky — chrani ho zabezpeceni na urovni radku
 * (RLS) v supabase/schema.sql, ne utajeni. Servisni klic sem NIKDY nepatri.
 */

export const SUPABASE_URL =
  import.meta.env.PUBLIC_SUPABASE_URL || 'https://kcnfrihxmlvnhwroiriy.supabase.co';
export const SUPABASE_KEY =
  import.meta.env.PUBLIC_SUPABASE_KEY || 'sb_publishable_FXhCUUk79dd3BzYD0BcP5w_pvfqtr2G';

const ULOZISTE = 'retroweb.ucet';

export type Relace = {
  access_token: string;
  refresh_token: string;
  expires_at: number; // sekundy od epochy
  email: string;
};

export type Znacka = {
  game_slug: string;
  platform_slug: string;
  zajima: boolean;
  hral: boolean;
};

/* ------------------------------------------------------------------ relace */

export function nactiRelaci(): Relace | null {
  try {
    const s = localStorage.getItem(ULOZISTE);
    return s ? (JSON.parse(s) as Relace) : null;
  } catch {
    return null; // soukrome okno nebo zakazana uloziste
  }
}

function ulozRelaci(r: Relace | null) {
  try {
    if (r) localStorage.setItem(ULOZISTE, JSON.stringify(r));
    else localStorage.removeItem(ULOZISTE);
  } catch {
    /* bez uloziste se proste neprihlasi natrvalo */
  }
  document.dispatchEvent(new CustomEvent('retroweb:ucet', { detail: r }));
}

export function prihlasenyEmail(): string | null {
  return nactiRelaci()?.email ?? null;
}

/** Platny pristupovy token; kdyz vyprsel, obnovi ho. null = neprihlasen. */
export async function token(): Promise<string | null> {
  const r = nactiRelaci();
  if (!r) return null;
  // obnovujeme minutu pred vyprsenim, at dotaz neselze na hranici
  if (r.expires_at - 60 > Date.now() / 1000) return r.access_token;

  const odpoved = await fetch(`${SUPABASE_URL}/auth/v1/token?grant_type=refresh_token`, {
    method: 'POST',
    headers: { apikey: SUPABASE_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: r.refresh_token }),
  });
  if (!odpoved.ok) {
    ulozRelaci(null); // obnova selhala, relace uz neplati
    return null;
  }
  const d = await odpoved.json();
  const nova: Relace = {
    access_token: d.access_token,
    refresh_token: d.refresh_token,
    expires_at: Math.floor(Date.now() / 1000) + (d.expires_in ?? 3600),
    email: d.user?.email ?? r.email,
  };
  ulozRelaci(nova);
  return nova.access_token;
}

/* -------------------------------------------------------------- prihlaseni */

/**
 * Posle na e-mail prihlasovaci odkaz. Ucet vznikne pri prvnim prihlaseni.
 *
 * Drive se posilal sestimistny kod, ktery uzivatel opisoval. Odkaz je o krok
 * min prace a hlavne funguje se sablonou, kterou ma Supabase v zakladu —
 * u kodu se musi sablona rucne prepsat na {{ .Token }}, jinak prijde odkaz
 * a v poli pro kod neni co vyplnit.
 */
export async function poslatOdkaz(email: string, navrat?: string): Promise<void> {
  const cil = navrat || (typeof location !== 'undefined' ? location.href.split('#')[0] : '');
  const url = `${SUPABASE_URL}/auth/v1/otp` + (cil ? `?redirect_to=${encodeURIComponent(cil)}` : '');
  const odpoved = await fetch(url, {
    method: 'POST',
    headers: { apikey: SUPABASE_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, create_user: true }),
  });
  if (!odpoved.ok) throw new Error(await chybovaHlaska(odpoved));
}

/**
 * Zpracuje navrat z prihlasovaciho odkazu. Supabase vraci tokeny ve fragmentu
 * adresy (#access_token=...), ktery se po ulozeni z adresniho radku smaze —
 * jinak by zustal v historii prohlizece i ve sdilenem odkazu.
 *
 * Vraci true, kdyz se nekdo prave prihlasil.
 */
export function zpracujNavrat(): boolean {
  if (typeof location === 'undefined' || !location.hash) return false;
  const p = new URLSearchParams(location.hash.slice(1));
  const access = p.get('access_token');
  const refresh = p.get('refresh_token');
  if (!access || !refresh) {
    // Supabase sem dava i chyby (vyprseny nebo uz pouzity odkaz).
    if (p.get('error') || p.get('error_description')) {
      history.replaceState(null, '', location.pathname + location.search);
    }
    return false;
  }
  ulozRelaci({
    access_token: access,
    refresh_token: refresh,
    expires_at: Math.floor(Date.now() / 1000) + Number(p.get('expires_in') || 3600),
    email: '',
  });
  history.replaceState(null, '', location.pathname + location.search);
  // Fragment adresy nese jen tokeny, ne e-mail. Dotahneme ho na pozadi,
  // aby hlavicka mohla ukazat, kdo je prihlaseny.
  void dotahniEmail();
  return true;
}

/** Zjisti e-mail prihlaseneho uzivatele a doplni ho do ulozene relace. */
async function dotahniEmail(): Promise<void> {
  const r = nactiRelaci();
  if (!r || r.email) return;
  try {
    const odpoved = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
      headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${r.access_token}` },
    });
    if (!odpoved.ok) return;
    const d = await odpoved.json();
    if (d?.email) ulozRelaci({ ...r, email: d.email });
  } catch {
    /* e-mail je jen ozdoba, prihlaseni funguje i bez nej */
  }
}

/** Text chyby z navratoveho odkazu, kdyz se prihlaseni nepovedlo. */
export function chybaZNavratu(): string | null {
  if (typeof location === 'undefined' || !location.hash) return null;
  const p = new URLSearchParams(location.hash.slice(1));
  return p.get('error_description') || p.get('error') || null;
}

export function odhlasit(): void {
  ulozRelaci(null);
}

async function chybovaHlaska(o: Response): Promise<string> {
  try {
    const d = await o.json();
    return d.error_description || d.msg || d.message || `Chyba ${o.status}`;
  } catch {
    return `Chyba ${o.status}`;
  }
}

/* ------------------------------------------------------------------ znacky */

async function hlavicky(): Promise<Record<string, string> | null> {
  const t = await token();
  if (!t) return null;
  return {
    apikey: SUPABASE_KEY,
    Authorization: `Bearer ${t}`,
    'Content-Type': 'application/json',
  };
}

/** Vsechny znacky prihlaseneho uzivatele. RLS zajisti, ze cizi neuvidi. */
export async function nactiZnacky(): Promise<Znacka[]> {
  const h = await hlavicky();
  if (!h) return [];
  const o = await fetch(
    `${SUPABASE_URL}/rest/v1/herni_znacky?select=game_slug,platform_slug,zajima,hral`,
    { headers: h },
  );
  if (!o.ok) return [];
  return (await o.json()) as Znacka[];
}

/**
 * Nastavi znacky u jedne hry. Kdyz zbude oboji vypnute, radek se smaze —
 * prazdny zaznam nema smysl drzet a "Muj seznam" by ho musel filtrovat.
 */
export async function ulozZnacku(
  gameSlug: string,
  platformSlug: string,
  zajima: boolean,
  hral: boolean,
): Promise<void> {
  const h = await hlavicky();
  if (!h) throw new Error('neprihlasen');

  if (!zajima && !hral) {
    const o = await fetch(`${SUPABASE_URL}/rest/v1/herni_znacky?game_slug=eq.${encodeURIComponent(gameSlug)}`, {
      method: 'DELETE',
      headers: h,
    });
    if (!o.ok) throw new Error(await chybovaHlaska(o));
    return;
  }

  const t = await token();
  const uzivatel = t ? uzivatelZTokenu(t) : null;
  if (!uzivatel) throw new Error('neprihlasen');

  const o = await fetch(`${SUPABASE_URL}/rest/v1/herni_znacky`, {
    method: 'POST',
    headers: { ...h, Prefer: 'resolution=merge-duplicates' },
    body: JSON.stringify({
      user_id: uzivatel,
      game_slug: gameSlug,
      platform_slug: platformSlug,
      zajima,
      hral,
    }),
  });
  if (!o.ok) throw new Error(await chybovaHlaska(o));
}

/** id uzivatele z tokenu — upsert ho potrebuje v tele, RLS pak overi shodu. */
function uzivatelZTokenu(t: string): string | null {
  try {
    const telo = t.split('.')[1];
    const json = atob(telo.replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(json).sub ?? null;
  } catch {
    return null;
  }
}

/* -------------------------------------------------------------- statistiky */

/** Souhrnna cisla pro administraci. Funkce v databazi pusti jen administratory. */
export async function statistiky(): Promise<any> {
  const h = await hlavicky();
  if (!h) throw new Error('neprihlasen');
  const o = await fetch(`${SUPABASE_URL}/rest/v1/rpc/statistiky`, {
    method: 'POST',
    headers: h,
    body: '{}',
  });
  if (!o.ok) throw new Error(await chybovaHlaska(o));
  return o.json();
}
