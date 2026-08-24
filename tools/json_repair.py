# -*- coding: utf-8 -*-
"""Shovivave nacteni JSONu, ktery vratil agent.

Agenti obcas zapisi do retezce doslovny konec radku misto \\n. JSON to
zakazuje, takze cely soubor spadne na "Invalid control character" a prijde
se o celou davku. Tenhle modul takove znaky uvnitr retezcu doescapuje.

Opravuje se jen to, co je bezpecne rozhodnutelne — ridici znaky uvnitr
retezce. Kdyz je soubor rozbity jinak, vyjimka propadne dal.
"""
import json

# Ridici znaky, ktere se v retezci musi psat escapovane.
_ESCAPES = {"\n": "\\n", "\r": "\\r", "\t": "\\t", "\b": "\\b", "\f": "\\f"}


def repair(text: str) -> str:
    """Doescapuje ridici znaky uvnitr retezcovych hodnot."""
    out = []
    in_str = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if in_str:
            if c == "\\":
                out.append(text[i: i + 2])
                i += 2
                continue
            if c == '"':
                in_str = False
                out.append(c)
                i += 1
                continue
            if c in _ESCAPES:
                out.append(_ESCAPES[c])
                i += 1
                continue
            if ord(c) < 0x20:
                out.append(f"\\u{ord(c):04x}")
                i += 1
                continue
        elif c == '"':
            in_str = True
        out.append(c)
        i += 1
    return "".join(out)


def loads(text: str, on_repair=None):
    """json.loads, ktery pri chybe na ridicim znaku jeste zkusi opravu.

    on_repair: volitelna funkce, ktera se zavola, kdyz oprava zabrala —
    at volajici muze nahlasit, ze soubor nebyl v poradku.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        if "control character" not in e.msg.lower():
            raise
        data = json.loads(repair(text))
        if on_repair:
            on_repair(e)
        return data


def load_file(path, on_repair=None):
    from pathlib import Path

    return loads(Path(path).read_text(encoding="utf-8"), on_repair)
