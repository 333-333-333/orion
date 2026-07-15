"""Implement deterministic Unicode, whitespace, and newline normalization."""

from __future__ import annotations

import re
import unicodedata

_BR_UNICODE_NORMALIZATION_FORM = "NFC"
_BR_WHITESPACE_PATTERN = re.compile(r"[ \t]+")
_BR_NEWLINE_PATTERN = re.compile(r"\r\n?|\n")


def normalize_unicode(raw_text: str) -> str:
    """Normalize input text to the configured Unicode normalization form."""
    return unicodedata.normalize(_BR_UNICODE_NORMALIZATION_FORM, raw_text)


def collapse_repeated_spaces(text: str) -> str:
    """Collapse adjacent horizontal whitespace without changing line boundaries."""
    return _BR_WHITESPACE_PATTERN.sub(" ", text)


def normalize_newlines(text: str) -> str:
    """Normalize CRLF and CR line endings to LF."""
    return _BR_NEWLINE_PATTERN.sub("\n", text)
