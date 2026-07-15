"""Infer guarded instance-to-class assertions from available evidence."""

from __future__ import annotations

import hashlib
import re
from typing import Any

_BR_TYPE_RELATION_INSTANCE_OF = 'instance_of'
_BR_TYPE_SOURCE_COPULA_PATTERN = 'copula_pattern'
_BR_TYPE_SOURCE_ENTITY_LABEL = 'entity_label'
_BR_TYPE_SOURCE_RELATION_PATTERN = 'relation_pattern'
_BR_TYPE_CONFIDENCE_COPULA = 0.9
_BR_TYPE_CONFIDENCE_ENTITY_LABEL = 0.92
_BR_TYPE_CONFIDENCE_RELATION_PATTERN = 0.86
_BR_TYPE_ENTITY_LABEL_TO_CLASS = {
    'PERSON': 'person',
    'ORG': 'organization',
}
_PHRASE_ARTICLES = {'a', 'an', 'the'}

_COPULA_PATTERN = re.compile(
    r'\b(?P<instance>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)\s+(?:is|are)\s+(?:a|an|the)\s+(?P<class>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)\b',
    re.IGNORECASE,
)


def _normalize_text(value: str | None) -> str:
    """Normalize text."""
    return (value or '').casefold().strip()


def _strip_leading_articles(value: str) -> str:
    """Remove leading articles."""
    tokens = [token for token in value.split(' ') if token]
    while tokens and tokens[0] in _PHRASE_ARTICLES:
        tokens.pop(0)
    return ' '.join(tokens)


def _singularize_token(token: str) -> str:
    """Apply the deterministic, suffix-based singularization rules to one token."""
    if len(token) > 3 and token.endswith('ies'):
        return token[:-3] + 'y'
    if len(token) > 4 and token.endswith(('ses', 'xes', 'zes', 'ches', 'shes')):
        return token[:-2]
    if len(token) > 3 and token.endswith('s') and not token.endswith(('ss', 'us', 'is')):
        return token[:-1]
    return token


def _normalize_phrase(value: str | None) -> str:
    """Normalize phrase."""
    normalized = re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value or ''))
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    normalized = _strip_leading_articles(normalized)
    return ' '.join(_singularize_token(token) for token in normalized.split(' ') if token)


def _phrase_tokens(value: str | None) -> list[str]:
    """Return normalized content tokens for phrase comparison."""
    return [token for token in _normalize_phrase(value).split(' ') if token and token not in _PHRASE_ARTICLES]


def _phrase_match_score(query: str | None, candidate: str | None) -> float:
    """Score normalized phrase overlap for deterministic reference resolution."""
    normalized_query = _normalize_phrase(query)
    normalized_candidate = _normalize_phrase(candidate)
    if not normalized_query or not normalized_candidate:
        return 0.0
    if normalized_query == normalized_candidate:
        return 1.0

    query_tokens = _phrase_tokens(normalized_query)
    candidate_tokens = _phrase_tokens(normalized_candidate)
    if not query_tokens or not candidate_tokens:
        return 0.0
    if query_tokens == candidate_tokens:
        return 0.98

    query_join = ' '.join(query_tokens)
    candidate_join = ' '.join(candidate_tokens)
    if query_join and f' {query_join} ' in f' {candidate_join} ':
        return 0.92

    # Expanded phrases may add modifiers, so containment outranks incidental overlap.
    query_set = set(query_tokens)
    candidate_set = set(candidate_tokens)
    if query_set <= candidate_set:
        return round(0.85 + (0.1 * (len(query_set) / max(len(candidate_set), 1))), 6)
    if candidate_set <= query_set:
        return round(0.75 + (0.05 * (len(candidate_set) / max(len(query_set), 1))), 6)

    overlap = len(query_set & candidate_set)
    if overlap:
        return round(0.5 + (0.4 * (overlap / max(len(query_set), len(candidate_set)))), 6)
    return 0.0


def _build_type_assertion_id(source_text_id: str, sentence_id: str, instance: str, class_name: str, source: str) -> str:
    """Build type assertion ID."""
    stable_key = f"{source_text_id}|{sentence_id}|{instance}|{class_name}|{_BR_TYPE_RELATION_INSTANCE_OF}|{source}".encode('utf-8')
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f'ta-{digest}'


def _concept_lookup(input_payload: dict[str, Any]) -> dict[str, str]:
    """Build a deterministic normalized-concept lookup."""
    entries: list[tuple[str, str]] = []
    for concept in input_payload.get('concepts', []):
        if not isinstance(concept, dict):
            continue
        concept_id = concept.get('concept_id')
        if not isinstance(concept_id, str) or not concept_id:
            continue
        for value in (concept.get('normalized_text'), concept.get('lemma'), concept.get('text')):
            normalized = _normalize_phrase(value if isinstance(value, str) else None)
            if normalized:
                entries.append((normalized, concept_id))
    entries.sort(key=lambda item: (item[0], item[1]))

    lookup: dict[str, str] = {}
    for normalized, concept_id in entries:
        if normalized not in lookup:
            lookup[normalized] = concept_id
    return lookup


def _entity_lookup(input_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Build a deterministic normalized-entity lookup."""
    entities: list[tuple[str, dict[str, Any]]] = []
    for entity in input_payload.get('entities', []):
        if not isinstance(entity, dict):
            continue
        normalized = _normalize_phrase(entity.get('normalized_text') or entity.get('text'))
        entity_id = entity.get('entity_id')
        if normalized and isinstance(entity_id, str) and entity_id:
            entities.append((normalized, entity))
    entities.sort(key=lambda item: (item[0], item[1].get('entity_id', '')))

    lookup: dict[str, dict[str, Any]] = {}
    for normalized, entity in entities:
        if normalized not in lookup:
            lookup[normalized] = entity
    return lookup


def _resolve_phrase_lookup(value: str | None, lookup: dict[str, Any]) -> Any:
    """Resolve phrase lookup."""
    normalized_query = _normalize_phrase(value)
    if not normalized_query:
        return None
    direct = lookup.get(normalized_query)
    if direct is not None:
        return direct

    best_value: Any = None
    best_score = 0.0
    best_size = 10 ** 9
    for normalized_candidate, candidate_value in lookup.items():
        score = _phrase_match_score(normalized_query, normalized_candidate)
        if score > best_score or (score == best_score and len(_phrase_tokens(normalized_candidate)) < best_size):
            best_score = score
            best_size = len(_phrase_tokens(normalized_candidate))
            best_value = candidate_value
    # A missing assertion is safer than assigning an instance through a weak fuzzy match.
    return best_value if best_score >= 0.75 else None


def _is_taxonomy_scaffold(value: str | None) -> bool:
    """Return whether a label is a type, kind, category, or form-of scaffold."""
    tokens = _phrase_tokens(value)
    return len(tokens) >= 3 and tokens[0] in {'type', 'kind', 'category', 'form'} and tokens[1] == 'of'


def _sentence_span(sentence: dict[str, Any], fallback_text: str) -> dict[str, int]:
    """Return sentence offsets, falling back to the supplied text length."""
    start_offset = sentence.get('start_offset')
    end_offset = sentence.get('end_offset')
    if isinstance(start_offset, int) and isinstance(end_offset, int):
        return {'start_offset': start_offset, 'end_offset': end_offset}
    return {'start_offset': 0, 'end_offset': len(fallback_text)}


def _build_type_assertion(*, source_text_id: str, sentence_id: str, instance: str, class_name: str, instance_ref: str, class_ref: str, source: str, confidence: float, evidence_span: dict[str, int]) -> dict[str, Any]:
    """Build type assertion."""
    return {
        'type_assertion_id': _build_type_assertion_id(source_text_id, sentence_id, instance, class_name, source),
        'instance': instance,
        'class': class_name,
        'instance_ref': instance_ref,
        'class_ref': class_ref,
        'relation_type': _BR_TYPE_RELATION_INSTANCE_OF,
        'source': source,
        'sentence_id': sentence_id,
        'source_text_id': source_text_id,
        'confidence': confidence,
        'evidence_span': evidence_span,
    }


def _extract_from_copula(input_payload: dict[str, Any], concept_lookup: dict[str, str], entity_lookup: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract from copula."""
    source_text_id = input_payload.get('source_text_id', '')
    candidates: list[dict[str, Any]] = []

    for sentence in input_payload.get('sentences', []):
        if not isinstance(sentence, dict):
            continue
        text = sentence.get('text', '')
        if not isinstance(text, str) or not text.strip():
            continue
        sentence_id = sentence.get('sentence_id', '')

        for match in _COPULA_PATTERN.finditer(text):
            instance = _normalize_phrase(match.group('instance'))
            class_name = _normalize_phrase(match.group('class'))
            if not instance or not class_name or instance == class_name or _is_taxonomy_scaffold(class_name):
                continue
            entity = _resolve_phrase_lookup(instance, entity_lookup)
            class_ref = _resolve_phrase_lookup(class_name, concept_lookup)
            # Copular text becomes instance_of only with entity evidence for the instance and concept evidence for the class.
            if entity is None or class_ref is None:
                continue
            instance_ref = entity.get('entity_id', '')
            if not isinstance(instance_ref, str) or not instance_ref:
                continue
            candidates.append(
                _build_type_assertion(
                    source_text_id=source_text_id,
                    sentence_id=sentence_id,
                    instance=instance,
                    class_name=class_name,
                    instance_ref=instance_ref,
                    class_ref=class_ref,
                    source=_BR_TYPE_SOURCE_COPULA_PATTERN,
                    confidence=_BR_TYPE_CONFIDENCE_COPULA,
                    evidence_span=_sentence_span(sentence, text),
                )
            )
    return candidates


def _extract_from_entity_label(input_payload: dict[str, Any], concept_lookup: dict[str, str]) -> list[dict[str, Any]]:
    """Extract from entity label."""
    source_text_id = input_payload.get('source_text_id', '')
    candidates: list[dict[str, Any]] = []

    for entity in input_payload.get('entities', []):
        if not isinstance(entity, dict):
            continue
        entity_id = entity.get('entity_id')
        if not isinstance(entity_id, str) or not entity_id:
            continue
        class_name = _BR_TYPE_ENTITY_LABEL_TO_CLASS.get(entity.get('label'))
        if class_name is None:
            continue
        class_ref = _resolve_phrase_lookup(class_name, concept_lookup)
        if class_ref is None:
            continue
        sentence_id = entity.get('sentence_id', '')
        candidates.append(
            _build_type_assertion(
                source_text_id=source_text_id,
                sentence_id=sentence_id,
                instance=_normalize_phrase(entity.get('normalized_text') or entity.get('text')),
                class_name=class_name,
                instance_ref=entity_id,
                class_ref=class_ref,
                source=_BR_TYPE_SOURCE_ENTITY_LABEL,
                confidence=_BR_TYPE_CONFIDENCE_ENTITY_LABEL,
                evidence_span={'start_offset': 0, 'end_offset': 0},
            )
        )
    return candidates


def _extract_from_relation_pattern(input_payload: dict[str, Any], concept_lookup: dict[str, str], entity_lookup: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract from relation pattern."""
    source_text_id = input_payload.get('source_text_id', '')
    candidates: list[dict[str, Any]] = []

    for relation in input_payload.get('relations', []):
        if not isinstance(relation, dict):
            continue
        relation_type = _normalize_text(relation.get('relation_type') or relation.get('predicate') or relation.get('label'))
        if relation_type not in {'is_a', 'instance_of', 'type'}:
            continue

        instance = _normalize_phrase(relation.get('subject') or relation.get('subject_text') or relation.get('source') or relation.get('head'))
        class_name = _normalize_phrase(relation.get('object') or relation.get('object_text') or relation.get('target') or relation.get('tail'))
        if not instance or not class_name or instance == class_name:
            continue

        entity = _resolve_phrase_lookup(instance, entity_lookup)
        class_ref = _resolve_phrase_lookup(class_name, concept_lookup)
        if entity is None or class_ref is None:
            continue

        instance_ref = entity.get('entity_id', '')
        if not isinstance(instance_ref, str) or not instance_ref:
            continue

        sentence_id = relation.get('sentence_id') or entity.get('sentence_id', '')
        candidates.append(
            _build_type_assertion(
                source_text_id=source_text_id,
                sentence_id=sentence_id,
                instance=instance,
                class_name=class_name,
                instance_ref=instance_ref,
                class_ref=class_ref,
                source=_BR_TYPE_SOURCE_RELATION_PATTERN,
                confidence=_BR_TYPE_CONFIDENCE_RELATION_PATTERN,
                evidence_span={'start_offset': 0, 'end_offset': 0},
            )
        )
    return candidates


def _extract_from_short_taxonomy_subjects(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract from short taxonomy subjects."""
    source_text_id = input_payload.get('source_text_id', '')
    candidates: list[dict[str, Any]] = []
    for relation in input_payload.get('taxonomy_relations', []):
        if not isinstance(relation, dict):
            continue
        instance = _normalize_phrase(relation.get('subclass') or relation.get('child'))
        class_name = _normalize_phrase(relation.get('superclass') or relation.get('parent'))
        # Only compact symbolic subjects are compatibility instances; longer terms remain taxonomy classes.
        if not instance or not class_name or class_name == 'type' or len(instance.replace(' ', '')) > 4:
            continue
        instance_ref = relation.get('subclass_ref') or ''
        class_ref = relation.get('superclass_ref') or ''
        if not isinstance(instance_ref, str) or not instance_ref or not isinstance(class_ref, str) or not class_ref:
            continue
        candidates.append(_build_type_assertion(
            source_text_id=source_text_id,
            sentence_id=relation.get('sentence_id', ''),
            instance=instance,
            class_name=class_name,
            instance_ref=instance_ref,
            class_ref=class_ref,
            source=_BR_TYPE_SOURCE_RELATION_PATTERN,
            confidence=_BR_TYPE_CONFIDENCE_RELATION_PATTERN,
            evidence_span=relation.get('evidence_span') if isinstance(relation.get('evidence_span'), dict) else {'start_offset': 0, 'end_offset': 0},
        ))
    return candidates


def _dedupe_stable(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate type assertions by instance, class, and relation type in deterministic order."""
    ordered = sorted(
        candidates,
        key=lambda item: (
            item.get('instance', ''),
            item.get('class', ''),
            item.get('relation_type', ''),
            item.get('source', ''),
            item.get('sentence_id', ''),
            item.get('type_assertion_id', ''),
        ),
    )

    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in ordered:
        key = f"{item.get('instance','')}|{item.get('class','')}|{item.get('relation_type','')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique
