"""Orchestrate the taxonomy induction pipeline stage while preserving the payload contract."""

from __future__ import annotations

import hashlib
from typing import Any

from pipeline.step_010_taxonomy_induction.rules import _dedupe_stable, _extract_candidates


def _claim_taxonomy_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Build subclass candidates directly from accepted semantic claims."""
    artifact = input_payload.get('semantic_claims')
    if not isinstance(artifact, dict):
        artifact = input_payload.get('canonical_claims')
    claims = artifact.get('claims', []) if isinstance(artifact, dict) else []
    candidates: list[dict[str, Any]] = []
    for claim in claims if isinstance(claims, list) else []:
        if (
            not isinstance(claim, dict)
            or claim.get('predicate') not in {'is_a', 'type_of'}
            or claim.get('condition')
        ):
            continue
        subclass = str(claim.get('subject', '')).strip()
        superclass = str(claim.get('object', '')).strip()
        source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
        evidence = str(source.get('evidence', '')).strip()
        raw_text = str(input_payload.get('raw_text', ''))
        evidence_start = raw_text.find(evidence) if evidence else -1
        evidence_span = {
            'start_offset': evidence_start,
            'end_offset': evidence_start + len(evidence),
        } if evidence_start >= 0 else {'start_offset': 0, 'end_offset': 0}
        if not subclass or not superclass or subclass == superclass:
            continue
        stable = f"{source.get('source_text_id', '')}|{source.get('sentence_id', '')}|{subclass}|{superclass}"
        candidates.append({
            'taxonomy_relation_id': f"tax-{hashlib.sha256(stable.encode('utf-8')).hexdigest()[:16]}",
            'subclass': subclass,
            'superclass': superclass,
            'subclass_ref': claim.get('claim_id', ''),
            'superclass_ref': claim.get('claim_id', ''),
            'relation_type': 'subclass_of',
            'source': 'canonical_claim',
            'sentence_id': str(source.get('sentence_id', '')),
            'source_text_id': str(source.get('source_text_id', '')),
            'confidence': 0.95,
            'evidence_span': evidence_span,
            'claim_id': claim.get('claim_id', ''),
        })
    return candidates


def extract_taxonomy_relations_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    """Project claim taxonomy first, falling back to pattern-derived taxonomy when necessary."""
    candidates = _claim_taxonomy_candidates(input_payload)
    artifact = input_payload.get('semantic_claims')
    if not isinstance(artifact, dict):
        artifact = input_payload.get('canonical_claims')
    accepted_claims = artifact.get('claims', []) if isinstance(artifact, dict) else []
    # Accepted semantic claims are authoritative, including an intentional absence of taxonomy.
    # Falling back here would turn example-level ``instance_of`` statements into subclasses.
    if not candidates and not accepted_claims:
        candidates = _extract_candidates(input_payload)
    taxonomy_relations = _dedupe_stable(candidates)

    artifact = input_payload.get('semantic_claims')
    if not isinstance(artifact, dict):
        artifact = input_payload.get('canonical_claims') if isinstance(input_payload.get('canonical_claims'), dict) else {}
    conditional_taxonomy_relations = [
        {
            'subclass': str(claim.get('subject', '')),
            'superclass': str(claim.get('object', '')),
            'relation_type': 'conditional_subclass_of',
            'claim_id': str(claim.get('claim_id', '')),
            **{
                key: str(claim[key])
                for key in (
                    'condition', 'condition_subject', 'condition_predicate',
                    'condition_modality', 'condition_polarity', 'condition_voice',
                )
                if claim.get(key) not in (None, '')
            },
        }
        for claim in artifact.get('claims', [])
        if isinstance(claim, dict) and claim.get('predicate') in {'is_a', 'type_of'} and claim.get('condition')
    ]

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['taxonomy_relations'] = taxonomy_relations
    result['conditional_taxonomy_relations'] = conditional_taxonomy_relations
    return result
