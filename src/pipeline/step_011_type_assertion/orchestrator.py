"""Orchestrate the type assertion pipeline stage while preserving the payload contract."""

from __future__ import annotations

import hashlib
import re
from typing import Any

from pipeline.step_011_type_assertion.rules import (
    _concept_lookup,
    _dedupe_stable,
    _entity_lookup,
    _extract_from_copula,
    _extract_from_entity_label,
    _extract_from_relation_pattern,
)


def _claim_term(value: Any) -> str:
    """Normalize a canonical claim endpoint to the type-assertion label form."""
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', str(value or ''))
    return re.sub(r'[^a-z0-9]+', ' ', spaced.casefold()).strip()


def _claim_type_assertions(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Project explicit ``instance_of`` claims without re-generalizing their evidence."""
    artifact = input_payload.get('semantic_claims')
    if not isinstance(artifact, dict):
        artifact = input_payload.get('canonical_claims')
    claims = artifact.get('claims', []) if isinstance(artifact, dict) else []
    raw_text = str(input_payload.get('raw_text', ''))
    assertions: list[dict[str, Any]] = []
    for claim in claims if isinstance(claims, list) else []:
        if not isinstance(claim, dict) or claim.get('predicate') != 'instance_of':
            continue
        instance = _claim_term(claim.get('subject'))
        class_name = _claim_term(claim.get('object'))
        claim_id = str(claim.get('claim_id', ''))
        source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
        source_text_id = str(source.get('source_text_id', ''))
        sentence_id = str(source.get('sentence_id', ''))
        evidence = str(source.get('evidence', ''))
        start = raw_text.find(evidence) if evidence else -1
        if not instance or not class_name or not claim_id:
            continue
        stable = f'{source_text_id}|{sentence_id}|{instance}|{class_name}|canonical_claim'
        assertions.append({
            'type_assertion_id': f"ta-{hashlib.sha256(stable.encode('utf-8')).hexdigest()[:16]}",
            'instance': instance,
            'class': class_name,
            'instance_ref': claim_id,
            'class_ref': claim_id,
            'relation_type': 'instance_of',
            'source': 'canonical_claim',
            'sentence_id': sentence_id,
            'source_text_id': source_text_id,
            'confidence': 0.95,
            'evidence_span': {
                'start_offset': start if start >= 0 else 0,
                'end_offset': start + len(evidence) if start >= 0 else 0,
            },
            'claim_id': claim_id,
        })
    return assertions


def extract_type_assertions_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    """Extract and deduplicate instance-to-class assertions from available linguistic evidence."""
    concept_lookup = _concept_lookup(input_payload)
    entity_lookup = _entity_lookup(input_payload)

    candidates = _claim_type_assertions(input_payload)
    if not candidates:
        candidates.extend(_extract_from_copula(input_payload, concept_lookup, entity_lookup))
        candidates.extend(_extract_from_entity_label(input_payload, concept_lookup))
        candidates.extend(_extract_from_relation_pattern(input_payload, concept_lookup, entity_lookup))
    type_assertions = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['type_assertions'] = type_assertions
    return result
