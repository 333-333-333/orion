"""Orchestrate the relation extraction pipeline stage while preserving the payload contract."""

from __future__ import annotations

from typing import Any

from pipeline.step_008_relation_extraction.rules import _dedupe_stable, _extract_copula_relations, _extract_svo_relations


def extract_relations_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    """Extract and deduplicate SVO and copular relations from the annotated payload."""
    candidates = []
    candidates.extend(_extract_svo_relations(input_payload))
    candidates.extend(_extract_copula_relations(input_payload))
    relations = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['relations'] = relations
    return result
