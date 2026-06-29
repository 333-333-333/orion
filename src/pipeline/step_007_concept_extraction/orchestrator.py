from __future__ import annotations

import hashlib
import re
from typing import Any

_BR_CONCEPT_CONFIDENCE_NOUN_CHUNK = 0.95
_BR_CONCEPT_CONFIDENCE_ENTITY_LABEL = 0.9
_BR_CONCEPT_CONFIDENCE_NOUN_TOKEN = 0.8
_PHRASE_CONNECTORS = {'of', 'and', 'in', 'on', 'for', 'with', 'to', 'by', 'as', 'from', 'into', 'over'}
_CONTEXT_BOUNDARY_PREPOSITIONS = {
    'after',
    'at',
    'before',
    'beside',
    'by',
    'during',
    'for',
    'from',
    'in',
    'into',
    'near',
    'on',
    'over',
    'to',
    'with',
}
_LEXICALIZED_PREPOSITIONAL_TERMS = {
    'data at rest',
    'data in transit',
    'defense in depth',
    'denial of service',
    'man in the middle',
}
_CLAUSAL_PREFIX_VERBS = {
    'attaches',
    'checks',
    'cleans',
    'confirms',
    'cuts',
    'grates',
    'keeps',
    'leaves',
    'links',
    'manages',
    'passes',
    'places',
    'prepares',
    'reaches',
    'receives',
    'records',
    'reviews',
    'rides',
    'scans',
    'serves',
    'stores',
    'stretches',
    'tells',
    'turns',
    'updates',
    'writes',
}
_PHRASE_HYPHENS = {'-', '–', '—', '/'}
_PHRASE_ARTICLES = {'a', 'an', 'the', 'any', 'each', 'one', 'more'}
_CONTEXT_BOUNDARY_PATTERN = re.compile(
    r"\b(" + '|'.join(re.escape(preposition) for preposition in sorted(_CONTEXT_BOUNDARY_PREPOSITIONS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)
_TEMPORAL_CONTEXT_PATTERN = re.compile(r"^\s*\d{1,2}(?::\d{2})?(?:\s*[ap]\.?m\.?)?\s*$", re.IGNORECASE)


def _normalize_text(value: str) -> str:
    return value.casefold().strip()


def _strip_leading_articles(value: str) -> str:
    tokens = [token for token in value.split(' ') if token]
    while tokens:
        if len(tokens) >= 3 and tokens[0] == 'one' and tokens[1] == 'or' and tokens[2] == 'more':
            tokens = tokens[3:]
            continue
        if tokens[0] in _PHRASE_ARTICLES:
            tokens.pop(0)
            continue
        break
    return ' '.join(tokens)


def _normalize_phrase(value: str | None) -> str:
    normalized = re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value or ''))
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return _strip_leading_articles(normalized)


def _resolve_sentence_id(sentences: list[dict[str, Any]], start_offset: int, end_offset: int) -> str:
    for sentence in sentences:
        if sentence['start_offset'] <= start_offset and end_offset <= sentence['end_offset']:
            return sentence['sentence_id']
    return ''


def _build_concept_id(source_text_id: str, lemma: str, text: str) -> str:
    stable_key = f"{source_text_id}|{_normalize_text(lemma)}|{_normalize_text(text)}".encode('utf-8')
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"con-{digest}"


def _trimmed_span(value: str, start_offset: int, end_offset: int) -> tuple[str, int, int]:
    left = 0
    right = len(value)
    while left < right and value[left].isspace():
        left += 1
    while right > left and value[right - 1].isspace():
        right -= 1
    return value[left:right], start_offset + left, start_offset + right if end_offset >= start_offset else end_offset


def _is_temporal_context(value: str) -> bool:
    return bool(_TEMPORAL_CONTEXT_PATTERN.match(value))


def _strip_clausal_prefix(value: str, start_offset: int) -> tuple[str, int, int]:
    match = re.match(
        r"^(?P<subject>[A-Z][A-Za-z0-9']*(?:\s+[A-Z][A-Za-z0-9']*){0,2})\s+(?P<verb>[a-z]+(?:s|es|ies))\s+(?P<object>.+)$",
        value,
    )
    if not match or match.group('verb').casefold() not in _CLAUSAL_PREFIX_VERBS:
        return value, start_offset, start_offset + len(value)
    object_text = match.group('object').strip()
    object_start = start_offset + match.start('object') + (len(match.group('object')) - len(match.group('object').lstrip()))
    return object_text, object_start, object_start + len(object_text)


def _segment_lemma(value: str, fallback: str) -> str:
    tokens = [token for token in re.sub(r"[^A-Za-z0-9']+", ' ', value).split() if token.casefold() not in _PHRASE_ARTICLES]
    return tokens[-1] if tokens else fallback


def _split_contextual_prepositional_phrase(text: str, start_offset: int, root_lemma: str) -> list[tuple[str, str, int, int]]:
    trimmed_text, trimmed_start, _ = _trimmed_span(text, start_offset, start_offset + len(text))
    normalized = _normalize_phrase(trimmed_text)
    if not trimmed_text or normalized in _LEXICALIZED_PREPOSITIONAL_TERMS:
        return [(trimmed_text, root_lemma, trimmed_start, trimmed_start + len(trimmed_text))] if trimmed_text else []

    matches = list(_CONTEXT_BOUNDARY_PATTERN.finditer(trimmed_text))
    if not matches:
        return [(trimmed_text, root_lemma, trimmed_start, trimmed_start + len(trimmed_text))]

    segments: list[tuple[str, str, int, int]] = []
    cursor = 0
    for match in matches:
        raw_segment, segment_start, segment_end = _trimmed_span(trimmed_text[cursor:match.start()], trimmed_start + cursor, trimmed_start + match.start())
        raw_segment, segment_start, segment_end = _strip_clausal_prefix(raw_segment, segment_start)
        if raw_segment and not _is_temporal_context(raw_segment):
            segments.append((raw_segment, _segment_lemma(raw_segment, root_lemma), segment_start, segment_end))
        cursor = match.end()

    raw_segment, segment_start, segment_end = _trimmed_span(trimmed_text[cursor:], trimmed_start + cursor, trimmed_start + len(trimmed_text))
    raw_segment, segment_start, segment_end = _strip_clausal_prefix(raw_segment, segment_start)
    if raw_segment and not _is_temporal_context(raw_segment):
        segments.append((raw_segment, _segment_lemma(raw_segment, root_lemma), segment_start, segment_end))

    fallback_text, fallback_start, fallback_end = _strip_clausal_prefix(trimmed_text, trimmed_start)
    return segments or [(fallback_text, root_lemma, fallback_start, fallback_end)]


def _append_candidate(candidates: list[dict[str, Any]], *, source_text_id: str, sentences: list[dict[str, Any]], text: str, lemma: str, source: str, start_offset: int, end_offset: int, confidence: float, boundary_limited: bool = False) -> None:
    sentence_id = _resolve_sentence_id(sentences, start_offset, end_offset)
    candidate = {
        'concept_id': _build_concept_id(source_text_id, lemma, text),
        'text': text,
        'lemma': lemma,
        'source': source,
        'start_offset': start_offset,
        'end_offset': end_offset,
        'sentence_id': sentence_id,
        'source_text_id': source_text_id,
        'confidence': confidence,
    }
    if boundary_limited:
        candidate['_boundary_limited'] = True
    candidates.append(candidate)


def _is_connector(token: Any) -> bool:
    text = getattr(token, 'text', '') or ''
    return text.casefold() in _PHRASE_CONNECTORS


def _token_kind(token: Any, previous: Any | None = None) -> str:
    text = getattr(token, 'text', '') or ''
    if text in _PHRASE_HYPHENS:
        return 'strong'
    if _is_connector(token):
        return 'connector'

    pos = getattr(token, 'pos_', '') or ''
    if pos in {'NOUN', 'PROPN', 'ADJ', 'NUM'}:
        return 'strong'

    if pos == 'VERB':
        morph = getattr(token, 'morph', None)
        verb_forms = set(morph.get('VerbForm')) if morph is not None and hasattr(morph, 'get') else set()
        if 'Part' in verb_forms:
            return 'strong'
        if previous is not None and getattr(previous, 'pos_', '') in {'ADJ', 'ADV'}:
            return 'weak'

    return ''


def _expand_phrase_left(doc: Any, start: int) -> int:
    while start > 0:
        prev = doc[start - 1]
        prev_prev = doc[start - 2] if start > 1 else None
        kind = _token_kind(prev, doc[start] if start < len(doc) else None)
        if kind in {'strong', 'weak'}:
            start -= 1
            if kind == 'weak':
                break
            continue
        if kind == 'connector' and prev_prev is not None:
            prev_kind = _token_kind(prev_prev, prev)
            if prev_kind in {'strong', 'weak'}:
                start -= 2
                if prev_kind == 'weak':
                    break
                continue
        break
    return start


def _expand_phrase_right(doc: Any, end: int) -> int:
    while end < len(doc):
        current = doc[end]
        next_token = doc[end + 1] if end + 1 < len(doc) else None
        kind = _token_kind(current, doc[end - 1] if end > 0 else None)
        if kind in {'strong', 'weak'}:
            end += 1
            if kind == 'weak':
                break
            continue
        if kind == 'connector' and next_token is not None:
            next_kind = _token_kind(next_token, current)
            if next_kind in {'strong', 'weak'}:
                end += 2
                if next_kind == 'weak':
                    break
                continue
        break
    return end


def _expand_candidate(candidate: dict[str, Any], doc: Any) -> dict[str, Any]:
    start_offset = int(candidate.get('start_offset', 0) or 0)
    end_offset = int(candidate.get('end_offset', 0) or 0)
    output_candidate = {key: value for key, value in candidate.items() if key != '_boundary_limited'}
    char_span = getattr(doc, 'char_span', None)
    can_expand = callable(char_span) and hasattr(doc, '__getitem__') and hasattr(doc, '__len__') and not candidate.get('_boundary_limited')
    span = char_span(start_offset, end_offset, alignment_mode='expand') if can_expand else None
    if span is None:
        expanded_text = str(candidate.get('text', '')).strip()
        normalized_text = _normalize_phrase(expanded_text)
        lemma = str(candidate.get('lemma', '')).strip() or expanded_text
        return {
            **output_candidate,
            'text': expanded_text,
            'lemma': lemma,
            'normalized_text': normalized_text,
            'concept_id': _build_concept_id(str(candidate.get('source_text_id', '')), lemma, expanded_text),
        }

    start = _expand_phrase_left(doc, span.start)
    end = _expand_phrase_right(doc, span.end)
    expanded_text = doc[start:end].text.strip()
    if not expanded_text:
        expanded_text = str(candidate.get('text', '')).strip()
    normalized_text = _normalize_phrase(expanded_text)
    lemma = str(candidate.get('lemma', '')).strip() or expanded_text
    return {
        **candidate,
        'text': expanded_text,
        'lemma': lemma,
        'normalized_text': normalized_text,
        'start_offset': getattr(doc[start], 'idx', start_offset),
        'end_offset': getattr(doc[end - 1], 'idx', end_offset) + len(getattr(doc[end - 1], 'text', '')) if end > start else end_offset,
        'concept_id': _build_concept_id(str(candidate.get('source_text_id', '')), lemma, expanded_text),
    }


def _collect_noun_chunk_candidates(input_payload: dict[str, Any], doc: Any) -> list[dict[str, Any]]:
    source_text_id = input_payload['source_text_id']
    sentences = input_payload['sentences']
    candidates: list[dict[str, Any]] = []
    for chunk in getattr(doc, 'noun_chunks', []):
        text = getattr(chunk, 'text', '') or ''
        if text.strip() == '':
            continue
        root = getattr(chunk, 'root', None)
        lemma = getattr(root, 'lemma_', text) if root is not None else text
        start_offset = getattr(chunk, 'start_char', 0)
        for segment_text, segment_lemma, segment_start, segment_end in _split_contextual_prepositional_phrase(text, start_offset, lemma):
            _append_candidate(
                candidates,
                source_text_id=source_text_id,
                sentences=sentences,
                text=segment_text,
                lemma=segment_lemma,
                source='noun_chunk',
                start_offset=segment_start,
                end_offset=segment_end,
                confidence=_BR_CONCEPT_CONFIDENCE_NOUN_CHUNK,
                boundary_limited=segment_text != text,
            )
    return candidates


def _collect_entity_label_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload['source_text_id']
    sentences = input_payload['sentences']
    candidates: list[dict[str, Any]] = []
    for entity in input_payload.get('entities', []):
        text = entity.get('text', '')
        if not isinstance(text, str) or text.strip() == '':
            continue
        _append_candidate(
            candidates,
            source_text_id=source_text_id,
            sentences=sentences,
            text=text,
            lemma=text,
            source='entity_label',
            start_offset=entity.get('start_offset', 0),
            end_offset=entity.get('end_offset', 0),
            confidence=_BR_CONCEPT_CONFIDENCE_ENTITY_LABEL,
        )
    return candidates


def _collect_noun_token_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload['source_text_id']
    sentences = input_payload['sentences']
    candidates: list[dict[str, Any]] = []
    for token in input_payload.get('tokens', []):
        pos = token.get('pos', '')
        if pos not in {'NOUN', 'PROPN'}:
            continue
        text = token.get('text', '')
        if not isinstance(text, str) or text.strip() == '':
            continue
        lemma = token.get('lemma', text)
        _append_candidate(
            candidates,
            source_text_id=source_text_id,
            sentences=sentences,
            text=text,
            lemma=lemma,
            source='noun_token',
            start_offset=token.get('start_offset', 0),
            end_offset=token.get('end_offset', 0),
            confidence=_BR_CONCEPT_CONFIDENCE_NOUN_TOKEN,
        )
    return candidates


def _collect_modifier_token_candidates(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    source_text_id = input_payload['source_text_id']
    sentences = input_payload['sentences']
    candidates: list[dict[str, Any]] = []
    for token in input_payload.get('tokens', []):
        pos = token.get('pos', '')
        dep = token.get('dependency', '')
        tag = token.get('tag', '')
        text = token.get('text', '')
        if not isinstance(text, str) or text.strip() == '':
            continue
        if pos == 'ADJ' and dep in {'amod', 'nsubj', 'conj', 'acomp', 'attr'}:
            _append_candidate(
                candidates,
                source_text_id=source_text_id,
                sentences=sentences,
                text=text,
                lemma=token.get('lemma', text),
                source='modifier_token',
                start_offset=token.get('start_offset', 0),
                end_offset=token.get('end_offset', 0),
                confidence=0.74,
            )
            continue
        if pos == 'VERB' and dep in {'conj', 'nsubj', 'nsubjpass', 'advcl'} and tag in {'VBZ', 'VBP', 'VBD', 'VBG', 'VBN'}:
            _append_candidate(
                candidates,
                source_text_id=source_text_id,
                sentences=sentences,
                text=text,
                lemma=token.get('lemma', text),
                source='modifier_token',
                start_offset=token.get('start_offset', 0),
                end_offset=token.get('end_offset', 0),
                confidence=0.72,
            )
    return candidates


_CLAUSE_NOISE_HEADS = {'ability', 'possibility', 'process', 'consequence'}
_RELATIVE_PRONOUNS = {'that', 'which', 'who', 'whom', 'whose'}


def _is_noisy_concept(candidate: dict[str, Any]) -> bool:
    normalized = str(candidate.get('normalized_text') or '').strip()
    tokens = [token for token in normalized.split(' ') if token]
    if not tokens:
        return True
    if tokens[0] in _RELATIVE_PRONOUNS or normalized in _RELATIVE_PRONOUNS:
        return True
    if len(tokens) >= 2 and tokens[0] in {'type', 'kind', 'category', 'form'} and tokens[1] == 'of':
        return True
    if normalized not in _LEXICALIZED_PREPOSITIONAL_TERMS and any(token in _CONTEXT_BOUNDARY_PREPOSITIONS for token in tokens[1:]):
        return True
    compact = ''.join(tokens)
    if compact.startswith(('typeof', 'kindof', 'categoryof', 'formof')):
        return True
    if tokens[0] in _CLAUSE_NOISE_HEADS and ('of' in tokens or 'that' in tokens):
        return True
    if any(token in _RELATIVE_PRONOUNS for token in tokens[1:]):
        return True
    return False


def _dedupe_deterministic(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for concept in candidates:
        dedupe_key = (_normalize_text(str(concept.get('normalized_text', concept.get('lemma', '')))), _normalize_text(concept['text']))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        unique.append(concept)
    return unique


def _rebuild_concept(candidate: dict[str, Any], text: str, lemma: str, start_offset: int, end_offset: int) -> dict[str, Any]:
    return {
        **candidate,
        'text': text,
        'lemma': lemma,
        'normalized_text': _normalize_phrase(text),
        'start_offset': start_offset,
        'end_offset': end_offset,
        'concept_id': _build_concept_id(str(candidate.get('source_text_id', '')), lemma, text),
    }


def _split_expanded_contextual_candidate(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    text = str(candidate.get('text', '')).strip()
    normalized = _normalize_phrase(text)
    tokens = [token for token in normalized.split(' ') if token]
    has_context_boundary = normalized not in _LEXICALIZED_PREPOSITIONAL_TERMS and any(token in _CONTEXT_BOUNDARY_PREPOSITIONS for token in tokens[1:])
    if not has_context_boundary:
        stripped_text, stripped_start, stripped_end = _strip_clausal_prefix(text, int(candidate.get('start_offset', 0) or 0))
        if stripped_text != text:
            return [_rebuild_concept(candidate, stripped_text, _segment_lemma(stripped_text, str(candidate.get('lemma', ''))), stripped_start, stripped_end)]
        return [candidate]

    root_lemma = str(candidate.get('lemma') or text)
    segments = _split_contextual_prepositional_phrase(text, int(candidate.get('start_offset', 0) or 0), root_lemma)
    return [_rebuild_concept(candidate, segment_text, segment_lemma, segment_start, segment_end) for segment_text, segment_lemma, segment_start, segment_end in segments]


def extract_concepts_from_payload(input_payload: dict[str, Any], doc: Any) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    candidates.extend(_collect_noun_chunk_candidates(input_payload, doc))
    candidates.extend(_collect_entity_label_candidates(input_payload))
    candidates.extend(_collect_noun_token_candidates(input_payload))
    candidates.extend(_collect_modifier_token_candidates(input_payload))

    expanded_candidates = [_expand_candidate(candidate, doc) for candidate in candidates]
    boundary_candidates = [segment for candidate in expanded_candidates for segment in _split_expanded_contextual_candidate(candidate)]
    concepts = _dedupe_deterministic([candidate for candidate in boundary_candidates if not _is_noisy_concept(candidate)])

    return {
        'raw_text': input_payload['raw_text'],
        'source_text_id': input_payload['source_text_id'],
        'metadata': input_payload.get('metadata', {}),
        'preprocessed_text': input_payload['preprocessed_text'],
        'operations_applied': input_payload.get('operations_applied', []),
        'sentences': input_payload['sentences'],
        'tokens': input_payload['tokens'],
        'entities': input_payload['entities'],
        'concepts': concepts,
    }
