# -*- coding: utf-8 -*-
"""Dohledá z Wikidata (zdarma, bez auth) oficiální PEGI/ESRB rating + rok vydání
(P577) + vývojáře/studio (P178). STRIKTNÍ párování: přijme jen když je entita
videohra (P31) a její název PŘESNĚ (normalizovaně) sedí na naši hru — jinak nechá
prázdné (proti falešným datům). Výstupy:
  - src/data/game_ratings.json : {slug: {pegi, esrb}}
  - src/data/game_meta.json    : {slug: {year, studio}}  (jen doplněk, když chybí)
"""
import json, re, sys, time, subprocess, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_content as P
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
UA = "RetroWeb-ratings/1.0 (personal retro gaming site)"
API = "https://www.wikidata.org/w/api.php?"

VG = {"Q7889", "Q865493", "Q7058673"}  # video game, video game (compilation), series
_label_cache = {}


def get(params):
    url = API + urllib.parse.urlencode(params)
    for a in range(4):
        # --ssl-no-revoke: Windows schannel jinak padá na CRYPT_E_NO_REVOCATION_CHECK
        r = subprocess.run(["curl", "-sL", "--ssl-no-revoke", "--max-time", "30", "-A", UA, url],
                           capture_output=True)
        try:
            return json.loads(r.stdout)
        except Exception:
            time.sleep(1.2 * (a + 1))
    return {}


def clean(name):
    t = re.split(r"[/(\[]", name)[0]
    return t.strip() or name


def label_of(qid):
    if qid in _label_cache:
        return _label_cache[qid]
    d = get({"action": "wbgetentities", "ids": qid, "props": "labels", "languages": "en", "format": "json"})
    lab = ((d.get("entities", {}).get(qid, {}).get("labels", {}).get("en") or {}).get("value", "")) or qid
    _label_cache[qid] = lab
    return lab


def claim_qids(entity, prop):
    out = []
    for c in entity.get("claims", {}).get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
        if isinstance(v, dict) and v.get("id"):
            out.append(v["id"])
    return out


def claim_year(entity, prop="P577"):
    """Nejstarší rok z P577 (publication date)."""
    years = []
    for c in entity.get("claims", {}).get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
        t = v.get("time") if isinstance(v, dict) else None
        if t:
            m = re.search(r"([+-])(\d{4})", t)
            if m and m.group(2) != "0000":
                years.append(int(m.group(2)))
    return str(min(years)) if years else None


def meta_for(name):
    """Vrátí {pegi,esrb,year,studio} pro přesně napárovanou videohru, jinak None."""
    want = P.norm_name(name)
    res = get({"action": "wbsearchentities", "search": clean(name), "language": "en",
               "format": "json", "type": "item", "limit": "6"})
    ids = [x["id"] for x in res.get("search", [])]
    if not ids:
        return None
    ent = get({"action": "wbgetentities", "ids": "|".join(ids[:6]),
               "props": "claims|labels", "languages": "en", "format": "json"})
    for qid in ids[:6]:
        e = ent.get("entities", {}).get(qid, {})
        lab = (e.get("labels", {}).get("en") or {}).get("value", "")
        if P.norm_name(lab) != want:
            continue
        p31 = set(claim_qids(e, "P31"))
        if not (p31 & VG):
            continue
        out = {}
        pegi = claim_qids(e, "P908")
        esrb = claim_qids(e, "P852")
        if pegi:
            out["pegi"] = label_of(pegi[0])
        if esrb:
            out["esrb"] = label_of(esrb[0]).replace("Entertainment Software Rating Board ", "")
        yr = claim_year(e)
        if yr:
            out["year"] = yr
        dev = claim_qids(e, "P178")
        if dev:
            dl = label_of(dev[0])
            if dl and not re.match(r"^Q\d+$", dl):  # neukládej holé QID (selhal převod na název)
                out["studio"] = dl
        if out:
            return out
    return None


d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
games = [(g["slug"], g["name"], g.get("year"), g.get("studio"), g.get("rating"))
         for p in d["platforms"] for g in p["games"]]

rat_file = ROOT / "src/data/game_ratings.json"
meta_file = ROOT / "src/data/game_meta.json"
ratings = json.loads(rat_file.read_text("utf-8")) if rat_file.exists() else {}
meta = json.loads(meta_file.read_text("utf-8")) if meta_file.exists() else {}

done_r = done_m = 0
for i, (slug, name, year, studio, rating) in enumerate(games):
    # jeden pokus na hru; meta.json slouží jako značka „už zkoušeno" (resume)
    if slug in meta:
        continue
    try:
        r = meta_for(name)
    except Exception:
        r = None
    meta.setdefault(slug, {})  # označ jako zpracované (i když prázdné)
    if r:
        rd = {k: v for k, v in r.items() if k in ("pegi", "esrb")}
        md = {}
        if not year and r.get("year"):
            md["year"] = r["year"]
        if not studio and r.get("studio"):
            md["studio"] = r["studio"]
        if rd and slug not in ratings:
            ratings[slug] = rd
            done_r += 1
        if md:
            meta[slug] = md
            done_m += 1
            print(f"  [{done_m}] {name} -> {md}")
    if i % 40 == 0:
        rat_file.write_text(json.dumps(ratings, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    time.sleep(0.12)

rat_file.write_text(json.dumps(ratings, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
print(f"\nHotovo: +{done_r} ratingů (celkem {len(ratings)}), +{done_m} rok/studio doplněno.")
