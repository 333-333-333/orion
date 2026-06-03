from __future__ import annotations

import hashlib
import re
from typing import Any

_BR_REL_CONFIDENCE_SVO = 0.9
_BR_REL_CONFIDENCE_COPULA = 0.88
_PHRASE_ARTICLES = {'a', 'an', 'the'}


def _normalize_text(value: str) -> str:
    return value.casefold().strip()


def _normalize_phrase(value: str | None) -> str:
    normalized = re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value or ''))
    return re.sub(r'\s+', ' ', normalized).strip()


def _singularize_token(token: str) -> str:
    if len(token) > 3 and token.endswith('ies'):
        return token[:-3] + 'y'
    if len(token) > 4 and token.endswith(('ses', 'xes', 'zes', 'ches', 'shes')):
        return token[:-2]
    if len(token) > 3 and token.endswith('s') and not token.endswith(('ss', 'us', 'is')):
        return token[:-1]
    return token


def _normalize_fact_phrase(value: str | None) -> str:
    normalized = _normalize_phrase(value)
    if not normalized:
        return ''
    return ' '.join(_singularize_token(token) for token in normalized.split(' ') if token)


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


def _build_relation_id(source_text_id: str, sentence_id: str, subject_text: str, predicate: str, object_text: str) -> str:
    stable_key = f"{source_text_id}|{sentence_id}|{_normalize_fact_phrase(subject_text)}|{_normalize_text(predicate)}|{_normalize_fact_phrase(object_text)}".encode('utf-8')
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"rel-{digest}"


def _make_ref_lookup(input_payload: dict[str, Any]) -> dict[tuple[int, int, str], str]:
    lookup: dict[tuple[int, int, str], str] = {}
    for entity in input_payload.get('entities', []):
        start_offset = entity.get('start_offset', -1)
        end_offset = entity.get('end_offset', -1)
        for value in (entity.get('normalized_text'), entity.get('text')):
            normalized = _normalize_fact_phrase(value if isinstance(value, str) else None)
            if normalized:
                lookup[(start_offset, end_offset, normalized)] = entity.get('entity_id', '')
    for concept in input_payload.get('concepts', []):
        start_offset = concept.get('start_offset', -1)
        end_offset = concept.get('end_offset', -1)
        for value in (concept.get('normalized_text'), concept.get('lemma'), concept.get('text')):
            normalized = _normalize_fact_phrase(value if isinstance(value, str) else None)
            if normalized and (start_offset, end_offset, normalized) not in lookup:
                lookup[(start_offset, end_offset, normalized)] = concept.get('concept_id', '')
    return lookup


def _resolve_ref(lookup: dict[tuple[int, int, str], str], text: str, start_offset: int, end_offset: int) -> str:
    normalized_query = _normalize_fact_phrase(text)
    if not normalized_query:
        return ''

    direct = lookup.get((start_offset, end_offset, normalized_query))
    if direct:
        return direct

    best_ref = ''
    best_score = 0.0
    best_size = 10 ** 9
    for (start, end, norm_text), ref_id in lookup.items():
        if start == start_offset and end == end_offset:
            return ref_id
        score = _phrase_match_score(normalized_query, norm_text)
        if score > best_score or (score == best_score and len(_phrase_tokens(norm_text)) < best_size):
            best_score = score
            best_size = len(_phrase_tokens(norm_text))
            best_ref = ref_id
    return best_ref if best_score >= 0.75 else ''



def _make_coref_lookup(input_payload: dict[str, Any]) -> dict[tuple[int, int, str], dict[str, Any]]:
    lookup: dict[tuple[int, int, str], dict[str, Any]] = {}
    for coref in input_payload.get('coreferences', []):
        if coref.get('status') != 'resolved':
            continue
        mention = coref.get('mention', '')
        mention_span = coref.get('mention_span', {})
        key = (
            mention_span.get('start_offset', -1),
            mention_span.get('end_offset', -1),
            _normalize_text(mention),
        )
        lookup[key] = coref
    return lookup


def _resolve_subject_from_coreference(subject: dict[str, Any], coref_lookup: dict[tuple[int, int, str], dict[str, Any]]) -> tuple[str, int, int]:
    key = (
        subject.get('start_offset', -1),
        subject.get('end_offset', -1),
        _normalize_text(subject.get('text', '')),
    )
    coref = coref_lookup.get(key)
    if not coref:
        return subject.get('text', ''), subject.get('start_offset', -1), subject.get('end_offset', -1)
    return (
        coref.get('antecedent', subject.get('text', '')),
        coref.get('antecedent_span', {}).get('start_offset', subject.get('start_offset', -1)),
        coref.get('antecedent_span', {}).get('end_offset', subject.get('end_offset', -1)),
    )


def _group_tokens_by_sentence(tokens: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for token in tokens:
        grouped.setdefault(token.get('sentence_id', ''), []).append(token)
    for sentence_id in grouped:
        grouped[sentence_id] = sorted(grouped[sentence_id], key=lambda t: (t.get('start_offset', 0), t.get('end_offset', 0), t.get('token_id', '')))
    return grouped


def _is_relation_nominal(token: dict[str, Any]) -> bool:
    return token.get('pos') in {'NOUN', 'PROPN', 'PRON'} and _normalize_phrase(token.get('text', '')) not in {'', 'that'}


def _is_relation_predicate_candidate(token: dict[str, Any]) -> bool:
    normalized = _normalize_phrase(token.get('lemma') or token.get('text', ''))
    return bool(normalized) and normalized not in {'be'} and token.get('pos') in {'VERB', 'NOUN'}


def _object_text_from_nominals(tokens: list[dict[str, Any]], object_token: dict[str, Any]) -> str:
    phrase_tokens = [
        token for token in tokens
        if token.get('start_offset', -1) >= object_token.get('start_offset', -1)
        and token.get('end_offset', -1) <= object_token.get('end_offset', -1)
        and _normalize_phrase(token.get('text', ''))
    ]
    return _normalize_fact_phrase(' '.join(token.get('text', '') for token in phrase_tokens) or object_token.get('text', ''))


def _extract_segmented_active_relations(
    source_text_id: str,
    sentence_id: str,
    sentence_tokens: list[dict[str, Any]],
    ref_lookup: dict[tuple[int, int, str], str],
    coref_lookup: dict[tuple[int, int, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    relations: list[dict[str, Any]] = []
    segments: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for token in sentence_tokens:
        if token.get('pos') == 'PUNCT' and token.get('text') in {',', ';', '.'}:
            if current:
                segments.append(current)
                current = []
            continue
        if token.get('pos') == 'CCONJ' and token.get('text', '').lower() in {'and'} and not current:
            continue
        current.append(token)
    if current:
        segments.append(current)

    for segment in segments:
        content = [token for token in segment if token.get('pos') not in {'DET', 'AUX', 'PART', 'SCONJ', 'CCONJ', 'ADP', 'PUNCT', 'ADV', 'ADJ', 'NUM'}]
        if len(content) < 3:
            continue
        for index in range(0, len(content) - 2):
            subject = content[index]
            predicate = content[index + 1]
            if not _is_relation_nominal(subject) or not _is_relation_predicate_candidate(predicate):
                continue
            objects = [token for token in content[index + 2:] if _is_relation_nominal(token)]
            if not objects:
                continue
            obj = objects[0]
            resolved_subject_text, resolved_subject_start, resolved_subject_end = _resolve_subject_from_coreference(subject, coref_lookup)
            resolved_subject_text = _normalize_fact_phrase(resolved_subject_text)
            object_text = _normalize_fact_phrase(_object_text_from_nominals(segment, obj))
            start_offset = min(token.get('start_offset', 0) for token in segment)
            end_offset = max(token.get('end_offset', 0) for token in segment)
            relations.append(
                {
                    'relation_id': _build_relation_id(source_text_id, sentence_id, resolved_subject_text, predicate.get('lemma', predicate.get('text', '')), object_text),
                    'subject_text': resolved_subject_text,
                    'subject_ref': _resolve_ref(ref_lookup, resolved_subject_text, resolved_subject_start, resolved_subject_end),
                    'predicate': predicate.get('lemma', predicate.get('text', '')),
                    'object_text': object_text,
                    'object_ref': _resolve_ref(ref_lookup, object_text, obj.get('start_offset', -1), obj.get('end_offset', -1)),
                    'sentence_id': sentence_id,
                    'source_text_id': source_text_id,
                    'confidence': _BR_REL_CONFIDENCE_SVO,
                    'evidence_span': {'start_offset': start_offset, 'end_offset': end_offset},
                    'start_offset': start_offset,
                    'end_offset': end_offset,
                }
            )
    return relations


def _extract_svo_relations(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload['source_text_id']
    tokens = input_payload.get('tokens', [])
    ref_lookup = _make_ref_lookup(input_payload)
    coref_lookup = _make_coref_lookup(input_payload)
    grouped = _group_tokens_by_sentence(tokens)
    relations: list[dict[str, Any]] = []

    for sentence_id, sentence_tokens in grouped.items():
        verbs = [t for t in sentence_tokens if t.get('pos') == 'VERB']
        sentence_start = min((t.get('start_offset', 0) for t in sentence_tokens), default=0)
        sentence_end = max((t.get('end_offset', 0) for t in sentence_tokens), default=0)

        def _subjects_for(verb_token: dict[str, Any]) -> list[dict[str, Any]]:
            verb_text = verb_token.get('text', '')
            direct = [t for t in sentence_tokens if t.get('dependency') in {'nsubj', 'nsubjpass'} and t.get('head_text') == verb_text]
            if direct:
                return direct
            if verb_token.get('dependency') == 'conj':
                head_text = verb_token.get('head_text', '')
                return [t for t in sentence_tokens if t.get('dependency') in {'nsubj', 'nsubjpass'} and t.get('head_text') == head_text]
            return []

        relations.extend(_extract_segmented_active_relations(source_text_id, sentence_id, sentence_tokens, ref_lookup, coref_lookup))

        for verb in verbs:
            verb_head = verb.get('text', '')
            subjects = _subjects_for(verb)
            active_subjects = [s for s in subjects if s.get('dependency') == 'nsubj']
            passive_subjects = [s for s in subjects if s.get('dependency') == 'nsubjpass']
            objects = [t for t in sentence_tokens if t.get('dependency') in {'dobj', 'obj', 'pobj'} and t.get('head_text') == verb_head]

            for subject in active_subjects:
                resolved_subject_text, resolved_subject_start, resolved_subject_end = _resolve_subject_from_coreference(subject, coref_lookup)
                resolved_subject_text = _normalize_fact_phrase(resolved_subject_text)
                for obj in objects:
                    object_text = _normalize_fact_phrase(obj.get('text', ''))
                    relations.append(
                        {
                            'relation_id': _build_relation_id(source_text_id, sentence_id, resolved_subject_text, verb.get('lemma', verb.get('text', '')), object_text),
                            'subject_text': resolved_subject_text,
                            'subject_ref': _resolve_ref(ref_lookup, resolved_subject_text, resolved_subject_start, resolved_subject_end),
                            'predicate': verb.get('lemma', verb.get('text', '')),
                            'object_text': object_text,
                            'object_ref': _resolve_ref(ref_lookup, object_text, obj.get('start_offset', -1), obj.get('end_offset', -1)),
                            'sentence_id': sentence_id,
                            'source_text_id': source_text_id,
                            'confidence': _BR_REL_CONFIDENCE_SVO,
                            'evidence_span': {'start_offset': sentence_start, 'end_offset': sentence_end},
                            'start_offset': sentence_start,
                            'end_offset': sentence_end,
                        }
                    )

            if passive_subjects:
                agents = [t for t in sentence_tokens if t.get('dependency') == 'pobj' and t.get('head_text') == 'by']
                for passive_subject in passive_subjects:
                    for agent in agents:
                        subject_text = _normalize_fact_phrase(agent.get('text', ''))
                        object_text = _normalize_fact_phrase(passive_subject.get('text', ''))
                        relations.append(
                            {
                                'relation_id': _build_relation_id(source_text_id, sentence_id, subject_text, verb.get('lemma', verb.get('text', '')), object_text),
                                'subject_text': subject_text,
                                'subject_ref': _resolve_ref(ref_lookup, subject_text, agent.get('start_offset', -1), agent.get('end_offset', -1)),
                                'predicate': verb.get('lemma', verb.get('text', '')),
                                'object_text': object_text,
                                'object_ref': _resolve_ref(ref_lookup, object_text, passive_subject.get('start_offset', -1), passive_subject.get('end_offset', -1)),
                                'sentence_id': sentence_id,
                                'source_text_id': source_text_id,
                                'confidence': _BR_REL_CONFIDENCE_SVO,
                                'evidence_span': {'start_offset': sentence_start, 'end_offset': sentence_end},
                                'start_offset': sentence_start,
                                'end_offset': sentence_end,
                            }
                        )
    return relations


def _extract_copula_relations(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload['source_text_id']
    tokens = input_payload.get('tokens', [])
    ref_lookup = _make_ref_lookup(input_payload)
    grouped = _group_tokens_by_sentence(tokens)
    relations: list[dict[str, Any]] = []

    for sentence_id, sentence_tokens in grouped.items():
        copulas = [t for t in sentence_tokens if t.get('lemma') == 'be' and t.get('pos') in {'AUX', 'VERB'}]
        for copula in copulas:
            copula_head = copula.get('text', '')
            subjects = [t for t in sentence_tokens if t.get('dependency') == 'nsubj' and t.get('head_text') == copula_head]
            attrs = [t for t in sentence_tokens if t.get('dependency') in {'attr', 'acomp'} and t.get('head_text') == copula_head]
            for subject in subjects:
                for attr in attrs:
                    subject_text = _normalize_fact_phrase(subject.get('text', ''))
                    object_text = _normalize_fact_phrase(attr.get('text', ''))
                    start_offset = min(subject.get('start_offset', 0), copula.get('start_offset', 0), attr.get('start_offset', 0))
                    end_offset = max(subject.get('end_offset', 0), copula.get('end_offset', 0), attr.get('end_offset', 0))
                    relations.append(
                        {
                            'relation_id': _build_relation_id(source_text_id, sentence_id, subject_text, copula.get('lemma', copula.get('text', '')), object_text),
                            'subject_text': subject_text,
                            'subject_ref': _resolve_ref(ref_lookup, subject_text, subject.get('start_offset', -1), subject.get('end_offset', -1)),
                            'predicate': copula.get('lemma', copula.get('text', '')),
                            'object_text': object_text,
                            'object_ref': _resolve_ref(ref_lookup, object_text, attr.get('start_offset', -1), attr.get('end_offset', -1)),
                            'sentence_id': sentence_id,
                            'source_text_id': source_text_id,
                            'confidence': _BR_REL_CONFIDENCE_COPULA,
                            'evidence_span': {'start_offset': start_offset, 'end_offset': end_offset},
                            'start_offset': start_offset,
                            'end_offset': end_offset,
                        }
                    )
    return relations


def _dedupe_stable(relations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    sorted_relations = sorted(relations, key=lambda r: (r['sentence_id'], r['start_offset'], r['end_offset'], r['relation_id']))
    for relation in sorted_relations:
        key = f"{_normalize_text(relation['subject_text'])}|{_normalize_text(relation['predicate'])}|{_normalize_text(relation['object_text'])}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(relation)
    return unique


def extract_relations_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    candidates = []
    candidates.extend(_extract_svo_relations(input_payload))
    candidates.extend(_extract_copula_relations(input_payload))
    relations = _dedupe_stable(candidates)

    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['relations'] = relations
    return result
