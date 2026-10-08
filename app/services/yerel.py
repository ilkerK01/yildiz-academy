from __future__ import annotations

import json
from functools import lru_cache

from markupsafe import escape

from app.services.answers import public_choices

# Ders ve lab içeriğinin İngilizce sürümü `en_json` kolonunda tutulur.
# Çeviri yoksa ya da bir alan eksikse Türkçe asıl metin gösterilir.


@lru_cache(maxsize=256)
def _coz(ham: str) -> dict:
    try:
        veri = json.loads(ham)
    except (ValueError, TypeError):
        return {}
    return veri if isinstance(veri, dict) else {}


def ceviri(obj) -> dict:
    ham = getattr(obj, "en_json", None)
    return _coz(ham) if ham else {}


def alan(obj, ad: str, kod: str):
    deger = getattr(obj, ad, "")
    if kod != "en" or obj is None:
        return deger
    return ceviri(obj).get(ad) or deger


def adim(step, kod: str) -> dict:
    metin = {
        "prompt_html": step.prompt_html or str(escape(step.prompt_md)),
        "artifact": step.artifact,
        "choices": public_choices(step.choices_json),
        "hints": [h.text_html or str(escape(h.text_md)) for h in step.hints],
    }
    if kod != "en":
        return metin
    en = (ceviri(step.lab).get("steps") or {}).get(str(step.step_index)) or {}
    if en.get("prompt_html"):
        metin["prompt_html"] = en["prompt_html"]
    if en.get("artifact") and step.artifact:
        metin["artifact"] = en["artifact"]
    secenekler = en.get("choices") or []
    if secenekler and len(secenekler) == len(metin["choices"]):
        metin["choices"] = [str(s) for s in secenekler]
    for i, ipucu in enumerate(en.get("hints") or []):
        if i < len(metin["hints"]) and ipucu:
            metin["hints"][i] = ipucu
    return metin
