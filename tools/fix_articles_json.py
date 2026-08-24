# -*- coding: utf-8 -*-
"""Opravi soubory clanku, ve kterych zustala neescapovana uvozovka.

Clanky se ukladaji jako {"slug": "<markdown>"}. Kdyz text obsahuje ceskou
uvozovku „takhle" a zaviraci se zapise jako obycejne ", rozbije to JSON —
parse_content.py takovy soubor jen ohlasi a CELY preskoci, takze se tise
ztrati vsechny clanky v nem.

Skript projde src/data/articles/*.json, u vadnych souboru doescapuje uvozovky
uvnitr hodnot a soubor prepise. Bez --write jen hlasi, co by udelal.

Pouziti:  python tools/fix_articles_json.py [--write]
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "src" / "data" / "articles"

# Uvozovka konci HODNOTU, jen kdyz po ni jde dalsi klic nebo konec objektu.
# Pouhe „nasleduje carka" nestaci — text casto obsahuje ceskou uvozovku prave
# pred carkou (… „osmdesatkovou hernu", docekala se …).
VALUE_END = re.compile(r'"\s*(?:,\s*"[^"\\]+"\s*:|\}\s*$)')
# Uvozovka konci KLIC, kdyz po ni jde dvojtecka. Klice jsou slugy bez uvozovek,
# takze u nich zadna nejednoznacnost nehrozi.
KEY_END = re.compile(r'"\s*:')


def repair(text: str) -> str:
    """Doescapuje uvozovky, ktere jsou uvnitr hodnoty misto na jejim konci."""
    out: list[str] = []
    # None = mimo retezec, "key" = uvnitr klice, "value" = uvnitr hodnoty
    state = None
    expect_key = True
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if state is None:
            out.append(c)
            if c == '"':
                state = "key" if expect_key else "value"
            elif c == ":":
                expect_key = False
            elif c in ",{":
                expect_key = True
            i += 1
            continue
        if c == "\\":
            out.append(text[i: i + 2])
            i += 2
            continue
        if c == '"':
            done = KEY_END.match(text, i) if state == "key" else VALUE_END.match(text, i)
            if done:
                out.append(c)
                state = None
            else:
                out.append('\\"')
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def main() -> int:
    write = "--write" in sys.argv
    bad = 0
    for f in sorted(ARTICLES.glob("*.json")):
        raw = f.read_text(encoding="utf-8")
        try:
            json.loads(raw)
            continue
        except json.JSONDecodeError as e:
            bad += 1
            fixed = repair(raw)
            try:
                data = json.loads(fixed)
            except json.JSONDecodeError as e2:
                print(f"  [x] {f.name}: opravit se nepodarilo ({e2})")
                continue
            print(f"  [OK] {f.name}: {len(data)} clanku zachraneno (puvodne: {e.msg})")
            if write:
                with io.open(f, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump(data, fh, ensure_ascii=False, indent=1)
    if not bad:
        print("vsechny soubory clanku jsou v poradku")
    elif not write:
        print("\n(nic se nezapsalo — spust znovu s --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
