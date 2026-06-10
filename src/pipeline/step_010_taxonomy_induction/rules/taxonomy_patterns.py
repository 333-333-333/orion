from __future__ import annotations

import hashlib
import re
from typing import Any

_BR_TAX_RELATION_TYPE_SUBCLASS_OF = 'subclass_of'
_BR_TAX_SOURCE_COPULA_PATTERN = 'copula_pattern'
_BR_TAX_SOURCE_SUCH_AS_PATTERN = 'such_as_pattern'
_BR_TAX_SOURCE_RELATION_PATTERN = 'relation_pattern'
_BR_TAX_CONFIDENCE_COPULA = 0.9
_BR_TAX_CONFIDENCE_SUCH_AS = 0.88
_BR_TAX_CONFIDENCE_RELATION = 0.86
_PHRASE_ARTICLES = {'a', 'an', 'the'}
_TAXONOMY_SCAFFOLD_HEADS = {'type', 'kind', 'category', 'form'}
_BR_TAX_DEFINITION_ONLY_PARENT_HEADS = {'document', 'model', 'set', 'control', 'controls'}
_CLAUSE_STOP_WORDS = {'that', 'which', 'who', 'whom', 'whose', 'where', 'when'}
_CLAUSE_CONNECTORS = {'to', 'by', 'for', 'with', 'from', 'in', 'on', 'at'}

_COPULA_PATTERN = re.compile(r'\b(?P<sub>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)\s+(?:is|are)\s+(?:a|an|the)\s+(?:(?:type|kind|category|form)s?\s+of\s+)?(?P<sup>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)\b', re.IGNORECASE)
_SUCH_AS_PATTERN = re.compile(r'\b(?P<sup>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)s?\s+such\s+as\s+(?P<sub>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)s?\b', re.IGNORECASE)
_INCLUDING_PATTERN = re.compile(r'\b(?P<sup>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)s?\s+including\s+(?P<sub>(?:[A-Za-z][A-Za-z\-]*\s+){0,5}[A-Za-z][A-Za-z\-]*)s?\b', re.IGNORECASE)


def _normalize_text(value: str | None) -> str:
    return (value or '').casefold().strip()


def _strip_leading_articles(value: str) -> str:
    tokens = [token for token in value.split(' ') if token]
    while tokens and tokens[0] in _PHRASE_ARTICLES:
        tokens.pop(0)
    return ' '.join(tokens)


def _singularize_token(token: str) -> str:
    if len(token) > 3 and token.endswith('ies'):
        return token[:-3] + 'y'
    if len(token) > 4 and token.endswith(('ses', 'xes', 'zes', 'ches', 'shes')):
        return token[:-2]
    if len(token) > 3 and token.endswith('s') and not token.endswith(('ss', 'us', 'is')):
        return token[:-1]
    return token


def _normalize_phrase(value: str | None) -> str:
    normalized = re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value or ''))
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    normalized = _strip_leading_articles(normalized)
    return ' '.join(_singularize_token(token) for token in normalized.split(' ') if token)


def _is_definition_only_parent_candidate(value: str | None) -> bool:
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', str(value or ''))
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    tokens = [token for token in _normalize_phrase(spaced).split(' ') if token]
    return len(tokens) >= 2 and tokens[-1] in _BR_TAX_DEFINITION_ONLY_PARENT_HEADS


def _canonicalize_head_phrase(value: str | None) -> str:
    tokens = [token for token in _normalize_phrase(value).split(' ') if token]
    if not tokens:
        return ''
    if len(tokens) >= 2 and tokens[0] in _TAXONOMY_SCAFFOLD_HEADS and tokens[1] == 'of':
        tokens = tokens[2:]
    if not tokens:
        return ''

    result: list[str] = []
    for index, token in enumerate(tokens):
        if not result and token in _PHRASE_ARTICLES:
            continue
        if result:
            if token in _CLAUSE_STOP_WORDS:
                break
            if len(token) > 4 and token.endswith(('ed', 'ing', 'en')):
                next_token = tokens[index + 1] if index + 1 < len(tokens) else ''
                if not next_token or next_token in _CLAUSE_CONNECTORS or next_token in _CLAUSE_STOP_WORDS or next_token in _PHRASE_ARTICLES:
                    break
        result.append(token)
    return ' '.join(result)


def _phrase_tokens(value: str | None) -> list[str]:
    return [token for token in _normalize_phrase(value).split(' ') if token and token not in _PHRASE_ARTICLES]


def _phrase_match_score(query: str | None, candidate: str | None) -> float:
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


def _build_taxonomy_relation_id(source_text_id: str, sentence_id: str, subclass: str, superclass: str) -> str:
    stable_key = f"{source_text_id}|{sentence_id}|{subclass}|{superclass}|{_BR_TAX_RELATION_TYPE_SUBCLASS_OF}".encode('utf-8')
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f'tax-{digest}'


def _concept_lookup(input_payload: dict[str, Any]) -> dict[str, str]:
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


def _resolve_phrase_text(value: str | None, concept_lookup: dict[str, str]) -> str:
    normalized_query = _normalize_phrase(value)
    if not normalized_query:
        return ''
    if normalized_query in concept_lookup:
        return normalized_query

    best_text = ''
    best_score = 0.0
    best_size = 10 ** 9
    for normalized_candidate in concept_lookup:
        score = _phrase_match_score(normalized_query, normalized_candidate)
        if score > best_score or (score == best_score and len(_phrase_tokens(normalized_candidate)) < best_size):
            best_score = score
            best_size = len(_phrase_tokens(normalized_candidate))
            best_text = normalized_candidate
    return best_text if best_score >= 0.75 else ''


def _resolve_concept_ref(value: str | None, concept_lookup: dict[str, str]) -> str:
    resolved_text = _resolve_phrase_text(value, concept_lookup)
    return concept_lookup.get(resolved_text, '') if resolved_text else ''


def _entity_text_set(input_payload: dict[str, Any]) -> set[str]:
    values: set[str] = set()
    for entity in input_payload.get('entities', []):
        if not isinstance(entity, dict):
            continue
        for value in (entity.get('normalized_text'), entity.get('text')):
            normalized = _normalize_phrase(value if isinstance(value, str) else None)
            if normalized:
                values.add(normalized)
    return values


def _sentence_span(sentence: dict[str, Any], fallback_text: str) -> dict[str, int]:
    start_offset = sentence.get('start_offset')
    end_offset = sentence.get('end_offset')
    if isinstance(start_offset, int) and isinstance(end_offset, int):
        return {'start_offset': start_offset, 'end_offset': end_offset}
    return {'start_offset': 0, 'end_offset': len(fallback_text)}


def _is_instance_like(subclass: str, entity_set: set[str], concept_lookup: dict[str, str]) -> bool:
    return subclass in entity_set and subclass not in concept_lookup


def _candidate_from_match(match: re.Match[str], sentence: dict[str, Any], source_text_id: str, concept_lookup: dict[str, str], entity_set: set[str], source: str, confidence: float) -> dict[str, Any] | None:
    subclass = _resolve_phrase_text(match.group('sub'), concept_lookup) or _normalize_phrase(match.group('sub'))
    superclass_head = _canonicalize_head_phrase(match.group('sup'))
    superclass = _resolve_phrase_text(superclass_head, concept_lookup) or superclass_head
    if not subclass or not superclass:
        return None
    if subclass == superclass:
        return None
    if _is_definition_only_parent_candidate(superclass):
        return None
    if _is_instance_like(subclass, entity_set, concept_lookup):
        return None

    subclass_ref = _resolve_concept_ref(subclass, concept_lookup)
    superclass_ref = _resolve_concept_ref(superclass, concept_lookup)
    if not subclass_ref:
        return None

    sentence_id = sentence.get('sentence_id', '')
    evidence_span = _sentence_span(sentence, sentence.get('text', ''))
    return {
        'taxonomy_relation_id': _build_taxonomy_relation_id(source_text_id, sentence_id, subclass, superclass),
        'subclass': subclass,
        'superclass': superclass,
        'subclass_ref': subclass_ref,
        'superclass_ref': superclass_ref,
        'relation_type': _BR_TAX_RELATION_TYPE_SUBCLASS_OF,
        'source': source,
        'sentence_id': sentence_id,
        'source_text_id': source_text_id,
        'confidence': confidence,
        'evidence_span': evidence_span,
    }


def _type_scaffold_candidate(match: re.Match[str], sentence: dict[str, Any], source_text_id: str, concept_lookup: dict[str, str]) -> dict[str, Any] | None:
    if ' type of ' not in match.group(0).casefold() and ' kind of ' not in match.group(0).casefold():
        return None
    sub_tokens = _phrase_tokens(match.group('sub'))
    if not sub_tokens:
        return None
    subclass = sub_tokens[-1]
    subclass_ref = _resolve_concept_ref(subclass, concept_lookup)
    if not subclass_ref:
        return None
    sentence_id = sentence.get('sentence_id', '')
    return {
        'taxonomy_relation_id': _build_taxonomy_relation_id(source_text_id, sentence_id, subclass, 'type'),
        'subclass': subclass,
        'superclass': 'type',
        'subclass_ref': subclass_ref,
        'superclass_ref': '',
        'relation_type': _BR_TAX_RELATION_TYPE_SUBCLASS_OF,
        'source': _BR_TAX_SOURCE_COPULA_PATTERN,
        'sentence_id': sentence_id,
        'source_text_id': source_text_id,
        'confidence': _BR_TAX_CONFIDENCE_COPULA,
        'evidence_span': _sentence_span(sentence, sentence.get('text', '')),
    }


def _extract_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload.get('source_text_id', '')
    concept_lookup = _concept_lookup(input_payload)
    entity_set = _entity_text_set(input_payload)

    candidates: list[dict[str, Any]] = []
    for sentence in input_payload.get('sentences', []):
        if not isinstance(sentence, dict):
            continue
        text = sentence.get('text', '')
        if not isinstance(text, str) or not text.strip():
            continue

        for match in _COPULA_PATTERN.finditer(text):
            candidate = _candidate_from_match(match, sentence, source_text_id, concept_lookup, entity_set, _BR_TAX_SOURCE_COPULA_PATTERN, _BR_TAX_CONFIDENCE_COPULA)
            if candidate is not None:
                candidates.append(candidate)
            scaffold = _type_scaffold_candidate(match, sentence, source_text_id, concept_lookup)
            if scaffold is not None:
                candidates.append(scaffold)

        for match in _SUCH_AS_PATTERN.finditer(text):
            candidate = _candidate_from_match(match, sentence, source_text_id, concept_lookup, entity_set, _BR_TAX_SOURCE_SUCH_AS_PATTERN, _BR_TAX_CONFIDENCE_SUCH_AS)
            if candidate is not None:
                candidates.append(candidate)

        for match in _INCLUDING_PATTERN.finditer(text):
            candidate = _candidate_from_match(match, sentence, source_text_id, concept_lookup, entity_set, _BR_TAX_SOURCE_RELATION_PATTERN, _BR_TAX_CONFIDENCE_RELATION)
            if candidate is not None:
                candidates.append(candidate)
    return candidates


def _dedupe_stable(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        candidates,
        key=lambda rel: (
            rel.get('sentence_id', ''),
            rel.get('subclass', ''),
            rel.get('superclass', ''),
            rel.get('source', ''),
            rel.get('taxonomy_relation_id', ''),
        ),
    )
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for rel in ordered:
        key = f"{rel.get('subclass','')}|{rel.get('superclass','')}|{rel.get('relation_type','')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(rel)
    return unique
