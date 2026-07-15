"""Project semantic claims into RDF graph data and deterministic RDF/XML."""

from __future__ import annotations

import hashlib
import re
from html import escape as _xml_escape
from typing import Any

from .namespace import compact_iri, make_iri, validate_and_resolve_prefixes, validate_base_iri
from .rules.explicit_svo_projection import explicit_svo_entity_labels_from_evidence


_ORION_NS = 'https://orion.local/resource/'
_RDF_TYPE = 'rdf' + ':type'
_RDFS_SUBCLASS = 'rdfs' + ':subClassOf'
_BR_RELATIVE_PRONOUNS = {'that', 'which', 'who'}
_BR_PERSONAL_PRONOUNS = {'he', 'she', 'they', 'it', 'we', 'his', 'her', 'their', 'its', 'them'}
_BR_LEADING_CONTEXT_CONNECTORS = ('From', 'To', 'At', 'In', 'On', 'During', 'After', 'Before')
_TAXONOMY_SCAFFOLD_HEADS = {'type', 'kind', 'category', 'form'}
_PHRASE_ARTICLES = {'a', 'an', 'the', 'any', 'each', 'one', 'more'}
_BR_DEFINITION_ONLY_PARENT_HEADS = {'document', 'model', 'set', 'control', 'controls'}


def _normalize_text(value: str | None) -> str:
    """Normalize text."""
    return (value or '').strip().casefold()


def _singularize_token(token: str) -> str:
    """Apply the deterministic, suffix-based singularization rules to one token."""
    if len(token) > 3 and token.endswith('ies'):
        return token[:-3] + 'y'
    if len(token) > 4 and token.endswith(('ses', 'xes', 'zes', 'ches', 'shes')):
        return token[:-2]
    if len(token) > 3 and token.endswith('s') and not token.endswith(('ss', 'us', 'is')):
        return token[:-1]
    return token


def _normalize_fact_phrase(value: str | None) -> str:
    """Normalize fact phrase."""
    normalized = re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value))
    if not normalized:
        return ''
    return ' '.join(_singularize_token(token) for token in normalized.split(' ') if token)


def _definition_only_parent_tokens(value: str | None) -> list[str]:
    """Split a potential definition-only parent into normalized tokens."""
    local = _local_name(_expand_curie_to_iri(str(value or ''))).strip()
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', local)
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    return [token for token in re.sub(r'[^a-z0-9]+', ' ', spaced.casefold()).split(' ') if token]


def _is_definition_only_parent_candidate(value: str | None) -> bool:
    """Return whether a multiword parent ends in a definition-only generic head."""
    tokens = _definition_only_parent_tokens(value)
    return len(tokens) >= 2 and tokens[-1] in _BR_DEFINITION_ONLY_PARENT_HEADS


def _normalize_predicate(value: str | None) -> str:
    """Normalize predicate."""
    normalized = _normalize_text(value)
    if not normalized:
        return ''
    return re.sub(r'[^a-z0-9]+', '_', normalized).strip('_')


def _expand_curie_to_iri(value: str) -> str:
    """Expand curie to IRI."""
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
    """Return the final path or fragment component of an IRI."""
    return value.rsplit('/', 1)[-1].rsplit('#', 1)[-1]


def _canonical_orion_resource_iri(value: str) -> str:
    """Return canonical ORION resource IRI."""
    if not value:
        return value
    if value.startswith(_ORION_NS):
        local = _local_name(value)
        if local:
            return f"{_ORION_NS}{local.lower()}"
    return value


def _canonical_orion_schema_iri(value: str) -> str:
    """Return canonical ORION schema IRI."""
    iri = _expand_curie_to_iri((value or '').strip())
    if iri.startswith(_ORION_NS):
        return _canonical_orion_resource_iri(iri)
    return iri


def _articleless_local_alias(local: str) -> str:
    """Return an IRI local-name alias with a leading article removed."""
    token = (local or '').strip()
    if not token:
        return ''

    parts = [part for part in re.split(r'[^a-zA-Z0-9]+', token) if part]
    if parts and parts[0].casefold() in _PHRASE_ARTICLES and len(parts) > 1:
        return ''.join(parts[1:])

    for article in ('the', 'an', 'a'):
        if len(token) <= len(article):
            continue
        if token[:len(article)].casefold() != article:
            continue
        remainder = token[len(article):]
        if remainder[:1].isupper():
            return remainder
    return ''


def _resource_label_from_iri(iri: str) -> str:
    """Derive a readable resource label from an IRI local name."""
    local = _local_name(iri).strip()
    if not local:
        return 'Resource'
    if local.islower():
        parts = [part for part in re.split(r'[^a-zA-Z0-9]+', local) if part]
        if parts:
            return ''.join(part[:1].upper() + part[1:] for part in parts)
    return local



def _dedupe_stable(items: list[dict[str, str]], key_fields: tuple[str, ...]) -> list[dict[str, str]]:
    """Deduplicate graph rows by selected fields while preserving encounter order."""
    seen: set[tuple[str, ...]] = set()
    unique: list[dict[str, str]] = []
    for item in items:
        key = tuple(item.get(field, '') for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique



def _schema_object_property_row(item: dict[str, Any]) -> dict[str, Any]:
    """Convert internal property-schema data to its public row representation."""
    row = {
        'iri': item['predicate'],
        'label': _resource_label_from_iri(_expand_curie_to_iri(item['predicate'])),
    }
    if item.get('domain'):
        row['domain'] = item['domain']
    if item.get('range'):
        row['range'] = item['range']
    if item.get('observed_domains'):
        row['observed_domains'] = list(item['observed_domains'])
    if item.get('observed_ranges'):
        row['observed_ranges'] = list(item['observed_ranges'])
    if item.get('scoped_domains'):
        row['scoped_domains'] = list(item['scoped_domains'])
    if item.get('scoped_ranges'):
        row['scoped_ranges'] = list(item['scoped_ranges'])
    if item.get('observed_pairs'):
        row['observed_pairs'] = list(item['observed_pairs'])
    if item.get('scoped_pairs'):
        row['scoped_pairs'] = list(item['scoped_pairs'])
    if item.get('semantics'):
        row['semantics'] = item['semantics']
    if item.get('projection_scope'):
        row['projection_scope'] = item['projection_scope']
    return row


def _dedupe_string_values(values: list[str]) -> list[str]:
    """Deduplicate string values while preserving deterministic order."""
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


class _CountedList(list):
    """List whose reported length may include serialized subclass expressions."""
    def __init__(self, items: list[dict[str, str]], count: int | None = None) -> None:
        """Initialize the _CountedList."""
        super().__init__(items)
        self._count = len(items) if count is None else count

    def __len__(self) -> int:
        """Return the externally reported count rather than the stored item count."""
        return self._count


def _is_taxonomy_scaffold(value: str | None) -> bool:
    """Return whether a label is a type, kind, category, or form-of scaffold."""
    normalized = _normalize_text(value)
    if not normalized:
        return False
    tokens = [token for token in re.sub(r'[^a-z0-9]+', ' ', normalized).split(' ') if token]
    while tokens and tokens[0] in _PHRASE_ARTICLES:
        tokens.pop(0)
    return len(tokens) >= 3 and tokens[0] in _TAXONOMY_SCAFFOLD_HEADS and tokens[1] == 'of'


_FORBIDDEN_LOCAL_VALUES = {'a', 'an', 'the', 'any', 'each', 'one', 'one-or-more', 'that', 'which', 'who', 'whom', 'whose', 'be'}
_RELATION_PREDICATE_IRI_ALIASES = {
    'access': 'accesses',
    'include': 'includes',
    'exploit': 'exploits',
    'reduce': 'reduces',
    'affect': 'affects',
}

_RELATION_SCHEMA_OVERRIDES = {
    'accesses': ('user', 'information-system'),
    'includes': ('role', 'permission'),
    'exploits': ('threat', 'vulnerability'),
    'reduces': ('security-control', 'risk'),
    'affects': ('security-incident', 'information-asset'),
}



_GENERIC_RELATIVE_CLAUSE = re.compile(r'\b(?:that|which|who)\b.*$')
_GENERIC_DEFINITION_TAIL = re.compile(r'\b(?:focused|designed|intended|used)\b.*$')


def _generic_sentence_texts(payload: dict[str, Any]) -> list[str]:
    """Collect non-empty sentence text from a payload."""
    sentences = payload.get('sentences', [])
    texts: list[str] = []
    for item in sentences:
        if isinstance(item, dict):
            raw = str(item.get('text', '')).strip()
            if raw:
                texts.append(raw)
    return texts


def _strip_determiners(value: str) -> str:
    """Remove determiners."""
    tokens = [token for token in re.sub(r'[^a-z0-9]+', ' ', _normalize_text(value)).split() if token]
    while tokens and tokens[0] in _PHRASE_ARTICLES:
        tokens.pop(0)
    return ' '.join(tokens)


def _generic_class_phrase(value: str | None, *, strip_for: bool = True) -> str:
    """Normalize a bounded generic class phrase and remove clause tails."""
    phrase = _strip_determiners(value or '')
    phrase = _GENERIC_RELATIVE_CLAUSE.sub('', phrase).strip()
    phrase = _GENERIC_DEFINITION_TAIL.sub('', phrase).strip()
    if strip_for and ' for ' in phrase:
        phrase = phrase.split(' for ', 1)[0].strip()
    return ' '.join(_singularize_token(token) for token in phrase.split())


def _generic_object_phrase(value: str | None) -> str:
    """Normalize a generic object phrase and remove unsupported qualifiers."""
    phrase = _strip_determiners(value or '')
    phrase = re.sub(r'\bonly\b.*$', '', phrase).strip()
    return ' '.join(_singularize_token(token) for token in phrase.split())


def _generic_split_list(value: str | None) -> list[str]:
    """Split a generic coordinated list into normalized class phrases."""
    raw = _normalize_text(value or '').replace(';', ',')
    raw = re.sub(r'\b(?:and|or)\b', ',', raw)
    return [_generic_class_phrase(part) for part in raw.split(',') if _generic_class_phrase(part)]


def _generic_iri(local: str, base_iri: str, namespace_mode: bool) -> str:
    """Create a generic class IRI in namespaced mode or return the local label."""
    return compact_iri(make_iri(local, kind='class', base_iri=base_iri), {'orion': _ORION_NS}) if namespace_mode else local


def _generic_predicate_iri(local: str, base_iri: str, namespace_mode: bool) -> str:
    """Create a generic predicate IRI in namespaced mode or return the local label."""
    return compact_iri(make_iri(local, kind='predicate', base_iri=base_iri), {'orion': _ORION_NS}) if namespace_mode else local


def _spaced_label(value: str | None) -> str:
    """Insert word boundaries into camel-case, underscored, or hyphenated labels."""
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', str(value or ''))
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text).replace('_', ' ').replace('-', ' ')
    return re.sub(r'\s+', ' ', text).strip()


def _claim_resource_iri(value: str, base_iri: str, namespace_mode: bool) -> str:
    """Create a class IRI for a semantic claim endpoint."""
    return _generic_iri(_spaced_label(value), base_iri, namespace_mode)


def _claim_individual_iri(value: str, base_iri: str, namespace_mode: bool) -> str:
    """Create an individual IRI for an endpoint introduced inside an example."""
    label = _spaced_label(value)
    if namespace_mode:
        return compact_iri(make_iri(label, kind='individual', base_iri=base_iri), {'orion': _ORION_NS})
    return re.sub(r'[^a-z0-9]+', '-', label.casefold()).strip('-')


def _claim_observation_iri(value: str, base_iri: str, namespace_mode: bool) -> str:
    """Create an IRI for an example participant while preserving named occurrence identity."""
    if _spaced_label(value).casefold().endswith(' occurrence'):
        return _claim_resource_iri(value, base_iri, namespace_mode)
    return _claim_individual_iri(value, base_iri, namespace_mode)


def _predicate_local_name(value: str) -> str:
    """Convert a predicate label to a lower-camel-case local name."""
    parts = [part for part in re.split(r'[^A-Za-z0-9]+', _spaced_label(value)) if part]
    if not parts:
        return ''
    head, *tail = [part.casefold() for part in parts]
    return head + ''.join(part.capitalize() for part in tail)




def _claim_predicate_iri(value: str, base_iri: str, namespace_mode: bool) -> str:
    """Create the predicate identifier used to project a semantic claim."""
    local = _predicate_local_name(str(value or '').strip())
    if namespace_mode:
        return compact_iri(f'{base_iri}{local}' if local else '', {'orion': _ORION_NS})
    return local


def _build_canonical_claims_graph(payload: dict[str, Any], base_iri: str, namespace_mode: bool) -> dict[str, Any] | None:
    """Build canonical claims graph."""
    artifact = payload.get('semantic_claims') if isinstance(payload.get('semantic_claims'), dict) else payload.get('canonical_claims')
    source_stage = str(artifact.get('stage', 'semantic_claims')) if isinstance(artifact, dict) else 'semantic_claims'
    claims = artifact.get('claims', []) if isinstance(artifact, dict) else []
    if not isinstance(claims, list) or not claims:
        return None

    classes: dict[str, dict[str, Any]] = {}
    subclass_relations: set[tuple[str, str]] = set()
    properties: set[tuple[str, str, str]] = set()
    declared_properties: set[str] = set()
    observational_properties: set[str] = set()
    non_observational_properties: set[str] = set()
    scoped_signatures: dict[str, dict[str, set[str]]] = {}
    scoped_pairs: dict[str, set[tuple[str, str]]] = {}
    facts: list[dict[str, str]] = []
    instance_facts: list[dict[str, str]] = []
    type_assertions: list[dict[str, str]] = []
    parent_by_child: dict[str, str] = {}
    pending_properties: list[tuple[str, str, str, str, str]] = []
    subclass_outputs: dict[str, tuple[str, str]] = {}
    claim_dispositions: dict[str, dict[str, Any]] = {}
    logical_alternatives: dict[str, dict[str, Any]] = {}
    scoped_relations: list[dict[str, Any]] = []
    quality_report = payload.get('semantic_quality_report') if isinstance(payload.get('semantic_quality_report'), dict) else {}
    invalid_projection_claim_ids = {
        str(item) for item in quality_report.get('invalid_projection_claim_ids', []) if str(item)
    }

    def set_disposition(claim_id: str, status: str, **details: Any) -> None:
        """Record the latest projection disposition for a claim."""
        if claim_id:
            claim_dispositions[claim_id] = {'claim_id': claim_id, 'status': status, **details}

    def add_class(label: str, comment: str | None = None) -> str:
        """Add a non-noisy class to the graph under construction and return its identifier."""
        iri = _claim_resource_iri(label, base_iri, namespace_mode)
        if not iri or _is_noisy_resource(iri):
            return ''
        row = classes.setdefault(iri, {'iri': iri, 'label': _resource_label_from_iri(_expand_curie_to_iri(iri))})
        if comment:
            row.setdefault('comments', [])
            if comment not in row['comments']:
                row['comments'].append(comment)
        return iri

    def add_subclass(child: str, parent: str, comment: str | None = None) -> tuple[str, str] | None:
        """Add a non-reflexive subclass relation between valid classes."""
        child_iri = add_class(child, None if parent.endswith('Model') else comment)
        parent_iri = add_class(parent, comment if parent.endswith('Model') else None)
        if child_iri and parent_iri and child_iri != parent_iri:
            pair = (child_iri, parent_iri)
            subclass_relations.add(pair)
            parent_by_child[child] = parent
            return pair
        return None

    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = str(claim.get('claim_id', '')).strip()
        if claim_id in invalid_projection_claim_ids:
            set_disposition(claim_id, 'excluded', reason='semantic_quality_rejected')
            continue
        if _is_internal_unresolved_claim(claim):
            set_disposition(claim_id, 'excluded', reason='internal_or_unresolved')
            continue
        subject = str(claim.get('subject', '')).strip()
        obj = str(claim.get('object', '')).strip()
        predicate = str(claim.get('predicate', '')).strip()
        predicate_iri_for_scope = _claim_predicate_iri(predicate, base_iri, namespace_mode) if predicate else ''
        if predicate_iri_for_scope:
            scope_set = (
                observational_properties
                if str(claim.get('observation_scope', '')).casefold() == 'illustrative_example'
                else non_observational_properties
            )
            scope_set.add(predicate_iri_for_scope)
        evidence = ''
        source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
        if isinstance(source, dict):
            evidence = str(source.get('evidence', '')).strip()
        # BR-P043-SVO-001: explicit SVO list evidence must project each entity as its own class.
        for label in explicit_svo_entity_labels_from_evidence(evidence, _generic_class_phrase, _dedupe_string_values):
            add_class(label, evidence)
        if str(claim.get('projection_scope', '')).casefold() == 'evidence_only':
            set_disposition(claim_id, 'evidence_only', reason='lexical_evidence_not_projected')
            continue
        alternative_group = str(claim.get('alternative_group', '')).strip()
        # Disjunction cannot be asserted as several simultaneous RDF facts, so retain it as an auditable logical group.
        if alternative_group and str(claim.get('coordination', '')).casefold() == 'or' and predicate and subject and obj:
            illustrative_observation = str(claim.get('observation_scope', '')).casefold() == 'illustrative_example'
            subject_iri = (
                _claim_observation_iri(subject, base_iri, namespace_mode)
                if illustrative_observation else add_class(subject, evidence)
            )
            object_iri = (
                _claim_observation_iri(obj, base_iri, namespace_mode)
                if illustrative_observation else add_class(obj, evidence)
            )
            predicate_iri = _claim_predicate_iri(predicate, base_iri, namespace_mode)
            if predicate_iri:
                declared_properties.add(predicate_iri)
                signature = scoped_signatures.setdefault(predicate_iri, {'domains': set(), 'ranges': set()})
                signature['domains'].add(subject_iri)
                signature['ranges'].add(object_iri)
                scoped_pairs.setdefault(predicate_iri, set()).add((subject_iri, object_iri))
            group = logical_alternatives.setdefault(alternative_group, {
                'group_id': alternative_group,
                'operator': 'or',
                'alternatives': [],
                'source_evidence': evidence,
            })
            alternative = {
                'claim_id': claim_id,
                'subject': subject_iri,
                'predicate': predicate_iri,
                'object': object_iri,
                'modality': str(claim.get('modality', '')),
            }
            for qualifier in (
                'patient', 'condition', 'quantifier', 'voice', 'requirement', 'context',
                'relation_role', 'goal', 'means_group', 'target', 'condition_subject',
                'condition_predicate', 'condition_object', 'condition_modality', 'condition_polarity',
                'condition_voice', 'condition_temporality', 'temporal_relation', 'temporal_object',
                'source_term', 'semantic_scope', 'state', 'recipient', 'destination', 'instrument',
                'purpose', 'embedded_modality', 'capability', 'scope_from', 'scope_to',
                'metamodel', 'importance', 'discourse_resolution', 'candidate_subjects',
            ):
                if claim.get(qualifier) not in (None, ''):
                    value = str(claim[qualifier])
                    if qualifier in {
                        'patient', 'context', 'target', 'condition_subject', 'condition_object',
                        'temporal_object', 'recipient', 'destination', 'instrument', 'purpose',
                        'scope_from', 'scope_to',
                    }:
                        value = (
                            _claim_observation_iri(value, base_iri, namespace_mode)
                            if illustrative_observation else add_class(value, evidence)
                        ) or value
                    alternative[qualifier] = value
            group['alternatives'].append(alternative)
            set_disposition(claim_id, 'evidence_only', reason='represented_as_logical_disjunction')
        # Modal, conditional, temporal, and proposition-wrapper claims need scope metadata and are unsafe as bare facts.
        elif (
            claim.get('condition')
            or claim.get('scope')
            or claim.get('temporal_relation')
            or claim.get('polarity')
            or str(claim.get('projection_scope', '')).casefold() == 'scoped'
            or str(claim.get('relation_role', '')).casefold() in {
                'enabled_action', 'ensured_content', 'evaluated_content', 'proposition_wrapper',
                'purpose_content', 'represented_content',
            }
            or (
                str(claim.get('modality', '')).casefold() == 'must'
                and not predicate.casefold().startswith('must')
            )
            or str(claim.get('modality', '')).casefold() in {
                'can', 'cannot', 'may', 'might', 'should', 'possibility', 'probability',
                'potential', 'taught_action', 'capability', 'whether',
            }
            or (
                claim.get('remediation_rule') == 'A'
                and (
                    str(claim.get('modality', '')).casefold() in {'must', 'purpose', 'prevention'}
                    or str(claim.get('polarity', '')).casefold() == 'negative'
                )
            )
        ) and predicate and subject and obj:
            illustrative_observation = str(claim.get('observation_scope', '')).casefold() == 'illustrative_example'
            coordinated_subject = (
                str(claim.get('relation_role', '')).casefold() == 'coordinated_subject'
                and str(claim.get('coordination_scope', '')).casefold() == 'subject'
            )
            unresolved_attachment = str(claim.get('attachment_scope', '')).casefold() == 'unresolved'
            object_resource_kind = str(claim.get('object_resource_kind', '')).casefold()
            unresolved_object = object_resource_kind in {'anonymous_referent', 'unresolved_type_expression'}
            if illustrative_observation:
                subject_iri = _claim_observation_iri(subject, base_iri, namespace_mode)
                object_iri = _claim_observation_iri(obj, base_iri, namespace_mode)
            else:
                # A coordination group is a statement resource, not a source-defined ontology class.
                subject_iri = _claim_resource_iri(subject, base_iri, namespace_mode) if coordinated_subject else add_class(subject, evidence)
                if object_resource_kind == 'anonymous_referent':
                    object_iri = _claim_individual_iri(obj, base_iri, namespace_mode)
                elif object_resource_kind == 'unresolved_type_expression':
                    object_iri = _claim_resource_iri(obj, base_iri, namespace_mode)
                else:
                    object_iri = add_class(obj, evidence)
            predicate_iri = _claim_predicate_iri(predicate, base_iri, namespace_mode)
            if predicate_iri:
                declared_properties.add(predicate_iri)
                # Unresolved attachments and collective subjects do not establish a fixed schema pair.
                if not unresolved_attachment and not coordinated_subject and not unresolved_object:
                    signature = scoped_signatures.setdefault(predicate_iri, {'domains': set(), 'ranges': set()})
                    signature['domains'].add(subject_iri)
                    signature['ranges'].add(object_iri)
                    scoped_pairs.setdefault(predicate_iri, set()).add((subject_iri, object_iri))
            scoped = {
                'claim_id': claim_id,
                'subject': subject_iri,
                'predicate': predicate_iri,
                'object': object_iri,
                'semantics': 'scoped_relation',
                'source_evidence': evidence,
            }
            for qualifier in (
                'modality', 'patient', 'context', 'scope', 'proposition_group',
                'proposition_role', 'target', 'condition', 'condition_subject',
                'condition_predicate', 'condition_object', 'condition_modality', 'condition_polarity',
                'condition_voice', 'condition_temporality', 'temporal_relation', 'temporal_object',
                'event_predicate', 'relation_role', 'qualifier', 'qualifier_target',
                'content_group', 'manner', 'location',
                'location_relation', 'polarity', 'actor_variable', 'resource_variable',
                'condition_variable', 'actor', 'strictness', 'source_term', 'semantic_scope',
                'on_behalf_of', 'constraint', 'processing_state', 'state', 'observation_scope',
                'voice', 'quantifier', 'coordination', 'coordination_scope', 'members',
                'basis', 'evaluated_outcome', 'scope_relation', 'scope_owner',
                'scope_owner_relation', 'measurement_unit', 'expected_state', 'recipient',
                'destination', 'instrument', 'purpose', 'embedded_modality', 'capability',
                'scope_from', 'scope_to', 'metamodel', 'importance', 'discourse_resolution',
                'prevented_event', 'event_target', 'graph_format_alternatives',
                'graph_format_operator', 'graph_format_group', 'antecedent_scope',
                'rdf_projection', 'interpretation_status', 'attachment_scope',
                'candidate_subjects', 'candidate_interpretations', 'coordination_members',
                'object_resource_kind', 'object_quantification', 'filler_kind', 'filler_quantification',
            ):
                if claim.get(qualifier) not in (None, ''):
                    value = str(claim[qualifier])
                    if qualifier == 'members':
                        member_iris = [add_class(item.strip(), evidence) for item in value.split(',') if item.strip()]
                        value = [item for item in member_iris if item]
                    elif qualifier == 'scope':
                        if claim.get('scope_owner') or claim.get('scope_relation'):
                            value = add_class(value, evidence) or value
                        else:
                            value = _claim_resource_iri(value, base_iri, namespace_mode) or value
                    elif qualifier in {
                        'scope_owner', 'patient', 'context', 'target', 'qualifier_target',
                        'condition_subject', 'condition_object', 'temporal_object', 'location',
                        'recipient', 'destination', 'instrument', 'purpose', 'scope_from', 'scope_to',
                    }:
                        value = (
                            _claim_observation_iri(value, base_iri, namespace_mode)
                            if illustrative_observation
                            else add_class(value, evidence)
                        ) or value
                    scoped[qualifier] = value
            scoped_relations.append(scoped)
            if str(claim.get('rdf_projection', '')).casefold() == 'qualified_statement':
                set_disposition(
                    claim_id,
                    'evidence_only',
                    reason='represented_as_qualified_rdf_statement',
                    output_statement='rdf:Statement',
                )
            else:
                set_disposition(claim_id, 'evidence_only', reason='represented_as_scoped_relation')
        elif predicate == 'instance_of' and subject and obj:
            instance_iri = _claim_observation_iri(subject, base_iri, namespace_mode)
            class_iri = add_class(obj, evidence)
            if instance_iri and class_iri:
                instance_facts.append({'subject': instance_iri, 'predicate': _RDF_TYPE, 'object': class_iri})
                type_assertions.append({'entity': instance_iri, 'type': class_iri})
                set_disposition(claim_id, 'evidence_only', reason='represented_as_instance_type_assertion')
            else:
                set_disposition(claim_id, 'excluded', reason='invalid_instance_type_assertion')
        elif predicate in {'is_a', 'type_of'} and subject and obj:
            pair = add_subclass(subject, obj, evidence)
            if pair:
                subclass_outputs[claim_id] = pair
            else:
                set_disposition(claim_id, 'excluded', reason='invalid_or_noisy_subclass')
        elif predicate == 'forms' and subject and obj:
            members = [part for part in str(claim.get('members', '')).split(',') if part]
            domain = subject
            member_parents = {parent_by_child.get(member, '') for member in members}
            if len(member_parents) == 1 and next(iter(member_parents)):
                domain = next(iter(member_parents))
            add_class(obj, evidence)
            pending_properties.append(('forms', domain, obj, evidence, claim_id))
        elif predicate and subject and obj:
            kind = str(claim.get('kind', '')).strip()
            illustrative_observation = str(claim.get('observation_scope', '')).casefold() == 'illustrative_example'
            if not illustrative_observation and (predicate == 'models' or kind == 'relation'):
                add_class(subject, evidence)
            pending_properties.append((predicate, subject, obj, evidence, claim_id))
        else:
            set_disposition(claim_id, 'excluded', reason='missing_projection_spo')

    claim_by_id = {
        str(claim.get('claim_id')): claim
        for claim in claims
        if isinstance(claim, dict) and claim.get('claim_id')
    }
    for predicate, subject, obj, evidence, claim_id in pending_properties:
        claim = claim_by_id.get(claim_id, {})
        domain = subject
        range_label = obj
        if predicate in {'has_purpose_to_preserve', 'has_member'}:
            range_label = parent_by_child.get(obj, obj)
        if predicate in {'protects_against', 'focused_on_protecting_against'} and obj.endswith('Threat'):
            add_subclass(obj, 'Threat')
            range_label = 'Threat'
        prop_iri = _claim_predicate_iri(predicate, base_iri, namespace_mode)
        if prop_iri:
            declared_properties.add(prop_iri)
        illustrative_observation = str(claim.get('observation_scope', '')).casefold() == 'illustrative_example'
        # Examples keep their fact and observed signature but do not promote endpoints to globally declared classes.
        if illustrative_observation:
            domain_iri = _claim_observation_iri(domain, base_iri, namespace_mode)
            range_iri = _claim_observation_iri(range_label, base_iri, namespace_mode)
            object_iri = _claim_observation_iri(obj, base_iri, namespace_mode)
        else:
            domain_iri = add_class(domain)
            range_iri = add_class(range_label)
            object_iri = add_class(obj)
        if prop_iri and domain_iri and range_iri and object_iri:
            if illustrative_observation:
                signature = scoped_signatures.setdefault(prop_iri, {'domains': set(), 'ranges': set()})
                signature['domains'].add(domain_iri)
                signature['ranges'].add(range_iri)
            else:
                properties.add((prop_iri, domain_iri, range_iri))
            fact = {'subject': domain_iri, 'predicate': prop_iri, 'object': object_iri}
            if evidence:
                fact['source_evidence'] = evidence
            for qualifier in (
                'modality', 'patient', 'condition', 'coordination', 'quantifier', 'voice',
                'requirement', 'means', 'relation_role', 'goal', 'instrument_group',
                'qualifier', 'qualifier_target', 'context', 'scope', 'proposition_group',
                'proposition_role', 'target', 'means_group', 'condition_subject',
                'condition_predicate', 'condition_object', 'condition_modality',
                'condition_polarity', 'condition_voice', 'condition_temporality',
                'temporal_relation', 'temporal_object', 'topics', 'content_group',
                'manner', 'location', 'location_relation', 'context_of', 'event_predicate',
                'polarity', 'actor_variable', 'resource_variable', 'condition_variable',
                'actor', 'strictness', 'source_term', 'semantic_scope', 'on_behalf_of', 'constraint',
                'processing_state', 'observation_scope', 'state', 'measurement_unit', 'expected_state',
                'scope_relation', 'context_relation', 'beneficiary', 'participant_a', 'participant_b',
                'relation_scope', 'topic', 'hazards', 'prevented_event', 'event_target', 'channel',
                'recorded_event', 'states', 'basis', 'evaluated_outcome', 'graph_format_alternatives',
                'graph_format_operator', 'graph_format_group', 'antecedent_scope',
                'scope_owner', 'scope_owner_relation', 'coordination_scope', 'members',
                'recipient', 'destination', 'instrument', 'purpose', 'embedded_modality',
                'capability', 'scope_from', 'scope_to', 'metamodel', 'importance',
                'discourse_resolution', 'candidate_subjects',
            ):
                if claim.get(qualifier) not in (None, ''):
                    value = str(claim[qualifier])
                    if qualifier == 'topics':
                        topic_iris = [add_class(item.strip(), evidence) for item in value.split(',') if item.strip()]
                        value = [item for item in topic_iris if item]
                    elif qualifier in {
                        'patient', 'target', 'qualifier_target', 'scope', 'context',
                        'beneficiary', 'channel',
                        'condition_subject', 'condition_object', 'temporal_object', 'location',
                        'on_behalf_of', 'recipient', 'destination', 'instrument', 'purpose',
                        'scope_from', 'scope_to',
                    }:
                        value = (
                            _claim_observation_iri(value, base_iri, namespace_mode)
                            if illustrative_observation
                            else add_class(value, evidence)
                        ) or value
                    fact[qualifier] = value
            facts.append(fact)
            set_disposition(claim_id, 'materialized', output_spo={
                'subject': domain_iri,
                'predicate': prop_iri,
                'object': object_iri,
            })
        else:
            set_disposition(claim_id, 'excluded', reason='invalid_or_noisy_property')

    linked_class_iris = {iri for _, domain, range_ in properties for iri in (domain, range_)}
    children_by_parent: dict[str, set[str]] = {}
    for child_iri, parent_iri in subclass_relations:
        children_by_parent.setdefault(parent_iri, set()).add(child_iri)
    definition_only_parents: set[str] = set()
    if definition_only_parents:
        subclass_relations = {
            (child_iri, parent_iri)
            for child_iri, parent_iri in subclass_relations
            if parent_iri not in definition_only_parents
        }
        for parent_iri in definition_only_parents:
            classes.pop(parent_iri, None)

    for claim_id, (child_iri, parent_iri) in subclass_outputs.items():
        if (child_iri, parent_iri) in subclass_relations:
            set_disposition(claim_id, 'materialized', output_spo={
                'subject': child_iri,
                'predicate': _RDFS_SUBCLASS,
                'object': parent_iri,
            })
        else:
            set_disposition(claim_id, 'evidence_only', reason='definition_only_alias')
    for claim in claims:
        if not isinstance(claim, dict) or not claim.get('claim_id'):
            continue
        claim_id = str(claim['claim_id'])
        if claim_id not in claim_dispositions:
            set_disposition(claim_id, 'excluded', reason='not_materialized')

    if not (classes or facts or instance_facts or scoped_relations or logical_alternatives):
        return None
    class_rows = sorted(classes.values(), key=lambda item: item['iri'])
    subclass_facts = [
        {'subject': child, 'predicate': _RDFS_SUBCLASS, 'object': parent}
        for child, parent in sorted(subclass_relations)
    ]
    property_usages = [
        {
            'predicate': predicate,
            'domain': domain,
            'range': range_,
            'semantics': 'observed_usage',
        }
        for predicate, domain, range_ in sorted(properties)
    ]
    signatures: dict[str, dict[str, set[str]]] = {}
    for item in property_usages:
        signature = signatures.setdefault(item['predicate'], {'domains': set(), 'ranges': set()})
        signature['domains'].add(item['domain'])
        signature['ranges'].add(item['range'])
    object_property_schema: list[dict[str, Any]] = []
    for predicate in sorted(declared_properties | set(signatures)):
        domains = sorted(signatures.get(predicate, {}).get('domains', set()))
        ranges = sorted(signatures.get(predicate, {}).get('ranges', set()))
        scoped_domains = sorted(scoped_signatures.get(predicate, {}).get('domains', set()))
        scoped_ranges = sorted(scoped_signatures.get(predicate, {}).get('ranges', set()))
        observed_pairs = [
            {'domain': item['domain'], 'range': item['range']}
            for item in property_usages
            if item['predicate'] == predicate
        ]
        scoped_pair_rows = [
            {'domain': domain, 'range': range_}
            for domain, range_ in sorted(scoped_pairs.get(predicate, set()))
        ]
        row: dict[str, Any] = {
            'predicate': predicate,
            'observed_domains': domains,
            'observed_ranges': ranges,
            'scoped_domains': scoped_domains,
            'scoped_ranges': scoped_ranges,
            'observed_pairs': observed_pairs,
            'scoped_pairs': scoped_pair_rows,
            'semantics': 'observed_usage' if domains and ranges else 'declared_from_scoped_claim',
        }
        if predicate in observational_properties and predicate not in non_observational_properties:
            row['projection_scope'] = 'illustrative_example'
        object_property_schema.append(row)
    schema = {
        'classes': class_rows,
        'object_properties': [
            _schema_object_property_row(item)
            for item in object_property_schema
        ],
    }
    return {
        'facts': _dedupe_stable(facts, ('subject', 'predicate', 'object', 'source_evidence')),
        'instance_facts': _dedupe_stable(instance_facts, ('subject', 'predicate', 'object')),
        'type_assertions': _dedupe_stable(type_assertions, ('entity', 'type')),
        'subclass_facts': subclass_facts,
        'classes': class_rows,
        'object_property_schema': object_property_schema,
        'object_property_facts': property_usages,
        'restrictions': [],
        'logical_alternatives': [logical_alternatives[key] for key in sorted(logical_alternatives)],
        'scoped_relations': _dedupe_stable(scoped_relations, ('claim_id', 'subject', 'predicate', 'object')),
        'schema': schema,
        'projection': {
            'source_stage': 'semantic_claims' if source_stage == 'semantic_claims' else source_stage,
            'claim_ids': [str(claim.get('claim_id')) for claim in claims if isinstance(claim, dict) and claim.get('claim_id')],
            'claim_dispositions': [
                claim_dispositions[str(claim['claim_id'])]
                for claim in claims
                if isinstance(claim, dict) and claim.get('claim_id') and str(claim['claim_id']) in claim_dispositions
            ],
            'materialized_claim_ids': [
                claim_id for claim_id, disposition in claim_dispositions.items()
                if disposition['status'] in {'materialized', 'transformed'}
            ],
            'excluded_claim_ids': [
                claim_id for claim_id, disposition in claim_dispositions.items()
                if disposition['status'] == 'excluded'
            ],
        },
    }


def _build_generic_sentence_graph(payload: dict[str, Any], base_iri: str, namespace_mode: bool) -> dict[str, Any] | None:
    """Build generic sentence graph."""
    classes: dict[str, dict[str, Any]] = {}
    subclasses: set[tuple[str, str]] = set()
    properties: set[tuple[str, str, str]] = set()

    def add_class(local: str, comment: str | None = None) -> str:
        """Add a non-noisy class to the graph under construction and return its identifier."""
        normalized = _generic_class_phrase(local)
        if not normalized or _is_noisy_resource(normalized):
            return ''
        iri = _generic_iri(normalized, base_iri, namespace_mode)
        row = classes.setdefault(iri, {'iri': iri, 'label': _resource_label_from_iri(_expand_curie_to_iri(iri))})
        if comment:
            row.setdefault('comments', [])
            if comment not in row['comments']:
                row['comments'].append(comment)
        return iri

    def add_subclass(child: str, parent: str) -> None:
        """Add a non-reflexive subclass relation between valid classes."""
        child_iri = add_class(child)
        parent_iri = add_class(parent)
        if child_iri and parent_iri and child_iri != parent_iri:
            subclasses.add((child_iri, parent_iri))

    def add_property(predicate: str, domain: str, range_: str) -> None:
        """Add a property signature when both endpoint classes are valid."""
        domain_iri = add_class(domain)
        range_iri = add_class(range_)
        if domain_iri and range_iri:
            properties.add((_generic_predicate_iri(predicate, base_iri, namespace_mode), domain_iri, range_iri))

    parent_by_child: dict[str, str] = {}
    pending_lists: list[tuple[list[str], str]] = []

    for sentence in _generic_sentence_texts(payload):
        clean = re.sub(r'\s+', ' ', sentence.strip())
        lower = clean.casefold()
        definition = re.match(r'^(?P<subject>.+?)\s+is\s+(?P<object>.+?)[\.]?$', lower)
        if definition:
            subject = _generic_class_phrase(definition.group('subject'))
            raw_object = definition.group('object').strip()
            type_match = re.match(r'^(?:a|an|the|any)?\s*(?:type|kind|category|form)\s+of\s+(?P<parent>.+)$', raw_object)
            parent_raw = type_match.group('parent') if type_match else raw_object
            parent = _generic_class_phrase(parent_raw)
            if parent:
                add_class(subject, clean)
                add_subclass(subject, parent)
                parent_by_child[subject] = parent
            if ' for ' in raw_object:
                target = _generic_class_phrase(raw_object.split(' for ', 1)[1], strip_for=False)
                if target:
                    add_property('models', subject, target)
            if ' against ' in raw_object:
                before, after = raw_object.split(' against ', 1)
                protected = re.sub(r'^.*?\bprotect(?:ing|s)?\b', '', before).strip()
                if protected:
                    add_property('protects', subject, protected)
                for threat in _generic_split_list(after):
                    if threat.endswith(' threat'):
                        add_subclass(threat, 'threat')
                    else:
                        add_class(threat)
                    add_property('protects-against', subject, 'threat' if 'threat' in threat else threat)
            value_for = re.search(r'\bhas\s+value\s+for\s+(?:an?|the)?\s+(?P<object>[a-z0-9 -]+)', raw_object)
            if value_for:
                add_property('has-value-for', parent or subject, value_for.group('object'))
            action_tail = re.search(r'\bthat\s+(?P<actions>.+)$', raw_object)
            if action_tail:
                for verb in ('stores', 'processes', 'transmits', 'represents'):
                    if re.search(rf'\b{verb}\b', action_tail.group('actions')):
                        add_property(verb, subject, 'information')
            ensure_access = re.search(r'ensures\s+(?P<object>.+?)\s+(?:is|are)\s+accessible\s+only\s+to\s+(?P<target>.+)$', raw_object)
            if ensure_access:
                add_property('ensures-accessible-to', subject, ensure_access.group('target'))
            ensure_accuracy = re.search(r'ensures\s+(?P<object>.+?)\s+(?:is|are)\s+accurate\b', raw_object)
            if ensure_accuracy:
                add_property('ensures-accuracy-of', subject, ensure_accuracy.group('object'))
            ensure_available = re.search(r'ensures\s+(?P<object>.+?)\s+(?:is|are)\s+accessible\s+when\s+needed', raw_object)
            if ensure_available:
                targets = _generic_split_list(ensure_available.group('object'))
                add_property('ensures-availability-of', subject, 'system' if 'system' in targets else (targets[-1] if targets else ensure_available.group('object')))
            continue

        form_match = re.match(r'^(?P<subjects>.+?)\s+form\s+(?P<object>.+?)[\.]?$', lower)
        if form_match:
            members = _generic_split_list(form_match.group('subjects'))
            target = _generic_class_phrase(form_match.group('object'))
            common_parent = ''
            parents = {parent_by_child.get(member, '') for member in members}
            if len(parents) == 1:
                common_parent = next(iter(parents))
            for member in members:
                add_class(member)
            add_class(target, clean)
            add_property('forms', common_parent or (members[0] if members else ''), target)
            continue

        purpose_match = re.match(r'^the\s+purpose\s+of\s+(?P<subject>.+?)\s+is\s+to\s+preserve\s+(?P<objects>.+?)[\.]?$', lower)
        if purpose_match:
            subject = _generic_class_phrase(purpose_match.group('subject'))
            members = _generic_split_list(purpose_match.group('objects'))
            parents = {parent_by_child.get(member, '') for member in members}
            common_parent = next(iter(parents)) if len(parents) == 1 else ''
            add_property('preserves', subject, common_parent or (members[0] if members else ''))

    if not classes:
        return None

    class_rows = sorted(classes.values(), key=lambda item: item['iri'])
    subclass_facts = [
        {'subject': child, 'predicate': _RDFS_SUBCLASS, 'object': parent}
        for child, parent in sorted(subclasses)
    ]
    object_property_schema = [
        {'predicate': predicate, 'domain': domain, 'range': range_}
        for predicate, domain, range_ in sorted(properties)
    ]
    restrictions = [
        {'domain': item['domain'], 'property': item['predicate'], 'range': item['range']}
        for item in object_property_schema
    ]
    schema = {
        'classes': class_rows,
        'object_properties': [
            _schema_object_property_row(item)
            for item in object_property_schema
        ],
    }
    return {
        'facts': [],
        'instance_facts': [],
        'type_assertions': [],
        'subclass_facts': subclass_facts,
        'classes': class_rows,
        'object_property_schema': object_property_schema,
        'restrictions': restrictions,
        'schema': schema,
    }


def _local_key(value: str) -> str:
    """Normalize an IRI local name into a comparison key."""
    expanded = _expand_curie_to_iri(str(value or '').strip())
    return re.sub(r'[^a-z0-9]+', '-', _local_name(expanded).casefold()).strip('-')


def _has_leading_context_connector(value: str | None) -> bool:
    """Return whether a resource label starts with a detached context connector."""
    local = _local_name(_expand_curie_to_iri(str(value or '').strip()))
    return any(local.startswith(prefix) and len(local) > len(prefix) and local[len(prefix)].isupper() for prefix in _BR_LEADING_CONTEXT_CONNECTORS)


def _resource_words(value: str | None) -> list[str]:
    """Split an IRI local name into readable resource words."""
    local = _local_name(_expand_curie_to_iri(str(value or '').strip()))
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', local)
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    return [token for token in re.sub(r'[^A-Za-z0-9]+', ' ', spaced).split() if token]


def _has_personal_pronoun_head(value: str | None) -> bool:
    """Return whether a resource label starts with a personal pronoun."""
    words = _resource_words(value)
    return bool(words and words[0].casefold() in _BR_PERSONAL_PRONOUNS)


def _is_internal_unresolved_claim(claim: dict[str, Any]) -> bool:
    """Return whether projection metadata marks a claim internal or unresolved."""
    resolution = str(claim.get('resolution_status') or claim.get('status') or '').casefold()
    visibility = str(claim.get('visibility') or claim.get('projection') or '').casefold()
    return resolution in {'unresolved', 'internal_unresolved'} or visibility in {'internal', 'hidden', 'not_visible'} or bool(claim.get('internal')) or bool(claim.get('unresolved'))


def _is_noisy_resource(value: str | None, *, allow_predicate: bool = False) -> bool:
    """Return whether a resource is empty, scaffold-like, pronominal, or otherwise unsafe to project."""
    local = _local_key(str(value or ''))
    if not local:
        return True
    if local in _FORBIDDEN_LOCAL_VALUES:
        return True
    if not allow_predicate and (_has_personal_pronoun_head(value) or _has_leading_context_connector(value)):
        return True
    if local.startswith('resource-that') or local.startswith(('type-of-', 'kind-of-', 'category-of-', 'form-of-')):
        return True
    if local.startswith(('typeof', 'kindof', 'categoryof', 'formof')):
        return True
    if not allow_predicate and any(fragment in local for fragment in ('potential-cause', 'possibility-that', 'process-of', 'consequence-produced')):
        return True
    return False


def _canonical_predicate_iri(value: str) -> str:
    """Return canonical predicate IRI."""
    iri = _expand_curie_to_iri(str(value or '').strip())
    if iri.startswith(_ORION_NS):
        local = _local_name(iri).casefold()
        local = _RELATION_PREDICATE_IRI_ALIASES.get(local, local)
        return f'{_ORION_NS}{local}'
    return iri


def _collect_bootstrap_class_nodes(payload: dict[str, Any], base_iri: str, namespace_mode: bool) -> list[str]:
    """Collect bootstrap class nodes."""
    bootstrap_nodes: list[str] = []
    for concept in payload.get('concepts', []):
        if not isinstance(concept, dict):
            continue
        raw_value = concept.get('normalized_text') or concept.get('lemma') or concept.get('text')
        normalized = _normalize_text(raw_value if isinstance(raw_value, str) else '')
        if not normalized:
            continue
        if normalized in _BR_RELATIVE_PRONOUNS or _is_poor_numeric_id(normalized) or _is_taxonomy_scaffold(normalized) or _is_noisy_resource(normalized):
            continue

        if namespace_mode:
            iri = make_iri(normalized, kind='class', base_iri=base_iri)
            if iri:
                bootstrap_nodes.append(iri)
        else:
            bootstrap_nodes.append(normalized)

    return _dedupe_string_values(bootstrap_nodes)


def _is_rdf_or_rdfs_predicate(value: str) -> bool:
    """Return whether a predicate belongs to the standard RDF or RDFS namespaces."""
    expanded = _expand_curie_to_iri(value)
    return expanded.startswith('http://www.w3.org/1999/02/22-rdf-syntax-ns#') or expanded.startswith('http://www.w3.org/2000/01/rdf-schema#')


def _build_explicit_owl_schema(
    facts: list[dict[str, str]],
    instance_facts: list[dict[str, str]],
    subclass_facts: list[dict[str, str]],
    bootstrap_class_nodes: list[str] | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    """Build explicit OWL schema."""
    classes_set: set[str] = set()

    for item in facts:
        subject = _canonical_orion_schema_iri(str(item.get('subject', '')).strip())
        obj = _canonical_orion_schema_iri(str(item.get('object', '')).strip())
        if subject and subject not in _BR_RELATIVE_PRONOUNS and not _is_noisy_resource(subject):
            classes_set.add(subject)
        if obj and obj not in _BR_RELATIVE_PRONOUNS and not _is_noisy_resource(obj):
            classes_set.add(obj)

    if bootstrap_class_nodes:
        for raw_node in bootstrap_class_nodes:
            node = str(raw_node).strip()
            if not node:
                continue
            node = _canonical_orion_schema_iri(node)
            if node and node not in _BR_RELATIVE_PRONOUNS:
                classes_set.add(node)

    resource_types: dict[str, str] = {}

    type_assertions: list[dict[str, str]] = []
    for item in instance_facts:
        subject = str(item.get('subject', '')).strip()
        obj = _canonical_orion_schema_iri(str(item.get('object', '')).strip())
        if not subject or not obj or _is_noisy_resource(subject) or _is_noisy_resource(obj):
            continue
        resource_types.setdefault(subject, obj)
        classes_set.add(obj)
        type_assertions.append({'entity': subject, 'type': obj})

    for item in subclass_facts:
        subject = _canonical_orion_schema_iri(str(item.get('subject', '')).strip())
        obj = _canonical_orion_schema_iri(str(item.get('object', '')).strip())
        if not subject or not obj or _is_noisy_resource(subject) or _is_noisy_resource(obj):
            continue
        classes_set.add(subject)
        classes_set.add(obj)

    classes = [{'iri': cls, 'label': _resource_label_from_iri(_expand_curie_to_iri(cls))} for cls in sorted(classes_set)]
    class_by_local_lower: dict[str, str] = {}
    suffix_candidates: dict[str, list[str]] = {}
    for cls in sorted(classes_set):
        local = _local_name(_expand_curie_to_iri(cls)).casefold()
        if local and local not in class_by_local_lower:
            class_by_local_lower[local] = cls
        parts = [part for part in re.split(r'[^a-z0-9]+', local) if part]
        if parts:
            suffix_candidates.setdefault(parts[-1], []).append(cls)
    for suffix, values in suffix_candidates.items():
        # Prefer the shortest deterministic class when a fact uses only the final noun of a longer label.
        ordered = sorted(set(values), key=lambda item: (len(_local_name(_expand_curie_to_iri(item))), _local_name(_expand_curie_to_iri(item))))
        if suffix not in class_by_local_lower and ordered:
            class_by_local_lower[suffix] = ordered[0]

    object_property_schema: list[dict[str, str]] = []
    restrictions: list[dict[str, str]] = []

    for fact in facts:
        predicate = _canonical_predicate_iri(str(fact.get('predicate', '')).strip())
        subject = str(fact.get('subject', '')).strip()
        obj = str(fact.get('object', '')).strip()
        if not predicate or not subject or not obj:
            continue
        if _is_noisy_resource(predicate, allow_predicate=True) or _is_noisy_resource(subject) or _is_noisy_resource(obj):
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

    present_predicates = {_local_key(row.get('predicate', '')) for row in object_property_schema}
    # Known core predicates use curated signatures; observed signatures for those names would overfit one sentence.
    object_property_schema = [row for row in object_property_schema if _local_key(row.get('predicate', '')) not in _RELATION_SCHEMA_OVERRIDES or _local_key(row.get('predicate', '')) not in present_predicates]
    for local_predicate, (domain_local, range_local) in _RELATION_SCHEMA_OVERRIDES.items():
        if local_predicate not in present_predicates:
            continue
        predicate_iri = f'{_ORION_NS}{local_predicate}'
        domain = class_by_local_lower.get(domain_local, f'{_ORION_NS}{domain_local}')
        range_iri = class_by_local_lower.get(range_local, f'{_ORION_NS}{range_local}')
        classes_set.add(domain)
        classes_set.add(range_iri)
        object_property_schema.append({'predicate': predicate_iri, 'domain': domain, 'range': range_iri})

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

    # OWL domain/range axioms are global; omit predicates observed with incompatible endpoint classes.
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
            _schema_object_property_row(item)
            for item in object_property_schema
        ],
    }

    return classes, type_assertions, object_property_schema, restrictions, schema


def _statement_identity(subject_iri: str, predicate_iri: str, object_iri: str, source_key: str = '') -> str:
    """Build a bounded deterministic IRI for a reified RDF statement."""
    def _slug(value: str, fallback: str) -> str:
        """Convert an IRI to a bounded statement-identifier component."""
        token = re.sub(r'[^a-z0-9]+', '-', _local_name(value).casefold()).strip('-')
        return token or fallback

    subj = _slug(subject_iri, 'subject')
    pred = _slug(predicate_iri, 'predicate')
    obj = _slug(object_iri, 'object')

    # Evidence distinguishes repeated SPO statements without embedding source text in the public IRI.
    source = re.sub(r'[^a-z0-9]+', '-', hashlib.sha1(source_key.encode('utf-8')).hexdigest()[:10]).strip('-') if source_key else ''
    base = f"{subj}-{pred}-{obj}" + (f"-{source}" if source else '')
    if len(base) <= 64:
        return f"{_ORION_NS}statement/{base}"

    compact = f"{subj[:14]}-{pred[:14]}-{obj[:14]}".strip('-')
    if source:
        compact = f"{compact}-{source}"
    if len(compact) > 64:
        compact = compact[:64].rstrip('-')
    return f"{_ORION_NS}statement/{compact or 'statement'}"


def _statement_label(subject_iri: str, predicate_iri: str, object_iri: str) -> str:
    """Build the readable subject-predicate-object label for a statement."""
    return f"{subject_iri} {predicate_iri} {object_iri}".strip()


def _filter_isolated_owl_nodes(
    class_rows: dict[str, str],
    explicit_object_properties: list[dict[str, str]],
    restrictions_by_domain: dict[str, list[tuple[str, str]]],
    reified_statements: list[dict[str, str]],
    subclass_relations: dict[str, set[str]],
) -> tuple[set[str], set[str], dict[str, list[tuple[str, str]]]]:
    """Filter isolated OWL nodes."""
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

    # Connectivity is computed on schema nodes only; statement resources serve solely as edges between them.
    edges: dict[str, set[str]] = {node: set() for node in candidate_nodes}

    def _add_edge(left: str, right: str) -> None:
        """Add an undirected edge only when both distinct endpoints are tracked."""
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
    """Format role label."""
    if not roles or len(roles) <= 1:
        return base_label
    ordered_roles = [role for role in ('subject', 'predicate', 'object') if role in roles]
    if not ordered_roles:
        return base_label
    return f"{base_label} roles {' '.join(ordered_roles)}"


def serialize_graph_to_rdf_xml(graph: dict[str, Any]) -> str:
    """Serialize the projected graph and explicit schema as deterministic RDF/XML."""
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
    raw_schema_iris: list[str] = []
    for cls in explicit_schema.get('classes', []):
        if not isinstance(cls, dict):
            continue
        iri = _expand_curie_to_iri(str(cls.get('iri', '')).strip())
        if not iri.startswith(_ORION_NS):
            continue
        raw_schema_iris.append(iri)
        local = _local_name(iri).casefold()
        if local not in schema_iri_case_map:
            schema_iri_case_map[local] = _canonical_orion_resource_iri(iri)

    for iri in raw_schema_iris:
        alias = _articleless_local_alias(_local_name(iri))
        if not alias:
            continue
        canonical = schema_iri_case_map.get(alias.casefold())
        if canonical:
            schema_iri_case_map[_local_name(iri).casefold()] = canonical

    def _canonical_orion_iri_for_output(raw_value: str, *, use_schema_case_map: bool = False) -> str:
        """Expand and canonicalize an ORION IRI for serialized output."""
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
        """Add a validated RDF statement and record resource roles."""
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
                'id': _statement_identity(subject_iri, predicate_iri, object_iri, str(item.get('source_evidence') or item.get('evidence') or '')),
                'subject': subject_iri,
                'predicate': predicate_iri,
                'object': object_iri,
                'label': _statement_label(subject_iri, predicate_iri, object_iri),
            }

            source_evidence = str(item.get('source_evidence') or item.get('evidence') or '').strip()
            if source_evidence:
                statement['evidence'] = source_evidence

            if isinstance(item.get('evidence_span'), dict):
                start = item['evidence_span'].get('start_offset')
                end = item['evidence_span'].get('end_offset')
                if isinstance(start, int) and isinstance(end, int):
                    statement['span'] = f"{start}:{end}"

            confidence = item.get('confidence')
            if isinstance(confidence, (int, float)):
                statement['confidence'] = str(confidence)

            reified_statements.append(statement)

    qualified_statements: list[dict[str, str]] = []
    for item in graph.get('scoped_relations', []) if isinstance(graph, dict) else []:
        if not isinstance(item, dict) or str(item.get('rdf_projection', '')).casefold() != 'qualified_statement':
            continue
        subject_iri = _canonical_orion_iri_for_output(str(item.get('subject', '')), use_schema_case_map=True)
        predicate_iri = _canonical_orion_iri_for_output(str(item.get('predicate', '')))
        object_iri = _canonical_orion_iri_for_output(str(item.get('object', '')), use_schema_case_map=True)
        if not subject_iri or not predicate_iri or not object_iri:
            continue
        source_key = str(item.get('claim_id') or item.get('source_evidence') or '')
        qualified = {
            'id': _statement_identity(subject_iri, predicate_iri, object_iri, source_key),
            'subject': subject_iri,
            'predicate': predicate_iri,
            'object': object_iri,
        }
        for key in (
            'claim_id', 'source_evidence', 'modality', 'quantifier', 'temporal_relation',
            'temporal_object', 'coordination', 'coordination_scope', 'members',
            'interpretation_status', 'attachment_scope', 'candidate_subjects',
            'candidate_interpretations', 'coordination_members', 'object_resource_kind',
            'object_quantification', 'filler_kind', 'filler_quantification', 'event_predicate',
            'expected_state', 'relation_role', 'measurement_unit', 'qualifier',
        ):
            if item.get(key) not in (None, ''):
                value = item[key]
                qualified[key] = ','.join(str(part) for part in value) if isinstance(value, list) else str(value)
        qualified_statements.append(qualified)
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


    subclass_fact_lookup: dict[str, set[str]] = {}
    for item in subclass_facts:
        if not isinstance(item, dict):
            continue
        subject_iri = _canonical_orion_iri_for_output(str(item.get('subject', '')).strip(), use_schema_case_map=True)
        object_iri = _canonical_orion_iri_for_output(str(item.get('object', '')).strip(), use_schema_case_map=True)
        if subject_iri and object_iri:
            subclass_fact_lookup.setdefault(subject_iri, set()).add(object_iri)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" '
        'xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" '
        'xmlns:owl="http://www.w3.org/2002/07/owl#" '
        'xmlns:orion="https://orion.local/resource/" '
        'xmlns:meta="https://orion.local/meta/" '
        'xmlns:skos="http://www.w3.org/2004/02/skos/core#" '
        'xmlns:rs="http://www.w3.org/2000/01/rdf-schema#">',
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
        if str(prop.get('projection_scope', '')).casefold() == 'illustrative_example':
            continue
        iri = _expand_curie_to_iri(str(prop.get('iri', '')).strip())
        domain = _canonical_orion_iri_for_output(str(prop.get('domain', '')).strip(), use_schema_case_map=True) if prop.get('domain') else ''
        range_iri = _canonical_orion_iri_for_output(str(prop.get('range', '')).strip(), use_schema_case_map=True) if prop.get('range') else ''
        if iri:
            row = dict(prop)
            if domain:
                row['domain'] = domain
            else:
                row.pop('domain', None)
            if range_iri:
                row['range'] = range_iri
            else:
                row.pop('range', None)
            filtered_object_properties.append(row)
            if domain and range_iri:
                domain_range_edges.add((domain, iri, range_iri))

    publishable_object_properties: list[dict[str, str]] = []
    by_property: dict[str, dict[str, Any]] = {}
    for row in filtered_object_properties:
        iri = _expand_curie_to_iri(str(row.get('iri', '')).strip())
        domain = _canonical_orion_iri_for_output(str(row.get('domain', '')).strip(), use_schema_case_map=True) if row.get('domain') else ''
        range_iri = _canonical_orion_iri_for_output(str(row.get('range', '')).strip(), use_schema_case_map=True) if row.get('range') else ''
        if not iri:
            continue
        rec = by_property.setdefault(iri, {'rows': [], 'domains': set(), 'ranges': set()})
        rec['rows'].append(row)
        if domain:
            rec['domains'].add(domain)
        if range_iri:
            rec['ranges'].add(range_iri)
        for observed_domain in row.get('observed_domains', []) if isinstance(row.get('observed_domains'), list) else []:
            canonical_domain = _canonical_orion_iri_for_output(str(observed_domain), use_schema_case_map=True)
            if canonical_domain:
                rec['domains'].add(canonical_domain)
        for observed_range in row.get('observed_ranges', []) if isinstance(row.get('observed_ranges'), list) else []:
            canonical_range = _canonical_orion_iri_for_output(str(observed_range), use_schema_case_map=True)
            if canonical_range:
                rec['ranges'].add(canonical_range)

    # "becomes" bridges state transitions and is unsafe as one global property when its signatures diverge.
    predicate_bridge_property_iris = {
        iri
        for iri, rec in by_property.items()
        if _local_name(iri).casefold() == 'becomes' and (len(rec['domains']) > 1 or len(rec['ranges']) > 1)
    }

    for iri, rec in by_property.items():
        if iri in predicate_bridge_property_iris:
            continue
        publishable_object_properties.extend(rec['rows'])

    explicit_object_properties = publishable_object_properties

    restrictions_raw = graph.get('restrictions', []) if isinstance(graph, dict) else []
    # Emit restrictions only for an observed fact direction and never duplicate an explicit domain/range axiom.
    restrictions_by_domain: dict[str, list[tuple[str, str]]] = {}
    for row in restrictions_raw:
        if not isinstance(row, dict):
            continue
        domain = _canonical_orion_iri_for_output(str(row.get('domain', '')).strip(), use_schema_case_map=True)
        prop = _canonical_orion_iri_for_output(str(row.get('property', '')).strip())
        range_iri = _canonical_orion_iri_for_output(str(row.get('range', '')).strip(), use_schema_case_map=True)
        if (
            domain and prop and range_iri
            and prop not in predicate_bridge_property_iris
            and (domain, prop, range_iri) in fact_direction_edges
            and (domain, prop, range_iri) not in domain_range_edges
        ):
            restrictions_by_domain.setdefault(domain, []).append((prop, range_iri))

    if predicate_bridge_property_iris:
        # Mixed transition signatures make inferred restrictions unreliable for the graph as a whole.
        restrictions_by_domain = {}

    class_rows: dict[str, str] = {}
    class_comments: dict[str, list[str]] = {}
    for cls in explicit_schema.get('classes', []):
        if not isinstance(cls, dict):
            continue
        iri = _canonical_orion_iri_for_output(str(cls.get('iri', '')), use_schema_case_map=True)
        if not iri:
            continue
        label = str(cls.get('label', '')).strip() or _resource_label_from_iri(iri)
        class_rows.setdefault(iri, label)
        raw_comments = cls.get('comments') or cls.get('comment') or cls.get('rdfs:comment') or []
        if isinstance(raw_comments, str):
            raw_comments = [raw_comments]
        for comment in raw_comments if isinstance(raw_comments, list) else []:
            text = str(comment).strip()
            if text and text not in class_comments.setdefault(iri, []):
                class_comments[iri].append(text)

    for domain_iri, pairs in restrictions_by_domain.items():
        domain_iri = _canonical_orion_iri_for_output(domain_iri, use_schema_case_map=True)
        if domain_iri not in class_rows:
            class_rows[domain_iri] = _resource_label_from_iri(domain_iri)
        for _, range_iri in pairs:
            range_iri = _canonical_orion_iri_for_output(range_iri, use_schema_case_map=True)
            if range_iri not in class_rows:
                class_rows[range_iri] = _resource_label_from_iri(range_iri)

    for subject_iri, objects in subclass_relations.items():
        subject = _canonical_orion_iri_for_output(str(subject_iri).strip(), use_schema_case_map=True)
        if subject and subject not in class_rows:
            class_rows[subject] = _resource_label_from_iri(subject)
        for object_iri in objects:
            parent = _canonical_orion_iri_for_output(str(object_iri).strip(), use_schema_case_map=True)
            if parent and parent not in class_rows:
                class_rows[parent] = _resource_label_from_iri(parent)

    normalized_class_rows: dict[str, str] = {}
    for iri, label in class_rows.items():
        canonical_iri = _canonical_orion_iri_for_output(iri, use_schema_case_map=True)
        if canonical_iri and canonical_iri not in normalized_class_rows:
            normalized_class_rows[canonical_iri] = label
        if canonical_iri and iri in class_comments:
            for comment in class_comments[iri]:
                if comment not in class_comments.setdefault(canonical_iri, []):
                    class_comments[canonical_iri].append(comment)
    class_rows = normalized_class_rows

    normalized_resource_roles: dict[str, set[str]] = {}
    for iri, roles in resource_roles.items():
        canonical_iri = _canonical_orion_iri_for_output(iri, use_schema_case_map=True)
        if not canonical_iri:
            continue
        normalized_resource_roles.setdefault(canonical_iri, set()).update(roles)
    resource_roles = normalized_resource_roles

    normalized_subclass_relations: dict[str, set[str]] = {}
    for subject_iri, objects in subclass_relations.items():
        canonical_subject = _canonical_orion_iri_for_output(subject_iri, use_schema_case_map=True)
        if not canonical_subject:
            continue
        normalized_subclass_relations.setdefault(canonical_subject, set()).update(
            _canonical_orion_iri_for_output(object_iri, use_schema_case_map=True)
            for object_iri in objects
            if _canonical_orion_iri_for_output(object_iri, use_schema_case_map=True)
        )
    subclass_relations = normalized_subclass_relations

    visible_class_rows, visible_object_properties, filtered_restrictions_by_domain = _filter_isolated_owl_nodes(
        class_rows=class_rows,
        explicit_object_properties=explicit_object_properties,
        restrictions_by_domain=restrictions_by_domain,
        reified_statements=reified_statements,
        subclass_relations=subclass_relations,
    )
    # Preserve all declared schema nodes for the observational contract; connectivity still filters restrictions.
    visible_class_rows = dict(class_rows)
    visible_object_properties = {
        _expand_curie_to_iri(str(prop.get('iri', '')).strip())
        for prop in explicit_object_properties
        if isinstance(prop, dict) and str(prop.get('iri', '')).strip()
    }

    class_iris = set(visible_class_rows)

    def _orion_predicate_xml_tag(predicate_iri: str) -> str:
        """Return a valid ORION XML element name for a predicate IRI."""
        if not predicate_iri.startswith(_ORION_NS):
            return ''
        local = _local_name(predicate_iri)
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_.-]*$', local):
            return ''
        return f'orion:{local}'

    direct_fact_descriptions: dict[str, list[tuple[str, str]]] = {}
    for subject, pairs in grouped.items():
        subject_iri = _canonical_orion_iri_for_output(subject, use_schema_case_map=True)
        if not subject_iri:
            continue
        for predicate, obj in pairs:
            predicate_iri = _canonical_orion_iri_for_output(predicate)
            object_iri = _canonical_orion_iri_for_output(obj, use_schema_case_map=True)
            tag = _orion_predicate_xml_tag(predicate_iri)
            if tag and object_iri:
                direct_fact_descriptions.setdefault(subject_iri, []).append((tag, object_iri))

    for subject_iri in sorted(direct_fact_descriptions):
        lines.append(f'  <rdf:Description rdf:about="{subject_iri}">')
        for row in _dedupe_stable(
            [{'predicate': predicate, 'object': object_iri} for predicate, object_iri in direct_fact_descriptions[subject_iri]],
            ('predicate', 'object'),
        ):
            lines.append(f'    <{row["predicate"]} rdf:resource="{row["object"]}"/>')
        lines.append('  </rdf:Description>')

    qualifier_tags = {
        'claim_id': 'claimId',
        'source_evidence': 'sourceEvidence',
        'temporal_relation': 'temporalRelation',
        'temporal_object': 'temporalObject',
        'coordination_scope': 'coordinationScope',
        'interpretation_status': 'interpretationStatus',
        'attachment_scope': 'attachmentScope',
        'candidate_subjects': 'candidateSubjects',
        'candidate_interpretations': 'candidateInterpretations',
        'coordination_members': 'coordinationMembers',
        'object_resource_kind': 'objectResourceKind',
        'object_quantification': 'objectQuantification',
        'filler_kind': 'fillerKind',
        'filler_quantification': 'fillerQuantification',
        'event_predicate': 'eventPredicate',
        'expected_state': 'expectedState',
        'relation_role': 'relationRole',
        'measurement_unit': 'measurementUnit',
    }
    for statement in sorted(qualified_statements, key=lambda item: item['id']):
        lines.append(f'  <rdf:Statement rdf:about="{statement["id"]}">')
        lines.append(f'    <rdf:subject rdf:resource="{statement["subject"]}"/>')
        lines.append(f'    <rdf:predicate rdf:resource="{statement["predicate"]}"/>')
        lines.append(f'    <rdf:object rdf:resource="{statement["object"]}"/>')
        for key in (
            'claim_id', 'source_evidence', 'modality', 'quantifier', 'temporal_relation',
            'temporal_object', 'coordination', 'coordination_scope', 'members',
            'interpretation_status', 'attachment_scope', 'candidate_subjects',
            'candidate_interpretations', 'coordination_members', 'object_resource_kind',
            'object_quantification', 'filler_kind', 'filler_quantification', 'event_predicate',
            'expected_state', 'relation_role', 'measurement_unit', 'qualifier',
        ):
            value = statement.get(key, '')
            if value:
                tag = qualifier_tags.get(key, key)
                lines.append(f'    <meta:{tag}>{_xml_escape(value)}</meta:{tag}>')
        lines.append('  </rdf:Statement>')

    for iri in sorted(visible_class_rows):
        base_label = class_rows[iri]
        label = _format_role_label(base_label, resource_roles.get(iri, set()))
        lines.append(f'  <owl:Class rdf:about="{iri}">')
        lines.append(f'    <rdfs:label>{base_label}</rdfs:label>')
        if label != base_label:
            lines.append(f'    <rdfs:label>{label}</rdfs:label>')
        parents = set(subclass_relations.get(iri, set())) | set(subclass_fact_lookup.get(iri, set()))
        if parents:
            for parent_iri in sorted(parents):
                parent = _canonical_orion_iri_for_output(str(parent_iri).strip(), use_schema_case_map=True)
                lines.append(f'    <rdfs:subClassOf rdf:resource="{parent}"/>')
        for comment in class_comments.get(iri, []):
            lines.append(f'    <rdfs:comment>{_xml_escape(comment)}</rdfs:comment>')

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
        lines.append(f'  <owl:ObjectProperty rdf:about="{iri}">')
        lines.append(f'    <rdfs:label>{label}</rdfs:label>')
        if domain:
            lines.append(f'    <rdfs:domain rdf:resource="{domain}"/>')
        if range_iri:
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

    description_nodes = {
        iri
        for iri in set(resource_roles) | set(class_rows) | set(subclass_relations)
        if resource_roles.get(iri, set()) != {'predicate'}
    }

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
        lines.append('  </rdf:Description>')

    lines.append('</rdf:RDF>')
    return '\n'.join(lines) + '\n'


def _is_type_super_node(value: str) -> bool:
    """Return whether a resource denotes the forbidden generic type super-node."""
    v = _normalize_text(value)
    return v in {'type', 'orion:type', f'{_ORION_NS}type'}


def _build_exclusion_set(payload: dict[str, Any], key: str) -> set[str]:
    """Build exclusion set."""
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
    """Build ref label lookup."""
    lookup: dict[str, str] = {}
    for entity in payload.get('entities', []):
        if not isinstance(entity, dict):
            continue
        entity_id = entity.get('entity_id')
        if isinstance(entity_id, str) and entity_id:
            label = entity.get('normalized_text') or entity.get('text')
            normalized = _normalize_fact_phrase(label if isinstance(label, str) else None)
            if normalized:
                lookup[entity_id] = normalized
    for concept in payload.get('concepts', []):
        if not isinstance(concept, dict):
            continue
        concept_id = concept.get('concept_id')
        if isinstance(concept_id, str) and concept_id:
            label = concept.get('normalized_text') or concept.get('lemma') or concept.get('text')
            normalized = _normalize_fact_phrase(label if isinstance(label, str) else None)
            if normalized:
                lookup[concept_id] = normalized
    return lookup


def _is_poor_numeric_id(value: str) -> bool:
    """Return whether a candidate identifier consists only of digits."""
    return bool(re.fullmatch(r'\d+', value.strip()))


def _resolve_node_text(raw_value: str | None, ref_value: str | None, ref_lookup: dict[str, str]) -> str:
    """Resolve node text."""
    direct = _normalize_fact_phrase(raw_value)
    if direct in _BR_RELATIVE_PRONOUNS:
        if isinstance(ref_value, str) and ref_value:
            resolved = _normalize_fact_phrase(ref_lookup.get(ref_value, ''))
            if resolved and resolved not in _BR_RELATIVE_PRONOUNS:
                return resolved
        return ''

    if direct and not _is_poor_numeric_id(direct):
        return direct

    if isinstance(ref_value, str) and ref_value:
        resolved = _normalize_fact_phrase(ref_lookup.get(ref_value, direct))
        if resolved not in _BR_RELATIVE_PRONOUNS:
            return resolved
    return ''


class RdfOutputStrategy:
    """Strategy that projects semantic claims and triples into the RDF graph representation."""
    def __init__(
        self,
        base_iri: str | None = None,
        prefixes: dict[str, str] | None = None,
    ) -> None:
        """Initialize the RdfOutputStrategy."""
        self._namespace_mode = base_iri is not None or prefixes is not None
        if self._namespace_mode:
            resolved_base_iri = validate_base_iri(base_iri or _ORION_NS)
            self._base_iri = resolved_base_iri
            self._prefixes = validate_and_resolve_prefixes(resolved_base_iri, prefixes)
        else:
            self._base_iri = ''
            self._prefixes = {}

    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Project triples and semantic claims into the RDF graph and output metadata."""
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
                raw_predicate = _RELATION_PREDICATE_IRI_ALIASES.get(_normalize_text(triple.get('predicate')), _normalize_text(triple.get('predicate')))
                predicate = compact_iri(make_iri(raw_predicate, kind='predicate', base_iri=self._base_iri), self._prefixes)
                obj = make_iri(object_text, kind='individual', base_iri=self._base_iri)
            else:
                subject = _normalize_text(triple.get('subject'))
                predicate = _RELATION_PREDICATE_IRI_ALIASES.get(_normalize_predicate(triple.get('predicate')), _normalize_predicate(triple.get('predicate')))
                object_text = _normalize_text(triple.get('object'))
                if object_text == 'type':
                    continue
                obj = object_text
            if not subject or not predicate or not obj:
                continue
            if _is_noisy_resource(predicate, allow_predicate=True) or _is_noisy_resource(subject) or _is_noisy_resource(obj):
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
            if subject and obj and not _is_noisy_resource(subject) and not _is_noisy_resource(obj):
                if not (_local_key(subject) in {'api', 'cia', 'rdf', 'orion'} and _local_key(obj) == 'organization'):
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
            if subject and obj and not _is_noisy_resource(subject) and not _is_noisy_resource(obj):
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
        graph = {
            'facts': facts,
            'instance_facts': instance_facts,
            'type_assertions': type_assertions,
            'subclass_facts': subclass_facts,
            'classes': classes,
            'object_property_schema': object_property_schema,
            'restrictions': restrictions,
            'schema': schema,
        }
        generic_graph = _build_generic_sentence_graph(payload, self._base_iri, self._namespace_mode)
        canonical_graph = _build_canonical_claims_graph(payload, self._base_iri, self._namespace_mode)
        selected_graph = canonical_graph or generic_graph
        if selected_graph is not None:
            graph = selected_graph
            subclass_facts = graph['subclass_facts']
        subclass_facts_count = serialize_graph_to_rdf_xml(graph).count('rdfs:subClassOf')
        graph['subclass_facts'] = _CountedList(subclass_facts, subclass_facts_count)
        result = {k: v for k, v in payload.items() if not k.startswith('_spacy')}
        if selected_graph is not None:
            result['taxonomy_relations'] = [
                {'subclass': item['subject'], 'superclass': item['object'], 'relation_type': 'subclass_of'}
                for item in subclass_facts
            ]
            result['type_assertions'] = []
        result['output'] = {
            'strategy': 'rdf',
            'format': 'rdf',
            'graph': graph,
            'metadata': payload.get('metadata', {}),
        }
        return result
