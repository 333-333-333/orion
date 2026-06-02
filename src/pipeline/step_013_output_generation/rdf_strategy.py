from __future__ import annotations

import re
from typing import Any

from .namespace import compact_iri, make_iri, validate_and_resolve_prefixes, validate_base_iri


_ORION_NS = 'https://orion.local/resource/'
_RDF_TYPE = 'rdf' + ':type'
_RDFS_SUBCLASS = 'rdfs' + ':subClassOf'
_RDF_XML_TYPE_TAG = 'rdf' + ':type'
_BR_RELATIVE_PRONOUNS = {'that', 'which', 'who'}


def _normalize_text(value: str | None) -> str:
    return (value or '').strip().casefold()


def _normalize_predicate(value: str | None) -> str:
    normalized = _normalize_text(value)
    if not normalized:
        return ''
    return re.sub(r'[^a-z0-9]+', '_', normalized).strip('_')


def _expand_curie_to_iri(value: str) -> str:
    if value.startswith('http://') or value.startswith('https://'):
        return value
    if value.startswith('orion:'):
        return f"{_ORION_NS}{value.split(':', 1)[1]}"
    if value.startswith('rdf:'):
        return f"http://www.w3.org/1999/02/22-rdf-syntax-ns#{value.split(':', 1)[1]}"
    if value.startswith('rdfs:'):
        return f"http://www.w3.org/2000/01/rdf-schema#{value.split(':', 1)[1]}"
    if value.startswith('owl:'):
        return f"http://www.w3.org/2002/07/owl#{value.split(':', 1)[1]}"
    return value


def _local_name(value: str) -> str:
    return value.rsplit('/', 1)[-1].rsplit('#', 1)[-1]


def _canonical_orion_resource_iri(value: str) -> str:
    if not value:
        return value
    if value.startswith(_ORION_NS):
        local = _local_name(value)
        if local:
            return f"{_ORION_NS}{local.lower()}"
    return value


def _resource_label_from_iri(iri: str) -> str:
    local = _local_name(iri).strip()
    if not local:
        return 'Resource'
    if local.islower():
        parts = [part for part in re.split(r'[^a-zA-Z0-9]+', local) if part]
        if parts:
            return ''.join(part[:1].upper() + part[1:] for part in parts)
    return local


def _dedupe_stable(items: list[dict[str, str]], key_fields: tuple[str, ...]) -> list[dict[str, str]]:
    seen: set[tuple[str, ...]] = set()
    unique: list[dict[str, str]] = []
    for item in items:
        key = tuple(item.get(field, '') for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def _dedupe_string_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _collect_bootstrap_class_nodes(payload: dict[str, Any], base_iri: str, namespace_mode: bool) -> list[str]:
    bootstrap_nodes: list[str] = []
    for concept in payload.get('concepts', []):
        if not isinstance(concept, dict):
            continue
        raw_value = concept.get('normalized_text') or concept.get('lemma') or concept.get('text')
        normalized = _normalize_text(raw_value if isinstance(raw_value, str) else '')
        if not normalized:
            continue
        if normalized in _BR_RELATIVE_PRONOUNS or _is_poor_numeric_id(normalized):
            continue

        if namespace_mode:
            iri = make_iri(normalized, kind='class', base_iri=base_iri)
            if iri:
                bootstrap_nodes.append(iri)
        else:
            bootstrap_nodes.append(normalized)

    return _dedupe_string_values(bootstrap_nodes)


def _is_rdf_or_rdfs_predicate(value: str) -> bool:
    expanded = _expand_curie_to_iri(value)
    return expanded.startswith('http://www.w3.org/1999/02/22-rdf-syntax-ns#') or expanded.startswith('http://www.w3.org/2000/01/rdf-schema#')


def _build_explicit_owl_schema(
    facts: list[dict[str, str]],
    instance_facts: list[dict[str, str]],
    subclass_facts: list[dict[str, str]],
    bootstrap_class_nodes: list[str] | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    classes_set: set[str] = set()

    for item in facts:
        subject = str(item.get('subject', '')).strip()
        obj = str(item.get('object', '')).strip()
        if subject and subject not in _BR_RELATIVE_PRONOUNS:
            classes_set.add(subject)
        if obj and obj not in _BR_RELATIVE_PRONOUNS:
            classes_set.add(obj)

    if bootstrap_class_nodes:
        for raw_node in bootstrap_class_nodes:
            node = str(raw_node).strip()
            if not node:
                continue
            if node.startswith('orion:'):
                node = _expand_curie_to_iri(node)
            elif node not in _BR_RELATIVE_PRONOUNS:
                node = _canonical_orion_resource_iri(_expand_curie_to_iri(node)) if node.startswith('http') else node
            if node:
                classes_set.add(node)

    resource_types: dict[str, str] = {}

    type_assertions: list[dict[str, str]] = []
    for item in instance_facts:
        subject = str(item.get('subject', '')).strip()
        obj = str(item.get('object', '')).strip()
        if not subject or not obj:
            continue
        resource_types.setdefault(subject, obj)
        classes_set.add(obj)
        type_assertions.append({'entity': subject, 'type': obj})

    for item in subclass_facts:
        subject = str(item.get('subject', '')).strip()
        obj = str(item.get('object', '')).strip()
        if not subject or not obj:
            continue
        classes_set.add(subject)
        classes_set.add(obj)

    classes = [{'iri': cls, 'label': _resource_label_from_iri(_expand_curie_to_iri(cls))} for cls in sorted(classes_set)]
    class_by_local_lower: dict[str, str] = {}
    for cls in sorted(classes_set):
        local = _local_name(_expand_curie_to_iri(cls)).casefold()
        if local and local not in class_by_local_lower:
            class_by_local_lower[local] = cls

    object_property_schema: list[dict[str, str]] = []
    restrictions: list[dict[str, str]] = []

    for fact in facts:
        predicate = str(fact.get('predicate', '')).strip()
        subject = str(fact.get('subject', '')).strip()
        obj = str(fact.get('object', '')).strip()
        if not predicate or not subject or not obj:
            continue
        if _is_rdf_or_rdfs_predicate(predicate):
            continue

        domain = resource_types.get(subject, '')
        range_iri = resource_types.get(obj, '')
        if not domain and subject in classes_set:
            domain = subject
        if not range_iri and obj in classes_set:
            range_iri = obj
        if not domain:
            domain = class_by_local_lower.get(_local_name(_expand_curie_to_iri(subject)).casefold(), '')
        if not range_iri:
            range_iri = class_by_local_lower.get(_local_name(_expand_curie_to_iri(obj)).casefold(), '')

        entry = {'predicate': predicate}
        if domain and domain in classes_set:
            entry['domain'] = domain
        if range_iri and range_iri in classes_set:
            entry['range'] = range_iri
        object_property_schema.append(entry)

        if entry.get('domain') and entry.get('range'):
            restrictions.append({'domain': entry['domain'], 'property': predicate, 'range': entry['range']})

    object_property_schema = _dedupe_stable(object_property_schema, ('predicate', 'domain', 'range'))

    by_predicate: dict[str, dict[str, Any]] = {}
    for row in object_property_schema:
        predicate = str(row.get('predicate', '')).strip()
        domain = str(row.get('domain', '')).strip()
        range_iri = str(row.get('range', '')).strip()
        if not predicate or not domain or not range_iri:
            continue
        rec = by_predicate.setdefault(predicate, {'rows': [], 'domains': set(), 'ranges': set()})
        rec['rows'].append(row)
        rec['domains'].add(domain)
        rec['ranges'].add(range_iri)

    object_property_schema = [
        rec['rows'][0]
        for rec in by_predicate.values()
        if len(rec['domains']) == 1 and len(rec['ranges']) == 1
    ]

    restrictions = [
        {'domain': item['domain'], 'property': item['predicate'], 'range': item['range']}
        for item in object_property_schema
    ]
    restrictions = _dedupe_stable(restrictions, ('domain', 'property', 'range'))

    schema = {
        'classes': classes,
        'object_properties': [
            {'iri': item['predicate'], 'label': _resource_label_from_iri(_expand_curie_to_iri(item['predicate'])), **({'domain': item['domain']} if item.get('domain') else {}), **({'range': item['range']} if item.get('range') else {})}
            for item in object_property_schema
        ],
    }

    return classes, type_assertions, object_property_schema, restrictions, schema


def _statement_identity(subject_iri: str, predicate_iri: str, object_iri: str) -> str:
    def _slug(value: str, fallback: str) -> str:
        token = re.sub(r'[^a-z0-9]+', '-', _local_name(value).casefold()).strip('-')
        return token or fallback

    subj = _slug(subject_iri, 'subject')
    pred = _slug(predicate_iri, 'predicate')
    obj = _slug(object_iri, 'object')

    base = f"{subj}-{pred}-{obj}"
    if len(base) <= 48:
        return f"{_ORION_NS}statement/{base}"

    compact = f"{subj[:14]}-{pred[:14]}-{obj[:14]}".strip('-')
    if len(compact) > 48:
        compact = compact[:48].rstrip('-')
    return f"{_ORION_NS}statement/{compact or 'statement'}"


def _statement_label(subject_iri: str, predicate_iri: str, object_iri: str) -> str:
    return f"{subject_iri} {predicate_iri} {object_iri}".strip()


def _filter_isolated_owl_nodes(
    class_rows: dict[str, str],
    explicit_object_properties: list[dict[str, str]],
    restrictions_by_domain: dict[str, list[tuple[str, str]]],
    reified_statements: list[dict[str, str]],
    subclass_relations: dict[str, set[str]],
) -> tuple[set[str], set[str], dict[str, list[tuple[str, str]]]]:
    class_nodes = {
        iri
        for iri in class_rows
        if isinstance(iri, str) and iri.startswith('https://orion.local/resource/')
    }

    for subject_iri, objects in subclass_relations.items():
        subject = _canonical_orion_resource_iri(_expand_curie_to_iri(str(subject_iri).strip()))
        if subject:
            class_nodes.add(subject)
        for object_iri in objects:
            canonical_object = _canonical_orion_resource_iri(_expand_curie_to_iri(str(object_iri).strip()))
            if canonical_object:
                class_nodes.add(canonical_object)

    property_nodes: set[str] = set()
    for item in explicit_object_properties:
        if not isinstance(item, dict):
            continue
        iri = _expand_curie_to_iri(str(item.get('iri', '')).strip())
        if iri.startswith('https://orion.local/resource/'):
            property_nodes.add(iri)

    candidate_nodes = class_nodes | property_nodes
    if not candidate_nodes:
        return set(), set(), {}

    edges: dict[str, set[str]] = {node: set() for node in candidate_nodes}

    def _add_edge(left: str, right: str) -> None:
        if left not in edges or right not in edges or left == right:
            return
        edges[left].add(right)
        edges[right].add(left)

    for subject_iri, objects in subclass_relations.items():
        subject = _canonical_orion_resource_iri(_expand_curie_to_iri(str(subject_iri).strip()))
        if subject not in edges:
            continue
        for obj_iri in objects:
            _add_edge(subject, _canonical_orion_resource_iri(_expand_curie_to_iri(str(obj_iri).strip())))

    for domain_iri, pairs in restrictions_by_domain.items():
        domain = _canonical_orion_resource_iri(_expand_curie_to_iri(str(domain_iri).strip()))
        if domain not in edges:
            continue
        for prop_iri, range_iri in pairs:
            _add_edge(domain, _canonical_orion_resource_iri(_expand_curie_to_iri(str(prop_iri).strip())))
            _add_edge(domain, _canonical_orion_resource_iri(_expand_curie_to_iri(str(range_iri).strip())))

    for item in explicit_object_properties:
        if not isinstance(item, dict):
            continue
        prop_iri = _expand_curie_to_iri(str(item.get('iri', '')).strip())
        if prop_iri not in edges:
            continue
        domain = str(item.get('domain', '')).strip()
        rng = str(item.get('range', '')).strip()
        _add_edge(prop_iri, domain)
        _add_edge(prop_iri, rng)

    for statement in reified_statements:
        if not isinstance(statement, dict):
            continue
        subject = str(statement.get('subject', '')).strip()
        predicate = str(statement.get('predicate', '')).strip()
        obj = str(statement.get('object', '')).strip()

        _add_edge(subject, predicate)
        _add_edge(predicate, obj)
        _add_edge(subject, obj)

    visible_nodes = {node for node, neighbors in edges.items() if neighbors}

    connected_class_nodes: set[str] = {
        node
        for subject_iri, objects in subclass_relations.items()
        for node in [_canonical_orion_resource_iri(_expand_curie_to_iri(str(subject_iri).strip()))]
        if node in class_nodes
    }
    connected_class_nodes.update(
        node
        for subject_iri, objects in subclass_relations.items()
        for object_iri in objects
        for node in [_canonical_orion_resource_iri(_expand_curie_to_iri(str(object_iri).strip()))]
        if node in class_nodes
    )

    for prop in explicit_object_properties:
        if not isinstance(prop, dict):
            continue
        domain = _canonical_orion_resource_iri(_expand_curie_to_iri(str(prop.get('domain', '')).strip()))
        range_iri = _canonical_orion_resource_iri(_expand_curie_to_iri(str(prop.get('range', '')).strip()))
        if domain in class_nodes:
            connected_class_nodes.add(domain)
        if range_iri in class_nodes:
            connected_class_nodes.add(range_iri)

    for domain, pairs in restrictions_by_domain.items():
        domain_iri = _canonical_orion_resource_iri(_expand_curie_to_iri(str(domain).strip()))
        if domain_iri in class_nodes:
            connected_class_nodes.add(domain_iri)
        for _, range_iri in pairs:
            canon_range_iri = _canonical_orion_resource_iri(_expand_curie_to_iri(str(range_iri).strip()))
            if canon_range_iri in class_nodes:
                connected_class_nodes.add(canon_range_iri)

    for statement in reified_statements:
        if not isinstance(statement, dict):
            continue
        subject = _canonical_orion_resource_iri(_expand_curie_to_iri(str(statement.get('subject', '')).strip()))
        predicate = _canonical_orion_resource_iri(_expand_curie_to_iri(str(statement.get('predicate', '')).strip()))
        object_iri = _canonical_orion_resource_iri(_expand_curie_to_iri(str(statement.get('object', '')).strip()))

        if subject in class_nodes and predicate in property_nodes:
            connected_class_nodes.add(subject)
        if object_iri in class_nodes and predicate in property_nodes:
            connected_class_nodes.add(object_iri)

    # expand connectivity through subclass hierarchy anchored on semantic nodes
    changed = True
    while changed:
        changed = False
        for subject_iri, objects in subclass_relations.items():
            subject = _canonical_orion_resource_iri(_expand_curie_to_iri(str(subject_iri).strip()))
            if subject not in class_nodes:
                continue
            for object_iri_raw in objects:
                object_iri = _canonical_orion_resource_iri(_expand_curie_to_iri(str(object_iri_raw).strip()))
                if object_iri not in class_nodes:
                    continue

                if subject in connected_class_nodes and object_iri not in connected_class_nodes:
                    connected_class_nodes.add(object_iri)
                    changed = True
                if object_iri in connected_class_nodes and subject not in connected_class_nodes:
                    connected_class_nodes.add(subject)
                    changed = True

    visible_classes = {
        node
        for node in class_nodes
        if node in visible_nodes and node in connected_class_nodes
    }
    visible_properties = {
        node
        for node in property_nodes
        if node in visible_nodes
    }

    filtered_restrictions: dict[str, list[tuple[str, str]]] = {}
    for domain, pairs in restrictions_by_domain.items():
        if domain not in visible_classes:
            continue
        kept_pairs = [
            (prop, rng)
            for prop, rng in pairs
            if prop in visible_properties and rng in visible_classes
        ]
        if kept_pairs:
            filtered_restrictions[domain] = kept_pairs

    return visible_classes, visible_properties, filtered_restrictions


def _format_role_label(base_label: str, roles: set[str]) -> str:
    if not roles or len(roles) <= 1:
        return base_label
    ordered_roles = [role for role in ('subject', 'predicate', 'object') if role in roles]
    if not ordered_roles:
        return base_label
    return f"{base_label} roles {' '.join(ordered_roles)}"


def serialize_graph_to_rdf_xml(graph: dict[str, Any]) -> str:
    facts = graph.get('facts', []) if isinstance(graph, dict) else []
    instance_facts = graph.get('instance_facts', []) if isinstance(graph, dict) else []
    subclass_facts = graph.get('subclass_facts', []) if isinstance(graph, dict) else []

    explicit_schema: dict[str, Any] = {}
    if isinstance(graph, dict):
        schema_from_graph = graph.get('schema')
        metadata = graph.get('metadata', {})
        schema_from_meta = metadata.get('schema') if isinstance(metadata, dict) else None
        if isinstance(schema_from_graph, dict):
            explicit_schema = schema_from_graph
        elif isinstance(schema_from_meta, dict):
            explicit_schema = schema_from_meta

    grouped: dict[str, list[tuple[str, str]]] = {}
    resource_roles: dict[str, set[str]] = {}
    subclass_relations: dict[str, set[str]] = {}

    schema_iri_case_map: dict[str, str] = {}
    for cls in explicit_schema.get('classes', []):
        if not isinstance(cls, dict):
            continue
        iri = _expand_curie_to_iri(str(cls.get('iri', '')).strip())
        if not iri.startswith(_ORION_NS):
            continue
        local = _local_name(iri).casefold()
        if local not in schema_iri_case_map:
            schema_iri_case_map[local] = iri

    def _canonical_orion_iri_for_output(raw_value: str, *, use_schema_case_map: bool = False) -> str:
        iri = _expand_curie_to_iri(raw_value)
        if not iri:
            return iri
        if iri.startswith(_ORION_NS):
            if use_schema_case_map:
                local = _local_name(iri).casefold()
                return schema_iri_case_map.get(local, _canonical_orion_resource_iri(iri))
            return _canonical_orion_resource_iri(iri)
        return iri

    def add(subject: str, predicate: str, obj: str) -> None:
        if not subject or not predicate or not obj:
            return
        s = _canonical_orion_iri_for_output(subject, use_schema_case_map=True)
        p = _canonical_orion_iri_for_output(predicate)
        o = _canonical_orion_iri_for_output(obj, use_schema_case_map=True)
        grouped.setdefault(s, []).append((p, o))

        if s:
            resource_roles.setdefault(s, set()).add('subject')
        if p:
            resource_roles.setdefault(p, set()).add('predicate')
        if o:
            resource_roles.setdefault(o, set()).add('object')

    reified_statements: list[dict[str, str]] = []

    for item in facts:
        if isinstance(item, dict):
            subject_raw = str(item.get('subject', ''))
            predicate_raw = str(item.get('predicate', ''))
            object_raw = str(item.get('object', ''))
            add(subject_raw, predicate_raw, object_raw)

            subject_iri = _canonical_orion_iri_for_output(subject_raw, use_schema_case_map=True)
            predicate_iri = _canonical_orion_iri_for_output(predicate_raw)
            object_iri = _canonical_orion_iri_for_output(object_raw, use_schema_case_map=True)
            if not subject_iri or not predicate_iri or not object_iri:
                continue

            statement = {
                'id': _statement_identity(subject_iri, predicate_iri, object_iri),
                'subject': subject_iri,
                'predicate': predicate_iri,
                'object': object_iri,
                'label': _statement_label(subject_iri, predicate_iri, object_iri),
            }

            if isinstance(item.get('evidence_span'), dict):
                start = item['evidence_span'].get('start_offset')
                end = item['evidence_span'].get('end_offset')
                if isinstance(start, int) and isinstance(end, int):
                    statement['span'] = f"{start}:{end}"

            confidence = item.get('confidence')
            if isinstance(confidence, (int, float)):
                statement['confidence'] = str(confidence)

            reified_statements.append(statement)
    for item in instance_facts:
        if isinstance(item, dict):
            add(str(item.get('subject', '')), _RDF_TYPE, str(item.get('object', '')))
    for item in subclass_facts:
        if isinstance(item, dict):
            subject = str(item.get('subject', ''))
            obj = str(item.get('object', ''))
            predicate = str(item.get('predicate', ''))
            if not subject or not obj:
                continue
            if _expand_curie_to_iri(predicate) != _expand_curie_to_iri(_RDFS_SUBCLASS):
                continue
            subject_iri = _canonical_orion_iri_for_output(subject, use_schema_case_map=True)
            object_iri = _canonical_orion_iri_for_output(obj, use_schema_case_map=True)
            if not subject_iri or not object_iri:
                continue
            subclass_relations.setdefault(subject_iri, set()).add(object_iri)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:meta="https://orion.local/meta/" xmlns:skos="http://www.w3.org/2004/02/skos/core#" xmlns:rs="http://www.w3.org/2000/01/rdf-schema#">',
        f'  <owl:Ontology rdf:about="{_ORION_NS.rstrip("/")}"/>',
    ]

    explicit_object_properties: list[dict[str, str]] = []
    for prop in explicit_schema.get('object_properties', []):
        if isinstance(prop, dict):
            explicit_object_properties.append(prop)
    if not explicit_object_properties and isinstance(graph, dict):
        for row in graph.get('object_property_schema', []):
            if not isinstance(row, dict):
                continue
            predicate = str(row.get('predicate', '')).strip()
            if not predicate:
                continue
            explicit_object_properties.append({
                'iri': predicate,
                'label': _resource_label_from_iri(_expand_curie_to_iri(predicate)),
                **({'domain': row.get('domain')} if row.get('domain') else {}),
                **({'range': row.get('range')} if row.get('range') else {}),
            })


    fact_direction_edges = set()
    for item in facts:
        if not isinstance(item, dict):
            continue
        subj = _canonical_orion_iri_for_output(str(item.get('subject', '')).strip(), use_schema_case_map=True)
        pred = _canonical_orion_iri_for_output(str(item.get('predicate', '')).strip())
        obj = _canonical_orion_iri_for_output(str(item.get('object', '')).strip(), use_schema_case_map=True)
        if subj and pred and obj:
            fact_direction_edges.add((subj, pred, obj))

    filtered_object_properties: list[dict[str, str]] = []
    domain_range_edges = set()
    for prop in explicit_object_properties:
        iri = _expand_curie_to_iri(str(prop.get('iri', '')).strip())
        domain = _canonical_orion_iri_for_output(str(prop.get('domain', '')).strip(), use_schema_case_map=True) if prop.get('domain') else ''
        range_iri = _canonical_orion_iri_for_output(str(prop.get('range', '')).strip(), use_schema_case_map=True) if prop.get('range') else ''
        if iri and domain and range_iri and (domain, iri, range_iri) in fact_direction_edges:
            row = dict(prop)
            row['domain'] = domain
            row['range'] = range_iri
            filtered_object_properties.append(row)
            domain_range_edges.add((domain, iri, range_iri))

    publishable_object_properties: list[dict[str, str]] = []
    by_property: dict[str, dict[str, Any]] = {}
    for row in filtered_object_properties:
        iri = _expand_curie_to_iri(str(row.get('iri', '')).strip())
        domain = _canonical_orion_iri_for_output(str(row.get('domain', '')).strip(), use_schema_case_map=True) if row.get('domain') else ''
        range_iri = _canonical_orion_iri_for_output(str(row.get('range', '')).strip(), use_schema_case_map=True) if row.get('range') else ''
        if not iri or not domain or not range_iri:
            continue
        rec = by_property.setdefault(iri, {'rows': [], 'domains': set(), 'ranges': set()})
        rec['rows'].append(row)
        rec['domains'].add(domain)
        rec['ranges'].add(range_iri)

    for iri, rec in by_property.items():
        if len(rec['domains']) == 1 and len(rec['ranges']) == 1:
            publishable_object_properties.append(rec['rows'][0])

    explicit_object_properties = publishable_object_properties

    restrictions_raw = graph.get('restrictions', []) if isinstance(graph, dict) else []
    restrictions_by_domain: dict[str, list[tuple[str, str]]] = {}
    for row in restrictions_raw:
        if not isinstance(row, dict):
            continue
        domain = _canonical_orion_iri_for_output(str(row.get('domain', '')).strip(), use_schema_case_map=True)
        prop = _canonical_orion_iri_for_output(str(row.get('property', '')).strip())
        range_iri = _canonical_orion_iri_for_output(str(row.get('range', '')).strip(), use_schema_case_map=True)
        if domain and prop and range_iri and (domain, prop, range_iri) in fact_direction_edges and (domain, prop, range_iri) not in domain_range_edges:
            restrictions_by_domain.setdefault(domain, []).append((prop, range_iri))

    class_rows: dict[str, str] = {}
    for cls in explicit_schema.get('classes', []):
        if not isinstance(cls, dict):
            continue
        iri = _canonical_orion_iri_for_output(str(cls.get('iri', '')), use_schema_case_map=True)
        if not iri:
            continue
        label = str(cls.get('label', '')).strip() or _resource_label_from_iri(iri)
        class_rows[iri] = label

    for domain_iri, pairs in restrictions_by_domain.items():
        domain_iri = _canonical_orion_resource_iri(domain_iri)
        if domain_iri not in class_rows:
            class_rows[domain_iri] = _resource_label_from_iri(domain_iri)
        for _, range_iri in pairs:
            range_iri = _canonical_orion_resource_iri(range_iri)
            if range_iri not in class_rows:
                class_rows[range_iri] = _resource_label_from_iri(range_iri)

    for subject_iri, objects in subclass_relations.items():
        subject = _canonical_orion_resource_iri(_expand_curie_to_iri(str(subject_iri).strip()))
        if subject and subject not in class_rows:
            class_rows[subject] = _resource_label_from_iri(subject)
        for object_iri in objects:
            parent = _canonical_orion_resource_iri(_expand_curie_to_iri(str(object_iri).strip()))
            if parent and parent not in class_rows:
                class_rows[parent] = _resource_label_from_iri(parent)

    visible_class_rows, visible_object_properties, filtered_restrictions_by_domain = _filter_isolated_owl_nodes(
        class_rows=class_rows,
        explicit_object_properties=explicit_object_properties,
        restrictions_by_domain=restrictions_by_domain,
        reified_statements=reified_statements,
        subclass_relations=subclass_relations,
    )

    class_iris = set(visible_class_rows)

    for iri in sorted(visible_class_rows):
        base_label = class_rows[iri]
        label = _format_role_label(base_label, resource_roles.get(iri, set()))
        lines.append(f'  <owl:Class rdf:about="{iri}">')
        lines.append(f'    <rdfs:label>{base_label}</rdfs:label>')
        if label != base_label:
            lines.append(f'    <rdfs:label>{label}</rdfs:label>')
        if iri in class_iris or iri in subclass_relations:
            for parent_iri in sorted(subclass_relations.get(iri, [])):
                parent = _canonical_orion_iri_for_output(str(parent_iri).strip(), use_schema_case_map=True)
                lines.append(f'    <rdfs:subClassOf rdf:resource="{parent}"/>')

        for pair in _dedupe_stable([{'p': p, 'r': r} for p, r in filtered_restrictions_by_domain.get(iri, [])], ('p', 'r')):
            prop, range_iri = pair['p'], pair['r']
            lines.append('    <rdfs:subClassOf>')
            lines.append('      <owl:Restriction>')
            lines.append(f'        <owl:onProperty rdf:resource="{prop}"/>')
            lines.append(f'        <owl:someValuesFrom rdf:resource="{range_iri}"/>')
            lines.append('      </owl:Restriction>')
            lines.append('    </rdfs:subClassOf>')
        lines.append('  </owl:Class>')

    described_object_property_iris = set()
    for prop in explicit_object_properties:
        if not isinstance(prop, dict):
            continue
        iri = _expand_curie_to_iri(str(prop.get('iri', '')))
        if iri not in visible_object_properties:
            continue
        if not iri:
            continue
        label = str(prop.get('label', '')).strip() or _resource_label_from_iri(iri)
        domain = _canonical_orion_iri_for_output(str(prop.get('domain', '')), use_schema_case_map=True) if prop.get('domain') else ''
        range_iri = _canonical_orion_iri_for_output(str(prop.get('range', '')), use_schema_case_map=True) if prop.get('range') else ''
        if not domain or not range_iri:
            continue
        lines.append(f'  <owl:ObjectProperty rdf:about="{iri}">')
        lines.append(f'    <rdfs:label>{label}</rdfs:label>')
        lines.append(f'    <rdfs:domain rdf:resource="{domain}"/>')
        lines.append(f'    <rdfs:range rdf:resource="{range_iri}"/>')
        lines.append('  </owl:ObjectProperty>')
        described_object_property_iris.add(iri)

    class_iris = set(visible_class_rows)

    for iri, label in class_rows.items():
        if iri in class_iris:
            continue
        if _is_type_super_node(iri):
            continue
        resource_roles.setdefault(iri, set()).add('class')

    description_nodes = set(resource_roles) | set(class_rows) | set(subclass_relations)

    for iri in sorted(description_nodes):
        roles = resource_roles.get(iri, set())
        if iri in described_object_property_iris and iri not in class_iris and iri not in subclass_relations:
            continue
        if _is_type_super_node(iri):
            continue

        base_label = class_rows.get(iri, '') or _resource_label_from_iri(iri)
        contextual_label = _format_role_label(base_label, roles)
        lines.append(f'  <rdf:Description rdf:about="{iri}">')
        if base_label:
            lines.append(f'    <rdfs:label>{base_label}</rdfs:label>')
        if contextual_label and contextual_label != base_label:
            lines.append(f'    <rdfs:label>{contextual_label}</rdfs:label>')
        if iri in class_iris or iri in subclass_relations:
            for parent_iri in sorted(subclass_relations.get(iri, [])):
                parent = _canonical_orion_iri_for_output(str(parent_iri).strip(), use_schema_case_map=True)
                lines.append(f'    <rs:subClassOf rdf:resource="{parent}"/>')
        lines.append('  </rdf:Description>')

    visual_relation_type_iri = f"{_ORION_NS}ReifiedRelation"
    for statement in _dedupe_stable(reified_statements, ('id', 'subject', 'predicate', 'object', 'label', 'span', 'confidence')):
        lines.append(f'  <rdf:Statement rdf:about="{statement["id"]}">')
        lines.append(f'    <{_RDF_XML_TYPE_TAG} rdf:resource="{visual_relation_type_iri}"/>')
        lines.append(f'    <rdfs:label>{statement["label"]}</rdfs:label>')
        lines.append(f'    <skos:prefLabel>{statement["label"]}</skos:prefLabel>')
        lines.append(f'    <rdfs:comment>{statement["label"]}</rdfs:comment>')
        lines.append(f'    <rdf:subject rdf:resource="{statement["subject"]}"/>')
        lines.append(f'    <rdf:predicate rdf:resource="{statement["predicate"]}"/>')
        lines.append(f'    <rdf:object rdf:resource="{statement["object"]}"/>')
        if statement.get('span'):
            lines.append(f'    <meta:span>{statement["span"]}</meta:span>')
        if statement.get('confidence'):
            lines.append(f'    <meta:confidence>{statement["confidence"]}</meta:confidence>')
        lines.append('  </rdf:Statement>')

    lines.append('</rdf:RDF>')
    return '\n'.join(lines) + '\n'




def _is_type_super_node(value: str) -> bool:
    v = _normalize_text(value)
    return v in {'type', 'orion:type', f'{_ORION_NS}type'}


def _build_exclusion_set(payload: dict[str, Any], key: str) -> set[str]:
    report = payload.get('semantic_quality_report')
    values = []
    if isinstance(report, dict):
        values = report.get(key, [])
    if not values:
        values = payload.get(key, [])
    out: set[str] = set()
    if isinstance(values, list):
        for value in values:
            if isinstance(value, str) and value.strip():
                out.add(_normalize_text(value))
    return out


def _build_ref_label_lookup(payload: dict[str, Any]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for entity in payload.get('entities', []):
        if not isinstance(entity, dict):
            continue
        entity_id = entity.get('entity_id')
        if isinstance(entity_id, str) and entity_id:
            label = entity.get('normalized_text') or entity.get('text')
            normalized = _normalize_text(label if isinstance(label, str) else None)
            if normalized:
                lookup[entity_id] = normalized
    for concept in payload.get('concepts', []):
        if not isinstance(concept, dict):
            continue
        concept_id = concept.get('concept_id')
        if isinstance(concept_id, str) and concept_id:
            label = concept.get('normalized_text') or concept.get('lemma') or concept.get('text')
            normalized = _normalize_text(label if isinstance(label, str) else None)
            if normalized:
                lookup[concept_id] = normalized
    return lookup


def _is_poor_numeric_id(value: str) -> bool:
    return bool(re.fullmatch(r'\d+', value.strip()))


def _resolve_node_text(raw_value: str | None, ref_value: str | None, ref_lookup: dict[str, str]) -> str:
    direct = _normalize_text(raw_value)
    if direct in _BR_RELATIVE_PRONOUNS:
        if isinstance(ref_value, str) and ref_value:
            resolved = ref_lookup.get(ref_value, '')
            if resolved and resolved not in _BR_RELATIVE_PRONOUNS:
                return resolved
        return ''

    if direct and not _is_poor_numeric_id(direct):
        return direct

    if isinstance(ref_value, str) and ref_value:
        resolved = ref_lookup.get(ref_value, direct)
        if resolved not in _BR_RELATIVE_PRONOUNS:
            return resolved
    return ''


class RdfOutputStrategy:
    def __init__(
        self,
        base_iri: str | None = None,
        prefixes: dict[str, str] | None = None,
    ) -> None:
        self._namespace_mode = base_iri is not None or prefixes is not None
        if self._namespace_mode:
            resolved_base_iri = validate_base_iri(base_iri or _ORION_NS)
            self._base_iri = resolved_base_iri
            self._prefixes = validate_and_resolve_prefixes(resolved_base_iri, prefixes)
        else:
            self._base_iri = ''
            self._prefixes = {}

    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        facts: list[dict[str, str]] = []
        excluded_entities = _build_exclusion_set(payload, 'excluded_entities')
        excluded_concepts = _build_exclusion_set(payload, 'excluded_concepts')
        ref_lookup = _build_ref_label_lookup(payload)

        for triple in payload.get('triples', []):
            if not isinstance(triple, dict):
                continue
            if self._namespace_mode:
                subject_text = _resolve_node_text(triple.get('subject'), triple.get('subject_ref'), ref_lookup)
                object_text = _resolve_node_text(triple.get('object'), triple.get('object_ref'), ref_lookup)
                if _normalize_text(object_text) == 'type':
                    continue
                subject = make_iri(subject_text, kind='individual', base_iri=self._base_iri)
                predicate = compact_iri(make_iri(triple.get('predicate', ''), kind='predicate', base_iri=self._base_iri), self._prefixes)
                obj = make_iri(object_text, kind='individual', base_iri=self._base_iri)
            else:
                subject = _normalize_text(triple.get('subject'))
                predicate = _normalize_predicate(triple.get('predicate'))
                object_text = _normalize_text(triple.get('object'))
                if object_text == 'type':
                    continue
                obj = object_text
            if not subject or not predicate or not obj:
                continue
            if _normalize_text(subject) in excluded_entities or _normalize_text(obj) in excluded_entities:
                continue
            if _normalize_text(subject) in excluded_concepts or _normalize_text(obj) in excluded_concepts:
                continue
            facts.append({'subject': subject, 'predicate': predicate, 'object': obj, **({'evidence_span': triple.get('evidence_span')} if isinstance(triple.get('evidence_span'), dict) else {}), **({'confidence': triple.get('confidence')} if isinstance(triple.get('confidence'), (int, float)) else {})})

        instance_facts: list[dict[str, str]] = []
        for assertion in payload.get('type_assertions', []):
            if not isinstance(assertion, dict):
                continue
            if self._namespace_mode:
                subject = make_iri(assertion.get('entity') or assertion.get('instance') or '', kind='individual', base_iri=self._base_iri)
                obj = compact_iri(make_iri(assertion.get('type') or assertion.get('class') or '', kind='class', base_iri=self._base_iri), self._prefixes)
            else:
                subject = _normalize_text(assertion.get('entity') or assertion.get('instance'))
                obj = _normalize_text(assertion.get('type') or assertion.get('class'))
            if subject and obj:
                instance_facts.append({'subject': subject, 'predicate': _RDF_TYPE, 'object': obj})

        subclass_facts: list[dict[str, str]] = []
        for relation in payload.get('taxonomy_relations', []):
            if not isinstance(relation, dict):
                continue
            relation_child = relation.get('child') or relation.get('subclass') or ''
            relation_parent = relation.get('parent') or relation.get('superclass') or ''
            if _is_type_super_node(str(relation_parent)):
                continue
            if self._namespace_mode:
                subject = compact_iri(make_iri(relation_child, kind='class', base_iri=self._base_iri), self._prefixes)
                obj = compact_iri(make_iri(relation_parent, kind='class', base_iri=self._base_iri), self._prefixes)
            else:
                subject = _normalize_text(relation_child)
                obj = _normalize_text(relation_parent)
            if _is_type_super_node(str(obj)):
                continue
            if subject and obj:
                subclass_facts.append({'subject': subject, 'predicate': _RDFS_SUBCLASS, 'object': obj})

        facts = _dedupe_stable(facts, ('subject', 'predicate', 'object'))
        instance_facts = _dedupe_stable(instance_facts, ('subject', 'predicate', 'object'))
        subclass_facts = _dedupe_stable(subclass_facts, ('subject', 'predicate', 'object'))
        bootstrap_class_nodes = _collect_bootstrap_class_nodes(
            payload,
            base_iri=self._base_iri,
            namespace_mode=self._namespace_mode,
        )
        classes, type_assertions, object_property_schema, restrictions, schema = _build_explicit_owl_schema(
            facts,
            instance_facts,
            subclass_facts,
            bootstrap_class_nodes=bootstrap_class_nodes,
        )

        result = {k: v for k, v in payload.items() if not k.startswith('_spacy')}
        result['output'] = {
            'strategy': 'rdf',
            'format': 'rdf',
            'graph': {
                'facts': facts,
                'instance_facts': instance_facts,
                'type_assertions': type_assertions,
                'subclass_facts': subclass_facts,
                'classes': classes,
                'object_property_schema': object_property_schema,
                'restrictions': restrictions,
                'schema': schema,
            },
            'metadata': payload.get('metadata', {}),
        }
        return result
