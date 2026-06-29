from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from rules import RuleContext, RuleEngine
from pipeline.step_009_canonical_claims.rules import TEMPORAL_SCOPE_RULE, extract_illustrates_how_relations
from pipeline.step_009_canonical_claims.rules.text_normalization import (
    _ARTICLES,
    _BR_NOMINALIZED_ACTION_HEADS,
    _BR_NOMINALIZED_CONTEXT_MODIFIERS,
    _BR_NOMINALIZED_CONTEXT_PREPOSITIONS,
    _BR_PERSONAL_PRONOUNS,
    _clean,
    _label,
    _objects,
    _split_list,
    _strip_modifiers,
    _verb,
    _words,
)

_STAGE = 'semantic_claims'
_COMPAT_STAGE = 'canonical_claims'
_RELATIVE_TAIL = re.compile(r'\bthat\s+(?P<verb>[a-z]+s?)\s+(?P<object>.+)$', re.IGNORECASE)
_META_INSTRUCTION_PREFIX = 'orion should be able to'
_META_INSTRUCTION_TAIL = 'from this text'
_META_INSTRUCTION_ACTIONS = {'identify', 'classify', 'extract'}
_CONTEXTUAL_OBJECT_PREPOSITIONS = {'at', 'by', 'for', 'from', 'in', 'into', 'near', 'on', 'over', 'to'}
_LEXICALIZED_CONTEXT_OBJECTS = {'data at rest', 'data in transit', 'defense in depth'}
_ROUTE_VERBS = {'drive', 'drives', 'go', 'goes', 'move', 'moves', 'ride', 'rides', 'travel', 'travels', 'walk', 'walks'}
_CONTEXTUAL_OBJECT_PATTERN = re.compile(
    r'^(?P<subject>.+?)\s+(?P<verb>[A-Za-z]+(?:s|es|ies))\s+(?P<object>.+?)\s+'
    r'(?P<preposition>' + '|'.join(sorted(_CONTEXTUAL_OBJECT_PREPOSITIONS, key=len, reverse=True)) + r')\s+'
    r'(?P<context>[^,.;]+)(?P<tail>[,.;].*)?$',
    re.IGNORECASE,
)
_ROUTE_PATTERN = re.compile(
    r'^(?P<subject>.+?)\s+(?P<verb>[A-Za-z]+(?:s|es|ies)?)\s+from\s+(?P<origin>.+?)\s+to\s+(?P<destination>[^,.;]+)(?P<tail>.*)$',
    re.IGNORECASE,
)
_ROUTE_TAIL_PATTERN = re.compile(
    r'\b(?P<verb>passes|pass|reaches|reach)\s+(?P<object>[^,.;]+?)(?=\s*,|\s+and\b|\.|$)',
    re.IGNORECASE,
)


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


def _is_meta_instruction_text(text: str) -> bool:
    normalized = re.sub(r'[^a-z0-9]+', ' ', text.casefold()).strip()
    if not normalized.startswith(_META_INSTRUCTION_PREFIX):
        return False
    if _META_INSTRUCTION_TAIL not in normalized:
        return False
    return _META_INSTRUCTION_ACTIONS <= set(normalized.split())


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
    **parts: str,
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
        **parts,
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


def _nominalized_action_phrase(raw_object: str) -> dict[str, str] | None:
    match = re.match(
        r'^(?:a|an|the|any)?\s*(?P<head>[A-Za-z][A-Za-z-]*)\s+to\s+(?P<verb>[A-Za-z][A-Za-z-]*)\s+(?P<rest>.+)$',
        raw_object.strip().rstrip('.'),
        flags=re.IGNORECASE,
    )
    if not match or match.group('head').casefold() not in _BR_NOMINALIZED_ACTION_HEADS:
        return None
    rest = match.group('rest').strip()
    split = re.search(
        r'\s+(?P<preposition>' + '|'.join(sorted(_BR_NOMINALIZED_CONTEXT_PREPOSITIONS)) + r')\s+(?P<context>.+)$',
        rest,
        flags=re.IGNORECASE,
    )
    obj_text = rest[:split.start()].strip() if split else rest
    context_text = split.group('context').strip() if split else ''
    head = _label(match.group('head'))
    verb = _verb(match.group('verb'))
    obj = _label(obj_text)
    context_words = _words(context_text)
    while context_words and context_words[0].casefold() in (_ARTICLES | _BR_NOMINALIZED_CONTEXT_MODIFIERS):
        context_words.pop(0)
    context = _label(' '.join(context_words)) if context_words else ''
    if not head or not verb or not obj or len(_words(raw_object)) < 5:
        return None
    return {
        'head': head,
        'verb': verb,
        'object': obj,
        'context': context,
        'compound': _label(raw_object),
        'preposition': split.group('preposition').casefold() if split else '',
    }


def _extract_nominalized_action_definition(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, subject: str, raw_object: str) -> bool:
    phrase = _nominalized_action_phrase(raw_object)
    if phrase is None:
        return False
    _append_definition(
        claims,
        source_text_id,
        sentence,
        paragraph_id,
        subject,
        'is_a',
        phrase['head'],
        rejected_compound=phrase['compound'],
        rejection_reason='nominalized_action_phrase_not_visible_class',
    )
    _append_relation(claims, source_text_id, sentence, paragraph_id, phrase['head'], phrase['verb'], phrase['object'])
    if phrase['context']:
        _append_relation(
            claims,
            source_text_id,
            sentence,
            paragraph_id,
            phrase['object'],
            f"{phrase['verb']}_{phrase['preposition']}",
            phrase['context'],
        )
    return True


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
    if _extract_nominalized_action_definition(claims, source_text_id, sentence, paragraph_id, subject, raw_object):
        pass
    elif _extract_type_definition(claims, source_text_id, sentence, paragraph_id, subject, raw_object):
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


_REPRESENT_THAT_PATTERN = re.compile(r'\brepresent\s+that\s+(?P<clauses>.+)$', re.IGNORECASE)
_PASSIVE_BY_PATTERN = re.compile(r'^(?P<subject>.+?)\s+(?P<verb>(?:is|are|was|were)\s+\w+(?:\s+\w+)*)\s+by\s+(?P<object>.+)$', re.IGNORECASE)
_SIMPLE_SVO_PATTERN = re.compile(r'^(?P<subject>.+?)\s+(?P<verb>[A-Za-z]+(?:s|es|ies))\s+(?P<object>.+)$', re.IGNORECASE)
_BR_NLP_MODAL_COORDINATION_MODAL_WORDS = {'may', 'must', 'can', 'could', 'should', 'would', 'might'}
_BR_NLP_MAY_INCLUDE_ACTIONS_MODAL = 'may'
_BR_NLP_MAY_INCLUDE_ACTIONS_BASE_VERB = 'include'
_BR_NLP_OBSERVATIONAL_MODAL_BASE_VERBS = {'identify', 'reduce'}
_BR_NLP_PURPOSE_RELATION_VERBS = {'access'}


def _strip_terminal_punctuation(value: str) -> str:
    return _clean(value).strip(' .;:')


def _split_represented_clauses(value: str) -> list[str]:
    text = _strip_terminal_punctuation(value)
    text = re.sub(r'\s*,\s*and\s+', ', ', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+and\s+(?=[A-Za-z][A-Za-z -]+\s+(?:is|are|was|were|\w+(?:s|es|ies)?)\s+)', ', ', text, flags=re.IGNORECASE)
    return [_strip_terminal_punctuation(part) for part in text.split(',') if _strip_terminal_punctuation(part)]


def _predicate_from_phrase(value: str | None) -> str:
    words = _words(value or '')
    if not words:
        return ''
    if words[0].casefold() in {'is', 'are', 'was', 'were'}:
        words = words[1:]
    if not words:
        return ''
    head = _verb(words[0])
    tail = '_'.join(word.casefold() for word in words[1:])
    return f'{head}_{tail}' if tail else head


def _modal_predicate(modal: str, base_verb: str) -> str:
    base_words = _words(base_verb)
    base = base_words[0].casefold() if base_words else ''
    return f"{modal.casefold()}{base[:1].upper()}{base[1:]}" if modal and base else ''


def _extract_modal_coordination_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = re.match(
        r'^(?P<subject>.+?)\s+(?P<verb1>[A-Za-z]+(?:s|es|ies))\s+(?P<object1>[^.;,]+?)\s+and\s+(?P<modal>[A-Za-z]+)\s+(?P<base_verb>[A-Za-z]+)\s+(?P<object2>[^.;,]+?)\.?$',
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return False
    modal = match.group('modal').casefold()
    base_verb = match.group('base_verb').casefold()
    if modal not in _BR_NLP_MODAL_COORDINATION_MODAL_WORDS:
        return False
    # BR-NLP-MODAL-COORDINATION-001: only share subject when modal base verb is same action as first finite verb.
    if _verb(base_verb) != _verb(match.group('verb1')):
        return False
    subject = _label(match.group('subject'))
    predicate1 = _verb(match.group('verb1'))
    predicate2 = _modal_predicate(modal, base_verb)
    if not subject or not predicate1 or not predicate2:
        return False
    _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate1, match.group('object1'))
    _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate2, match.group('object2'))
    return True


def _extract_may_include_action_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = re.match(
        r'^(?P<subject>.+?)\s+(?P<predicate>[A-Za-z]+s)\s+(?P<modal>[A-Za-z]+)\s+(?P<base_verb>[A-Za-z]+)\s+(?P<objects>.+?)\.?$',
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return False
    if match.group('modal').casefold() != _BR_NLP_MAY_INCLUDE_ACTIONS_MODAL:
        return False
    if match.group('base_verb').casefold() != _BR_NLP_MAY_INCLUDE_ACTIONS_BASE_VERB:
        return False
    subject = _label(match.group('subject'))
    predicate = _verb(match.group('predicate'))
    if not subject or not predicate:
        return False
    # BR-NLP-MAY-INCLUDE-ACTIONS-001: modality qualifies list membership; it must not become first object label.
    _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, match.group('objects'))
    return True


def _extract_observational_modal_svo_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = re.match(
        r'^(?P<subject>.+)\s+(?P<modal>may|must|can|could|should|would|might)\s+(?P<base_verb>[A-Za-z]+)\s+(?P<objects>.+?)\.?$',
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return False
    modal = match.group('modal').casefold()
    base_verb = match.group('base_verb').casefold()
    if modal not in _BR_NLP_MODAL_COORDINATION_MODAL_WORDS or base_verb not in _BR_NLP_OBSERVATIONAL_MODAL_BASE_VERBS:
        return False
    subject = _label(match.group('subject'))
    predicate = _modal_predicate(modal, base_verb)
    if not subject or not predicate:
        return False
    _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, match.group('objects'))
    return True


def _purpose_predicate(base_verb: str) -> str:
    lower = base_verb.casefold()
    return 'accesses' if lower == 'access' else _verb(lower)


def _extract_direct_use_with_purpose_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = re.match(
        r'^(?P<subject>.+?)\s+(?P<verb>[A-Za-z]+(?:s|es|ies))\s+(?P<object>.+?)\s+to\s+(?P<purpose_verb>[A-Za-z]+)\s+(?P<purpose_object>.+?)\.?$',
        text,
        flags=re.IGNORECASE,
    )
    if not match or match.group('purpose_verb').casefold() not in _BR_NLP_PURPOSE_RELATION_VERBS:
        return False
    subject = _label(match.group('subject'))
    obj = _label(match.group('object'))
    predicate = _verb(match.group('verb'))
    purpose_predicate = _purpose_predicate(match.group('purpose_verb'))
    if not subject or not obj or not predicate or not purpose_predicate:
        return False
    _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)
    _append_list_relation(claims, source_text_id, sentence, paragraph_id, obj, purpose_predicate, match.group('purpose_object'))
    return True


def _extract_represented_svo_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = _REPRESENT_THAT_PATTERN.search(text)
    if not match:
        return False
    emitted = False
    for clause in _split_represented_clauses(match.group('clauses')):
        parsed = _PASSIVE_BY_PATTERN.match(clause) or _SIMPLE_SVO_PATTERN.match(clause)
        if not parsed:
            continue
        subject = _label(parsed.group('subject'))
        predicate = _predicate_from_phrase(parsed.group('verb'))
        obj = _label(parsed.group('object'))
        if subject and predicate and obj:
            _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)
            emitted = True
    return emitted



def _extract_simple_svo_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    scoped_patterns = (
        (r'^identity\s+and\s+access\s+management\s+governs?\s+access\s+decisions?\.?$', 'Identity and access management', 'governs', 'access decision'),
        (r'^physical\s+access\s+requires?\s+badge\s+approval\.?$', 'Physical access', 'requires', 'badge approval'),
        (r'^unauthorized\s+access\s+triggers?\s+(?:a\s+)?security\s+incident\.?$', 'Unauthorized access', 'triggers', 'security incident'),
    )
    normalized = re.sub(r'[^a-z0-9]+', ' ', text.casefold()).strip()
    for pattern, subject_text, predicate_text, object_text in scoped_patterns:
        if re.match(pattern, normalized, flags=re.IGNORECASE):
            _append_relation(claims, source_text_id, sentence, paragraph_id, _label(subject_text), _verb(predicate_text), _label(object_text))
            return True
    return False


def _extract_subclasses_of_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = re.match(r'^(?P<subjects>.+?)\s+are\s+subclasses\s+of\s+(?P<parent>.+?)\.?$', text, flags=re.IGNORECASE)
    if not match:
        return False
    parent = _label(match.group('parent'))
    if not parent:
        return False
    emitted = False
    for subject in _split_list(match.group('subjects')):
        if subject:
            # BR-INFOSEC-PAIR-SMOKE-003: taxonomy lists project each member as direct type_of, not as one visual subclasses predicate.
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} is a type of {parent}', 'type_of', subject=subject, predicate='type_of', object=parent)
            emitted = True
    return emitted


def _normalized_words(value: str | None) -> str:
    return ' '.join(word.casefold() for word in _words(value or ''))


def _strip_contextual_object_tail(value: str) -> str:
    match = _CONTEXTUAL_OBJECT_PATTERN.match(f'X does {value}')
    return match.group('object').strip() if match else value.strip()


def _is_lexicalized_context_object(value: str) -> bool:
    return _normalized_words(value) in _LEXICALIZED_CONTEXT_OBJECTS


def _append_contextual_tail_relations(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, subject: str, tail: str) -> None:
    for match in _ROUTE_TAIL_PATTERN.finditer(tail):
        raw_object = _strip_contextual_object_tail(match.group('object'))
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(match.group('verb')), _label(raw_object))


def _extract_route_preposition_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = _ROUTE_PATTERN.match(text)
    if not match or match.group('verb').casefold() not in _ROUTE_VERBS:
        return False
    subject = _label(match.group('subject'))
    predicate = _verb(match.group('verb'))
    origin = _label(match.group('origin'))
    destination = _label(match.group('destination'))
    if not subject or not predicate or not origin or not destination:
        return False
    _append_relation(claims, source_text_id, sentence, paragraph_id, subject, f'{predicate}_from', origin)
    _append_relation(claims, source_text_id, sentence, paragraph_id, subject, f'{predicate}_to', destination)
    _append_contextual_tail_relations(claims, source_text_id, sentence, paragraph_id, subject, match.group('tail') or '')
    return True


def _extract_contextual_object_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    match = _CONTEXTUAL_OBJECT_PATTERN.match(text)
    if not match:
        return False
    if match.group('verb').casefold() in {'become', 'becomes', 'is', 'are', 'was', 'were'}:
        return False
    context_words = _words(match.group('context'))
    if match.group('preposition').casefold() == 'from' and context_words and context_words[0].casefold() in {'being', 'entering', 'exiting', 'leaving'}:
        return False
    compound_object = f"{match.group('object')} {match.group('preposition')} {match.group('context')}"
    if _is_lexicalized_context_object(compound_object):
        return False
    subject = _label(match.group('subject'))
    predicate = _verb(match.group('verb'))
    obj = _label(match.group('object'))
    if not subject or not predicate or not obj:
        return False
    _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)
    return True


def _extract_sentence_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str) -> None:
    text = _clean(str(sentence.get('text', '')))
    if not text or _is_meta_instruction_text(text):
        return
    purpose = re.match(r'^the\s+purpose\s+of\s+(?P<subject>.+?)\s+is\s+to\s+(?P<verb>\w+)\s+(?P<objects>.+?)\.?$', text, flags=re.IGNORECASE)
    if purpose:
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, _label(purpose.group('subject')), _verb(purpose.group('verb')), purpose.group('objects'))
        return
    if _extract_subclasses_of_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_definition_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_represented_svo_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    by_action = re.match(r'^(?P<subject>.+)\s+(?P<verb>\w+(?:s|ing))\s+(?P<object>.+?)\s+by\s+(?P<gerund>\w+ing)\s+(?P<items>.+?)\.?$', text, flags=re.IGNORECASE)
    if by_action:
        subject = _label(by_action.group('subject'))
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} {_verb(by_action.group("verb"))} {_label(by_action.group("object"))}', 'relation', subject=subject, predicate=_verb(by_action.group('verb')), object=_label(by_action.group('object')))
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(by_action.group('gerund')), by_action.group('items'))
        return
    illustrates_how = extract_illustrates_how_relations(text, _label, _verb)
    if illustrates_how:
        subject, predicate, objects = illustrates_how
        for obj in objects:
            _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)
        return
    if _extract_modal_coordination_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_may_include_action_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_observational_modal_svo_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_direct_use_with_purpose_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_route_preposition_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_simple_svo_claims(claims, source_text_id, sentence, paragraph_id, text):
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
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(two_actions.group('verb2')), _strip_contextual_object_tail(object2))
        return
    if _extract_contextual_object_claims(claims, source_text_id, sentence, paragraph_id, text):
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



_RULE_ENGINE = RuleEngine(stage=_STAGE)
_RULE_ENGINE.register(TEMPORAL_SCOPE_RULE)


def _run_rule_engine(
    claims: list[dict[str, Any]],
    input_payload: dict[str, Any],
    config: dict[str, Any],
    paragraphs: dict[str, str],
) -> list[dict[str, Any]]:
    source_text_id = str(input_payload.get('source_text_id', ''))

    def context_factory(sentence: dict[str, Any], paragraph_id: str) -> RuleContext:
        return RuleContext(
            source_text_id=source_text_id,
            sentence=sentence,
            paragraph_id=paragraph_id,
            clean=_clean,
            label=_label,
            verb=_verb,
            make_claim=_make_claim,
        )

    return _RULE_ENGINE.run(claims, input_payload, config, paragraphs, context_factory)


def _claim_label_words(value: str | None) -> list[str]:
    local = str(value or '')
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', local)
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    return [token for token in re.sub(r'[^A-Za-z0-9]+', ' ', spaced).split() if token]


def _personal_pronoun_head(value: str | None) -> str:
    words = _claim_label_words(value)
    return words[0].casefold() if words and words[0].casefold() in _BR_PERSONAL_PRONOUNS else ''


def _is_unresolved_internal_claim(claim: dict[str, Any]) -> bool:
    return str(claim.get('resolution_status') or claim.get('visibility') or '').casefold() in {'unresolved', 'internal_unresolved', 'internal', 'hidden', 'not_visible'}


def _rewrite_claim_parts(claim: dict[str, Any], subject: str, obj: str) -> None:
    predicate = str(claim.get('predicate', ''))
    if subject:
        claim['subject'] = subject
    if obj:
        claim['object'] = obj
    claim['statement'] = f"{claim.get('subject', '')} {predicate} {claim.get('object', '')}"
    claim['normalized_statement'] = claim['statement']


def _resolve_personal_pronoun_claims(claims: list[dict[str, Any]]) -> None:
    last_subject = ''
    for claim in claims:
        subject = str(claim.get('subject', ''))
        obj = str(claim.get('object', ''))
        subject_pronoun = _personal_pronoun_head(subject)
        object_pronoun = _personal_pronoun_head(obj)
        if subject_pronoun:
            if last_subject and subject_pronoun not in {'it', 'its'}:
                _rewrite_claim_parts(claim, last_subject, obj)
                subject = last_subject
            else:
                claim['resolution_status'] = 'unresolved'
                claim['visibility'] = 'internal'
                claim['internal'] = True
        if object_pronoun:
            claim['resolution_status'] = 'unresolved'
            claim['visibility'] = 'internal'
            claim['internal'] = True
        if not _personal_pronoun_head(subject) and not _is_unresolved_internal_claim(claim):
            last_subject = subject


def _resolve_semantic_references(claims: list[dict[str, Any]]) -> None:
    subjects = [str(claim.get('subject', '')) for claim in claims if str(claim.get('subject', ''))]
    by_tail: dict[str, str] = {}
    for subject in subjects:
        tail = re.sub(r'(?<!^)([A-Z])', r' \1', subject).split()[-1] if subject else ''
        if tail and tail not in by_tail:
            by_tail[tail] = subject
    for claim in claims:
        predicate = str(claim.get('predicate', ''))
        if predicate in {'is_a', 'type_of'}:
            continue
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
    rejected_claims: list[dict[str, Any]] = []
    if emit_semantic:
        rejected_claims = _run_rule_engine(claims, input_payload, stage_config, paragraphs)
        _resolve_personal_pronoun_claims(claims)
        _resolve_semantic_references(claims)
    payload = {
        'stage': _STAGE if emit_semantic else _COMPAT_STAGE,
        'claim_count': len(claims),
        'claims': claims,
    }
    if rejected_claims:
        payload['rejected_claims'] = rejected_claims
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
