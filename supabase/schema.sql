-- RetroWeb — uzivatelske znacky u her a souhrnne statistiky.
--
-- Spustit v Supabase: SQL Editor -> New query -> vlozit cely soubor -> Run.
-- Skript je idempotentni, da se pustit opakovane.
--
-- Model: jeden radek na dvojici (uzivatel, hra) se dvema priznaky. Dva
-- booleany misto dvou radku proto, ze hra byva oznacena obema zaroven
-- ("hral jsem a chci se vratit") a takhle staci jeden zapis.

create table if not exists public.herni_znacky (
  user_id       uuid        not null references auth.users (id) on delete cascade,
  game_slug     text        not null,
  platform_slug text        not null,
  zajima        boolean     not null default false,
  hral          boolean     not null default false,
  vlozeno       timestamptz not null default now(),
  zmeneno       timestamptz not null default now(),
  primary key (user_id, game_slug)
);

-- Filtrovani v "Muj seznam" jde pres platformu a typ znacky; pri stovkach
-- radku na uzivatele se to bez indexu zbytecne prohledava cele.
create index if not exists herni_znacky_user_platforma
  on public.herni_znacky (user_id, platform_slug);
create index if not exists herni_znacky_hra
  on public.herni_znacky (game_slug);

-- Radek bez jedine znacky nema smysl drzet; klient ho maze, tohle je pojistka.
alter table public.herni_znacky
  drop constraint if exists herni_znacky_aspon_jedna;
alter table public.herni_znacky
  add constraint herni_znacky_aspon_jedna check (zajima or hral);

-- ---------------------------------------------------------------- RLS
-- Bez tohohle by anonymni klic dovolil cist cizi seznamy. Klic je verejny
-- (je primo ve strance), takze RLS je jedina ochrana — musi byt zapnute.
alter table public.herni_znacky enable row level security;

drop policy if exists "ctu jen sve" on public.herni_znacky;
create policy "ctu jen sve" on public.herni_znacky
  for select using (auth.uid() = user_id);

drop policy if exists "zapisuji jen sve" on public.herni_znacky;
create policy "zapisuji jen sve" on public.herni_znacky
  for insert with check (auth.uid() = user_id);

drop policy if exists "upravuji jen sve" on public.herni_znacky;
create policy "upravuji jen sve" on public.herni_znacky
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "mazu jen sve" on public.herni_znacky;
create policy "mazu jen sve" on public.herni_znacky
  for delete using (auth.uid() = user_id);

-- Kazda zmena posune zmeneno; klient to nemusi resit.
create or replace function public.dotknout_zmeneno()
returns trigger language plpgsql as $$
begin
  new.zmeneno := now();
  return new;
end $$;

drop trigger if exists herni_znacky_zmeneno on public.herni_znacky;
create trigger herni_znacky_zmeneno
  before update on public.herni_znacky
  for each row execute function public.dotknout_zmeneno();

-- ---------------------------------------------------------- administratori
-- Seznam e-mailu, ktere smi videt statistiky. Doplnte si svuj:
--   insert into public.admini (email) values ('vas@email.cz');
create table if not exists public.admini (
  email text primary key
);
alter table public.admini enable row level security;
-- Zadna policy = nikdo z klienta nevidi ani nemeni; ctou to jen funkce nize.

create or replace function public.je_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.admini
    where lower(email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;

-- ------------------------------------------------------------- statistiky
-- Vraci JEN souhrnna cisla, zadne e-maily ani identifikatory uzivatelu —
-- statistika ma odpovedet "kolik lidi a co si oznacuji", ne "kdo".
create or replace function public.statistiky()
returns json language plpgsql stable security definer set search_path = public as $$
declare vysledek json;
begin
  if not public.je_admin() then
    raise exception 'Pristup jen pro administratory';
  end if;

  select json_build_object(
    'uzivatelu_celkem',      (select count(*) from auth.users),
    'uzivatelu_se_znackou',  (select count(distinct user_id) from public.herni_znacky),
    'znacek_celkem',         (select count(*) from public.herni_znacky),
    'zajima',                (select count(*) from public.herni_znacky where zajima),
    'hral',                  (select count(*) from public.herni_znacky where hral),
    'novych_7dni',           (select count(*) from auth.users
                               where created_at > now() - interval '7 days'),
    'aktivnich_30dni',       (select count(distinct user_id) from public.herni_znacky
                               where zmeneno > now() - interval '30 days'),
    'nejcastejsi_hry',       (select coalesce(json_agg(r), '[]'::json) from (
                               select game_slug, platform_slug, count(*) as pocet
                               from public.herni_znacky
                               group by game_slug, platform_slug
                               order by count(*) desc, game_slug limit 25) r),
    'podle_platforem',       (select coalesce(json_agg(r), '[]'::json) from (
                               select platform_slug,
                                      count(*) as pocet,
                                      count(distinct user_id) as uzivatelu
                               from public.herni_znacky
                               group by platform_slug
                               order by count(*) desc) r)
  ) into vysledek;
  return vysledek;
end $$;

revoke all on function public.statistiky() from anon;
grant execute on function public.statistiky() to authenticated;
