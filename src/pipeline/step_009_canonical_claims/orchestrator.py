from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

_STAGE = 'semantic_claims'
_COMPAT_STAGE = 'canonical_claims'
_ARTICLES = {'a', 'an', 'the', 'any', 'each', 'one', 'more'}
_STOP_TAIL = re.compile(r'\b(?:focused|designed|intended|used|required)\b.*$', re.IGNORECASE)
_RELATIVE_TAIL = re.compile(r'\bthat\s+(?P<verb>[a-z]+s?)\s+(?P<object>.+)$', re.IGNORECASE)


def _clean(value: str | None) -> str:
    return re.sub(r'\s+', ' ', (value or '').strip())


def _words(value: str | None) -> list[str]:
    return [token for token in re.sub(r'[^A-Za-z0-9]+', ' ', value or '').split() if token]


def _singular(token: str) -> str:
    lower = token.casefold()
    if len(lower) > 3 and lower.endswith('ies'):
        return token[:-3] + 'y'
    if len(lower) > 4 and lower.endswith(('ses', 'xes', 'zes', 'ches', 'shes')):
        return token[:-2]
    if len(lower) > 3 and lower.endswith('s') and not lower.endswith(('ss', 'us', 'is')):
        return token[:-1]
    return token


def _phrase(value: str | None) -> str:
    text = _STOP_TAIL.sub('', _clean(value or ''))
    text = re.sub(r'\b(?:that|which|who)\b.*$', '', text, flags=re.IGNORECASE)
    tokens = _words(text)
    while tokens and tokens[0].casefold() in _ARTICLES:
        tokens.pop(0)
    normalized = []
    for index, token in enumerate(tokens):
        lower = token.casefold()
        normalized.append(lower if index > 0 and tokens[index - 1].casefold() == 'of' else _singular(lower))
    return ' '.join(normalized)


def _label(value: str | None) -> str:
    raw_tokens = _words(value or '')
    raw_by_lower = {token.casefold(): token for token in raw_tokens}
    parts = []
    for part in _phrase(value).split():
        raw = raw_by_lower.get(part.casefold(), '')
        parts.append(raw if raw.isupper() and len(raw) <= 4 else part[:1].upper() + part[1:])
    return ''.join(parts)


def _split_list(value: str | None) -> list[str]:
    text = _clean(value or '').rstrip('.')
    text = re.sub(r'\b(?:and|or)\b', ',', text, flags=re.IGNORECASE)
    return [label for part in text.split(',') if (label := _label(part))]


def _objects(value: str | None) -> list[str]:
    return [item for item in _split_list(value) if item]


def _verb(value: str | None) -> str:
    words = _words(value or '')
    token = (words[0].casefold() if words else '').replace(' ', '_')
    if not token:
        return ''
    if token.endswith('ing'):
        base = token[:-3]
        if len(base) > 2 and base[-1] == base[-2]:
            base = base[:-1]
        token = base
    if token.endswith('ies'):
        return token
    if token.endswith(('s', 'ss')):
        return token
    if token.endswith('y'):
        return token[:-1] + 'ies'
    if token.endswith(('x', 'z', 'ch', 'sh')):
        return token + 'es'
    return token + 's'


def _strip_modifiers(value: str) -> str:
    return re.sub(r'^(?:strategic|mandatory|good|technical|suspicious)\s+', '', _clean(value), flags=re.IGNORECASE)


def _paragraph_map(raw_text: str, sentences: list[dict[str, Any]], asset_ids: list[str] | None = None) -> dict[str, str]:
    starts: list[tuple[int, int]] = []
    cursor = 0
    for index, fragment in enumerate(re.split(r'\n\s*\n', raw_text), start=1):
        offset = raw_text.find(fragment, cursor)
        if offset < 0:
            offset = cursor
        starts.append((index, offset))
        cursor = offset + len(fragment)
    result: dict[str, str] = {}
    for sentence in sentences:
        sid = str(sentence.get('sentence_id', ''))
        start = int(sentence.get('start_offset', 0) or 0)
        paragraph_index = 1
        for candidate, offset in starts:
            if start >= offset:
                paragraph_index = candidate
        if sid:
            external_id = asset_ids[paragraph_index - 1] if asset_ids and paragraph_index <= len(asset_ids) else ''
            result[sid] = external_id or f'paragraph-{paragraph_index:03d}'
    return result


def _claim_id(source_text_id: str, sentence_id: str, statement: str) -> str:
    digest = hashlib.sha256(f'{source_text_id}|{sentence_id}|{statement}'.encode('utf-8')).hexdigest()[:16]
    return f'claim-{digest}'


def _make_claim(
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    statement: str,
    kind: str,
    **parts: str,
) -> dict[str, Any]:
    source = {
        'source_text_id': source_text_id,
        'sentence_id': str(sentence.get('sentence_id', '')),
        'paragraph_id': paragraph_id,
        'asset_id': paragraph_id,
        'evidence': str(sentence.get('text', '')).strip(),
    }
    return {
        'claim_id': _claim_id(source_text_id, source['sentence_id'], statement),
        'statement': statement,
        'normalized_statement': statement,
        'kind': kind,
        'source': source,
        'paragraph_id': paragraph_id,
        **{k: v for k, v in parts.items() if v},
    }


def _append(
    claims: list[dict[str, Any]],
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    statement: str,
    kind: str,
    **parts: str,
) -> None:
    if statement and statement not in {claim['statement'] for claim in claims}:
        claims.append(_make_claim(source_text_id, sentence, paragraph_id, statement, kind, **parts))


def _append_relation(
    claims: list[dict[str, Any]],
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    subject: str,
    predicate: str,
    obj: str,
    **parts: str,
) -> None:
    _append(
        claims,
        source_text_id,
        sentence,
        paragraph_id,
        f'{subject} {predicate} {obj}',
        'relation',
        subject=subject,
        predicate=predicate,
        object=obj,
        **parts,
    )


def _append_definition(
    claims: list[dict[str, Any]],
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    subject: str,
    predicate: str,
    obj: str,
) -> None:
    _append(
        claims,
        source_text_id,
        sentence,
        paragraph_id,
        f'{subject} is a {obj}',
        'definition',
        subject=subject,
        predicate=predicate,
        object=obj,
    )


def _append_list_relation(
    claims: list[dict[str, Any]],
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    subject: str,
    predicate: str,
    raw_objects: str,
) -> None:
    for obj in _objects(raw_objects):
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)


def _extract_relative_tail(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, subject: str, raw_tail: str) -> None:
    tail = raw_tail.strip().rstrip('.')
    rel = _RELATIVE_TAIL.search(tail)
    if not rel:
        return
    predicate = _verb(rel.group('verb'))
    objects = rel.group('object')
    purpose = re.search(r'\s+for\s+(?P<gerund>\w+ing)\s+(?P<target>.+)$', objects, flags=re.IGNORECASE)
    if purpose:
        objects = objects[:purpose.start()].strip()
    _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, objects)
    if purpose:
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(purpose.group('gerund')), purpose.group('target'))


def _extract_type_definition(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, subject: str, raw_object: str) -> bool:
    type_match = re.match(r'^(?:a|an|the|any)?\s*(?:type|kind|category|form)\s+of\s+(?P<parent>.+)$', raw_object, flags=re.IGNORECASE)
    parent_source = type_match.group('parent') if type_match else raw_object
    parts = re.split(r'\bthat\b', parent_source, maxsplit=1, flags=re.IGNORECASE)
    head = parts[0]
    tail = parts[1] if len(parts) > 1 else ''
    parent = _label(_strip_modifiers(head))
    if not parent:
        return False
    _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', parent)
    if tail:
        _extract_relative_tail(claims, source_text_id, sentence, paragraph_id, subject, 'that ' + tail)
    return True


def _extract_definition_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = re.match(r'^(?P<subject>.+?)\s+is\s+(?P<object>.+?)\.?$', text, flags=re.IGNORECASE)
    if not match:
        return False
    subject = _label(match.group('subject'))
    raw_object = match.group('object').strip().rstrip('.')
    if not subject:
        return False
    if _extract_type_definition(claims, source_text_id, sentence, paragraph_id, subject, raw_object):
        pass
    else:
        object_head = _label(re.split(r'\b(?:that|for)\b', raw_object, maxsplit=1, flags=re.IGNORECASE)[0])
        if object_head:
            _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', object_head)
        parts = re.split(r'\bthat\b', raw_object, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) > 1:
            _extract_relative_tail(claims, source_text_id, sentence, paragraph_id, subject, 'that ' + parts[1])
    required = re.search(r'\brequired\s+for\s+(?P<objects>.+)$', raw_object, flags=re.IGNORECASE)
    if required:
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, 'required_for', required.group('objects'))
    return True


def _extract_sentence_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str) -> None:
    text = _clean(str(sentence.get('text', '')))
    if not text:
        return
    purpose = re.match(r'^the\s+purpose\s+of\s+(?P<subject>.+?)\s+is\s+to\s+(?P<verb>\w+)\s+(?P<objects>.+?)\.?$', text, flags=re.IGNORECASE)
    if purpose:
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, _label(purpose.group('subject')), _verb(purpose.group('verb')), purpose.group('objects'))
        return
    if _extract_definition_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    by_action = re.match(r'^(?P<subject>.+)\s+(?P<verb>\w+(?:s|ing))\s+(?P<object>.+?)\s+by\s+(?P<gerund>\w+ing)\s+(?P<items>.+?)\.?$', text, flags=re.IGNORECASE)
    if by_action:
        subject = _label(by_action.group('subject'))
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} {_verb(by_action.group("verb"))} {_label(by_action.group("object"))}', 'relation', subject=subject, predicate=_verb(by_action.group('verb')), object=_label(by_action.group('object')))
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(by_action.group('gerund')), by_action.group('items'))
        return
    oversight = re.match(r'^(?P<subject>.+?)\s+provides\s+(?P<qualifier>.+?)\s+oversight\s+for\s+(?P<object>.+?)\.?$', text, flags=re.IGNORECASE)
    if oversight:
        _append(claims, source_text_id, sentence, paragraph_id, f'{_label(oversight.group("subject"))} provides oversight for {_label(oversight.group("object"))}', 'relation', subject=_label(oversight.group('subject')), predicate='provides_oversight_for', object=_label(oversight.group('object')))
        return
    two_actions = re.match(r'^(?P<subject>.+?)\s+(?P<verb1>\w+s)\s+(?P<object1>.+?)\s+and\s+(?P<verb2>\w+s|must)\s+(?P<object2>.+?)\.?$', text, flags=re.IGNORECASE)
    if two_actions:
        subject = _label(two_actions.group('subject'))
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(two_actions.group('verb1')), two_actions.group('object1'))
        object2 = two_actions.group('object2')
        if _verb(two_actions.group('verb2')) == 'musts':
            parts = object2.split(' ', 1)
            if len(parts) == 2:
                _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(parts[0]), parts[1])
            return
        support = re.match(r'(?P<resource>.+?)\s+for\s+(?P<target>.+)$', object2, flags=re.IGNORECASE)
        if support:
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(two_actions.group('verb2')), support.group('resource'))
            for resource in _objects(support.group('resource')):
                _append_list_relation(claims, source_text_id, sentence, paragraph_id, resource, 'supports', support.group('target'))
        else:
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(two_actions.group('verb2')), object2)
        return
    form = re.match(r'^(?P<subjects>.+?)\s+form\s+(?P<object>.+?)\.?$', text, flags=re.IGNORECASE)
    if form:
        target = _label(form.group('object'))
        members = _split_list(form.group('subjects'))
        if members:
            parents = {str(claim.get('object', '')) for claim in claims if claim.get('subject') in members and claim.get('predicate') in {'is_a', 'type_of'}}
            subject = next(iter(parents)) if len(parents) == 1 and next(iter(parents)) else members[0]
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} forms {target}', 'relation', subject=subject, predicate='forms', object=target, members=','.join(members))
        return
    if _extract_definition_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    shared_object = re.match(r'^(?P<subject>.+?)\s+(?P<verbs>\w+s(?:\s+and\s+\w+s)*)\s+(?P<object>.+?)(?:\s+that\s+(?P<tail>.+))?\.?$', text, flags=re.IGNORECASE)
    if shared_object:
        subject = _label(shared_object.group('subject'))
        raw_object = shared_object.group('object')
        with_match = re.match(r'(?P<object>.+?)\s+with\s+(?P<target>.+)$', raw_object, flags=re.IGNORECASE)
        object_text = with_match.group('object') if with_match else raw_object
        object_label = _label(object_text)
        for verb_word in re.split(r'\s+and\s+', shared_object.group('verbs'), flags=re.IGNORECASE):
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(verb_word), object_text)
        if with_match:
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, object_label, 'checked_against', with_match.group('target'))
        tail = shared_object.group('tail') or ''
        if tail:
            tail_match = re.match(r'(?P<verbs>\w+(?:\s+or\s+\w+)*)\s+(?P<object>.+)$', tail.rstrip('.'), flags=re.IGNORECASE)
            if tail_match:
                for verb_word in re.split(r'\s+or\s+', tail_match.group('verbs'), flags=re.IGNORECASE):
                    _append_list_relation(claims, source_text_id, sentence, paragraph_id, object_label, _verb(verb_word), tail_match.group('object'))
        return



def _extract_definition_claims_compat(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = re.match(r'^(?P<subject>.+?)\s+is\s+(?P<object>.+?)\.?$', text, flags=re.IGNORECASE)
    if not match:
        return False
    subject = _label(match.group('subject'))
    raw_object = match.group('object').strip().rstrip('.')
    type_match = re.match(r'^(?:a|an|the|any)?\s*(?:type|kind|category|form)\s+of\s+(?P<parent>.+)$', raw_object, flags=re.IGNORECASE)
    if type_match:
        parent = _label(type_match.group('parent'))
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} is a type of {parent}', 'type_of', subject=subject, predicate='type_of', object=parent)
        return True
    object_head = _label(raw_object.split(' for ', 1)[0])
    if object_head:
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} is a {object_head}', 'definition', subject=subject, predicate='is_a', object=object_head)
    if re.search(r'\bfocused\s+on\s+protecting\b', raw_object, flags=re.IGNORECASE):
        protected = re.search(r'focused\s+on\s+protecting\s+(?P<object>.+?)(?:\s+against\s+|$)', raw_object, flags=re.IGNORECASE)
        if protected:
            target = _label(protected.group('object'))
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} is focused on protecting {target}', 'relation', subject=subject, predicate='focused_on_protecting', object=target)
        against = re.search(r'\bagainst\s+(?P<objects>.+)$', raw_object, flags=re.IGNORECASE)
        if against:
            for item in _split_list(against.group('objects')):
                obj = item if item.endswith('Threat') else f'{item}Threat'
                _append(claims, source_text_id, sentence, paragraph_id, f'{subject} protects against {obj}', 'relation', subject=subject, predicate='protects_against', object=obj)
    if re.search(r'\bmodel\s+for\b', raw_object, flags=re.IGNORECASE):
        model_target = _label(re.split(r'\bfor\b', raw_object, maxsplit=1, flags=re.IGNORECASE)[1])
        if model_target:
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} is a model for {model_target}', 'relation', subject=subject, predicate='models', object=model_target)
    value_for = re.search(r'\bhas\s+value\s+for\s+(?P<object>.+?)(?:\s+and\s+that\s+|$)', raw_object, flags=re.IGNORECASE)
    if value_for:
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} has value for {_label(value_for.group("object"))}', 'relation', subject=subject, predicate='has_value_for', object=_label(value_for.group('object')))
    action_tail = re.search(r'\bthat\s+(?P<tail>.+)$', raw_object, flags=re.IGNORECASE)
    if action_tail:
        tail = action_tail.group('tail')
        for verb in ('stores', 'processes', 'transmits', 'represents'):
            if re.search(rf'\b{verb}\b', tail, flags=re.IGNORECASE):
                _append(claims, source_text_id, sentence, paragraph_id, f'{subject} {verb} Information', 'relation', subject=subject, predicate=verb, object='Information')
    ensure_access = re.search(r'ensures\s+(?P<object>.+?)\s+(?:is|are)\s+accessible\s+only\s+to\s+(?P<target>.+)$', raw_object, flags=re.IGNORECASE)
    if ensure_access:
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} ensures {_label(ensure_access.group("object"))} is accessible only to {_label(ensure_access.group("target"))}', 'relation', subject=subject, predicate='ensures_accessible_to', object=_label(ensure_access.group('target')), patient=_label(ensure_access.group('object')))
    ensure_quality = re.search(r'ensures\s+(?P<object>.+?)\s+(?:is|are)\s+(?P<qualities>.+)$', raw_object, flags=re.IGNORECASE)
    if ensure_quality:
        patient = _label(ensure_quality.group('object'))
        qualities = ensure_quality.group('qualities')
        if re.search(r'\baccurate\b', qualities, flags=re.IGNORECASE):
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} ensures {patient} is accurate', 'relation', subject=subject, predicate='ensures_accuracy_of', object=patient)
        if re.search(r'\bcomplete\b', qualities, flags=re.IGNORECASE):
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} ensures {patient} is complete', 'relation', subject=subject, predicate='ensures_completeness_of', object=patient)
        protected = re.search(r'protected\s+against\s+(?P<object>.+)$', qualities, flags=re.IGNORECASE)
        if protected:
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} protects {patient} against {_label(protected.group("object"))}', 'relation', subject=subject, predicate='protects_against', object=_label(protected.group('object')), patient=patient)
    ensure_available = re.search(r'ensures\s+(?P<objects>.+?)\s+(?:is|are)\s+accessible\s+when\s+needed', raw_object, flags=re.IGNORECASE)
    if ensure_available:
        for item in _split_list(ensure_available.group('objects')):
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} ensures {item} is accessible when needed', 'relation', subject=subject, predicate='ensures_availability_of', object=item)
    return True



def _extract_sentence_claims_compat(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str) -> None:
    text = _clean(str(sentence.get('text', '')))
    if not text:
        return
    purpose = re.match(r'^the\s+purpose\s+of\s+(?P<subject>.+?)\s+is\s+to\s+preserve\s+(?P<objects>.+?)\.?$', text, flags=re.IGNORECASE)
    if purpose:
        subject = _label(purpose.group('subject'))
        for item in _split_list(purpose.group('objects')):
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} preserves {item}', 'relation', subject=subject, predicate='preserves', object=item)
        return
    form = re.match(r'^(?P<subjects>.+?)\s+form\s+(?P<object>.+?)\.?$', text, flags=re.IGNORECASE)
    if form:
        target = _label(form.group('object'))
        members = _split_list(form.group('subjects'))
        if members:
            parents = {str(claim.get('object', '')) for claim in claims if claim.get('subject') in members and claim.get('predicate') in {'is_a', 'type_of'}}
            subject = next(iter(parents)) if len(parents) == 1 and next(iter(parents)) else members[0]
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} forms {target}', 'relation', subject=subject, predicate='forms', object=target, members=','.join(members))
        return
    _extract_definition_claims_compat(claims, source_text_id, sentence, paragraph_id, text)


def _resolve_semantic_references(claims: list[dict[str, Any]]) -> None:
    subjects = [str(claim.get('subject', '')) for claim in claims if str(claim.get('subject', ''))]
    by_tail: dict[str, str] = {}
    for subject in subjects:
        tail = re.sub(r'(?<!^)([A-Z])', r' \1', subject).split()[-1] if subject else ''
        if tail and tail not in by_tail:
            by_tail[tail] = subject
    for claim in claims:
        obj = str(claim.get('object', ''))
        if obj in by_tail and by_tail[obj] != obj:
            resolved = by_tail[obj]
            claim['object'] = resolved
            predicate = str(claim.get('predicate', ''))
            subject = str(claim.get('subject', ''))
            claim['statement'] = f'{subject} {predicate} {resolved}'
            claim['normalized_statement'] = claim['statement']


def _canonical_claims_config(config: dict[str, Any] | None) -> dict[str, Any]:
    return config if isinstance(config, dict) else {}


def _configured_artifact_path(config: dict[str, Any]) -> Path | None:
    raw_path = config.get('artifact_path') or config.get('output_path')
    if raw_path in (None, ''):
        return None
    return Path(raw_path)


def _configured_asset_ids(config: dict[str, Any]) -> list[str] | None:
    raw_ids = config.get('paragraph_asset_ids') or config.get('asset_ids')
    if not isinstance(raw_ids, list):
        return None
    ids = [str(item).strip() for item in raw_ids if str(item).strip()]
    return ids or None


def extract_canonical_claims_from_payload(input_payload: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    stage_config = _canonical_claims_config(config)
    source_text_id = str(input_payload.get('source_text_id', ''))
    sentences = [item for item in input_payload.get('sentences', []) if isinstance(item, dict)]
    paragraphs = _paragraph_map(str(input_payload.get('raw_text') or input_payload.get('preprocessed_text') or ''), sentences, _configured_asset_ids(stage_config))
    claims: list[dict[str, Any]] = []
    emit_semantic = bool(stage_config.get('emit_semantic_claims'))
    extractor = _extract_sentence_claims if emit_semantic else _extract_sentence_claims_compat
    for sentence in sentences:
        paragraph_id = paragraphs.get(str(sentence.get('sentence_id', '')), '')
        extractor(claims, source_text_id, sentence, paragraph_id)
    if emit_semantic:
        _resolve_semantic_references(claims)
    payload = {
        'stage': _STAGE if emit_semantic else _COMPAT_STAGE,
        'claim_count': len(claims),
        'claims': claims,
    }
    path = _configured_artifact_path(stage_config)
    result = {k: v for k, v in input_payload.items() if not k.startswith('_spacy')}
    result['canonical_claims'] = {**payload, 'stage': _COMPAT_STAGE}
    artifacts = result.get('artifacts') if isinstance(result.get('artifacts'), dict) else {}
    artifacts = {**artifacts, 'canonical_claims': result['canonical_claims']}
    if emit_semantic:
        result['semantic_claims'] = payload
        artifacts['semantic_claims'] = payload
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload if emit_semantic else result['canonical_claims'], ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        artifacts['semantic_claims_path' if emit_semantic else 'canonical_claims_path'] = str(path)
    result['artifacts'] = artifacts
    return result
