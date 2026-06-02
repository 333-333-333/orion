from __future__ import annotations

import re
from typing import Any

from .namespace import compact_iri, make_iri, validate_and_resolve_prefixes, validate_base_iri


def _normalize_text(value: str | None) -> str:
    return (value or '').strip().casefold()


def _normalize_predicate(value: str | None) -> str:
    normalized = _normalize_text(value)
    if not normalized:
        return ''
    return re.sub(r'[^a-z0-9]+', '_', normalized).strip('_')


def _dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _dedupe_pairs(items: list[dict[str, str]], key_fields: tuple[str, ...]) -> list[dict[str, str]]:
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
    def __init__(
        self,
        base_iri: str | None = None,
        prefixes: dict[str, str] | None = None,
    ) -> None:
        self._namespace_mode = base_iri is not None or prefixes is not None
        if self._namespace_mode:
            resolved_base_iri = validate_base_iri(base_iri or 'https://orion.local/resource/')
            self._base_iri = resolved_base_iri
            self._prefixes = validate_and_resolve_prefixes(resolved_base_iri, prefixes)
        else:
            self._base_iri = ''
            self._prefixes = {}

    def _compact(self, text: str, kind: str) -> str:
        return compact_iri(make_iri(text, kind=kind, base_iri=self._base_iri), self._prefixes)

    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self._namespace_mode:
            classes = _dedupe_strings([
                self._compact(concept.get('normalized_text') or concept.get('lemma') or concept.get('text') or '', 'class')
                for concept in payload.get('concepts', []) if isinstance(concept, dict)
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
            class_assertions.append({'individual': individual, 'class': class_name})

        subclass_axioms: list[dict[str, str]] = []
        for relation in payload.get('taxonomy_relations', []):
            if not isinstance(relation, dict):
                continue
            if self._namespace_mode:
                child = self._compact(relation.get('child') or '', 'class')
                parent = self._compact(relation.get('parent') or '', 'class')
            else:
                child = _normalize_text(relation.get('child'))
                parent = _normalize_text(relation.get('parent'))
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
