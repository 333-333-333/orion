"""Validate namespaces and create deterministic resource IRIs."""

from __future__ import annotations

import re
from urllib.parse import urlparse

_RESERVED_PREFIXES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
}
_DEFAULT_BASE_IRI = 'https://orion.local/resource/'
_DEFAULT_PREFIX = 'orion'
_PHRASE_ARTICLES = {'a', 'an', 'the', 'any', 'each', 'one', 'more'}


def _is_absolute_http_iri(value: str) -> bool:
    """Return whether a value is an absolute HTTP or HTTPS IRI with an authority."""
    parsed = urlparse(value)
    return parsed.scheme in {'http', 'https'} and bool(parsed.netloc)


def validate_base_iri(base_iri: str) -> str:
    """Validate and return an absolute HTTP(S) base IRI."""
    if not isinstance(base_iri, str) or base_iri.strip() == '':
        raise ValueError('base_iri must be a non-empty string')
    candidate = base_iri.strip()
    if not _is_absolute_http_iri(candidate):
        raise ValueError('base_iri must be an absolute http/https IRI')
    return candidate


def validate_and_resolve_prefixes(base_iri: str, custom_prefixes: dict[str, str] | None = None) -> dict[str, str]:
    """Validate custom prefixes and merge them with reserved and ORION namespaces."""
    resolved = dict(_RESERVED_PREFIXES)
    resolved[_DEFAULT_PREFIX] = base_iri

    if custom_prefixes is None:
        return resolved
    if not isinstance(custom_prefixes, dict) or len(custom_prefixes) == 0:
        raise ValueError('prefixes must be a non-empty mapping')

    for prefix, iri in custom_prefixes.items():
        if not isinstance(prefix, str) or prefix.strip() == '':
            raise ValueError('prefixes keys must be non-empty strings')

        clean_prefix = prefix.strip()
        if not isinstance(iri, str) or iri.strip() == '':
            raise ValueError(f'prefixes {clean_prefix} must map to non-empty string IRI')
        clean_iri = iri.strip()

        if not _is_absolute_http_iri(clean_iri):
            raise ValueError(f'prefixes {clean_prefix} must map to absolute http/https IRI')

        if clean_prefix in _RESERVED_PREFIXES and clean_iri != _RESERVED_PREFIXES[clean_prefix]:
            raise ValueError(f'{clean_prefix} prefix is reserved and cannot be overridden')

        resolved[clean_prefix] = clean_iri

    return resolved


def slugify_iri_part(text: str, style: str) -> str:
    """Convert text into the requested class, predicate, or individual IRI style."""
    normalized = re.sub(r'[^a-z0-9]+', ' ', (text or '').casefold()).strip()
    parts = [part for part in normalized.split(' ') if part]
    if not parts:
        return ''

    if style == 'class':
        while parts and parts[0] in _PHRASE_ARTICLES:
            if len(parts) >= 3 and parts[0] == 'one' and parts[1] == 'or' and parts[2] == 'more':
                parts = parts[3:]
                continue
            parts.pop(0)
        return ''.join(part.capitalize() for part in parts)
    if style == 'predicate':
        head, *tail = parts
        return head + ''.join(part.capitalize() for part in tail)
    if style == 'individual':
        return '-'.join(parts)
    raise ValueError('style must be one of: class, predicate, individual')


def make_iri(text: str, kind: str, base_iri: str = _DEFAULT_BASE_IRI) -> str:
    """Create an absolute IRI for a class, predicate, or individual label."""
    style = {'class': 'class', 'predicate': 'predicate', 'individual': 'individual'}.get(kind)
    if style is None:
        raise ValueError('kind must be one of: class, predicate, individual')
    slug = slugify_iri_part(text, style)
    return f"{base_iri}{slug}" if slug else ''


def compact_iri(iri: str, prefixes: dict[str, str] | None = None) -> str:
    """Compact an absolute IRI with the first matching namespace prefix."""
    mapping = prefixes or {**_RESERVED_PREFIXES, _DEFAULT_PREFIX: _DEFAULT_BASE_IRI}
    for prefix, namespace in mapping.items():
        if iri.startswith(namespace):
            suffix = iri[len(namespace):]
            if suffix:
                return f'{prefix}:{suffix}'
    return iri
