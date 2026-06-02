from __future__ import annotations

import re
import unicodedata
from typing import Any

from pipeline.step_001_input_intake.exceptions import OrionError

_BR_UNICODE_NORMALIZATION_FORM = "NFC"
_BR_WHITESPACE_PATTERN = re.compile(r"[ \t]+")
_BR_NEWLINE_PATTERN = re.compile(r"\r\n?|\n")


def _normalize_unicode(raw_text: str) -> str:
    return unicodedata.normalize(_BR_UNICODE_NORMALIZATION_FORM, raw_text)


def _collapse_repeated_spaces(text: str) -> str:
    return _BR_WHITESPACE_PATTERN.sub(" ", text)


def _normalize_newlines(text: str) -> str:
    return _BR_NEWLINE_PATTERN.sub("\n", text)


def preprocess_input(input_payload: dict[str, Any]) -> dict[str, Any]:
    raw_text = input_payload["raw_text"]

    preprocessed_text = _normalize_unicode(raw_text)
    preprocessed_text = _collapse_repeated_spaces(preprocessed_text)
    preprocessed_text = _normalize_newlines(preprocessed_text)

    if preprocessed_text.strip() == "":
        raise OrionError("Preprocessing produced empty text")

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": input_payload["source_text_id"],
        "metadata": input_payload["metadata"],
        "preprocessed_text": preprocessed_text,
        "operations_applied": [
            "unicode_normalization",
            "collapse_repeated_spaces",
            "normalize_newlines",
        ],
    }
