from __future__ import annotations

from typing import Any

from pipeline.step_003_sentence_segmentation.rules import SENTENCE_DELIMITERS, append_sentence


def segment_sentences(input_payload: dict[str, Any]) -> dict[str, Any]:
    preprocessed_text = input_payload["preprocessed_text"]
    source_text_id = input_payload["source_text_id"]

    sentences: list[dict[str, Any]] = []
    sentence_start = 0

    for idx, char in enumerate(preprocessed_text):
        if char in SENTENCE_DELIMITERS:
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
