/**
 * Uzivatelsky ucet a znacky u her — klient bezici v prohlizeci.
 *
 * Zamerne bez knihovny @supabase/supabase-js: web ma pres 25 tisic statickych
 * stranek a SDK by se pribalilo ke kazde. Potrebujeme z nej stejne jen prihlaseni
 * kodem z e-mailu a ctyri dotazy na tabulku, coz je par desitek radku pres fetch.
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

/** Posle na e-mail sestimistny kod. Ucet vznikne pri prvnim prihlaseni. */
export async function poslatKod(email: string): Promise<void> {
  const odpoved = await fetch(`${SUPABASE_URL}/auth/v1/otp`, {
    method: 'POST',
    headers: { apikey: SUPABASE_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, create_user: true }),
  });
  if (!odpoved.ok) throw new Error(await chybovaHlaska(odpoved));
}

/** Overi kod z e-mailu a ulozi relaci do prohlizece. */
export async function overitKod(email: string, kod: string): Promise<void> {
  const odpoved = await fetch(`${SUPABASE_URL}/auth/v1/verify`, {
    method: 'POST',
    headers: { apikey: SUPABASE_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, token: kod.trim(), type: 'email' }),
  });
  if (!odpoved.ok) throw new Error(await chybovaHlaska(odpoved));
  const d = await odpoved.json();
  ulozRelaci({
    access_token: d.access_token,
    refresh_token: d.refresh_token,
    expires_at: Math.floor(Date.now() / 1000) + (d.expires_in ?? 3600),
    email: d.user?.email ?? email,
  });
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
