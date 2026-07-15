"""Generate the compatibility OWL graph representation."""

from __future__ import annotations

import re
from typing import Any

from .namespace import compact_iri, make_iri, validate_and_resolve_prefixes, validate_base_iri


def _normalize_text(value: str | None) -> str:
    """Normalize text."""
    return (value or '').strip().casefold()


def _normalize_predicate(value: str | None) -> str:
    """Normalize predicate."""
    normalized = _normalize_text(value)
    if not normalized:
        return ''
    return re.sub(r'[^a-z0-9]+', '_', normalized).strip('_')


_TAXONOMY_SCAFFOLD_HEADS = {'type', 'kind', 'category', 'form'}
_PHRASE_ARTICLES = {'a', 'an', 'the'}


def _is_taxonomy_scaffold(value: str | None) -> bool:
    """Return whether a label is a type, kind, category, or form-of scaffold."""
    normalized = _normalize_text(value)
    if not normalized:
        return False
    tokens = [token for token in re.sub(r'[^a-z0-9]+', ' ', normalized).split(' ') if token]
    while tokens and tokens[0] in _PHRASE_ARTICLES:
        tokens.pop(0)
    return len(tokens) >= 3 and tokens[0] in _TAXONOMY_SCAFFOLD_HEADS and tokens[1] == 'of'


def _dedupe_strings(values: list[str]) -> list[str]:
    """Deduplicate strings while preserving deterministic order."""
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _dedupe_pairs(items: list[dict[str, str]], key_fields: tuple[str, ...]) -> list[dict[str, str]]:
    """Deduplicate pairs while preserving deterministic order."""
    seen: set[tuple[str, ...]] = set()
    unique: list[dict[str, str]] = []
    for item in items:
        key = tuple(item.get(field, '') for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


class OwlOutputStrategy:
    """Compatibility strategy that builds the lightweight OWL graph representation."""
    def __init__(
        self,
        base_iri: str | None = None,
        prefixes: dict[str, str] | None = None,
    ) -> None:
        """Initialize the OwlOutputStrategy."""
        self._namespace_mode = base_iri is not None or prefixes is not None
        if self._namespace_mode:
            resolved_base_iri = validate_base_iri(base_iri or 'https://orion.local/resource/')
            self._base_iri = resolved_base_iri
            self._prefixes = validate_and_resolve_prefixes(resolved_base_iri, prefixes)
        else:
            self._base_iri = ''
            self._prefixes = {}

    def _compact(self, text: str, kind: str) -> str:
        """Create and compact an IRI in the strategy namespace."""
        return compact_iri(make_iri(text, kind=kind, base_iri=self._base_iri), self._prefixes)

    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Generate the compatibility OWL graph without mutating the input payload."""
        if self._namespace_mode:
            classes = _dedupe_strings([
                self._compact(concept.get('normalized_text') or concept.get('lemma') or concept.get('text') or '', 'class')
                for concept in payload.get('concepts', [])
                if isinstance(concept, dict) and not _is_taxonomy_scaffold(concept.get('normalized_text') or concept.get('lemma') or concept.get('text'))
            ])
            individuals = _dedupe_strings([
                self._compact(entity.get('normalized_text') or entity.get('text') or '', 'individual')
                for entity in payload.get('entities', []) if isinstance(entity, dict)
            ])
            object_properties = _dedupe_strings([
                self._compact(relation.get('predicate') or '', 'predicate')
                for relation in payload.get('relations', []) if isinstance(relation, dict)
            ] + [
                self._compact(triple.get('predicate') or '', 'predicate')
                for triple in payload.get('triples', []) if isinstance(triple, dict)
            ])
        else:
            classes = _dedupe_strings([
                _normalize_text(concept.get('normalized_text') or concept.get('lemma') or concept.get('text'))
                for concept in payload.get('concepts', []) if isinstance(concept, dict)
            ])
            individuals = _dedupe_strings([
                _normalize_text(entity.get('normalized_text') or entity.get('text'))
                for entity in payload.get('entities', []) if isinstance(entity, dict)
            ])
            object_properties = _dedupe_strings([
                _normalize_predicate(relation.get('predicate'))
                for relation in payload.get('relations', []) if isinstance(relation, dict)
            ] + [
                _normalize_predicate(triple.get('predicate'))
                for triple in payload.get('triples', []) if isinstance(triple, dict)
            ])

        class_assertions: list[dict[str, str]] = []
        for assertion in payload.get('type_assertions', []):
            if not isinstance(assertion, dict):
                continue
            if self._namespace_mode:
                individual = self._compact(assertion.get('entity') or assertion.get('instance') or '', 'individual')
                class_name = self._compact(assertion.get('type') or assertion.get('class') or '', 'class')
            else:
                individual = _normalize_text(assertion.get('entity') or assertion.get('instance'))
                class_name = _normalize_text(assertion.get('type') or assertion.get('class'))
            if not individual or not class_name:
                continue
            if _is_taxonomy_scaffold(assertion.get('type') or assertion.get('class')):
                continue
            class_assertions.append({'individual': individual, 'class': class_name})

        subclass_axioms: list[dict[str, str]] = []
        for relation in payload.get('taxonomy_relations', []):
            if not isinstance(relation, dict):
                continue
            if self._namespace_mode:
                child_raw = relation.get('child') or ''
                parent_raw = relation.get('parent') or ''
                if _is_taxonomy_scaffold(parent_raw):
                    continue
                child = self._compact(child_raw, 'class')
                parent = self._compact(parent_raw, 'class')
            else:
                child = _normalize_text(relation.get('child'))
                parent = _normalize_text(relation.get('parent'))
                if _is_taxonomy_scaffold(parent):
                    continue
            if not child or not parent:
                continue
            subclass_axioms.append({'child': child, 'parent': parent})

        result = {k: v for k, v in payload.items() if not k.startswith('_spacy')}
        owl_graph = {
            'classes': classes,
            'individuals': individuals,
            'object_properties': object_properties,
            'class_assertions': _dedupe_pairs(class_assertions, ('individual', 'class')),
            'subclass_axioms': _dedupe_pairs(subclass_axioms, ('child', 'parent')),
        }
        result['output'] = {
            'strategy': 'owl',
            'format': 'owl',
            'graph': owl_graph,
            'ontology': owl_graph,
            'metadata': payload.get('metadata', {}),
        }
        return result
