from __future__ import annotations

import re

_ARTICLES = {'a', 'an', 'the', 'any', 'each', 'one', 'more'}
_STOP_TAIL = re.compile(r'\b(?:focused|designed|intended|used|required)\b.*$', re.IGNORECASE)
_BR_PERSONAL_PRONOUNS = {'he', 'she', 'they', 'it', 'we', 'his', 'her', 'their', 'its', 'them'}
_BR_LEADING_CONTEXT_PREPOSITIONS = {'from', 'to', 'at', 'in', 'on', 'during', 'after', 'before'}
_BR_POSSESSIVE_PRONOUNS = {'his', 'her', 'their', 'its'}
_BR_NOMINALIZED_ACTION_HEADS = {'ability', 'capability', 'capacity'}
_BR_NOMINALIZED_CONTEXT_PREPOSITIONS = {'to', 'for', 'with', 'from', 'in', 'on', 'at'}
_BR_NOMINALIZED_CONTEXT_MODIFIERS = {'specific', 'particular', 'explicit'}
_BR_NLP_MODAL_OBJECT_NOMINALIZATION_HEADS = {'likelihood'}
_BR_NLP_MODAL_OBJECT_NOMINALIZATION_PREPOSITION = 'of'


def _clean(value: str | None) -> str:
    return re.sub(r'\s+', ' ', (value or '').strip())


def _words(value: str | None) -> list[str]:
    return [token for token in re.sub(r'[^A-Za-z0-9]+', ' ', value or '').split() if token]


def _strip_endpoint_context(value: str | None) -> str:
    text = _clean(value or '')
    if not text:
        return ''
    contextual = '|'.join(sorted(_BR_LEADING_CONTEXT_PREPOSITIONS))
    pronouns = '|'.join(sorted(_BR_PERSONAL_PRONOUNS))
    comma_match = re.match(rf'^(?:{contextual})\b[^,]*,\s*(?P<rest>.+)$', text, flags=re.IGNORECASE)
    if comma_match:
        text = comma_match.group('rest').strip()
    pronoun_match = re.match(rf'^(?:{contextual})\b(?:\s+\w+){{0,3}}\s+(?P<pronoun>{pronouns})\b$', text, flags=re.IGNORECASE)
    if pronoun_match:
        text = pronoun_match.group('pronoun')
    else:
        text = re.sub(rf'^(?:{contextual})\s+', '', text, count=1, flags=re.IGNORECASE).strip()
    words = _words(text)
    if words and words[0].casefold() in _BR_POSSESSIVE_PRONOUNS:
        raw = re.sub(r'^\s*' + re.escape(words[0]) + r'\b', '', text, count=1, flags=re.IGNORECASE).strip()
        if raw:
            text = raw
    return text


def _singular(token: str) -> str:
    lower = token.casefold()
    if len(lower) > 3 and lower.endswith('ies'):
        return token[:-3] + 'y'
    if len(lower) > 4 and lower.endswith(('ses', 'xes', 'zes', 'ches', 'shes')):
        return token[:-2]
    if len(lower) > 3 and lower.endswith('s') and not lower.endswith(('ss', 'us', 'is')):
        return token[:-1]
    return token



def _reorder_nominalized_action_object(value: str) -> str:
    pattern = (
        r'^(?:a|an|the)?\s*'
        r'(?P<head>' + '|'.join(sorted(_BR_NLP_MODAL_OBJECT_NOMINALIZATION_HEADS)) + r')\s+'
        + _BR_NLP_MODAL_OBJECT_NOMINALIZATION_PREPOSITION +
        r'\s+(?P<action>[A-Za-z]+ing)\s+(?P<object>.+)$'
    )
    match = re.match(pattern, _clean(value), flags=re.IGNORECASE)
    if not match:
        return value
    object_words = _words(match.group('object'))
    while object_words and object_words[0].casefold() in _ARTICLES:
        object_words.pop(0)
    if not object_words:
        return value
    return ' '.join([*object_words, match.group('action'), match.group('head')])

def _phrase(value: str | None) -> str:
    text = _STOP_TAIL.sub('', _clean(value or ''))
    text = re.sub(r'\b(?:that|which|who)\b.*$', '', text, flags=re.IGNORECASE)
    # TASK-NLP-P039-P040-OBSERVATIONAL-CLEANUP: keep modal object as domain concept, not literal word order.
    text = _reorder_nominalized_action_object(text)
    tokens = _words(text)
    while tokens and tokens[0].casefold() in _ARTICLES:
        tokens.pop(0)
    normalized = []
    for index, token in enumerate(tokens):
        lower = token.casefold()
        normalized.append(lower if index > 0 and tokens[index - 1].casefold() == 'of' else _singular(lower))
    return ' '.join(normalized)


def _label(value: str | None) -> str:
    value = _strip_endpoint_context(value)
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
