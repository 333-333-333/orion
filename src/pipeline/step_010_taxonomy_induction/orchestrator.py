from __future__ import annotations

from typing import Any

from pipeline.step_010_taxonomy_induction.rules import _dedupe_stable, _extract_candidates


def extract_taxonomy_relations_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    candidates = _extract_candidates(input_payload)
    taxonomy_relations = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['taxonomy_relations'] = taxonomy_relations
    return result
