from __future__ import annotations

from typing import Any

from pipeline.step_012_semantic_quality.rules import _build_concept_noise, _build_entity_noise, _has_overlong_concept, _is_long_text


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
