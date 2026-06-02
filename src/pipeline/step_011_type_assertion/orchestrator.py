from __future__ import annotations

import hashlib
import re
from typing import Any

_BR_TYPE_RELATION_INSTANCE_OF = "instance_of"
_BR_TYPE_SOURCE_COPULA_PATTERN = "copula_pattern"
_BR_TYPE_SOURCE_ENTITY_LABEL = "entity_label"
_BR_TYPE_SOURCE_RELATION_PATTERN = "relation_pattern"
_BR_TYPE_CONFIDENCE_COPULA = 0.9
_BR_TYPE_CONFIDENCE_ENTITY_LABEL = 0.92
_BR_TYPE_CONFIDENCE_RELATION_PATTERN = 0.86
_BR_TYPE_ENTITY_LABEL_TO_CLASS = {
    "PERSON": "person",
    "ORG": "organization",
}

_COPULA_PATTERN = re.compile(
    r"\b(?P<instance>[A-Za-z][A-Za-z\-]*)\s+(?:is|are)\s+(?:a|an)\s+(?P<class>[A-Za-z][A-Za-z\-]*)\b",
    re.IGNORECASE,
)


def _normalize_text(value: str | None) -> str:
    return (value or "").casefold().strip()


def _build_type_assertion_id(source_text_id: str, sentence_id: str, instance: str, class_name: str, source: str) -> str:
    stable_key = f"{source_text_id}|{sentence_id}|{instance}|{class_name}|{_BR_TYPE_RELATION_INSTANCE_OF}|{source}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"ta-{digest}"


def _concept_lookup(input_payload: dict[str, Any]) -> dict[str, str]:
    ordered: list[tuple[str, str]] = []
    for concept in input_payload.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        concept_id = concept.get("concept_id")
        normalized = _normalize_text(concept.get("normalized_text") or concept.get("lemma") or concept.get("text"))
        if isinstance(concept_id, str) and concept_id and normalized:
            ordered.append((normalized, concept_id))
    ordered.sort(key=lambda item: (item[0], item[1]))

    lookup: dict[str, str] = {}
    for normalized, concept_id in ordered:
        if normalized not in lookup:
            lookup[normalized] = concept_id
    return lookup


def _entity_lookup(input_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entities: list[tuple[str, dict[str, Any]]] = []
    for entity in input_payload.get("entities", []):
        if not isinstance(entity, dict):
            continue
        normalized = _normalize_text(entity.get("normalized_text") or entity.get("text"))
        entity_id = entity.get("entity_id")
        if normalized and isinstance(entity_id, str) and entity_id:
            entities.append((normalized, entity))
    entities.sort(key=lambda item: (item[0], item[1].get("entity_id", "")))

    lookup: dict[str, dict[str, Any]] = {}
    for normalized, entity in entities:
        if normalized not in lookup:
            lookup[normalized] = entity
    return lookup


def _sentence_span(sentence: dict[str, Any], fallback_text: str) -> dict[str, int]:
    start_offset = sentence.get("start_offset")
    end_offset = sentence.get("end_offset")
    if isinstance(start_offset, int) and isinstance(end_offset, int):
        return {"start_offset": start_offset, "end_offset": end_offset}
    return {"start_offset": 0, "end_offset": len(fallback_text)}


def _build_type_assertion(*, source_text_id: str, sentence_id: str, instance: str, class_name: str, instance_ref: str, class_ref: str, source: str, confidence: float, evidence_span: dict[str, int]) -> dict[str, Any]:
    return {
        "type_assertion_id": _build_type_assertion_id(source_text_id, sentence_id, instance, class_name, source),
        "instance": instance,
        "class": class_name,
        "instance_ref": instance_ref,
        "class_ref": class_ref,
        "relation_type": _BR_TYPE_RELATION_INSTANCE_OF,
        "source": source,
        "sentence_id": sentence_id,
        "source_text_id": source_text_id,
        "confidence": confidence,
        "evidence_span": evidence_span,
    }


def _extract_from_copula(input_payload: dict[str, Any], concept_lookup: dict[str, str], entity_lookup: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    source_text_id = input_payload.get("source_text_id", "")
    candidates: list[dict[str, Any]] = []

    for sentence in input_payload.get("sentences", []):
        if not isinstance(sentence, dict):
            continue
        text = sentence.get("text", "")
        if not isinstance(text, str) or not text.strip():
            continue
        sentence_id = sentence.get("sentence_id", "")

        for match in _COPULA_PATTERN.finditer(text):
            instance = _normalize_text(match.group("instance"))
            class_name = _normalize_text(match.group("class"))
            if not instance or not class_name or instance == class_name:
                continue
            entity = entity_lookup.get(instance)
            class_ref = concept_lookup.get(class_name)
            if entity is None or class_ref is None:
                continue
            instance_ref = entity.get("entity_id", "")
            if not isinstance(instance_ref, str) or not instance_ref:
                continue
            candidates.append(
                _build_type_assertion(
                    source_text_id=source_text_id,
                    sentence_id=sentence_id,
                    instance=instance,
                    class_name=class_name,
                    instance_ref=instance_ref,
                    class_ref=class_ref,
                    source=_BR_TYPE_SOURCE_COPULA_PATTERN,
                    confidence=_BR_TYPE_CONFIDENCE_COPULA,
                    evidence_span=_sentence_span(sentence, text),
                )
            )
    return candidates


def _extract_from_entity_label(input_payload: dict[str, Any], concept_lookup: dict[str, str]) -> list[dict[str, Any]]:
    source_text_id = input_payload.get("source_text_id", "")
    candidates: list[dict[str, Any]] = []

    for entity in input_payload.get("entities", []):
        if not isinstance(entity, dict):
            continue
        entity_id = entity.get("entity_id")
        if not isinstance(entity_id, str) or not entity_id:
            continue
        class_name = _BR_TYPE_ENTITY_LABEL_TO_CLASS.get(entity.get("label"))
        if class_name is None:
            continue
        class_ref = concept_lookup.get(class_name)
        if class_ref is None:
            continue
        sentence_id = entity.get("sentence_id", "")
        candidates.append(
            _build_type_assertion(
                source_text_id=source_text_id,
                sentence_id=sentence_id,
                instance=_normalize_text(entity.get("normalized_text") or entity.get("text")),
                class_name=class_name,
                instance_ref=entity_id,
                class_ref=class_ref,
                source=_BR_TYPE_SOURCE_ENTITY_LABEL,
                confidence=_BR_TYPE_CONFIDENCE_ENTITY_LABEL,
                evidence_span={"start_offset": 0, "end_offset": 0},
            )
        )
    return candidates


def _extract_from_relation_pattern(input_payload: dict[str, Any], concept_lookup: dict[str, str], entity_lookup: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    source_text_id = input_payload.get("source_text_id", "")
    candidates: list[dict[str, Any]] = []

    for relation in input_payload.get("relations", []):
        if not isinstance(relation, dict):
            continue
        relation_type = _normalize_text(relation.get("relation_type") or relation.get("predicate") or relation.get("label"))
        if relation_type not in {"is_a", "instance_of", "type"}:
            continue

        instance = _normalize_text(relation.get("subject") or relation.get("subject_text") or relation.get("source") or relation.get("head"))
        class_name = _normalize_text(relation.get("object") or relation.get("object_text") or relation.get("target") or relation.get("tail"))
        if not instance or not class_name or instance == class_name:
            continue

        entity = entity_lookup.get(instance)
        class_ref = concept_lookup.get(class_name)
        if entity is None or class_ref is None:
            continue

        instance_ref = entity.get("entity_id", "")
        if not isinstance(instance_ref, str) or not instance_ref:
            continue

        sentence_id = relation.get("sentence_id") or entity.get("sentence_id", "")
        candidates.append(
            _build_type_assertion(
                source_text_id=source_text_id,
                sentence_id=sentence_id,
                instance=instance,
                class_name=class_name,
                instance_ref=instance_ref,
                class_ref=class_ref,
                source=_BR_TYPE_SOURCE_RELATION_PATTERN,
                confidence=_BR_TYPE_CONFIDENCE_RELATION_PATTERN,
                evidence_span={"start_offset": 0, "end_offset": 0},
            )
        )
    return candidates


def _dedupe_stable(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        candidates,
        key=lambda item: (
            item.get("instance", ""),
            item.get("class", ""),
            item.get("relation_type", ""),
            item.get("source", ""),
            item.get("sentence_id", ""),
            item.get("type_assertion_id", ""),
        ),
    )

    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in ordered:
        key = f"{item.get('instance','')}|{item.get('class','')}|{item.get('relation_type','')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def extract_type_assertions_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    concept_lookup = _concept_lookup(input_payload)
    entity_lookup = _entity_lookup(input_payload)

    candidates: list[dict[str, Any]] = []
    candidates.extend(_extract_from_copula(input_payload, concept_lookup, entity_lookup))
    candidates.extend(_extract_from_entity_label(input_payload, concept_lookup))
    candidates.extend(_extract_from_relation_pattern(input_payload, concept_lookup, entity_lookup))

    result = {k: v for k, v in input_payload.items() if not k.startswith("_spacy")}
    result["type_assertions"] = _dedupe_stable(candidates)
    return result
