"""Orchestrate the preprocessing pipeline stage while preserving the payload contract."""

from __future__ import annotations

from typing import Any

from pipeline.step_001_input_intake.exceptions import OrionError
from pipeline.step_002_preprocessing.rules import collapse_repeated_spaces, normalize_newlines, normalize_unicode


def preprocess_input(input_payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize accepted input text and return the preprocessing payload."""
    raw_text = input_payload["raw_text"]

    preprocessed_text = normalize_unicode(raw_text)
    preprocessed_text = collapse_repeated_spaces(preprocessed_text)
    preprocessed_text = normalize_newlines(preprocessed_text)

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
