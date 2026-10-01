from __future__ import annotations

import json
import re

from app.config import ANSWER_MAX_LENGTH

_TR_FOLD = str.maketrans(
    {
        "I": "i", "İ": "i", "ı": "i",
        "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç",
    }
)

_WS = re.compile(r"\s+")


def normalize(value: str) -> str:
    if value is None:
        return ""
    value = value[:ANSWER_MAX_LENGTH]
    value = value.translate(_TR_FOLD).lower()
    return _WS.sub(" ", value).strip()


def check(answer_type: str, answer_value: str, submitted: str) -> bool:
    given = normalize(submitted)

    if answer_type == "exact":
        return given == normalize(answer_value)

    if answer_type == "regex":
        try:
            pattern = re.compile(answer_value, re.IGNORECASE)
        except re.error:
            return False
        return bool(pattern.fullmatch(given))

    if answer_type == "choice":
        return given == normalize(str(answer_value))

    return False


def public_choices(choices_json: str | None) -> list[str]:
    if not choices_json:
        return []
    try:
        data = json.loads(choices_json)
    except (ValueError, TypeError):
        return []
    return [str(item) for item in data]


def validate_definition(answer_type: str, answer_value: str, choices: list | None) -> str | None:
    if answer_type not in {"exact", "regex", "choice"}:
        return f"Bilinmeyen cevap tipi: {answer_type}"

    if answer_type == "regex":
        try:
            re.compile(answer_value)
        except re.error as exc:
            return f"Regex derlenmedi: {exc}"

    if answer_type == "choice":
        if not choices:
            return "choice tipinde `choices` listesi zorunlu."
        try:
            index = int(answer_value)
        except (TypeError, ValueError):
            return "choice tipinde answer_value doğru şıkkın indeksi olmalı (0'dan başlar)."
        if not (0 <= index < len(choices)):
            return f"answer_value {index}, ama {len(choices)} şık var."

    return None
