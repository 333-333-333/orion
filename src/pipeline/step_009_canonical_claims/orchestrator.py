"""Orchestrate the canonical claims pipeline stage while preserving the payload contract."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from rules import RuleContext, RuleEngine
from pipeline.step_009_canonical_claims.rules import TEMPORAL_SCOPE_RULE, extract_illustrates_how_relations
from pipeline.step_009_canonical_claims.rules.dependency_svo import extract_dependency_relations
from pipeline.step_009_canonical_claims.rules.remediation_a import extract_remediation_a_claim_specs
from pipeline.step_009_canonical_claims.rules.remediation_a2 import extract_remediation_a2_claim_specs
from pipeline.step_009_canonical_claims.rules.remediation_b import extract_remediation_b_claim_specs
from pipeline.step_009_canonical_claims.rules.remediation_b2 import extract_remediation_b2_claim_specs
from pipeline.step_009_canonical_claims.rules.remediation_b3 import REMEDIATION_B3_RULE
from pipeline.step_009_canonical_claims.rules.remediation_c import extract_remediation_c_claims
from pipeline.step_009_canonical_claims.rules.remediation_c2 import extract_remediation_c2_claims
from pipeline.step_009_canonical_claims.rules.remediation_c3 import extract_remediation_c3_claims
from pipeline.step_009_canonical_claims.rules.remediation_d import REMEDIATION_D_RULE
from pipeline.step_009_canonical_claims.rules.remediation_d2 import REMEDIATION_D2_RULE
from pipeline.step_009_canonical_claims.rules.remediation_d3 import REMEDIATION_D3_RULE
from pipeline.step_009_canonical_claims.rules.remediation_d4 import REMEDIATION_D4_RULE
from pipeline.step_009_canonical_claims.rules.text_normalization import (
    _ARTICLES,
    _BR_NOMINALIZED_ACTION_HEADS,
    _BR_NOMINALIZED_CONTEXT_MODIFIERS,
    _BR_NOMINALIZED_CONTEXT_PREPOSITIONS,
    _BR_PERSONAL_PRONOUNS,
    _clean,
    _label,
    _objects,
    _singular,
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
    """Map sentence identifiers to configured asset IDs or deterministic paragraph IDs."""
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
    """Return whether sentence text is instructional scaffolding rather than domain evidence."""
    normalized = re.sub(r'[^a-z0-9]+', ' ', text.casefold()).strip()
    if normalized.startswith(('another example ', 'these relationships ')):
        return True
    if not normalized.startswith(_META_INSTRUCTION_PREFIX):
        return False
    if _META_INSTRUCTION_TAIL not in normalized:
        return False
    return _META_INSTRUCTION_ACTIONS <= set(normalized.split())


def _claim_id(source_text_id: str, sentence_id: str, statement: str) -> str:
    """Build a deterministic claim ID from source, sentence, and statement."""
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
    """Build claim."""
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
    """Append a unique claim built from the supplied statement and source context."""
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
    """Append a unique relation claim with explicit subject, predicate, and object."""
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
    """Append a unique definition claim in canonical is-a statement form."""
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
    """Split an object list and append one relation claim per object."""
    for obj in _objects(raw_objects):
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)


def _alternative_group_id(source_text_id: str, sentence: dict[str, Any], signature: str) -> str:
    """Build a deterministic ID shared by disjunctive alternatives."""
    return _claim_id(source_text_id, str(sentence.get('sentence_id', '')), f'alternative:{signature}')


def _append_alternative_objects(
    claims: list[dict[str, Any]],
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    subject: str,
    predicate: str,
    raw_objects: str,
    **parts: str,
) -> None:
    """Append disjunctive object claims that share an auditable alternative group."""
    objects = _objects(raw_objects)
    group = _alternative_group_id(source_text_id, sentence, f'{subject}|{predicate}|{raw_objects}')
    for obj in objects:
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, subject, predicate, obj,
            modality='disjunctive_alternative', coordination='or', alternative_group=group, **parts,
        )


def _extract_relative_tail(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, subject: str, raw_tail: str) -> None:
    """Extract relative tail."""
    tail = raw_tail.strip().rstrip('.')
    alternative = re.search(
        r'\bthat\s+(?P<verb1>[A-Za-z]+(?:s|es|ies))\s+or\s+(?P<verb2>[A-Za-z]+(?:s|es|ies))\s+(?P<object>.+)$',
        tail,
        flags=re.IGNORECASE,
    )
    if alternative:
        obj = _label(alternative.group('object'))
        group = _alternative_group_id(source_text_id, sentence, f'{subject}|{alternative.group(0)}')
        for raw_verb in (alternative.group('verb1'), alternative.group('verb2')):
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                subject, _verb(raw_verb), obj,
                modality='disjunctive_alternative', coordination='or', alternative_group=group,
            )
        return
    rel = _RELATIVE_TAIL.search(tail)
    if not rel:
        return
    predicate = _verb(rel.group('verb'))
    objects = rel.group('object')
    purpose = re.search(r'\s+for\s+(?P<gerund>\w+ing)\s+(?P<target>.+)$', objects, flags=re.IGNORECASE)
    if purpose:
        objects = objects[:purpose.start()].strip()
    defined_objects = _objects(objects)
    for obj in defined_objects:
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)
    if purpose:
        purpose_predicate = f'has_purpose_to_{_singular(_verb(purpose.group("gerund")))}'
        for obj in defined_objects:
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                obj, purpose_predicate, _label(purpose.group('target')), modality='purpose',
            )


def _nominalized_action_phrase(raw_object: str) -> dict[str, str] | None:
    """Parse a guarded nominalized action into head, action, object, and context parts."""
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
    """Extract nominalized action definition."""
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


_DEFINITION_QUALIFIER_PATTERN = re.compile(
    r'\b(?P<marker>that|which|who|whose|where|because|derived\s+from|imposed\s+by|defined\s+in|defined\s+by|'
    r'caused\s+by|involving|implemented|used\s+by|used\s+for|hosted\s+in|related\s+to|based\s+on)\b',
    re.IGNORECASE,
)


def _split_definition_head(value: str) -> tuple[str, str, str]:
    """Split definition head."""
    match = _DEFINITION_QUALIFIER_PATTERN.search(value)
    if not match:
        return value.strip(), '', ''
    return value[:match.start()].strip(), match.group('marker').casefold(), value[match.end():].strip()


def _extract_type_definition(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, subject: str, raw_object: str) -> bool:
    """Extract type definition."""
    type_match = re.match(r'^(?:a|an|the|any)?\s*(?:type|kind|category|form)\s+of\s+(?P<parent>.+)$', raw_object, flags=re.IGNORECASE)
    parent_source = type_match.group('parent') if type_match else raw_object
    head, marker, tail = _split_definition_head(parent_source)
    parent = _label(_strip_modifiers(head))
    if not parent:
        return False
    _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', parent)
    if tail and marker in {'that', 'which', 'who', 'whose', 'where'}:
        _extract_relative_tail(claims, source_text_id, sentence, paragraph_id, subject, 'that ' + tail)
    return True


def _extract_definition_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract definition claims."""
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
        definition_head, _, _ = _split_definition_head(raw_object)
        object_head = _label(re.split(r'\bfor\b', definition_head, maxsplit=1, flags=re.IGNORECASE)[0])
        if object_head:
            _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', object_head)
        parts = re.split(r'\bthat\b', raw_object, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) > 1:
            _extract_relative_tail(claims, source_text_id, sentence, paragraph_id, subject, 'that ' + parts[1])
    required = re.search(r'\brequired\s+for\s+(?P<objects>.+)$', raw_object, flags=re.IGNORECASE)
    if required:
        raw_targets = required.group('objects')
        patient_words = _words(raw_object[:required.start()])
        required_subject = _label(patient_words[-1]) if patient_words else subject
        if re.search(r'\bor\b', raw_targets, flags=re.IGNORECASE):
            _append_alternative_objects(
                claims, source_text_id, sentence, paragraph_id,
                required_subject, 'required_for', raw_targets,
                patient=required_subject, requirement='required', context=subject,
            )
        else:
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, required_subject, 'required_for', raw_targets)
    return True


_REPRESENT_THAT_PATTERN = re.compile(r'\brepresent\s+that\s+(?P<clauses>.+)$', re.IGNORECASE)
_REPORTING_THAT_PATTERN = re.compile(
    r'^(?P<subject>.+?)\s+(?P<verb>tells?|says?|reports?|notes?|indicates?)'
    r'(?:\s+(?P<recipient>.+?))?\s+that\s+(?P<clauses>.+?)\.?$',
    re.IGNORECASE,
)
_PASSIVE_BY_PATTERN = re.compile(r'^(?P<subject>.+?)\s+(?P<verb>(?:is|are|was|were)\s+\w+(?:\s+\w+)*)\s+by\s+(?P<object>.+)$', re.IGNORECASE)
_SIMPLE_SVO_PATTERN = re.compile(r'^(?P<subject>.+?)\s+(?P<verb>[A-Za-z]+(?:s|es|ies))\s+(?P<object>.+)$', re.IGNORECASE)
_BR_NLP_MODAL_COORDINATION_MODAL_WORDS = {'may', 'must', 'can', 'could', 'should', 'would', 'might'}
_BR_NLP_MAY_INCLUDE_ACTIONS_MODAL = 'may'
_BR_NLP_MAY_INCLUDE_ACTIONS_BASE_VERB = 'include'
_BR_NLP_OBSERVATIONAL_MODAL_BASE_VERBS = {'identify', 'reduce'}
_BR_NLP_PURPOSE_RELATION_VERBS = {'access'}


def _strip_terminal_punctuation(value: str) -> str:
    """Remove terminal punctuation."""
    return _clean(value).strip(' .;:')


def _split_represented_clauses(value: str) -> list[str]:
    """Split represented clauses."""
    text = _strip_terminal_punctuation(value)
    text = re.sub(r'\s*,\s*and\s+', ', ', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+and\s+(?=[A-Za-z][A-Za-z -]+\s+(?:is|are|was|were|\w+(?:s|es|ies)?)\s+)', ', ', text, flags=re.IGNORECASE)
    return [_strip_terminal_punctuation(part) for part in text.split(',') if _strip_terminal_punctuation(part)]


def _predicate_from_phrase(value: str | None) -> str:
    """Convert a verb phrase into its canonical predicate form."""
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
    """Combine a modal and base verb into the canonical predicate label."""
    base_words = _words(base_verb)
    base = base_words[0].casefold() if base_words else ''
    return f"{modal.casefold()}{base[:1].upper()}{base[1:]}" if modal and base else ''


def _extract_modal_coordination_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract modal coordination claims."""
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
    """Extract may include action claims."""
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
    """Extract observational modal SVO claims."""
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
    """Return the canonical predicate used for a purpose action."""
    lower = base_verb.casefold()
    return 'accesses' if lower == 'access' else _verb(lower)


def _extract_direct_use_with_purpose_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract direct use with purpose claims."""
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


def _strip_reported_object_tail(raw_object: str) -> str:
    """Remove reported object tail."""
    return re.split(r'\s+as\s+', raw_object.strip().rstrip('.'), maxsplit=1, flags=re.IGNORECASE)[0].strip()


def _append_svo_clause_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, raw_clauses: str) -> bool:
    """Parse supported clauses and append complete SVO claims, returning whether any were emitted."""
    emitted = False
    for clause in _split_represented_clauses(raw_clauses):
        parsed = _PASSIVE_BY_PATTERN.match(clause) or _SIMPLE_SVO_PATTERN.match(clause)
        if not parsed:
            continue
        subject = _label(parsed.group('subject'))
        predicate = _predicate_from_phrase(parsed.group('verb'))
        obj = _label(_strip_reported_object_tail(parsed.group('object')))
        if subject and predicate and obj:
            _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)
            emitted = True
    return emitted


def _extract_represented_svo_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract represented SVO claims."""
    match = _REPRESENT_THAT_PATTERN.search(text)
    if not match:
        return False
    return _append_svo_clause_claims(claims, source_text_id, sentence, paragraph_id, match.group('clauses'))


def _extract_reporting_that_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract reporting that claims."""
    match = _REPORTING_THAT_PATTERN.match(text)
    if not match:
        return False
    subject = _label(match.group('subject'))
    predicate = _verb(match.group('verb'))
    recipient = _label(match.group('recipient') or '')
    if subject and predicate and recipient:
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, recipient)
    _append_svo_clause_claims(claims, source_text_id, sentence, paragraph_id, match.group('clauses'))
    return True


def _extract_simple_svo_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract simple SVO claims."""
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
    """Extract subclasses of claims."""
    match = re.match(r'^(?P<subjects>.+?)\s+are\s+subclasses\s+of\s+(?P<parent>.+?)\.?$', text, flags=re.IGNORECASE)
    if not match:
        return False
    parent = _label(match.group('parent'))
    if not parent:
        return False
    emitted = False
    for subject in _split_list(match.group('subjects')):
        if subject:
            # BR-INFOSEC-PAIR-SMOKE-003: taxonomy lists project each member as direct type_of, not as a literal `subclasses` predicate.
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} is a type of {parent}', 'type_of', subject=subject, predicate='type_of', object=parent)
            emitted = True
    return emitted


def _normalized_words(value: str | None) -> str:
    """Return normalized words."""
    return ' '.join(word.casefold() for word in _words(value or ''))


def _strip_contextual_object_tail(value: str) -> str:
    """Remove contextual object tail."""
    match = _CONTEXTUAL_OBJECT_PATTERN.match(f'X does {value}')
    return match.group('object').strip() if match else value.strip()


def _is_lexicalized_context_object(value: str) -> bool:
    """Return whether a prepositional phrase is a configured lexicalized domain term."""
    return _normalized_words(value) in _LEXICALIZED_CONTEXT_OBJECTS


def _append_contextual_tail_relations(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, subject: str, tail: str) -> None:
    """Append supported route-tail relations while excluding their contextual suffixes."""
    for match in _ROUTE_TAIL_PATTERN.finditer(tail):
        raw_object = _strip_contextual_object_tail(match.group('object'))
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(match.group('verb')), _label(raw_object))


def _extract_route_preposition_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract route preposition claims."""
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
    """Extract contextual object claims."""
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
    _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, match.group('object'))
    return True


def _passive_base_verb(value: str) -> str:
    """Recover a deterministic base verb from a supported passive participle."""
    token = (_words(value)[0].casefold() if _words(value) else '')
    if token.endswith('ied'):
        return token[:-3] + 'y'
    if token.endswith('ed'):
        base = token[:-2]
        if len(base) > 2 and base[-1] == base[-2]:
            base = base[:-1]
        return base
    return token


def _condition_metadata(raw_condition: str) -> dict[str, str]:
    """Parse a supported condition into explicit modality, polarity, and voice metadata."""
    condition = _clean(raw_condition).strip().rstrip('.')
    cannot = re.match(r'^(?P<subject>.+?)\s+cannot\s+be\s+(?P<predicate>[A-Za-z-]+)$', condition, flags=re.IGNORECASE)
    if cannot:
        subject = _label(cannot.group('subject'))
        return {
            'condition': f'{subject} cannot be {cannot.group("predicate").casefold()}',
            'condition_subject': subject,
            'condition_predicate': _passive_base_verb(cannot.group('predicate')),
            'condition_modality': 'cannot',
            'condition_polarity': 'negative',
            'condition_voice': 'passive',
        }
    unavailable = re.match(r'^(?P<subject>.+?)\s+is\s+not\s+(?P<predicate>[A-Za-z-]+)$', condition, flags=re.IGNORECASE)
    if unavailable:
        subject = _label(unavailable.group('subject'))
        return {
            'condition': f'{subject} is not {unavailable.group("predicate").casefold()}',
            'condition_subject': subject,
            'condition_predicate': unavailable.group('predicate').casefold(),
            'condition_polarity': 'negative',
        }
    active = re.match(r'^(?P<subject>.+?)\s+(?P<predicate>[A-Za-z]+(?:s|es|ies))$', condition, flags=re.IGNORECASE)
    if active:
        subject = _label(active.group('subject'))
        return {
            'condition': f'{subject} {_verb(active.group("predicate"))}',
            'condition_subject': subject,
            'condition_predicate': _verb(active.group('predicate')),
            'condition_polarity': 'positive',
        }
    return {'condition': condition}


def _extract_compliance_privacy_claims(
    claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str,
) -> bool:
    """Extract compliance privacy claims."""
    lower = text.casefold().rstrip('.')
    if lower == 'compliance ensures that the organization meets legal, regulatory, contractual, and internal requirements':
        group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), text)
        for requirement in ('LegalRequirement', 'RegulatoryRequirement', 'ContractualRequirement', 'InternalRequirement'):
            _append_relation(claims, source_text_id, sentence, paragraph_id, 'Organization', 'meets', requirement, context='Compliance', proposition_group=group, relation_role='ensured_content')
        return True
    if lower == 'a compliance requirement is an obligation that must be satisfied':
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'ComplianceRequirement', 'is_a', 'Obligation')
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'ComplianceRequirement', 'requires', 'Satisfaction', modality='must', voice='passive')
        return True
    requirement = re.match(r'^(?:a|an) (?P<kind>legal|regulatory|contractual|internal) requirement is a type of compliance requirement (?P<qualifier>.+)$', lower)
    if requirement:
        subject = _label(requirement.group('kind') + ' requirement')
        _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', 'ComplianceRequirement')
        qualifier = requirement.group('qualifier')
        patterns = (
            ('derived from ', 'derived_from'), ('imposed by ', 'imposed_by'),
            ('defined in ', 'defined_in'), ('defined by ', 'defined_by'),
        )
        for prefix, predicate in patterns:
            if qualifier.startswith(prefix):
                _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, _label(qualifier[len(prefix):]), voice='passive')
                break
        return True
    if lower == 'an audit evaluates whether controls satisfy requirements':
        group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), text)
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'Audit', 'evaluates', 'RequirementSatisfaction', proposition_group=group)
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'Control', 'satisfies', 'Requirement', modality='whether', context='Audit', proposition_group=group, relation_role='evaluated_content', preserve_lexical_object='true')
        return True
    if lower == 'a nonconformity is a failure to meet a requirement':
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'Nonconformity', 'is_a', 'Failure')
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'Nonconformity', 'fails_to_meet', 'Requirement', preserve_lexical_object='true')
        return True
    if lower == 'privacy protects personal data and the rights of individuals':
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'Privacy', 'protects', 'PersonalData')
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'Privacy', 'protects', 'IndividualRight')
        return True
    if lower == 'a data subject is a person whose personal data is processed':
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'DataSubject', 'is_a', 'Person')
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'DataSubject', 'has_personal_data', 'PersonalData',
            processing_state='processed', voice='passive', relation_role='relative_clause_content',
        )
        return True
    if lower == 'a data controller determines the purposes and means of processing personal data':
        for obj in ('Purpose', 'Means'):
            _append_relation(claims, source_text_id, sentence, paragraph_id, 'DataController', 'determines', obj, context='PersonalDataProcessing')
        return True
    if lower == 'a data processor processes personal data on behalf of a controller':
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'DataProcessor', 'processes', 'PersonalData', on_behalf_of='Controller')
        return True
    if lower == 'a privacy notice informs data subjects about processing activities':
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'PrivacyNotice', 'informs', 'DataSubject', topics='ProcessingActivity')
        return True
    if lower == 'consent is a lawful basis for processing in some contexts':
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'Consent', 'is_a', 'LawfulBasis', condition='in some contexts')
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'Consent', 'applies_to', 'Processing', condition='in some contexts')
        return True
    operational = (
        ('data minimization limits personal data to what is necessary', 'DataMinimization', 'limits', 'PersonalData', {'constraint': 'necessary'}),
        ('purpose limitation restricts processing to defined purposes', 'PurposeLimitation', 'restricts', 'Processing', {'target': 'DefinedPurpose'}),
        ('retention limitation restricts how long personal data is stored', 'RetentionLimitation', 'restricts', 'StorageDuration', {'patient': 'PersonalData'}),
        ('data deletion removes personal data when it is no longer needed', 'DataDeletion', 'removes', 'PersonalData', {'condition': 'PersonalData is no longer needed', 'condition_subject': 'PersonalData', 'condition_predicate': 'needed', 'condition_polarity': 'negative'}),
    )
    for source, subject, predicate, obj, qualifiers in operational:
        if lower == source:
            _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj, **qualifiers)
            return True
    return False


def _extract_information_and_access_claims(
    claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str,
) -> bool:
    """Extract information and access claims."""
    helps = re.match(
        r'^Information classification helps organizations apply appropriate protection levels to different kinds of information\.?$',
        text, flags=re.IGNORECASE,
    )
    if helps:
        group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), text)
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'InformationClassification', 'helps', 'Organization', content_group=group)
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'Organization', 'applies', 'AppropriateProtectionLevel',
            target='InformationKind', context='InformationClassification', content_group=group, relation_role='enabled_action',
        )
        return True

    public = re.match(r'^Public information is a type of information that can be disclosed without causing harm\.?$', text, flags=re.IGNORECASE)
    if public:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'PublicInformation', 'is_a', 'Information')
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'PublicInformation', 'disclosure_causes', 'Harm',
            modality='can', polarity='negative', condition='when disclosed', proposition_role='defining_property',
        )
        return True

    internal = re.match(r'^Internal information is a type of information intended for use inside the organization\.?$', text, flags=re.IGNORECASE)
    if internal:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'InternalInformation', 'is_a', 'Information')
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'InternalInformation', 'intended_for', 'Use',
            location='Organization', location_relation='inside', modality='purpose',
        )
        return True

    confidential = re.match(
        r'^Confidential information is a type of information whose unauthorized disclosure may harm (?P<objects>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if confidential:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'ConfidentialInformation', 'is_a', 'Information')
        group = _alternative_group_id(source_text_id, sentence, confidential.group('objects'))
        for obj in _objects(confidential.group('objects')):
            _append_relation(
                claims, source_text_id, sentence, paragraph_id, 'UnauthorizedDisclosure', 'harms', obj,
                modality='may', coordination='or', alternative_group=group,
                context='ConfidentialInformation', proposition_role='defining_property',
            )
        return True

    restricted = re.match(
        r'^Restricted information is a type of highly sensitive information that requires strict access, storage, and transmission controls\.?$',
        text, flags=re.IGNORECASE,
    )
    if restricted:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'RestrictedInformation', 'is_a', 'HighlySensitiveInformation')
        for obj in ('AccessControl', 'StorageControl', 'TransmissionControl'):
            _append_relation(claims, source_text_id, sentence, paragraph_id, 'RestrictedInformation', 'requires', obj, strictness='strict')
        return True

    personal = re.match(r'^Personal data is a type of sensitive information that identifies or can identify a natural person\.?$', text, flags=re.IGNORECASE)
    if personal:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'PersonalData', 'is_a', 'SensitiveInformation')
        group = _alternative_group_id(source_text_id, sentence, text)
        for modality in ('explicit', 'can'):
            _append(
                claims, source_text_id, sentence, paragraph_id,
                f'PersonalData {"can " if modality == "can" else ""}identifies NaturalPerson', 'relation',
                subject='PersonalData', predicate='identifies', object='NaturalPerson',
                modality=modality, coordination='or', alternative_group=group,
            )
        return True

    financial = re.match(
        r'^Financial data is a type of sensitive information related to (?P<objects>.+?)\.?$', text, flags=re.IGNORECASE,
    )
    if financial:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'FinancialData', 'is_a', 'SensitiveInformation')
        objects = _objects(financial.group('objects'))
        group = _alternative_group_id(source_text_id, sentence, financial.group('objects'))
        for obj in objects:
            scoped_obj = 'FinancialAccount' if obj == 'Account' else obj
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                'FinancialData', 'related_to', scoped_obj,
                modality='disjunctive_alternative', coordination='or', alternative_group=group,
                source_term=obj, semantic_scope='financial_data_topic', preserve_lexical_object='true',
            )
        return True

    auth_data = re.match(r'^Authentication data is a type of restricted information because it can grant access to systems\.?$', text, flags=re.IGNORECASE)
    if auth_data:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'AuthenticationData', 'is_a', 'RestrictedInformation')
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'AuthenticationData', 'grants_access_to', 'System',
            modality='can', condition='because authentication data can grant access', proposition_role='defining_property',
        )
        return True

    access = re.match(r'^Access control regulates who can access which resource and under which conditions\.?$', text, flags=re.IGNORECASE)
    if access:
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'AccessControl', 'regulates', 'Access',
            actor_variable='who', resource_variable='which resource', condition_variable='which conditions', modality='can',
        )
        return True

    process = re.match(r'^(?P<subject>Identification|Authentication) is the process of (?P<verb>claiming|verifying) an identity\.?$', text, flags=re.IGNORECASE)
    if process:
        subject = _label(process.group('subject'))
        _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', 'Process')
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(process.group('verb')), 'Identity', relation_role='process_content')
        return True

    authorization = re.match(r'^Authorization is the process of determining what actions an authenticated identity may perform\.?$', text, flags=re.IGNORECASE)
    if authorization:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'Authorization', 'is_a', 'Process')
        group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), text)
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'Authorization', 'determines', 'Action',
            proposition_group=group, relation_role='process_content',
        )
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'AuthenticatedIdentity', 'performs', 'Action',
            modality='may', context='Authorization', proposition_group=group,
            relation_role='determined_action',
        )
        return True

    accountability = re.match(r'^Accountability is the ability to trace actions to a specific identity\.?$', text, flags=re.IGNORECASE)
    if accountability:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'Accountability', 'is_a', 'Ability')
        _append_relation(
            claims, source_text_id, sentence, paragraph_id, 'Accountability', 'traces_action_to', 'Identity',
            patient='Action', modality='capability', relation_role='ability_content', qualifier='specific',
            preserve_lexical_object='true',
        )
        return True

    service = re.match(r'^A service account is a type of non-human account used by (?P<objects>.+?)\.?$', text, flags=re.IGNORECASE)
    if service:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'ServiceAccount', 'is_a', 'NonHumanAccount')
        _append_alternative_objects(claims, source_text_id, sentence, paragraph_id, 'ServiceAccount', 'used_by', service.group('objects'), voice='passive')
        return True

    privileged = re.match(r'^A privileged account is a type of account with elevated permissions\.?$', text, flags=re.IGNORECASE)
    if privileged:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'PrivilegedAccount', 'is_a', 'Account')
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'PrivilegedAccount', 'has', 'Permission', qualifier='elevated')
        return True

    shared = re.match(r'^A shared account is a type of account used by multiple individuals and creates accountability risk\.?$', text, flags=re.IGNORECASE)
    if shared:
        _append_definition(claims, source_text_id, sentence, paragraph_id, 'SharedAccount', 'is_a', 'Account')
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'SharedAccount', 'used_by', 'Individual', quantifier='multiple', voice='passive')
        _append_relation(claims, source_text_id, sentence, paragraph_id, 'SharedAccount', 'creates', 'AccountabilityRisk')
        return True
    return False


_INSTRUCTION_ACTION_VERBS = {
    'classify', 'create', 'dispose', 'identify', 'protect', 'recognize', 'store', 'transmit',
}


def _extract_instructional_and_contextual_claims(
    claims: list[dict[str, Any]],
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    text: str,
) -> bool:
    """Extract instructional and contextual claims."""
    instructional = re.match(
        r'^(?P<subject>.+?)\s+(?P<verb>educates|teaches)\s+(?P<recipient>.+?)\s+'
        r'(?P<connector>about|to)\s+(?P<content>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if instructional:
        subject = _label(instructional.group('subject'))
        recipient = _label(instructional.group('recipient'))
        predicate = _verb(instructional.group('verb'))
        content = instructional.group('content').strip().rstrip('.')
        content_group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), content)
        if instructional.group('connector').casefold() == 'about':
            topics = _objects(content)
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                subject, predicate, recipient,
                topics=','.join(topics), content_group=content_group,
            )
            return True

        words = _words(content)
        actions: list[str] = []
        cursor = 0
        while cursor < len(words):
            word = words[cursor].casefold()
            if word in {'and', 'or'}:
                cursor += 1
                continue
            if word in _INSTRUCTION_ACTION_VERBS:
                actions.append(word)
                cursor += 1
                if word == 'dispose' and cursor < len(words) and words[cursor].casefold() == 'of':
                    cursor += 1
                continue
            break
        raw_target = ' '.join(words[cursor:]).strip()
        manner = ''
        location = ''
        location_match = re.search(r'\s+outside\s+(?P<location>.+)$', raw_target, flags=re.IGNORECASE)
        if location_match:
            location = _label(location_match.group('location'))
            raw_target = raw_target[:location_match.start()].strip()
        if raw_target.casefold().endswith(' safely'):
            manner = 'safely'
            raw_target = raw_target[:-len(' safely')].strip()
        targets = _objects(raw_target)
        _append_relation(
            claims, source_text_id, sentence, paragraph_id,
            subject, predicate, recipient,
            content_group=content_group, relation_role='introduces_instructional_content',
        )
        for action in actions:
            action_predicate = 'disposes_of' if action == 'dispose' else _verb(action)
            for target in targets:
                _append_relation(
                    claims, source_text_id, sentence, paragraph_id,
                    recipient, action_predicate, target,
                    modality='taught_action', context=subject, content_group=content_group,
                    relation_role='instructional_content', manner=manner, location=location,
                    location_relation='outside' if location else '',
                )
        return True

    contextual_patterns = (
        (
            r'^(?P<subject>.+?)\s+defines\s+(?P<object>.+?)\s+related\s+to\s+(?P<context>.+?)\.?$',
            'defines', 'related_to', 'context',
        ),
        (
            r'^(?P<subject>.+?)\s+(?P<verb>provides|defines|measure|measures)\s+(?P<object>.+?)\s+for\s+(?P<context>.+?)\.?$',
            '', 'related_to', 'context',
        ),
        (
            r'^(?P<subject>.+?)\s+(?:measure|measures)\s+(?P<object>.+?)\s+to\s+(?P<context>.+?)\.?$',
            'measures', 'in_context_of', 'context',
        ),
    )
    for pattern, fixed_predicate, context_predicate, _ in contextual_patterns:
        match = re.match(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        raw_subject = match.group('subject')
        raw_object = match.group('object')
        if re.search(r'\b(?:is|are|was|were)\b', raw_subject, flags=re.IGNORECASE) or raw_object.casefold().strip().endswith('oversight'):
            continue
        subject = _label(raw_subject)
        obj = _label(raw_object)
        predicate = fixed_predicate or _verb(match.groupdict().get('verb', ''))
        context = _label(match.group('context'))
        _append_relation(claims, source_text_id, sentence, paragraph_id, subject, predicate, obj)
        _append_relation(
            claims, source_text_id, sentence, paragraph_id,
            obj, context_predicate, context, context_of=f'{subject} {predicate} {obj}',
        )
        return True

    conditional = re.match(
        r'^(?P<subject>.+?)\s+(?P<verb>removes|revokes|disables)\s+(?P<object>.+?)\s+when\s+(?P<condition>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if conditional:
        _append_relation(
            claims, source_text_id, sentence, paragraph_id,
            _label(conditional.group('subject')), _verb(conditional.group('verb')), _label(conditional.group('object')),
            **_condition_metadata(conditional.group('condition')),
        )
        return True

    simple = re.match(
        r'^(?P<subject>.+?)\s+(?P<verb>reduce|reduces|reinforce|reinforces|measure|measures)\s+(?P<object>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if (
        simple
        and not re.search(r'\b(?:is|are|was|were|may|must|can|could|should|would|might)\b', simple.group('subject'), flags=re.IGNORECASE)
        and not re.search(r'\bby\b', simple.group('object'), flags=re.IGNORECASE)
    ):
        _append_relation(
            claims, source_text_id, sentence, paragraph_id,
            _label(simple.group('subject')), _verb(simple.group('verb')), _label(simple.group('object')),
        )
        return True
    return False


def _extract_scoped_semantic_claims(
    claims: list[dict[str, Any]],
    source_text_id: str,
    sentence: dict[str, Any],
    paragraph_id: str,
    text: str,
) -> bool:
    """Extract scoped semantic claims."""
    scoped_definition = re.match(
        r'^(?P<subject>.+?)\s+is\s+a\s+(?P<object>core\s+process)\s+in\s+(?P<scope>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if scoped_definition:
        _append_definition(
            claims, source_text_id, sentence, paragraph_id,
            _label(scoped_definition.group('subject')), 'is_a', _label(scoped_definition.group('object')),
            scope=_label(scoped_definition.group('scope')),
        )
        return True

    possibility = re.match(
        r'^(?P<subject>.+?)\s+is\s+the\s+possibility\s+that\s+(?P<agent>.+?)\s+'
        r'(?P<verb1>\w+s)\s+(?P<object1>.+?)\s+and\s+(?P<verb2>\w+s)\s+'
        r'(?P<object2>.+?)\s+to\s+(?P<target>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if possibility:
        subject = _label(possibility.group('subject'))
        agent = _label(possibility.group('agent'))
        group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), possibility.group(0))
        _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', 'Possibility')
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{agent} {possibility.group("verb1").casefold()} {_label(possibility.group("object1"))} under possibility defining {subject}',
            'relation', subject=agent, predicate=_verb(possibility.group('verb1')),
            object=_label(possibility.group('object1')), modality='possibility', context=subject,
            proposition_group=group, coordination='and', proposition_role='defining_content',
        )
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{agent} {possibility.group("verb2").casefold()} {_label(possibility.group("object2"))} to {_label(possibility.group("target"))} under possibility defining {subject}',
            'relation', subject=agent, predicate=_verb(possibility.group('verb2')),
            object=_label(possibility.group('object2')), target=_label(possibility.group('target')),
            modality='possibility', context=subject, proposition_group=group,
            coordination='and', proposition_role='defining_content',
        )
        return True

    passive_capability = re.match(
        r'^(?P<subject>.+?)\s+is\s+a\s+(?P<object>.+?)\s+that\s+can\s+be\s+'
        r'(?P<verb>[A-Za-z-]+)\s+by\s+(?P<agent>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if passive_capability:
        subject = _label(passive_capability.group('subject'))
        agent = _label(passive_capability.group('agent'))
        _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', _label(passive_capability.group('object')))
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{agent} can {_passive_base_verb(passive_capability.group("verb"))} {subject}', 'relation',
            subject=agent, predicate=_verb(_passive_base_verb(passive_capability.group('verb'))), object=subject,
            modality='can', voice='passive', patient=subject,
        )
        return True

    produced_definition = re.match(
        r'^(?P<subject>.+?)\s+is\s+the\s+(?P<object>.+?)\s+produced\s+by\s+(?P<sources>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if produced_definition:
        subject = _label(produced_definition.group('subject'))
        _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', _label(produced_definition.group('object')))
        _append_alternative_objects(
            claims, source_text_id, sentence, paragraph_id,
            subject, 'produced_by', produced_definition.group('sources'), voice='passive',
        )
        return True

    probability = re.match(
        r'^(?P<subject>.+?)\s+is\s+the\s+probability\s+that\s+(?P<event>.+?)\s+(?P<verb>occurs?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if probability:
        subject = _label(probability.group('subject'))
        _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', 'Probability')
        event = _label(probability.group('event'))
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{subject} has probability of {event} occurring',
            'relation', subject=subject, predicate='has_probability_of', object=event,
            modality='probability', event_predicate=_verb(probability.group('verb')),
            proposition_role='measured_event',
        )
        return True

    described_modal = re.match(
        r'^(?P<context>.+?)\s+describes\s+how\s+(?P<agent>.+?)\s+may\s+'
        r'(?P<verb1>\w+)\s+(?P<object1>.+?)\s+and\s+(?P<verb2>\w+)\s+(?P<object2>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if described_modal:
        context = _label(described_modal.group('context'))
        agent = _label(described_modal.group('agent'))
        group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), described_modal.group(0))
        for verb_key, object_key in (('verb1', 'object1'), ('verb2', 'object2')):
            raw_verb = described_modal.group(verb_key)
            obj = _label(described_modal.group(object_key))
            _append(
                claims, source_text_id, sentence, paragraph_id,
                f'{context} describes that {agent} may {raw_verb.casefold()} {obj}', 'relation',
                subject=agent, predicate=_verb(raw_verb), object=obj,
                modality='may', context=context, proposition_group=group,
                coordination='and', proposition_role='described_event',
            )
        return True

    reduction_means = re.match(
        r'^(?P<subject>.+?)\s+(?P<verb>reduces?)\s+(?P<object>.+?)\s+by\s+'
        r'(?P<actions>.+?)\s+for\s+(?P<target>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if reduction_means and re.search(r'\bor\b', reduction_means.group('actions'), flags=re.IGNORECASE):
        subject = _label(reduction_means.group('subject'))
        obj = _label(reduction_means.group('object'))
        target = _label(reduction_means.group('target'))
        group = _alternative_group_id(source_text_id, sentence, reduction_means.group('actions'))
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{subject} {_verb(reduction_means.group("verb"))} {obj}', 'relation',
            subject=subject, predicate=_verb(reduction_means.group('verb')), object=obj,
            means_group=group,
        )
        actions = [word for word in _words(reduction_means.group('actions')) if word.casefold() not in {'and', 'or'}]
        for action in actions:
            predicate = _verb(action)
            if action.casefold().startswith('compensat'):
                predicate = 'compensates_for'
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                subject, predicate, target,
                modality='disjunctive_alternative', coordination='or', alternative_group=group,
                relation_role='means_for', goal=f'{_verb(reduction_means.group("verb"))} {obj}',
                means_group=group,
            )
        return True

    typed_relative = re.match(
        r'^(?P<subject>.+?)\s+is\s+a\s+type\s+of\s+(?P<parent>.+?)\s+that\s+'
        r'(?P<verb>\w+s)\s+(?P<object>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if typed_relative:
        subject = _label(typed_relative.group('subject'))
        _append_definition(claims, source_text_id, sentence, paragraph_id, subject, 'is_a', _label(typed_relative.group('parent')))
        raw_object = typed_relative.group('object').strip().rstrip('.')
        condition_match = re.match(r'(?P<object>.+?)\s+when\s+(?P<condition>.+)$', raw_object, flags=re.IGNORECASE)
        temporal_match = re.match(r'(?P<object>.+?)\s+after\s+(?P<temporal>.+)$', raw_object, flags=re.IGNORECASE)
        alternative = re.search(r'\bor\b', raw_object, flags=re.IGNORECASE)
        if condition_match:
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                subject, _verb(typed_relative.group('verb')), _label(condition_match.group('object')),
                **_condition_metadata(condition_match.group('condition')),
            )
        elif temporal_match:
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                subject, _verb(typed_relative.group('verb')), _label(temporal_match.group('object')),
                temporal_relation='after', temporal_object=_label(temporal_match.group('temporal')),
            )
        elif alternative:
            _append_alternative_objects(
                claims, source_text_id, sentence, paragraph_id,
                subject, _verb(typed_relative.group('verb')), raw_object,
            )
        else:
            _append_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(typed_relative.group('verb')), _label(raw_object))
        return True

    potential_cause = re.match(
        r'^(?P<subject>.+?)\s+is\s+a\s+potential\s+cause\s+of\s+(?P<object>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if potential_cause:
        subject = _label(potential_cause.group('subject'))
        _append_definition(
            claims, source_text_id, sentence, paragraph_id,
            subject, 'is_a', 'PotentialCause', target=_label(potential_cause.group('object')), modality='potential',
        )
        return True

    conditional_definition = re.match(
        r'^(?P<subject>.+?)\s+is\s+a\s+(?P<object>.+?)\s+when\s+(?P<condition>.+?)\.?$',
        text, flags=re.IGNORECASE,
    )
    if conditional_definition:
        subject = _label(conditional_definition.group('subject'))
        obj = _label(conditional_definition.group('object'))
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{subject} is a {obj} when {_clean(conditional_definition.group("condition")).rstrip(".")}',
            'definition', subject=subject, predicate='is_a', object=obj,
            **_condition_metadata(conditional_definition.group('condition')),
        )
        return True
    return False


def _extract_sentence_claims(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str) -> None:
    """Extract sentence claims."""
    text = _clean(str(sentence.get('text', '')))
    if not text:
        return
    remediation_a2_specs = extract_remediation_a2_claim_specs(text)
    if remediation_a2_specs is not None:
        for spec in remediation_a2_specs:
            parts = dict(spec)
            kind = str(parts.pop('kind', 'relation'))
            parts.setdefault('remediation_rule', 'A2')
            statement = f"{parts.get('subject', '')} {parts.get('predicate', '')} {parts.get('object', '')}"
            _append(claims, source_text_id, sentence, paragraph_id, statement, kind, **parts)
        return
    remediation_b2_specs = extract_remediation_b2_claim_specs(text)
    remediation_b_specs = remediation_b2_specs if remediation_b2_specs is not None else extract_remediation_b_claim_specs(text)
    if remediation_b_specs is not None:
        for spec in remediation_b_specs:
            if str(spec.get('modality', '')).casefold() in {'must', 'should', 'purpose'}:
                spec.setdefault('projection_scope', 'scoped')
            subject = str(spec.get('subject', ''))
            predicate = str(spec.get('predicate', ''))
            obj = str(spec.get('object', ''))
            kind = str(spec.get('kind', 'relation'))
            statement = f'{subject} is a {obj}' if kind == 'definition' else f'{subject} {predicate} {obj}'
            _append(
                claims, source_text_id, sentence, paragraph_id, statement, kind,
                **{key: value for key, value in spec.items() if key != 'kind'},
            )
        return
    remediation_c3_specs = extract_remediation_c3_claims(text)
    if remediation_c3_specs is not None:
        for spec in remediation_c3_specs:
            parts = {
                key: value for key, value in spec.items()
                if key not in {'kind', 'subject', 'predicate', 'object'}
            }
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                str(spec['subject']), str(spec['predicate']), str(spec['object']), **parts,
            )
        return
    remediation_c2_specs = extract_remediation_c2_claims(text, sentence_id=str(sentence.get('sentence_id', '')))
    if remediation_c2_specs:
        for spec in remediation_c2_specs:
            parts = {
                key: value for key, value in spec.items()
                if key not in {'kind', 'subject', 'predicate', 'object'}
            }
            if spec.get('kind') == 'definition':
                _append_definition(
                    claims, source_text_id, sentence, paragraph_id,
                    str(spec['subject']), str(spec['predicate']), str(spec['object']), **parts,
                )
            else:
                _append_relation(
                    claims, source_text_id, sentence, paragraph_id,
                    str(spec['subject']), str(spec['predicate']), str(spec['object']), **parts,
                )
        return
    remediation_c_specs = extract_remediation_c_claims(text, label=_label, verb=_verb)
    if remediation_c_specs:
        for spec in remediation_c_specs:
            parts = {
                key: value for key, value in spec.items()
                if key not in {'kind', 'subject', 'predicate', 'object'}
            }
            if spec.get('kind') == 'definition':
                _append_definition(
                    claims, source_text_id, sentence, paragraph_id,
                    str(spec['subject']), str(spec['predicate']), str(spec['object']), **parts,
                )
            else:
                _append_relation(
                    claims, source_text_id, sentence, paragraph_id,
                    str(spec['subject']), str(spec['predicate']), str(spec['object']), **parts,
                )
        return
    remediation_specs = extract_remediation_a_claim_specs(text)
    if remediation_specs is not None:
        for spec in remediation_specs:
            parts = dict(spec)
            kind = str(parts.pop('kind', 'relation'))
            parts.setdefault('remediation_rule', 'A')
            statement = f"{parts.get('subject', '')} {parts.get('predicate', '')} {parts.get('object', '')}"
            _append(claims, source_text_id, sentence, paragraph_id, statement, kind, **parts)
        return
    if _is_meta_instruction_text(text):
        return
    purpose = re.match(r'^the\s+purpose\s+of\s+(?P<subject>.+?)\s+is\s+to\s+(?P<verb>\w+)\s+(?P<objects>.+?)\.?$', text, flags=re.IGNORECASE)
    if purpose:
        subject = _label(purpose.group('subject'))
        predicate = f"has_purpose_to_{purpose.group('verb').casefold()}"
        for obj in _objects(purpose.group('objects')):
            _append(
                claims, source_text_id, sentence, paragraph_id,
                f'{subject} has purpose to {purpose.group("verb").casefold()} {obj}',
                'relation', subject=subject, predicate=predicate, object=obj, modality='purpose',
            )
        return
    if _extract_subclasses_of_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_compliance_privacy_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_information_and_access_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_instructional_and_contextual_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_scoped_semantic_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_definition_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_represented_svo_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    if _extract_reporting_that_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    by_action = re.match(r'^(?P<subject>.+)\s+(?P<verb>\w+(?:s|ing))\s+(?P<object>.+?)\s+by\s+(?P<gerund>\w+ing)\s+(?P<items>.+?)\.?$', text, flags=re.IGNORECASE)
    if by_action:
        subject = _label(by_action.group('subject'))
        protected_object = _label(by_action.group('object'))
        primary_predicate = _verb(by_action.group('verb'))
        means_predicate = _verb(by_action.group('gerund'))
        instrument_group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), by_action.group('items'))
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{subject} {primary_predicate} {protected_object}', 'relation',
            subject=subject, predicate=primary_predicate, object=protected_object,
            means=by_action.group('gerund').casefold(), instrument_group=instrument_group,
        )
        for obj in _objects(by_action.group('items')):
            _append_relation(
                claims, source_text_id, sentence, paragraph_id,
                subject, means_predicate, obj,
                relation_role='means_for', goal=f'{primary_predicate} {protected_object}',
                instrument_group=instrument_group, preserve_lexical_object='true',
            )
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
        subject = _label(oversight.group('subject'))
        obj = _label(oversight.group('object'))
        qualifier = _label(oversight.group('qualifier'))
        predicate = f'provides_{oversight.group("qualifier").casefold()}_oversight_for'
        _append(
            claims, source_text_id, sentence, paragraph_id,
            f'{subject} provides {oversight.group("qualifier").casefold()} oversight for {obj}', 'relation',
            subject=subject, predicate=predicate, object=obj, qualifier=qualifier,
        )
        return
    two_actions = re.match(r'^(?P<subject>.+?)\s+(?P<verb1>\w+s)\s+(?P<object1>.+?)\s+and\s+(?P<verb2>\w+s|must)\s+(?P<object2>.+?)\.?$', text, flags=re.IGNORECASE)
    if two_actions:
        subject = _label(two_actions.group('subject'))
        _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(two_actions.group('verb1')), two_actions.group('object1'))
        object2 = two_actions.group('object2')
        if two_actions.group('verb2').casefold() == 'must':
            parts = object2.split(' ', 1)
            if len(parts) == 2:
                base_verb, raw_objects = parts
                predicate = _modal_predicate('must', base_verb)
                for obj in _objects(raw_objects):
                    _append(
                        claims, source_text_id, sentence, paragraph_id,
                        f'{subject} must {base_verb.casefold()} {obj}', 'relation',
                        subject=subject, predicate=predicate, object=obj, modality='must',
                    )
            return
        support = re.match(r'(?P<resource>.+?)\s+for\s+(?P<target>.+)$', object2, flags=re.IGNORECASE)
        if support:
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(two_actions.group('verb2')), support.group('resource'))
            for resource in _objects(support.group('resource')):
                for target in _objects(support.group('target')):
                    _append(
                        claims, source_text_id, sentence, paragraph_id,
                        f'{resource} is allocated for {target}', 'relation',
                        subject=resource, predicate='allocated_for', object=target, voice='passive',
                    )
        else:
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(two_actions.group('verb2')), _strip_contextual_object_tail(object2))
        return
    if _extract_contextual_object_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    form = re.match(r'^(?P<subjects>.+?)\s+form\s+(?P<object>.+?)\.?$', text, flags=re.IGNORECASE)
    if form:
        target = _label(form.group('object'))
        members = _split_list(form.group('subjects'))
        for member in members:
            _append(
                claims, source_text_id, sentence, paragraph_id,
                f'{target} has member {member}', 'relation',
                subject=target, predicate='has_member', object=member,
                members=','.join(members), modality='collective_composition',
            )
        return
    if _extract_definition_claims(claims, source_text_id, sentence, paragraph_id, text):
        return
    shared_object = re.match(r'^(?P<subject>.+?)\s+(?P<verbs>\w+s(?:\s+and\s+\w+s)*)\s+(?P<object>.+?)(?:\s+that\s+(?P<tail>.+))?\.?$', text, flags=re.IGNORECASE)
    if shared_object:
        subject = _label(shared_object.group('subject'))
        raw_object = shared_object.group('object')
        with_match = re.match(r'(?P<object>.+?)\s+with\s+(?P<target>.+)$', raw_object, flags=re.IGNORECASE)
        object_text = raw_object
        object_label = _label(object_text)
        for verb_word in re.split(r'\s+and\s+', shared_object.group('verbs'), flags=re.IGNORECASE):
            _append_list_relation(claims, source_text_id, sentence, paragraph_id, subject, _verb(verb_word), object_text)
        tail = shared_object.group('tail') or ''
        if tail:
            tail_match = re.match(r'(?P<verbs>\w+(?:\s+or\s+\w+)*)\s+(?P<object>.+)$', tail.rstrip('.'), flags=re.IGNORECASE)
            if tail_match:
                raw_verbs = re.split(r'\s+or\s+', tail_match.group('verbs'), flags=re.IGNORECASE)
                if len(raw_verbs) > 1:
                    obj = _label(tail_match.group('object'))
                    group = _alternative_group_id(source_text_id, sentence, f'{object_label}|{tail}')
                    for verb_word in raw_verbs:
                        _append_relation(
                            claims, source_text_id, sentence, paragraph_id,
                            object_label, _verb(verb_word), obj,
                            modality='disjunctive_alternative', coordination='or', alternative_group=group,
                        )
                else:
                    _append_list_relation(claims, source_text_id, sentence, paragraph_id, object_label, _verb(raw_verbs[0]), tail_match.group('object'))
        return



def _extract_definition_claims_compat(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str, text: str) -> bool:
    """Extract definition claims compat."""
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
        if against and protected:
            patient = _label(protected.group('object'))
            for item in _split_list(against.group('objects')):
                obj = item if item.endswith('Threat') else f'{item}Threat'
                _append(
                    claims, source_text_id, sentence, paragraph_id,
                    f'{subject} is focused on protecting {patient} against {obj}',
                    'relation', subject=subject, predicate='focused_on_protecting_against', object=obj,
                    patient=patient, modality='focus',
                )
    if re.search(r'\bmodel\s+for\b', raw_object, flags=re.IGNORECASE):
        model_target = _label(re.split(r'\bfor\b', raw_object, maxsplit=1, flags=re.IGNORECASE)[1])
        if model_target:
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} is a model for {model_target}', 'relation', subject=subject, predicate='models', object=model_target)
    value_for = re.search(r'\bhas\s+value\s+for\s+(?P<object>.+?)(?:\s+and\s+that\s+|$)', raw_object, flags=re.IGNORECASE)
    if value_for:
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} has value for {_label(value_for.group("object"))}', 'relation', subject=subject, predicate='has_value_for', object=_label(value_for.group('object')))
    action_tail = re.search(r'\band\s+that\s+(?P<tail>.+)$', raw_object, flags=re.IGNORECASE)
    if action_tail:
        coordinated = re.match(
            r'(?P<verbs>[A-Za-z]+(?:\s*,\s*(?!or\b)[A-Za-z]+)*\s*,?\s+or\s+[A-Za-z]+)\s+(?P<object>[^,.]+)$',
            action_tail.group('tail').strip().rstrip('.'),
            flags=re.IGNORECASE,
        )
        if coordinated:
            verbs = [part for part in re.findall(r'[A-Za-z]+', coordinated.group('verbs')) if part.casefold() != 'or']
            obj = _label(coordinated.group('object'))
            alternative_group = _claim_id(source_text_id, str(sentence.get('sentence_id', '')), action_tail.group('tail'))
            for verb in verbs:
                predicate = _verb(verb)
                _append(
                    claims, source_text_id, sentence, paragraph_id,
                    f'{subject} may {_singular(verb.casefold())} {obj} as one alternative',
                    'relation', subject=subject, predicate=predicate, object=obj,
                    modality='disjunctive_alternative', coordination='or', alternative_group=alternative_group,
                )
    ensure_access = re.search(r'ensures\s+(?P<object>.+?)\s+(?:is|are)\s+accessible\s+only\s+to\s+(?P<target>.+)$', raw_object, flags=re.IGNORECASE)
    if ensure_access:
        _append(claims, source_text_id, sentence, paragraph_id, f'{subject} ensures {_label(ensure_access.group("object"))} is accessible only to {_label(ensure_access.group("target"))}', 'relation', subject=subject, predicate='ensures_accessible_only_to', object=_label(ensure_access.group('target')), patient=_label(ensure_access.group('object')), quantifier='only')
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
            _append(claims, source_text_id, sentence, paragraph_id, f'{subject} ensures {item} is accessible when needed', 'relation', subject=subject, predicate='ensures_availability_of', object=item, condition='when_needed')
    return True



def _extract_sentence_claims_compat(claims: list[dict[str, Any]], source_text_id: str, sentence: dict[str, Any], paragraph_id: str) -> None:
    """Extract sentence claims compat."""
    text = _clean(str(sentence.get('text', '')))
    if not text:
        return
    purpose = re.match(r'^the\s+purpose\s+of\s+(?P<subject>.+?)\s+is\s+to\s+preserve\s+(?P<objects>.+?)\.?$', text, flags=re.IGNORECASE)
    if purpose:
        subject = _label(purpose.group('subject'))
        for item in _split_list(purpose.group('objects')):
            _append(
                claims, source_text_id, sentence, paragraph_id,
                f'{subject} has purpose to preserve {item}', 'relation',
                subject=subject, predicate='has_purpose_to_preserve', object=item, modality='purpose',
            )
        return
    form = re.match(r'^(?P<subjects>.+?)\s+form\s+(?P<object>.+?)\.?$', text, flags=re.IGNORECASE)
    if form:
        target = _label(form.group('object'))
        members = _split_list(form.group('subjects'))
        for member in members:
            _append(
                claims, source_text_id, sentence, paragraph_id,
                f'{target} has member {member}', 'relation',
                subject=target, predicate='has_member', object=member,
                members=','.join(members), modality='collective_composition',
            )
        return
    _extract_definition_claims_compat(claims, source_text_id, sentence, paragraph_id, text)



_RULE_ENGINE = RuleEngine(stage=_STAGE)
_RULE_ENGINE.register(TEMPORAL_SCOPE_RULE)
_RULE_ENGINE.register(REMEDIATION_D_RULE)
_RULE_ENGINE.register(REMEDIATION_D2_RULE)
_RULE_ENGINE.register(REMEDIATION_D3_RULE)
_RULE_ENGINE.register(REMEDIATION_D4_RULE)
_RULE_ENGINE.register(REMEDIATION_B3_RULE)


def _run_rule_engine(
    claims: list[dict[str, Any]],
    input_payload: dict[str, Any],
    config: dict[str, Any],
    paragraphs: dict[str, str],
) -> list[dict[str, Any]]:
    """Run rule engine."""
    source_text_id = str(input_payload.get('source_text_id', ''))

    def context_factory(sentence: dict[str, Any], paragraph_id: str) -> RuleContext:
        """Build the rule context for a sentence and paragraph."""
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
    """Split a claim label into words while preserving acronym boundaries."""
    local = str(value or '')
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', local)
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    return [token for token in re.sub(r'[^A-Za-z0-9]+', ' ', spaced).split() if token]


def _personal_pronoun_head(value: str | None) -> str:
    """Return the leading personal pronoun in a claim label, if present."""
    words = _claim_label_words(value)
    return words[0].casefold() if words and words[0].casefold() in _BR_PERSONAL_PRONOUNS else ''


def _is_projection_scaffold(value: str | None) -> bool:
    """Return whether a label begins with a type-of taxonomy scaffold."""
    words = [word.casefold() for word in _claim_label_words(value)]
    return len(words) >= 2 and words[:2] in (
        ['type', 'of'],
        ['kind', 'of'],
        ['category', 'of'],
        ['form', 'of'],
    )


def _semantic_claim_rejection_reason(claim: dict[str, Any]) -> str:
    """Return the projection-safety rejection reason for a semantic claim."""
    if not all(str(claim.get(field, '')).strip() for field in ('subject', 'predicate', 'object')):
        return 'missing_required_spo'
    if _is_projection_scaffold(str(claim.get('subject', ''))) or _is_projection_scaffold(str(claim.get('object', ''))):
        return 'projection_scaffold_resource'
    return ''


def _is_unresolved_internal_claim(claim: dict[str, Any]) -> bool:
    """Return whether claim metadata marks it unresolved or hidden from projection."""
    return str(claim.get('resolution_status') or claim.get('visibility') or '').casefold() in {'unresolved', 'internal_unresolved', 'internal', 'hidden', 'not_visible'}


def _rewrite_claim_parts(claim: dict[str, Any], subject: str, obj: str) -> None:
    """Replace resolved claim endpoints and rebuild its statement fields in place."""
    predicate = str(claim.get('predicate', ''))
    if subject:
        claim['subject'] = subject
    if obj:
        claim['object'] = obj
    claim['statement'] = f"{claim.get('subject', '')} {predicate} {claim.get('object', '')}"
    claim['normalized_statement'] = claim['statement']


def _resolve_personal_pronoun_claims(claims: list[dict[str, Any]]) -> None:
    """Resolve personal pronoun claims."""
    last_subject = ''
    for claim in claims:
        subject = str(claim.get('subject', ''))
        obj = str(claim.get('object', ''))
        subject_pronoun = _personal_pronoun_head(subject)
        object_pronoun = _personal_pronoun_head(obj)
        if subject_pronoun:
            # Recency is accepted for person-like pronouns; resolving it/its would guess an inanimate referent.
            if last_subject and subject_pronoun not in {'it', 'its'}:
                _rewrite_claim_parts(claim, last_subject, obj)
                subject = last_subject
            else:
                claim['resolution_status'] = 'unresolved'
                claim['visibility'] = 'internal'
                claim['internal'] = True
        if object_pronoun:
            # No object-antecedent model exists, so pronoun objects remain internal instead of being guessed.
            claim['resolution_status'] = 'unresolved'
            claim['visibility'] = 'internal'
            claim['internal'] = True
        if not _personal_pronoun_head(subject) and not _is_unresolved_internal_claim(claim):
            last_subject = subject


def _resolve_semantic_references(claims: list[dict[str, Any]]) -> None:
    """Resolve semantic references."""
    subjects = [str(claim.get('subject', '')) for claim in claims if str(claim.get('subject', ''))]
    by_tail: dict[str, str] = {}
    # The first full subject for a terminal noun becomes its deterministic shorthand target.
    for subject in subjects:
        tail = re.sub(r'(?<!^)([A-Z])', r' \1', subject).split()[-1] if subject else ''
        if tail and tail not in by_tail:
            by_tail[tail] = subject
    for claim in claims:
        predicate = str(claim.get('predicate', ''))
        # Taxonomy, dependency-derived, and explicitly lexical claims must retain source endpoint wording.
        if predicate in {'is_a', 'type_of'} or claim.get('extracted_by') == 'CORE-SEM-DEPENDENCY-001' or claim.get('preserve_lexical_object'):
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
    """Return a mapping suitable for canonical-claim configuration."""
    return config if isinstance(config, dict) else {}


def _configured_artifact_path(config: dict[str, Any]) -> Path | None:
    """Return the configured artifact path when output persistence is enabled."""
    raw_path = config.get('artifact_path') or config.get('output_path')
    if raw_path in (None, ''):
        return None
    return Path(raw_path)


def _configured_asset_ids(config: dict[str, Any]) -> list[str] | None:
    """Return normalized configured paragraph asset identifiers."""
    raw_ids = config.get('paragraph_asset_ids') or config.get('asset_ids')
    if not isinstance(raw_ids, list):
        return None
    ids = [str(item).strip() for item in raw_ids if str(item).strip()]
    return ids or None


def extract_canonical_claims_from_payload(input_payload: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Extract canonical or semantic claims, apply configured rules, and preserve source traceability."""
    stage_config = _canonical_claims_config(config)
    source_text_id = str(input_payload.get('source_text_id', ''))
    sentences = [item for item in input_payload.get('sentences', []) if isinstance(item, dict)]
    paragraphs = _paragraph_map(str(input_payload.get('raw_text') or input_payload.get('preprocessed_text') or ''), sentences, _configured_asset_ids(stage_config))
    claims: list[dict[str, Any]] = []
    emit_semantic = bool(stage_config.get('emit_semantic_claims'))
    extractor = _extract_sentence_claims if emit_semantic else _extract_sentence_claims_compat
    for sentence in sentences:
        paragraph_id = paragraphs.get(str(sentence.get('sentence_id', '')), '')
        before_count = len(claims)
        extractor(claims, source_text_id, sentence, paragraph_id)
        if emit_semantic and not _is_meta_instruction_text(str(sentence.get('text', ''))):
            added_claims = claims[before_count:]
            has_complete_claim = any(
                all(str(claim.get(field, '')).strip() for field in ('subject', 'predicate', 'object'))
                for claim in added_claims
            )
            represented_sentence = ' represent that ' in f" {str(sentence.get('text', '')).casefold()} "
            has_structured_representation = any(
                claim.get('relation_role') == 'represented_content' for claim in added_claims
            )
            if not has_complete_claim or (represented_sentence and not has_structured_representation):
                existing_spo = {
                    (str(claim.get('subject', '')), str(claim.get('predicate', '')), str(claim.get('object', '')))
                    for claim in added_claims
                }
                for relation in extract_dependency_relations(input_payload, sentence, label=_label, verb_form=_verb):
                    key = (relation['subject'], relation['predicate'], relation['object'])
                    if key in existing_spo:
                        continue
                    _append_relation(
                        claims,
                        source_text_id,
                        sentence,
                        paragraph_id,
                        relation['subject'],
                        relation['predicate'],
                        relation['object'],
                        modality=relation.get('modality', ''),
                        voice=relation.get('voice', ''),
                        extracted_by=relation.get('extracted_by', ''),
                    )
                    existing_spo.add(key)
    rejected_claims: list[dict[str, Any]] = []
    if emit_semantic:
        rejected_claims = _run_rule_engine(claims, input_payload, stage_config, paragraphs)
        _resolve_personal_pronoun_claims(claims)
        _resolve_semantic_references(claims)
        accepted_claims: list[dict[str, Any]] = []
        for claim in claims:
            reason = _semantic_claim_rejection_reason(claim)
            if reason:
                rejected_claims.append({
                    **claim,
                    'type': 'invalid_semantic_claim',
                    'rejection_reason': reason,
                })
            else:
                accepted_claims.append(claim)
        claims = accepted_claims
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
