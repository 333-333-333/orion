from __future__ import annotations

import hashlib
import re
from typing import Any

_BR_TRIPLE_CONFIDENCE_DEFAULT = 0.5
_TAXONOMY_SCAFFOLD_HEADS = {'type', 'kind', 'category', 'form'}
_CLAUSE_STOP_WORDS = {'that', 'which', 'who', 'whom', 'whose', 'where', 'when'}
_CLAUSE_CONNECTORS = {'to', 'by', 'for', 'with', 'from', 'in', 'on', 'at'}
_OBJECT_HEADS = {'requirement', 'control'}


def _normalize_text(value: str | None) -> str:
    return (value or '').casefold().strip()


def _normalize_lemma_like(value: str | None) -> str:
    text = _normalize_text(value)
    if not text:
        return text
    if len(text) > 4 and text.endswith('ied'):
        return text[:-3] + 'y'
    if len(text) > 4 and text.endswith('ies'):
        return text[:-3] + 'y'
    if len(text) > 4 and text.endswith('ing'):
        base = text[:-3]
        if len(base) > 2 and base[-1] == base[-2]:
            base = base[:-1]
        return base
    if len(text) > 3 and text.endswith('ed'):
        base = text[:-2]
        if len(base) > 2 and base[-1] == base[-2]:
            base = base[:-1]
        return base
    if len(text) > 3 and text.endswith('s') and not text.endswith('ss'):
        return text[:-1]
    return text


def _normalize_fact_phrase(value: str | None) -> str:
    text = re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value or ''))
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return ''
    return ' '.join(_normalize_lemma_like(token) for token in text.split(' ') if token)


def _canonicalize_head_phrase(value: str | None) -> str:
    tokens = [token for token in _normalize_text(value or '').split(' ') if token]
    if not tokens:
        return ''
    while tokens and tokens[0] in {'a', 'an', 'the'}:
        tokens.pop(0)
    if len(tokens) >= 2 and tokens[0] in _TAXONOMY_SCAFFOLD_HEADS and tokens[1] == 'of':
        tokens = tokens[2:]
    if not tokens:
        return ''

    result: list[str] = []
    for index, token in enumerate(tokens):
        if not result and token in {'a', 'an', 'the'}:
            continue
        if result:
            if token in _CLAUSE_STOP_WORDS:
                break
            if len(token) > 4 and token.endswith(('ed', 'ing', 'en')):
                next_token = tokens[index + 1] if index + 1 < len(tokens) else ''
                if not next_token or next_token in _CLAUSE_CONNECTORS or next_token in _CLAUSE_STOP_WORDS:
                    break
        result.append(token)
    return ' '.join(result)


def _canonicalize_relation_object(value: str | None) -> str:
    normalized = _normalize_fact_phrase(value)
    if not normalized:
        return ''

    tokens = normalized.split(' ')
    for token in reversed(tokens):
        if token in _OBJECT_HEADS:
            return token
    return normalized


def _build_triple_id(source_text_id: str, sentence_id: str, subject: str, predicate: str, obj: str) -> str:
    stable_key = f"{source_text_id}|{sentence_id}|{subject}|{predicate}|{obj}".encode('utf-8')
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"tri-{digest}"


def _build_ref_normalized_lookup(input_payload: dict[str, Any]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for entity in input_payload.get('entities', []):
        entity_id = entity.get('entity_id')
        if isinstance(entity_id, str) and entity_id:
            lookup[entity_id] = _normalize_fact_phrase(entity.get('normalized_text') or entity.get('text'))
    for concept in input_payload.get('concepts', []):
        concept_id = concept.get('concept_id')
        if isinstance(concept_id, str) and concept_id:
            lookup[concept_id] = _normalize_fact_phrase(
                concept.get('normalized_text') or concept.get('lemma') or concept.get('text')
            )
    return lookup


def _relation_to_triple(relation: dict[str, Any], ref_lookup: dict[str, str]) -> dict[str, Any]:
    relation_id = relation.get('relation_id', '')
    sentence_id = relation.get('sentence_id', '')
    source_text_id = relation.get('source_text_id', '')

    subject_ref = relation.get('subject_ref')
    object_ref = relation.get('object_ref')

    subject = ref_lookup.get(subject_ref, '') if isinstance(subject_ref, str) and subject_ref else ''
    if not subject:
        subject = _normalize_fact_phrase(relation.get('subject_text'))

    obj = ref_lookup.get(object_ref, '') if isinstance(object_ref, str) and object_ref else ''
    if not obj:
        obj = relation.get('object_text')
    obj = _canonicalize_relation_object(obj)

    raw_predicate = _normalize_text(relation.get('predicate'))
    if raw_predicate in {'satisfied_by', 'satisfiedby'}:
        predicate = 'satisfiedBy'
    else:
        predicate = _normalize_lemma_like(raw_predicate)

    triple = {
        'triple_id': _build_triple_id(source_text_id, sentence_id, subject, predicate, obj),
        'subject': subject,
        'predicate': predicate,
        'object': obj,
        'subject_ref': subject_ref if subject_ref is not None else None,
        'predicate_ref': relation_id,
        'object_ref': object_ref if object_ref is not None else None,
        'relation_id': relation_id,
        'sentence_id': sentence_id,
        'source_text_id': source_text_id,
        'confidence': relation.get('confidence', _BR_TRIPLE_CONFIDENCE_DEFAULT),
        'evidence_span': relation.get('evidence_span', {'start_offset': 0, 'end_offset': 0}),
    }
    return triple



def _claim_to_triple(claim: dict[str, Any]) -> dict[str, Any]:
    source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
    subject = _normalize_fact_phrase(claim.get('subject'))
    predicate = _normalize_lemma_like(_normalize_text(claim.get('predicate')))
    obj = _normalize_fact_phrase(claim.get('object'))
    sentence_id = str(source.get('sentence_id') or claim.get('sentence_id') or '')
    source_text_id = str(source.get('source_text_id') or claim.get('source_text_id') or '')
    return {
        'triple_id': _build_triple_id(source_text_id, sentence_id, subject, predicate, obj),
        'subject': subject,
        'predicate': predicate,
        'object': obj,
        'subject_ref': claim.get('claim_id'),
        'predicate_ref': claim.get('claim_id'),
        'object_ref': claim.get('claim_id'),
        'relation_id': claim.get('claim_id'),
        'sentence_id': sentence_id,
        'source_text_id': source_text_id,
        'confidence': 0.95,
        'evidence_span': {'start_offset': 0, 'end_offset': 0},
    }


def _dedupe_stable(triples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        triples,
        key=lambda t: (
            t.get('sentence_id', ''),
            t.get('subject', ''),
            t.get('predicate', ''),
            t.get('object', ''),
            t.get('relation_id', ''),
            t.get('triple_id', ''),
        ),
    )
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for triple in ordered:
        key = f"{triple.get('subject','')}|{triple.get('predicate','')}|{triple.get('object','')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(triple)
    return unique


def extract_triples_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    semantic = input_payload.get('semantic_claims')
    claims = semantic.get('claims', []) if isinstance(semantic, dict) else []
    if isinstance(claims, list) and claims:
        candidates = [
            _claim_to_triple(claim)
            for claim in claims
            if (
                isinstance(claim, dict)
                and claim.get('claim_id')
                and claim.get('subject')
                and claim.get('predicate')
                and claim.get('object')
            )
        ]
    else:
        relations = input_payload.get('relations', [])
        if not isinstance(relations, list):
            relations = []
        ref_lookup = _build_ref_normalized_lookup(input_payload)
        candidates = [
            _relation_to_triple(relation, ref_lookup)
            for relation in relations
            if isinstance(relation, dict) and relation.get('relation_id')
        ]
    triples = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['triples'] = triples
    return result
