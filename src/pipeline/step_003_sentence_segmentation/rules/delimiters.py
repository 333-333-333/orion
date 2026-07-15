"""Implement sentence-boundary rules and deterministic sentence records."""

from __future__ import annotations

import hashlib
from typing import Any

SENTENCE_DELIMITERS = frozenset({".", "?", "!"})
_TIME_ABBREVIATION_PREFIXES = frozenset({"a", "p"})


def is_sentence_delimiter(text: str, index: int) -> bool:
    """Return whether the character at an index terminates a sentence under abbreviation rules."""
    char = text[index]
    if char not in SENTENCE_DELIMITERS:
        return False
    # The first dot is always internal to a.m./p.m.; only the final dot may end a sentence.
    if char == "." and _is_time_abbreviation_first_period(text, index):
        return False
    if char == "." and _is_time_abbreviation_final_period(text, index):
        return _is_sentence_boundary_after(text, index)
    return True


def _is_time_abbreviation_first_period(text: str, index: int) -> bool:
    """Return whether an index is the first period in an a.m. or p.m. abbreviation."""
    return (
        index >= 1
        and index + 2 < len(text)
        and text[index - 1].casefold() in _TIME_ABBREVIATION_PREFIXES
        and text[index + 1].casefold() == "m"
        and text[index + 2] == "."
    )


def _is_time_abbreviation_final_period(text: str, index: int) -> bool:
    """Return whether an index is the final period in an a.m. or p.m. abbreviation."""
    return (
        index >= 3
        and text[index - 3].casefold() in _TIME_ABBREVIATION_PREFIXES
        and text[index - 2] == "."
        and text[index - 1].casefold() == "m"
    )


def _is_sentence_boundary_after(text: str, index: int) -> bool:
    """Treat end of text or the next uppercase non-space character as a sentence boundary."""
    for next_char in text[index + 1:]:
        if next_char.isspace():
            continue
        return next_char.isupper()
    return True


def build_sentence_id(source_text_id: str, index: int, start_offset: int, end_offset: int, text: str) -> str:
    """Build a deterministic sentence identifier from source identity, offsets, and text."""
    stable_key = f"{source_text_id}|{index}|{start_offset}|{end_offset}|{text}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"sent-{digest}"


def append_sentence(sentences: list[dict[str, Any]], source_text_id: str, preprocessed_text: str, start: int, end: int) -> None:
    """Append a non-empty, offset-preserving sentence record to the sentence collection."""
    fragment = preprocessed_text[start:end]
    stripped = fragment.strip()
    if not stripped:
        return

    left_trim = len(fragment) - len(fragment.lstrip())
    right_trim = len(fragment.rstrip())

    start_offset = start + left_trim
    end_offset = start + right_trim

    index = len(sentences)
    sentence_text = preprocessed_text[start_offset:end_offset]
    sentences.append(
        {
            "sentence_id": build_sentence_id(source_text_id, index, start_offset, end_offset, sentence_text),
            "text": sentence_text,
            "index": index,
            "start_offset": start_offset,
            "end_offset": end_offset,
            "source_text_id": source_text_id,
        }
    )
