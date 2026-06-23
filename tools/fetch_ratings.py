# -*- coding: utf-8 -*-
"""Dohledá oficiální PEGI/ESRB rating z Wikidata (zdarma, bez auth).
STRIKTNÍ párování: přijme jen když je entita videohra (P31) a její název přesně
sedí (normalizovaně) na naši hru — jinak nechá prázdné. Výstup: game_ratings.json."""
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
        r = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
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


def rating_for(name):
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
        pegi = claim_qids(e, "P908")
        esrb = claim_qids(e, "P852")
        out = {}
        if pegi:
            out["pegi"] = label_of(pegi[0])           # např. "PEGI 12"
        if esrb:
            out["esrb"] = label_of(esrb[0]).replace("Entertainment Software Rating Board ", "")
        if out:
            return out
    return None


d = json.loads((ROOT / "src/data/dataset.json").read_text("utf-8"))
games = [(g["slug"], g["name"]) for p in d["platforms"] for g in p["games"]]
out_file = ROOT / "src/data/game_ratings.json"
ratings = json.loads(out_file.read_text("utf-8")) if out_file.exists() else {}
done = 0
for i, (slug, name) in enumerate(games):
    if slug in ratings:
        continue
    try:
        r = rating_for(name)
    except Exception:
        r = None
    if r:
        ratings[slug] = r
        done += 1
        print(f"  [{done}] {name} -> {r}")
    if i % 40 == 0:
        out_file.write_text(json.dumps(ratings, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    time.sleep(0.15)
out_file.write_text(json.dumps(ratings, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
print(f"\nHotovo: {len(ratings)} her s ratingem (z {len(games)}).")
