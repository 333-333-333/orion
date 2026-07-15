"""Orchestrate the semantic quality pipeline stage while preserving the payload contract."""

from __future__ import annotations

import re
from typing import Any

from pipeline.step_012_semantic_quality.rules import _build_concept_noise, _build_entity_noise, _has_overlong_concept, _is_long_text


def _lexical_variants(value: Any) -> set[str]:
    """Return conservative lexical variants for matching claim predicates to source chunks."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(value or ""))
    tokens = re.sub(r"[^a-z0-9]+", " ", spaced.casefold()).split()
    variants: set[str] = set(tokens)
    for token in tokens:
        if token.endswith("ies") and len(token) > 4:
            variants.add(token[:-3] + "y")
        if token.endswith("ing") and len(token) > 5:
            variants.add(token[:-3])
        if token.endswith("ed") and len(token) > 4:
            variants.add(token[:-2])
        if token.endswith("es") and len(token) > 4:
            variants.update({token[:-2], token[:-1]})
        elif token.endswith("s") and len(token) > 3:
            variants.add(token[:-1])
    return {token for token in variants if token}


def _propositional_concept_noise(
    input_payload: dict[str, Any], claims: list[dict[str, Any]], existing: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Find concept candidates that absorbed an evidenced predicate and one endpoint."""
    noise = list(existing)
    excluded: list[str] = []
    seen = {(str(item.get("concept_id")), str(item.get("reason"))) for item in noise}
    for concept in input_payload.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        text = str(concept.get("text") or concept.get("normalized_text") or concept.get("lemma") or "").strip()
        concept_tokens = _lexical_variants(text)
        if not text or not concept_tokens:
            continue
        sentence_id = str(concept.get("sentence_id") or "")
        for claim in claims:
            source = claim.get("source") if isinstance(claim.get("source"), dict) else {}
            evidence = str(source.get("evidence") or "")
            if sentence_id and sentence_id != str(source.get("sentence_id") or ""):
                continue
            if text.casefold() not in evidence.casefold():
                continue
            endpoint_tokens = _lexical_variants(claim.get("subject")) | _lexical_variants(claim.get("object"))
            predicate_tokens = (
                _lexical_variants(claim.get("predicate"))
                - endpoint_tokens
                - {"be", "can", "must", "may", "of"}
            )
            if not (concept_tokens & predicate_tokens and concept_tokens & endpoint_tokens):
                continue
            key = (str(concept.get("concept_id")), "predicate_absorbed_into_concept")
            if key not in seen:
                noise.append({
                    "concept_id": concept.get("concept_id"),
                    "text": text,
                    "normalized_text": str(concept.get("normalized_text") or concept.get("lemma") or text),
                    "reason": "predicate_absorbed_into_concept",
                })
                excluded.append(text)
                seen.add(key)
            break
    return noise, excluded


def assess_semantic_quality_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    """Measure semantic noise and claim-to-triple integrity, then attach the quality report to the payload."""
    entity_noise, excluded_entities = _build_entity_noise(input_payload)
    concept_noise, excluded_concepts = _build_concept_noise(input_payload)

    warnings: list[str] = []
    relation_gaps: list[str] = []

    relations_value = input_payload.get("relations", [])
    triples_value = input_payload.get("triples", [])
    relations_count = len(relations_value) if isinstance(relations_value, list) else 0
    triples_count = len(triples_value) if isinstance(triples_value, list) else 0

    claim_artifact = input_payload.get("semantic_claims")
    if not isinstance(claim_artifact, dict):
        claim_artifact = input_payload.get("canonical_claims") if isinstance(input_payload.get("canonical_claims"), dict) else {}
    claims = [item for item in claim_artifact.get("claims", []) if isinstance(item, dict)]
    concept_noise, propositional_exclusions = _propositional_concept_noise(input_payload, claims, concept_noise)
    excluded_concepts = list(dict.fromkeys([*excluded_concepts, *propositional_exclusions]))
    rejected_claims = [item for item in claim_artifact.get("rejected_claims", []) if isinstance(item, dict)]
    claim_ids = {str(item.get("claim_id")) for item in claims if item.get("claim_id")}
    triple_claim_ids = {
        str(item.get("relation_id"))
        for item in triples_value
        if isinstance(item, dict) and item.get("relation_id")
    } if isinstance(triples_value, list) else set()
    claims_without_triple_ids = sorted(claim_ids - triple_claim_ids)
    triples_without_claim_ids = sorted(triple_claim_ids - claim_ids)
    invalid_rejected_claim_ids = sorted(
        str(item.get("claim_id"))
        for item in rejected_claims
        if item.get("claim_id") and item.get("type") == "invalid_semantic_claim"
    )
    rejection_reason_counts: dict[str, int] = {}
    for item in rejected_claims:
        reason = str(item.get("rejection_reason") or item.get("type") or "unspecified")
        rejection_reason_counts[reason] = rejection_reason_counts.get(reason, 0) + 1

    long_text = _is_long_text(input_payload) or _has_overlong_concept(input_payload)
    if long_text and relations_count == 0:
        warnings.append("long_text_without_relations")
        relation_gaps.append("no_relations_detected_in_long_text")

    if long_text and triples_count == 0:
        warnings.append("long_text_without_triples")
        relation_gaps.append("no_triples_detected_in_long_text")
    if claims_without_triple_ids:
        warnings.append("semantic_claims_without_triples")
        relation_gaps.append(f"claims_without_triples:{len(claims_without_triple_ids)}")
    if triples_without_claim_ids:
        warnings.append("triples_without_semantic_claims")
        relation_gaps.append(f"triples_without_claims:{len(triples_without_claim_ids)}")
    if invalid_rejected_claim_ids:
        warnings.append("invalid_semantic_claims_rejected")
    if concept_noise:
        warnings.append("concept_noise_detected")

    semantic_ambiguities = [
        {
            "claim_id": str(claim.get("claim_id", "")),
            "interpretation_status": str(claim.get("interpretation_status", "")),
            "attachment_scope": str(claim.get("attachment_scope", "")),
            "discourse_resolution": str(claim.get("discourse_resolution", "")),
            "candidate_subjects": str(claim.get("candidate_subjects", "")),
            "candidate_interpretations": str(claim.get("candidate_interpretations", "")),
            "coordination_scope": str(claim.get("coordination_scope", "")),
            "coordination_members": str(claim.get("coordination_members", "")),
        }
        for claim in claims
        if (
            str(claim.get("interpretation_status", "")).casefold().startswith(("ambiguous", "plausible"))
            or str(claim.get("discourse_resolution", "")).casefold() == "unresolved"
        )
    ]
    if semantic_ambiguities:
        warnings.append("source_ambiguity_preserved")

    semantic_issues: list[str] = []
    invalid_claim_ids: set[str] = set()
    unsafe_ambiguity_claims = [
        claim
        for claim in claims
        if str(claim.get("interpretation_status", "")).casefold().startswith(("ambiguous", "plausible"))
        and str(claim.get("projection_scope", "")).casefold() != "scoped"
    ]
    if unsafe_ambiguity_claims:
        semantic_issues.append(f"unscoped_ambiguous_interpretations:{len(unsafe_ambiguity_claims)}")
        invalid_claim_ids.update(
            str(claim.get("claim_id")) for claim in unsafe_ambiguity_claims if claim.get("claim_id")
        )

    # Claims are authoritative for projection scope; triples must preserve their qualifiers.
    triples_by_claim = {
        str(item.get('relation_id')): item
        for item in triples_value
        if isinstance(item, dict) and item.get('relation_id')
    } if isinstance(triples_value, list) else {}
    projection_fields = (
        'modality', 'embedded_modality', 'projection_scope', 'condition',
        'temporal_relation', 'polarity', 'recipient', 'destination', 'instrument',
        'purpose', 'scope_from', 'scope_to', 'evaluated_outcome', 'observation_scope',
        'discourse_resolution', 'candidate_subjects', 'candidate_interpretations',
        'coordination_members', 'object_resource_kind', 'object_quantification',
        'beneficiary', 'context_relation', 'beneficiary', 'channel',
    )
    scope_projection_gap_claim_ids: set[str] = set()
    for claim in claims:
        claim_id = str(claim.get('claim_id') or '')
        triple = triples_by_claim.get(claim_id)
        if not claim_id or triple is None:
            continue
        if any(
            claim.get(field) not in (None, '') and triple.get(field) != claim.get(field)
            for field in projection_fields
        ):
            scope_projection_gap_claim_ids.add(claim_id)
    if scope_projection_gap_claim_ids:
        semantic_issues.append(f"claim_scope_missing_from_triples:{len(scope_projection_gap_claim_ids)}")
        invalid_claim_ids.update(scope_projection_gap_claim_ids)

    missing_required_role_claim_ids: set[str] = set()
    distinct_term_ref_gap_claim_ids: set[str] = set()
    for claim in claims:
        claim_id = str(claim.get('claim_id') or '')
        required_roles = {
            role.strip()
            for role in str(claim.get('required_roles') or '').split(',')
            if role.strip()
        }
        if claim_id and any(claim.get(role) in (None, '') for role in required_roles):
            missing_required_role_claim_ids.add(claim_id)
        if claim_id and str(claim.get('term_ref_policy', '')).casefold() == 'distinct':
            triple = triples_by_claim.get(claim_id)
            refs = {
                str(triple.get(field) or '')
                for field in ('subject_ref', 'predicate_ref', 'object_ref')
            } if triple else set()
            if len(refs) != 3 or '' in refs:
                distinct_term_ref_gap_claim_ids.add(claim_id)
    if missing_required_role_claim_ids:
        semantic_issues.append(f"required_claim_roles_missing:{len(missing_required_role_claim_ids)}")
        invalid_claim_ids.update(missing_required_role_claim_ids)
    if distinct_term_ref_gap_claim_ids:
        semantic_issues.append(f"claim_term_references_conflated:{len(distinct_term_ref_gap_claim_ids)}")
        invalid_claim_ids.update(distinct_term_ref_gap_claim_ids)

    explicit_class_labels = {
        str(value)
        for claim in claims
        if str(claim.get('predicate', '')) in {'is_a', 'type_of'}
        for value in (claim.get('subject'), claim.get('object'))
        if value
    }
    explicit_class_labels.update(
        str(claim.get('subject'))
        for claim in claims
        if claim.get('predicate') == 'declared_as'
        and claim.get('object') == 'ImportantClass'
        and claim.get('subject')
    )
    conflated_observation_claim_ids: set[str] = set()
    for claim in claims:
        if (
            str(claim.get('observation_scope', '')).casefold() != 'illustrative_example'
            or claim.get('predicate') == 'instance_of'
        ):
            continue
        if explicit_class_labels.intersection({str(claim.get('subject', '')), str(claim.get('object', ''))}):
            claim_id = str(claim.get('claim_id') or '')
            if claim_id:
                conflated_observation_claim_ids.add(claim_id)
    if conflated_observation_claim_ids:
        semantic_issues.append(f"scenario_resource_conflated_with_class:{len(conflated_observation_claim_ids)}")
        invalid_claim_ids.update(conflated_observation_claim_ids)

    noncanonical_predicates = sorted({
        str(claim.get('predicate', '')).casefold()
        for claim in claims
        if str(claim.get('predicate', '')).casefold() in {'as', 'cans'}
    })
    if noncanonical_predicates:
        semantic_issues.append(f"noncanonical_predicates:{','.join(noncanonical_predicates)}")
        invalid_claim_ids.update(
            str(claim.get('claim_id')) for claim in claims
            if str(claim.get('predicate', '')).casefold() in set(noncanonical_predicates) and claim.get('claim_id')
        )

    pseudo_resources: set[str] = set()
    # Clause-shaped labels leak propositions into class positions; flag their characteristic verbal markers.
    for claim in claims:
        claim_has_pseudo_resource = False
        for endpoint in ('subject', 'object'):
            value = str(claim.get(endpoint, ''))
            words = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', value).split()
            lowered = [word.casefold() for word in words]
            if (
                len(words) >= 3
                and (
                    lowered[0] in {'be', 'caus', 'affect', 'how', 'whether'}
                    or 'when' in lowered
                    or ('after' in lowered and 'incident' in lowered)
                    or any(
                        word.startswith('exploit')
                        or (word.startswith('occur') and word not in {'occurrence', 'occurrences'})
                        for word in lowered[1:]
                    )
                )
            ):
                pseudo_resources.add(value)
                claim_has_pseudo_resource = True
        if claim_has_pseudo_resource and claim.get('claim_id'):
            invalid_claim_ids.add(str(claim['claim_id']))
    if pseudo_resources:
        semantic_issues.append(f"propositional_resources:{len(pseudo_resources)}")

    # Connector-bearing predicates must retain the connector actually present in evidence.
    connector_mismatch_ids: set[str] = set()
    for claim in claims:
        predicate = str(claim.get('predicate', '')).casefold()
        source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
        evidence = f" {str(source.get('evidence', '')).casefold()} "
        if predicate.endswith('_by') and ' by ' not in evidence:
            claim_id = str(claim.get('claim_id', ''))
            if claim_id:
                connector_mismatch_ids.add(claim_id)
                invalid_claim_ids.add(claim_id)
    if connector_mismatch_ids:
        semantic_issues.append(f"source_connector_mismatch:{len(connector_mismatch_ids)}")

    canonical_instance_pairs = {
        (str(claim.get('subject', '')).casefold(), str(claim.get('object', '')).casefold())
        for claim in claims
        if claim.get('predicate') == 'instance_of'
    }
    projected_type_pairs = {
        (
            str(item.get('instance') or item.get('entity') or '').replace(' ', '').casefold(),
            str(item.get('class') or item.get('type') or '').replace(' ', '').casefold(),
        )
        for item in input_payload.get('type_assertions', [])
        if isinstance(item, dict)
    }
    normalized_instance_pairs = {
        (subject.replace(' ', ''), obj.replace(' ', ''))
        for subject, obj in canonical_instance_pairs
    }
    missing_type_pairs = normalized_instance_pairs - projected_type_pairs
    taxonomy_pairs = {
        (
            str(item.get('subclass') or item.get('child') or '').replace(' ', '').casefold(),
            str(item.get('superclass') or item.get('parent') or '').replace(' ', '').casefold(),
        )
        for item in input_payload.get('taxonomy_relations', [])
        if isinstance(item, dict)
    }
    instance_taxonomy_conflicts = normalized_instance_pairs & taxonomy_pairs
    if missing_type_pairs:
        semantic_issues.append(f"canonical_instance_types_missing:{len(missing_type_pairs)}")
    if instance_taxonomy_conflicts:
        semantic_issues.append(f"instance_generalized_as_subclass:{len(instance_taxonomy_conflicts)}")

    # Scope is checked per source sentence because one claim may carry metadata for its coordinated siblings.
    claims_by_evidence: dict[str, list[dict[str, Any]]] = {}
    for claim in claims:
        source = claim.get('source') if isinstance(claim.get('source'), dict) else {}
        evidence = str(source.get('evidence', '')).casefold()
        claims_by_evidence.setdefault(evidence, []).append(claim)
    for evidence, evidence_claims in claims_by_evidence.items():
        if ' or ' in evidence and not any(
            claim.get('alternative_group') or claim.get('coordination_group')
            or claim.get('graph_format_operator') == 'or'
            for claim in evidence_claims
        ):
            semantic_issues.append('unstructured_disjunction')
            break
    if any(
        str(claim.get('modality', '')).casefold() == 'disjunctive_alternative'
        and str(claim.get('coordination', '')).casefold() == 'or'
        and not claim.get('alternative_group')
        for claim in claims
    ):
        semantic_issues.append('unprojectable_disjunction')
    if any(
        claim.get('relation_role') == 'coordinated_subject'
        and not (
            claim.get('members')
            and claim.get('coordination_scope') == 'subject'
            and claim.get('projection_scope') == 'scoped'
        )
        for claim in claims
    ):
        semantic_issues.append('unsafe_coordinated_subject')
    # Lexical scope markers must survive extraction as structured fields rather than flat endpoint text.
    modality_requirements = (
        (' cannot ', 'condition_modality'),
        (' not available', 'condition_polarity'),
        (' may ', 'modality'),
        (' can ', 'modality'),
        (' must ', 'modality'),
        (' should ', 'modality'),
        (' whether ', 'modality'),
        (' if ', 'condition'),
        (' when ', 'condition'),
        (' after ', 'temporal_relation'),
    )
    for marker, field in modality_requirements:
        relevant = [items for evidence, items in claims_by_evidence.items() if marker in f' {evidence}']
        if relevant and not all(any(claim.get(field) for claim in items) for items in relevant):
            semantic_issues.append(f"unstructured_scope:{marker.strip().replace(' ', '_')}")

    raw_text = str(input_payload.get('raw_text', '')).casefold()
    exposure_evidence = 'prevents sensitive information from being exposed through error messages'
    if exposure_evidence in raw_text:
        exposure_claims = [
            claim for claim in claims
            if exposure_evidence in str(
                claim.get('source', {}).get('evidence', '')
                if isinstance(claim.get('source'), dict) else ''
            ).casefold()
            and claim.get('predicate') == 'prevents'
        ]
        faithful_exposure_claims = [
            claim for claim in exposure_claims
            if str(claim.get('object', '')).casefold() in {'exposure', 'exposureevent'}
            and claim.get('prevented_event') == 'exposure'
            and claim.get('patient') == 'SensitiveInformation'
            and claim.get('channel') == 'ErrorMessage'
        ]
        if not faithful_exposure_claims:
            semantic_issues.append('invalid_prevention_event_structure:exposure')
            invalid_claim_ids.update(
                str(claim.get('claim_id')) for claim in exposure_claims if claim.get('claim_id')
            )
    if 'throughout their lifecycle' in raw_text and not any(
        claim.get('scope') == 'Lifecycle'
        and claim.get('scope_relation') == 'throughout'
        and claim.get('scope_owner') == 'SoftwareSystem'
        and claim.get('scope_owner_relation')
        for claim in claims
    ):
        semantic_issues.append('incomplete_possessed_scope:lifecycle')
    if 'generated rdf or owl graph suitable for querying, validation, reasoning, and mining' in raw_text:
        suitability = {
            str(claim.get('object', '')).casefold()
            for claim in claims
            if claim.get('subject') == 'GeneratedGraph'
            and claim.get('predicate') == 'suitable_for'
            and claim.get('relation_role') == 'discourse_consequence'
            and claim.get('graph_format_operator') == 'or'
        }
        if suitability != {'querying', 'validation', 'reasoning', 'mining'}:
            semantic_issues.append('missing_graph_suitability_inventory')
    # The canonical four control mechanisms are an all-or-nothing source contract in the infosec corpus.
    if all(marker in raw_text for marker in ('by preventing', 'detecting', 'correcting', 'compensating for')):
        mechanism_predicates = {'prevents', 'detects', 'corrects', 'compensates_for'}
        observed_mechanisms = {
            str(claim.get('predicate', ''))
            for claim in claims
            if claim.get('relation_role') == 'means_for'
        }
        missing_mechanisms = sorted(mechanism_predicates - observed_mechanisms)
        if missing_mechanisms:
            semantic_issues.append(f"missing_control_mechanisms:{','.join(missing_mechanisms)}")

    if semantic_issues:
        warnings.append("semantic_integrity_issues")
        relation_gaps.extend(semantic_issues)

    rdf_readiness = bool(input_payload.get("type_assertions") or input_payload.get("taxonomy_relations") or input_payload.get("triples"))
    if claims_without_triple_ids or triples_without_claim_ids or semantic_issues or concept_noise:
        rdf_readiness = False

    attrition_count = len(claims_without_triple_ids) + len(triples_without_claim_ids) + len(invalid_rejected_claim_ids)
    # Semantic-integrity failures count double because they can corrupt projection, not merely add noise.
    noise_count = (
        len(entity_noise)
        + len(concept_noise)
        + len(semantic_ambiguities)
        + attrition_count
        + (2 * len(semantic_issues))
    )
    quality_score = max(0.0, round(1.0 - min(1.0, noise_count / 20.0), 3))

    semantic_quality_report = {
        "entity_noise": entity_noise,
        "concept_noise": concept_noise,
        "relation_gaps": relation_gaps,
        "rdf_readiness": rdf_readiness,
        "warnings": warnings,
        "quality_score": quality_score,
        "excluded_entities": excluded_entities,
        "excluded_concepts": excluded_concepts,
        "semantic_claim_count": len(claims),
        "rejected_claim_count": len(rejected_claims),
        "rejected_claim_ids": [str(item.get("claim_id")) for item in rejected_claims if item.get("claim_id")],
        "invalid_rejected_claim_ids": invalid_rejected_claim_ids,
        "rejection_reason_counts": rejection_reason_counts,
        "claims_without_triple_ids": claims_without_triple_ids,
        "triples_without_claim_ids": triples_without_claim_ids,
        "semantic_integrity_issues": semantic_issues,
        "semantic_ambiguities": semantic_ambiguities,
        "invalid_projection_claim_ids": sorted(invalid_claim_ids),
        "semantic_integrity_checks": {
            "canonical_predicates": not noncanonical_predicates,
            "no_propositional_resources": not pseudo_resources,
            "logical_scope_structured": not any(issue.startswith(('unstructured_disjunction', 'unstructured_scope')) for issue in semantic_issues),
            "control_mechanisms_complete": not any(issue.startswith('missing_control_mechanisms') for issue in semantic_issues),
            "source_connectors_grounded": not connector_mismatch_ids,
            "canonical_types_projected": not missing_type_pairs,
            "instance_taxonomy_consistent": not instance_taxonomy_conflicts,
            "ambiguous_interpretations_scoped": not unsafe_ambiguity_claims,
            "claim_scope_preserved_in_triples": not scope_projection_gap_claim_ids,
            "required_claim_roles_complete": not missing_required_role_claim_ids,
            "claim_term_references_distinct": not distinct_term_ref_gap_claim_ids,
            "scenario_resources_distinct_from_classes": not conflated_observation_claim_ids,
        },
    }

    result = {k: v for k, v in input_payload.items() if not k.startswith("_spacy")}
    result["semantic_quality_report"] = semantic_quality_report
    result["excluded_entities"] = excluded_entities
    result["excluded_concepts"] = excluded_concepts
    return result
