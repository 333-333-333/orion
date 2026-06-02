from __future__ import annotations

import hashlib
from typing import Any

_BR_SENTENCE_DELIMITERS = frozenset({".", "?", "!"})


def _build_sentence_id(source_text_id: str, index: int, start_offset: int, end_offset: int, text: str) -> str:
    stable_key = f"{source_text_id}|{index}|{start_offset}|{end_offset}|{text}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"sent-{digest}"


def _append_sentence(sentences: list[dict[str, Any]], source_text_id: str, preprocessed_text: str, start: int, end: int) -> None:
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
            "sentence_id": _build_sentence_id(source_text_id, index, start_offset, end_offset, sentence_text),
            "text": sentence_text,
            "index": index,
            "start_offset": start_offset,
            "end_offset": end_offset,
            "source_text_id": source_text_id,
        }
    )


def segment_sentences(input_payload: dict[str, Any]) -> dict[str, Any]:
    preprocessed_text = input_payload["preprocessed_text"]
    source_text_id = input_payload["source_text_id"]

    sentences: list[dict[str, Any]] = []
    sentence_start = 0

    for idx, char in enumerate(preprocessed_text):
        if char in _BR_SENTENCE_DELIMITERS:
            _append_sentence(sentences, source_text_id, preprocessed_text, sentence_start, idx + 1)
            sentence_start = idx + 1

    if sentence_start < len(preprocessed_text):
        _append_sentence(sentences, source_text_id, preprocessed_text, sentence_start, len(preprocessed_text))

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": source_text_id,
        "metadata": input_payload["metadata"],
        "preprocessed_text": preprocessed_text,
        "operations_applied": input_payload["operations_applied"],
        "sentences": sentences,
    }
