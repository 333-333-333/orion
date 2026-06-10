from __future__ import annotations

from typing import Any

from pipeline.step_011_type_assertion.rules import (
    _concept_lookup,
    _dedupe_stable,
    _entity_lookup,
    _extract_from_copula,
    _extract_from_entity_label,
    _extract_from_relation_pattern,
    _extract_from_short_taxonomy_subjects,
)


def extract_type_assertions_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    concept_lookup = _concept_lookup(input_payload)
    entity_lookup = _entity_lookup(input_payload)

    candidates: list[dict[str, Any]] = []
    candidates.extend(_extract_from_copula(input_payload, concept_lookup, entity_lookup))
    candidates.extend(_extract_from_entity_label(input_payload, concept_lookup))
    candidates.extend(_extract_from_relation_pattern(input_payload, concept_lookup, entity_lookup))
    candidates.extend(_extract_from_short_taxonomy_subjects(input_payload))
    type_assertions = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['type_assertions'] = type_assertions
    return result
