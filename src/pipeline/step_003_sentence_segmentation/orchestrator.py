"""Orchestrate the sentence segmentation pipeline stage while preserving the payload contract."""

from __future__ import annotations

from typing import Any

from pipeline.step_003_sentence_segmentation.rules import append_sentence, is_sentence_delimiter


def segment_sentences(input_payload: dict[str, Any]) -> dict[str, Any]:
    """Segment preprocessed text while preserving deterministic source offsets and identifiers."""
    preprocessed_text = input_payload["preprocessed_text"]
    source_text_id = input_payload["source_text_id"]

    sentences: list[dict[str, Any]] = []
    sentence_start = 0

    for idx in range(len(preprocessed_text)):
        if is_sentence_delimiter(preprocessed_text, idx):
            append_sentence(sentences, source_text_id, preprocessed_text, sentence_start, idx + 1)
            sentence_start = idx + 1

    if sentence_start < len(preprocessed_text):
        append_sentence(sentences, source_text_id, preprocessed_text, sentence_start, len(preprocessed_text))

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": source_text_id,
        "metadata": input_payload["metadata"],
        "preprocessed_text": preprocessed_text,
        "operations_applied": input_payload["operations_applied"],
        "sentences": sentences,
    }
