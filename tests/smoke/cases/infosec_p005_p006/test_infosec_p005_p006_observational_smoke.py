from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p005', 'p006']
_METRICS: dict[str, Any] | None = None
_ARTIFACT_DIR = _CASE_DIR / 'artifacts'


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p005_p006_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P005_P006 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p005_p006_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P005_P006 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p005_p006_scoped_claims_preserve_agents_modality_conditions_and_disjunction(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / 'observed_p005_p006_semantic_claims.json').read_text(encoding='utf-8'))
    claims = semantic['claims']
    observed = {(claim.get('subject'), claim.get('predicate'), claim.get('object')) for claim in claims}

    assert not ({'as', 'cans'} & {str(claim.get('predicate')) for claim in claims})
    assert {
        ('Threat', 'exploits', 'Vulnerability'),
        ('Threat', 'causes', 'Harm'),
        ('Threat', 'affects', 'Asset'),
        ('Likelihood', 'has_probability_of', 'RiskScenario'),
    } <= observed
    assert any(claim.get('target') == 'Asset' and claim.get('modality') == 'possibility' for claim in claims)
    assert any(claim.get('modality') == 'can' and claim.get('voice') == 'passive' for claim in claims)
    assert any(claim.get('temporal_relation') == 'after' and claim.get('temporal_object') == 'Incident' for claim in claims)
    assert any(claim.get('condition_modality') == 'cannot' and claim.get('condition_subject') == 'PrimaryControl' for claim in claims)
    assert any(claim.get('condition_polarity') == 'negative' and claim.get('condition_subject') == 'AutomatedEnforcement' for claim in claims)

    mechanisms = [claim for claim in claims if claim.get('relation_role') == 'means_for']
    assert {claim.get('predicate') for claim in mechanisms} == {'prevents', 'detects', 'corrects', 'compensates_for'}
    assert len({claim.get('alternative_group') for claim in mechanisms}) == 1
    detective = [claim for claim in claims if claim.get('subject') == 'DetectiveControl' and claim.get('predicate') == 'identifies']
    assert {claim.get('object') for claim in detective} == {'SuspiciousActivity', 'PolicyViolation'}
    assert len({claim.get('alternative_group') for claim in detective}) == 1


def test_p005_p006_quality_and_output_keep_scoped_semantics_out_of_global_axioms(tmp_path: Path):
    _metrics(tmp_path)
    graph = json.loads((_ARTIFACT_DIR / 'observed_p005_p006_graph_model.json').read_text(encoding='utf-8'))
    quality_payload = json.loads(
        (_ARTIFACT_DIR / 'pipeline_outputs' / 'observed_p005_p006_15_semantic_quality.json').read_text(encoding='utf-8')
    )
    quality = quality_payload['semantic_quality_report']

    assert quality['rdf_readiness']
    assert quality['semantic_integrity_issues'] == []
    assert all(quality['semantic_integrity_checks'].values())
    assert graph.get('scoped_relations')
    assert any(item.get('condition_modality') == 'cannot' for item in graph['scoped_relations'])
    assert any(item.get('modality') == 'possibility' for item in graph['scoped_relations'])
    assert not any(
        item.get('subject') == 'orion:ManualApproval' and item.get('object') == 'orion:CompensatingControl'
        for item in graph.get('subclass_facts', [])
    )
    assert not any(item.get('predicate') in {'orion:as', 'orion:cans'} for item in graph.get('facts', []))


def test_p005_p006_probability_and_information_security_scope_project_without_occurrence(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / 'observed_p005_p006_semantic_claims.json').read_text(encoding='utf-8'))
    graph = json.loads((_ARTIFACT_DIR / 'observed_p005_p006_graph_model.json').read_text(encoding='utf-8'))

    assert any(
        claim.get('subject') == 'Likelihood'
        and claim.get('predicate') == 'has_probability_of'
        and claim.get('object') == 'RiskScenario'
        and claim.get('event_predicate') == 'occurs'
        for claim in semantic['claims']
    )
    assert not any('Occurrence' in str(claim.get(endpoint, '')) for claim in semantic['claims'] for endpoint in ('subject', 'object'))
    assert any(
        item.get('subject') == 'orion:RiskManagement'
        and item.get('object') == 'orion:CoreProcess'
        and item.get('scope') == 'orion:InformationSecurity'
        for item in graph.get('scoped_relations', [])
    )
    assert 'Occurrence' not in {item.get('label') for item in graph.get('classes', [])}


def test_p005_p006_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P005_P006 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0
