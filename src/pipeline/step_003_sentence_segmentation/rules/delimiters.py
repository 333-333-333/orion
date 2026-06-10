from __future__ import annotations

import hashlib
from typing import Any

SENTENCE_DELIMITERS = frozenset({".", "?", "!"})


def build_sentence_id(source_text_id: str, index: int, start_offset: int, end_offset: int, text: str) -> str:
    stable_key = f"{source_text_id}|{index}|{start_offset}|{end_offset}|{text}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"sent-{digest}"


def append_sentence(sentences: list[dict[str, Any]], source_text_id: str, preprocessed_text: str, start: int, end: int) -> None:
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
