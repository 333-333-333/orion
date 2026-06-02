from __future__ import annotations

from typing import Any

_BR_SQ_TECH_ACRONYMS = {"CIA", "API", "RDF", "OWL", "IAM", "MFA", "SAST", "DAST"}
_BR_SQ_GENERIC_SUPERCLASSES = {"type", "thing", "collection", "factor"}
_BR_SQ_LONG_CONCEPT_TEXT_THRESHOLD = 256
_BR_SQ_LONG_TEXT_WARNING_THRESHOLD = 120


def _normalize(value: str | None) -> str:
    return (value or "").strip()


def _normalize_casefold(value: str | None) -> str:
    return _normalize(value).casefold()


def _is_long_text(payload: dict[str, Any]) -> bool:
    raw_text = payload.get("raw_text")
    if not isinstance(raw_text, str):
        return False
    return len(raw_text.strip()) >= _BR_SQ_LONG_TEXT_WARNING_THRESHOLD


def _has_overlong_concept(payload: dict[str, Any]) -> bool:
    for concept in payload.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        concept_text = _normalize(concept.get("text") or concept.get("normalized_text") or concept.get("lemma"))
        if len(concept_text) >= _BR_SQ_LONG_CONCEPT_TEXT_THRESHOLD:
            return True
    return False


def _build_entity_noise(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    noise: list[dict[str, Any]] = []
    excluded_entities: list[str] = []
    for entity in payload.get("entities", []):
        if not isinstance(entity, dict):
            continue
        label = _normalize(entity.get("label"))
        text = _normalize(entity.get("text"))
        normalized_text = _normalize(entity.get("normalized_text"))
        candidate = text or normalized_text
        if label != "ORG" or not candidate:
            continue
        if candidate.upper() not in _BR_SQ_TECH_ACRONYMS:
            continue
        noise.append({
            "entity_id": entity.get("entity_id"),
            "text": text or normalized_text,
            "normalized_text": normalized_text or _normalize_casefold(text),
            "label": label,
            "reason": "technical_acronym_misclassified_as_org",
        })
        excluded_entities.append(text or normalized_text)
    return noise, list(dict.fromkeys(excluded_entities))


def _build_concept_noise(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    noise: list[dict[str, Any]] = []
    excluded_concepts: list[str] = []
    for concept in payload.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        concept_text = _normalize(concept.get("text"))
        normalized_text = _normalize(concept.get("normalized_text") or concept.get("lemma") or concept.get("text"))
        superclass = _normalize_casefold(concept.get("superclass"))

        if concept_text.startswith("#"):
            noise.append({"concept_id": concept.get("concept_id"), "text": concept_text, "normalized_text": normalized_text, "reason": "header_chunk_noise"})
            excluded_concepts.append(concept_text)

        if len(concept_text or normalized_text) >= _BR_SQ_LONG_CONCEPT_TEXT_THRESHOLD:
            noise.append({"concept_id": concept.get("concept_id"), "text": concept_text, "normalized_text": normalized_text, "reason": "overlong_chunk_noise"})
            excluded_concepts.append(concept_text or normalized_text)

        if superclass in _BR_SQ_GENERIC_SUPERCLASSES:
            noise.append({"concept_id": concept.get("concept_id"), "text": concept_text, "normalized_text": normalized_text, "superclass": superclass, "reason": "generic_superclass_noise"})
            excluded_concepts.append(superclass)
            if normalized_text:
                excluded_concepts.append(normalized_text)

    return noise, list(dict.fromkeys([value for value in excluded_concepts if value]))


def assess_semantic_quality_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    entity_noise, excluded_entities = _build_entity_noise(input_payload)
    concept_noise, excluded_concepts = _build_concept_noise(input_payload)

    warnings: list[str] = []
    relation_gaps: list[str] = []

    relations_value = input_payload.get("relations", [])
    triples_value = input_payload.get("triples", [])
    relations_count = len(relations_value) if isinstance(relations_value, list) else 0
    triples_count = len(triples_value) if isinstance(triples_value, list) else 0

    long_text = _is_long_text(input_payload) or _has_overlong_concept(input_payload)
    if long_text and relations_count == 0:
        warnings.append("long_text_without_relations")
        relation_gaps.append("no_relations_detected_in_long_text")

    if long_text and triples_count == 0:
        warnings.append("long_text_without_triples")
        relation_gaps.append("no_triples_detected_in_long_text")

    rdf_readiness = bool(input_payload.get("type_assertions") or input_payload.get("taxonomy_relations") or input_payload.get("triples"))

    noise_count = len(entity_noise) + len(concept_noise)
    quality_score = max(0.0, round(1.0 - min(1.0, noise_count / 20.0), 3))

    semantic_quality_report = {
        "entity_noise": entity_noise,
        "concept_noise": concept_noise,
        "relation_gaps": relation_gaps,
        "rdf_readiness": rdf_readiness,
        "warnings": warnings,
        "quality_score": quality_score,
        "excluded_entities": excluded_entities,
        "excluded_concepts": excluded_concepts,
    }

    result = {k: v for k, v in input_payload.items() if not k.startswith("_spacy")}
    result["semantic_quality_report"] = semantic_quality_report
    result["excluded_entities"] = excluded_entities
    result["excluded_concepts"] = excluded_concepts
    return result
