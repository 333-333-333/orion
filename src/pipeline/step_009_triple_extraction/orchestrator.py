from __future__ import annotations

import hashlib
from typing import Any

_BR_TRIPLE_CONFIDENCE_DEFAULT = 0.5


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


def _build_triple_id(source_text_id: str, sentence_id: str, subject: str, predicate: str, obj: str) -> str:
    stable_key = f"{source_text_id}|{sentence_id}|{subject}|{predicate}|{obj}".encode('utf-8')
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"tri-{digest}"


def _build_ref_normalized_lookup(input_payload: dict[str, Any]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for entity in input_payload.get('entities', []):
        entity_id = entity.get('entity_id')
        if isinstance(entity_id, str) and entity_id:
            lookup[entity_id] = _normalize_text(entity.get('normalized_text') or entity.get('text'))
    for concept in input_payload.get('concepts', []):
        concept_id = concept.get('concept_id')
        if isinstance(concept_id, str) and concept_id:
            lookup[concept_id] = _normalize_text(concept.get('normalized_text') or concept.get('lemma') or concept.get('text'))
    return lookup


def _relation_to_triple(relation: dict[str, Any], ref_lookup: dict[str, str]) -> dict[str, Any]:
    relation_id = relation.get('relation_id', '')
    sentence_id = relation.get('sentence_id', '')
    source_text_id = relation.get('source_text_id', '')

    subject_ref = relation.get('subject_ref')
    object_ref = relation.get('object_ref')

    subject = ref_lookup.get(subject_ref, '') if isinstance(subject_ref, str) and subject_ref else ''
    if not subject:
        subject = _normalize_text(relation.get('subject_text'))

    obj = ref_lookup.get(object_ref, '') if isinstance(object_ref, str) and object_ref else ''
    if not obj:
        obj = _normalize_lemma_like(relation.get('object_text'))

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
    relations = input_payload.get('relations', [])
    if not isinstance(relations, list):
        relations = []

    ref_lookup = _build_ref_normalized_lookup(input_payload)
    candidates = [_relation_to_triple(r, ref_lookup) for r in relations if isinstance(r, dict) and r.get('relation_id')]
    triples = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['triples'] = triples
    return result
