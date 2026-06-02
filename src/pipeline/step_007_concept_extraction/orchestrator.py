from __future__ import annotations

import hashlib
from typing import Any

_BR_CONCEPT_CONFIDENCE_NOUN_CHUNK = 0.95
_BR_CONCEPT_CONFIDENCE_ENTITY_LABEL = 0.9
_BR_CONCEPT_CONFIDENCE_NOUN_TOKEN = 0.8


def _normalize_text(value: str) -> str:
    return value.casefold().strip()


def _resolve_sentence_id(sentences: list[dict[str, Any]], start_offset: int, end_offset: int) -> str:
    for sentence in sentences:
        if sentence["start_offset"] <= start_offset and end_offset <= sentence["end_offset"]:
            return sentence["sentence_id"]
    return ""


def _build_concept_id(source_text_id: str, lemma: str, text: str) -> str:
    stable_key = f"{source_text_id}|{_normalize_text(lemma)}|{_normalize_text(text)}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"con-{digest}"


def _append_candidate(candidates: list[dict[str, Any]], *, source_text_id: str, sentences: list[dict[str, Any]], text: str, lemma: str, source: str, start_offset: int, end_offset: int, confidence: float) -> None:
    sentence_id = _resolve_sentence_id(sentences, start_offset, end_offset)
    candidates.append(
        {
            "concept_id": _build_concept_id(source_text_id, lemma, text),
            "text": text,
            "lemma": lemma,
            "source": source,
            "start_offset": start_offset,
            "end_offset": end_offset,
            "sentence_id": sentence_id,
            "source_text_id": source_text_id,
            "confidence": confidence,
        }
    )


def _collect_noun_chunk_candidates(input_payload: dict[str, Any], doc: Any) -> list[dict[str, Any]]:
    source_text_id = input_payload["source_text_id"]
    sentences = input_payload["sentences"]
    candidates: list[dict[str, Any]] = []
    for chunk in getattr(doc, "noun_chunks", []):
        text = getattr(chunk, "text", "") or ""
        if text.strip() == "":
            continue
        root = getattr(chunk, "root", None)
        lemma = getattr(root, "lemma_", text) if root is not None else text
        _append_candidate(
            candidates,
            source_text_id=source_text_id,
            sentences=sentences,
            text=text,
            lemma=lemma,
            source="noun_chunk",
            start_offset=getattr(chunk, "start_char", 0),
            end_offset=getattr(chunk, "end_char", 0),
            confidence=_BR_CONCEPT_CONFIDENCE_NOUN_CHUNK,
        )
    return candidates


def _collect_entity_label_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload["source_text_id"]
    sentences = input_payload["sentences"]
    candidates: list[dict[str, Any]] = []
    for entity in input_payload.get("entities", []):
        text = entity.get("text", "")
        if not isinstance(text, str) or text.strip() == "":
            continue
        _append_candidate(
            candidates,
            source_text_id=source_text_id,
            sentences=sentences,
            text=text,
            lemma=text,
            source="entity_label",
            start_offset=entity.get("start_offset", 0),
            end_offset=entity.get("end_offset", 0),
            confidence=_BR_CONCEPT_CONFIDENCE_ENTITY_LABEL,
        )
    return candidates


def _collect_noun_token_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload["source_text_id"]
    sentences = input_payload["sentences"]
    candidates: list[dict[str, Any]] = []
    for token in input_payload.get("tokens", []):
        pos = token.get("pos", "")
        if pos not in {"NOUN", "PROPN"}:
            continue
        text = token.get("text", "")
        if not isinstance(text, str) or text.strip() == "":
            continue
        lemma = token.get("lemma", text)
        _append_candidate(
            candidates,
            source_text_id=source_text_id,
            sentences=sentences,
            text=text,
            lemma=lemma,
            source="noun_token",
            start_offset=token.get("start_offset", 0),
            end_offset=token.get("end_offset", 0),
            confidence=_BR_CONCEPT_CONFIDENCE_NOUN_TOKEN,
        )
    return candidates


def _dedupe_deterministic(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for concept in candidates:
        dedupe_key = (_normalize_text(concept["lemma"]), _normalize_text(concept["text"]))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        unique.append(concept)
    return unique


def extract_concepts_from_payload(input_payload: dict[str, Any], doc: Any) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    candidates.extend(_collect_noun_chunk_candidates(input_payload, doc))
    candidates.extend(_collect_entity_label_candidates(input_payload))
    candidates.extend(_collect_noun_token_candidates(input_payload))

    concepts = _dedupe_deterministic(candidates)

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": input_payload["source_text_id"],
        "metadata": input_payload.get("metadata", {}),
        "preprocessed_text": input_payload["preprocessed_text"],
        "operations_applied": input_payload.get("operations_applied", []),
        "sentences": input_payload["sentences"],
        "tokens": input_payload["tokens"],
        "entities": input_payload["entities"],
        "concepts": concepts,
    }
