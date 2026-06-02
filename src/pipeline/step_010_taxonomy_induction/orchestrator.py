from __future__ import annotations

import hashlib
import re
from typing import Any

_BR_TAX_RELATION_TYPE_SUBCLASS_OF = "subclass_of"
_BR_TAX_SOURCE_COPULA_PATTERN = "copula_pattern"
_BR_TAX_SOURCE_SUCH_AS_PATTERN = "such_as_pattern"
_BR_TAX_SOURCE_RELATION_PATTERN = "relation_pattern"
_BR_TAX_CONFIDENCE_COPULA = 0.9
_BR_TAX_CONFIDENCE_SUCH_AS = 0.88
_BR_TAX_CONFIDENCE_RELATION = 0.86

_COPULA_PATTERN = re.compile(r"\b(?P<sub>[A-Za-z][A-Za-z\-]*)\s+(?:is|are)\s+(?:a|an)\s+(?P<sup>[A-Za-z][A-Za-z\-]*)\b", re.IGNORECASE)
_SUCH_AS_PATTERN = re.compile(r"\b(?P<sup>[A-Za-z][A-Za-z\-]*)s?\s+such\s+as\s+(?P<sub>[A-Za-z][A-Za-z\-]*)s?\b", re.IGNORECASE)
_INCLUDING_PATTERN = re.compile(r"\b(?P<sup>[A-Za-z][A-Za-z\-]*)s?\s+including\s+(?P<sub>[A-Za-z][A-Za-z\-]*)s?\b", re.IGNORECASE)


def _normalize_text(value: str | None) -> str:
    return (value or "").casefold().strip()


def _singularize(token: str) -> str:
    text = _normalize_text(token)
    if len(text) > 3 and text.endswith("ies"):
        return text[:-3] + "y"
    if len(text) > 3 and text.endswith("s") and not text.endswith("ss"):
        return text[:-1]
    return text


def _build_taxonomy_relation_id(source_text_id: str, sentence_id: str, subclass: str, superclass: str) -> str:
    stable_key = f"{source_text_id}|{sentence_id}|{subclass}|{superclass}|{_BR_TAX_RELATION_TYPE_SUBCLASS_OF}".encode("utf-8")
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"tax-{digest}"


def _concept_lookup(input_payload: dict[str, Any]) -> dict[str, str]:
    entries: list[tuple[str, str]] = []
    for concept in input_payload.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        concept_id = concept.get("concept_id")
        if not isinstance(concept_id, str) or not concept_id:
            continue
        normalized = _singularize(concept.get("normalized_text") or concept.get("lemma") or concept.get("text"))
        if normalized:
            entries.append((normalized, concept_id))
    entries.sort(key=lambda item: (item[0], item[1]))

    lookup: dict[str, str] = {}
    for normalized, concept_id in entries:
        if normalized not in lookup:
            lookup[normalized] = concept_id
    return lookup


def _entity_text_set(input_payload: dict[str, Any]) -> set[str]:
    values: set[str] = set()
    for entity in input_payload.get("entities", []):
        if not isinstance(entity, dict):
            continue
        normalized = _singularize(entity.get("normalized_text") or entity.get("text"))
        if normalized:
            values.add(normalized)
    return values


def _sentence_span(sentence: dict[str, Any], fallback_text: str) -> dict[str, int]:
    start_offset = sentence.get("start_offset")
    end_offset = sentence.get("end_offset")
    if isinstance(start_offset, int) and isinstance(end_offset, int):
        return {"start_offset": start_offset, "end_offset": end_offset}
    return {"start_offset": 0, "end_offset": len(fallback_text)}


def _is_instance_like(subclass: str, entity_set: set[str], concept_lookup: dict[str, str]) -> bool:
    return subclass in entity_set and subclass not in concept_lookup


def _candidate_from_match(match: re.Match[str], sentence: dict[str, Any], source_text_id: str, concept_lookup: dict[str, str], entity_set: set[str], source: str, confidence: float) -> dict[str, Any] | None:
    subclass = _singularize(match.group("sub"))
    superclass = _singularize(match.group("sup"))
    if not subclass or not superclass:
        return None
    if subclass == superclass:
        return None
    if _is_instance_like(subclass, entity_set, concept_lookup):
        return None

    subclass_ref = concept_lookup.get(subclass)
    superclass_ref = concept_lookup.get(superclass)
    if not subclass_ref or not superclass_ref:
        return None

    sentence_id = sentence.get("sentence_id", "")
    evidence_span = _sentence_span(sentence, sentence.get("text", ""))
    return {
        "taxonomy_relation_id": _build_taxonomy_relation_id(source_text_id, sentence_id, subclass, superclass),
        "subclass": subclass,
        "superclass": superclass,
        "subclass_ref": subclass_ref,
        "superclass_ref": superclass_ref,
        "relation_type": _BR_TAX_RELATION_TYPE_SUBCLASS_OF,
        "source": source,
        "sentence_id": sentence_id,
        "source_text_id": source_text_id,
        "confidence": confidence,
        "evidence_span": evidence_span,
    }


def _extract_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload.get("source_text_id", "")
    concept_lookup = _concept_lookup(input_payload)
    entity_set = _entity_text_set(input_payload)

    candidates: list[dict[str, Any]] = []
    for sentence in input_payload.get("sentences", []):
        if not isinstance(sentence, dict):
            continue
        text = sentence.get("text", "")
        if not isinstance(text, str) or not text.strip():
            continue

        for match in _COPULA_PATTERN.finditer(text):
            candidate = _candidate_from_match(match, sentence, source_text_id, concept_lookup, entity_set, _BR_TAX_SOURCE_COPULA_PATTERN, _BR_TAX_CONFIDENCE_COPULA)
            if candidate is not None:
                candidates.append(candidate)

        for match in _SUCH_AS_PATTERN.finditer(text):
            candidate = _candidate_from_match(match, sentence, source_text_id, concept_lookup, entity_set, _BR_TAX_SOURCE_SUCH_AS_PATTERN, _BR_TAX_CONFIDENCE_SUCH_AS)
            if candidate is not None:
                candidates.append(candidate)

        for match in _INCLUDING_PATTERN.finditer(text):
            candidate = _candidate_from_match(match, sentence, source_text_id, concept_lookup, entity_set, _BR_TAX_SOURCE_RELATION_PATTERN, _BR_TAX_CONFIDENCE_RELATION)
            if candidate is not None:
                candidates.append(candidate)
    return candidates


def _dedupe_stable(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        candidates,
        key=lambda rel: (
            rel.get("sentence_id", ""),
            rel.get("subclass", ""),
            rel.get("superclass", ""),
            rel.get("source", ""),
            rel.get("taxonomy_relation_id", ""),
        ),
    )
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for rel in ordered:
        key = f"{rel.get('subclass','')}|{rel.get('superclass','')}|{rel.get('relation_type','')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(rel)
    return unique


def extract_taxonomy_relations_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    candidates = _extract_candidates(input_payload)
    taxonomy_relations = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith("_spacy")}
    result["taxonomy_relations"] = taxonomy_relations
    return result
