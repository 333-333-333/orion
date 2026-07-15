"""Orchestrate the concept extraction pipeline stage while preserving the payload contract."""

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
    """Normalize text."""
    return value.casefold().strip()


def _strip_leading_articles(value: str) -> str:
    """Remove leading articles."""
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
    """Normalize phrase."""
    normalized = re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value or ''))
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return _strip_leading_articles(normalized)


def _resolve_sentence_id(sentences: list[dict[str, Any]], start_offset: int, end_offset: int) -> str:
    """Return the sentence containing a source span, or an empty identifier."""
    for sentence in sentences:
        if sentence['start_offset'] <= start_offset and end_offset <= sentence['end_offset']:
            return sentence['sentence_id']
    return ''


def _build_concept_id(source_text_id: str, lemma: str, text: str) -> str:
    """Build concept ID."""
    stable_key = f"{source_text_id}|{_normalize_text(lemma)}|{_normalize_text(text)}".encode('utf-8')
    digest = hashlib.sha256(stable_key).hexdigest()[:16]
    return f"con-{digest}"


def _trimmed_span(value: str, start_offset: int, end_offset: int) -> tuple[str, int, int]:
    """Trim surrounding whitespace while preserving absolute source offsets."""
    left = 0
    right = len(value)
    while left < right and value[left].isspace():
        left += 1
    while right > left and value[right - 1].isspace():
        right -= 1
    return value[left:right], start_offset + left, start_offset + right if end_offset >= start_offset else end_offset


def _is_temporal_context(value: str) -> bool:
    """Return whether a phrase contains only a supported clock-time expression."""
    return bool(_TEMPORAL_CONTEXT_PATTERN.match(value))


def _strip_clausal_prefix(value: str, start_offset: int) -> tuple[str, int, int]:
    """Remove clausal prefix."""
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
    """Choose the final content token as a segment lemma, with a fallback."""
    tokens = [token for token in re.sub(r"[^A-Za-z0-9']+", ' ', value).split() if token.casefold() not in _PHRASE_ARTICLES]
    return tokens[-1] if tokens else fallback


def _split_contextual_prepositional_phrase(text: str, start_offset: int, root_lemma: str) -> list[tuple[str, str, int, int]]:
    """Split contextual prepositional phrase."""
    trimmed_text, trimmed_start, _ = _trimmed_span(text, start_offset, start_offset + len(text))
    normalized = _normalize_phrase(trimmed_text)
    # Terms such as "data at rest" are lexical units, not a concept plus removable context.
    if not trimmed_text or normalized in _LEXICALIZED_PREPOSITIONAL_TERMS:
        return [(trimmed_text, root_lemma, trimmed_start, trimmed_start + len(trimmed_text))] if trimmed_text else []

    # A preposition next to a hyphen belongs to the compound and must not split the phrase.
    matches = [
        match for match in _CONTEXT_BOUNDARY_PATTERN.finditer(trimmed_text)
        if not (
            (match.start() > 0 and trimmed_text[match.start() - 1] in _PHRASE_HYPHENS)
            or (match.end() < len(trimmed_text) and trimmed_text[match.end()] in _PHRASE_HYPHENS)
        )
    ]
    if not matches:
        return [(trimmed_text, root_lemma, trimmed_start, trimmed_start + len(trimmed_text))]

    segments: list[tuple[str, str, int, int]] = []
    cursor = 0
    for match in matches:
        raw_segment, segment_start, segment_end = _trimmed_span(trimmed_text[cursor:match.start()], trimmed_start + cursor, trimmed_start + match.start())
        raw_segment, segment_start, segment_end = _strip_clausal_prefix(raw_segment, segment_start)
        # Clock expressions provide context but are not useful standalone ontology classes.
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
    """Append a concept candidate with deterministic identity, span, and confidence metadata."""
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
    """Return whether a token is a configured phrase connector."""
    text = getattr(token, 'text', '') or ''
    return text.casefold() in _PHRASE_CONNECTORS


def _token_kind(token: Any, previous: Any | None = None) -> str:
    """Classify a token by whether it can extend a concept phrase."""
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
        dependency = getattr(token, 'dep_', '') or ''
        head_text = getattr(getattr(token, 'head', None), 'text', '') or ''
        adjacent_text = getattr(previous, 'text', '') if previous is not None else ''
        # Attributive participles belong to noun phrases; clausal participles mark a boundary.
        if 'Part' in verb_forms and dependency not in {'relcl', 'advcl'} and not (dependency == 'acl' and head_text == adjacent_text):
            return 'strong'
        if previous is not None and getattr(previous, 'pos_', '') in {'ADJ', 'ADV'}:
            return 'weak'

    return ''


def _expand_phrase_left(doc: Any, start: int) -> int:
    """Expand phrase left."""
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
    """Expand phrase right."""
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
    """Expand candidate."""
    start_offset = int(candidate.get('start_offset', 0) or 0)
    end_offset = int(candidate.get('end_offset', 0) or 0)
    output_candidate = {key: value for key, value in candidate.items() if key != '_boundary_limited'}
    char_span = getattr(doc, 'char_span', None)
    # Split candidates already encode a semantic boundary; re-expanding them would reattach context.
    can_expand = callable(char_span) and hasattr(doc, '__getitem__') and hasattr(doc, '__len__') and not candidate.get('_boundary_limited')
    span = char_span(start_offset, end_offset, alignment_mode='expand') if can_expand else None
    if span is None:
        expanded_text = str(candidate.get('text', '')).strip()
        article = re.match(r'^(?:a|an|the|any)\s+', expanded_text, flags=re.IGNORECASE)
        adjusted_start = int(candidate.get('start_offset', 0) or 0)
        if article:
            adjusted_start += article.end()
            expanded_text = expanded_text[article.end():]
        normalized_text = _normalize_phrase(expanded_text)
        lemma = str(candidate.get('lemma', '')).strip() or expanded_text
        return {
            **output_candidate,
            'text': expanded_text,
            'lemma': lemma,
            'normalized_text': normalized_text,
            'start_offset': adjusted_start,
            'concept_id': _build_concept_id(str(candidate.get('source_text_id', '')), lemma, expanded_text),
        }

    start = _expand_phrase_left(doc, span.start)
    end = _expand_phrase_right(doc, span.end)
    while start < end and getattr(doc[start], 'pos_', '') == 'DET' and getattr(doc[start], 'text', '').casefold() in _PHRASE_ARTICLES:
        start += 1
    while start < end and getattr(doc[start], 'pos_', '') == 'VERB' and getattr(doc[start], 'tag_', '') in {'VBG', 'VBN'} and getattr(doc[start], 'dep_', '') in {'pcomp', 'xcomp', 'advcl', 'relcl'}:
        start += 1
    while end > start and getattr(doc[end - 1], 'pos_', '') == 'VERB' and getattr(doc[end - 1], 'dep_', '') in {'acl', 'relcl', 'advcl'}:
        end -= 1
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
    """Collect noun chunk candidates."""
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
    """Collect entity label candidates."""
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
    """Collect noun token candidates."""
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
    """Collect modifier token candidates."""
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
    return candidates


_CLAUSE_NOISE_HEADS = {'ability', 'possibility', 'process', 'consequence'}
_RELATIVE_PRONOUNS = {'that', 'which', 'who', 'whom', 'whose'}


def _is_noisy_concept(candidate: dict[str, Any], verbal_spans: set[tuple[int, int]] | None = None) -> bool:
    """Return whether a candidate is verbal, scaffold, relative, contextual, or otherwise non-conceptual noise."""
    normalized = str(candidate.get('normalized_text') or '').strip()
    tokens = [token for token in normalized.split(' ') if token]
    if not tokens:
        return True
    if verbal_spans and len(tokens) == 1 and (int(candidate.get('start_offset', -1)), int(candidate.get('end_offset', -1))) in verbal_spans:
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
    """Deduplicate concepts by normalized label and sentence in source order."""
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for concept in candidates:
        dedupe_key = (_normalize_text(str(concept.get('normalized_text', concept.get('lemma', '')))), str(concept.get('sentence_id', '')))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        unique.append(concept)
    return unique


def _rebuild_concept(candidate: dict[str, Any], text: str, lemma: str, start_offset: int, end_offset: int) -> dict[str, Any]:
    """Rebuild concept."""
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
    """Split expanded contextual candidate."""
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


def _trim_verbal_boundaries(candidate: dict[str, Any], tokens: list[dict[str, Any]], raw_text: str) -> dict[str, Any]:
    """Trim verbal boundaries."""
    start = int(candidate.get('start_offset', 0) or 0)
    end = int(candidate.get('end_offset', 0) or 0)
    overlapping = sorted(
        [token for token in tokens if int(token.get('start_offset', -1)) >= start and int(token.get('end_offset', -1)) <= end],
        key=lambda token: int(token.get('start_offset', 0)),
    )
    removable = {'relcl', 'advcl', 'pcomp', 'xcomp'}
    while overlapping and overlapping[0].get('pos') == 'VERB' and (
        overlapping[0].get('tag') in {'VB', 'VBZ', 'VBP', 'VBD'}
        or overlapping[0].get('dependency') in removable
        or (
            overlapping[0].get('dependency') == 'acl'
            and len(overlapping) > 1
            and overlapping[0].get('head_text') == overlapping[1].get('text')
        )
    ):
        start = int(overlapping.pop(0).get('end_offset', start))
        while start < end and raw_text[start:end].startswith(' '):
            start += 1
    while overlapping and overlapping[-1].get('pos') == 'VERB' and (
        overlapping[-1].get('dependency') in removable
        or (
            overlapping[-1].get('dependency') == 'acl'
            and len(overlapping) > 1
            and overlapping[-1].get('head_text') == overlapping[-2].get('text')
        )
    ):
        end = int(overlapping.pop().get('start_offset', end))
        while end > start and raw_text[start:end].endswith(' '):
            end -= 1
    if start == int(candidate.get('start_offset', 0) or 0) and end == int(candidate.get('end_offset', 0) or 0):
        return candidate
    text = raw_text[start:end].strip()
    if not text:
        return candidate
    return _rebuild_concept(candidate, text, _segment_lemma(text, str(candidate.get('lemma', ''))), start, end)


def extract_concepts_from_payload(input_payload: dict[str, Any], doc: Any) -> dict[str, Any]:
    """Extract, normalize, filter, and deterministically deduplicate concept candidates."""
    candidates: list[dict[str, Any]] = []
    candidates.extend(_collect_noun_chunk_candidates(input_payload, doc))
    candidates.extend(_collect_entity_label_candidates(input_payload))
    candidates.extend(_collect_noun_token_candidates(input_payload))
    candidates.extend(_collect_modifier_token_candidates(input_payload))

    expanded_candidates = [_expand_candidate(candidate, doc) for candidate in candidates]
    boundary_candidates = [segment for candidate in expanded_candidates for segment in _split_expanded_contextual_candidate(candidate)]
    boundary_candidates = [
        _trim_verbal_boundaries(candidate, input_payload.get('tokens', []), str(input_payload.get('raw_text', '')))
        for candidate in boundary_candidates
    ]
    tokens = [token for token in input_payload.get('tokens', []) if isinstance(token, dict)]
    verbal_texts_by_sentence: dict[str, set[str]] = {}
    for token in tokens:
        if token.get('pos') == 'VERB':
            verbal_texts_by_sentence.setdefault(str(token.get('sentence_id', '')), set()).add(str(token.get('text', '')))
    coordinated_gerund_spans: set[tuple[int, int]] = set()
    # Coordination can form chains, so propagate verbal status to a fixed point before filtering concepts.
    changed = True
    while changed:
        changed = False
        for token in tokens:
            sentence_id = str(token.get('sentence_id', ''))
            text = str(token.get('text', ''))
            if (
                token.get('dependency') == 'conj'
                and text.casefold().endswith('ing')
                and str(token.get('head_text', '')) in verbal_texts_by_sentence.get(sentence_id, set())
                and text not in verbal_texts_by_sentence.get(sentence_id, set())
            ):
                verbal_texts_by_sentence.setdefault(sentence_id, set()).add(text)
                coordinated_gerund_spans.add((int(token.get('start_offset', -1)), int(token.get('end_offset', -1))))
                changed = True
    verbal_spans = {
        (int(token.get('start_offset', -1)), int(token.get('end_offset', -1)))
        for token in tokens
        if token.get('pos') == 'VERB'
    } | coordinated_gerund_spans
    concepts = _dedupe_deterministic([candidate for candidate in boundary_candidates if not _is_noisy_concept(candidate, verbal_spans)])

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
