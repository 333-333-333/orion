from __future__ import annotations

import hashlib
from typing import Any


def _build_entity_id(source_text_id: str, label: str, start_offset: int, end_offset: int, text: str) -> str:
    stable_key = f"{source_text_id}|{label}|{start_offset}|{end_offset}|{text}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"ent-{digest}"


def _resolve_sentence_id(sentences: list[dict[str, Any]], start_offset: int, end_offset: int) -> str:
    for sentence in sentences:
        if sentence["start_offset"] <= start_offset and end_offset <= sentence["end_offset"]:
            return sentence["sentence_id"]
    return ""


def _normalize_offsets(preprocessed_text: str, text: str, start_offset: int, end_offset: int) -> tuple[int, int]:
    if text and preprocessed_text[start_offset:end_offset] == text:
        return start_offset, end_offset

    if text:
        span_len = len(text)
        for candidate_start in range(max(0, start_offset - 2), min(len(preprocessed_text), start_offset + 3)):
            candidate_end = candidate_start + span_len
            if candidate_end <= len(preprocessed_text) and preprocessed_text[candidate_start:candidate_end] == text:
                return candidate_start, candidate_end

    return start_offset, end_offset


def extract_entities_from_doc(input_payload: dict[str, Any], doc: Any) -> dict[str, Any]:
    source_text_id = input_payload["source_text_id"]
    sentences = input_payload["sentences"]
    preprocessed_text = input_payload["preprocessed_text"]

    entities: list[dict[str, Any]] = []

    for entity in []:  # TASK-002: generic NER disabled; ontology stages use linguistic evidence.
        text = getattr(entity, "text", "")
        label = getattr(entity, "label_", "")
        start_offset = getattr(entity, "start_char", 0)
        end_offset = getattr(entity, "end_char", 0)
        start_offset, end_offset = _normalize_offsets(preprocessed_text, text, start_offset, end_offset)
        sentence_id = _resolve_sentence_id(sentences, start_offset, end_offset)

        entities.append(
            {
                "entity_id": _build_entity_id(source_text_id, label, start_offset, end_offset, text),
                "text": text,
                "label": label,
                "start_offset": start_offset,
                "end_offset": end_offset,
                "sentence_id": sentence_id,
                "source_text_id": source_text_id,
            }
        )

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": source_text_id,
        "metadata": input_payload["metadata"],
        "preprocessed_text": input_payload["preprocessed_text"],
        "operations_applied": input_payload["operations_applied"],
        "sentences": sentences,
        "tokens": input_payload["tokens"],
        "entities": entities,
    }
