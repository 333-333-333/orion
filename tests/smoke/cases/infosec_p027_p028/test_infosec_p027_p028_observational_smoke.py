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
_PARAGRAPH_IDS = ['p027', 'p028']
_METRICS: dict[str, Any] | None = None
_ARTIFACT_DIR = _CASE_DIR / 'artifacts'


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p027_p028_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P027_P028 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p027_p028_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P027_P028 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p027_p028_claims_preserve_compound_subjects_actions_and_scope(tmp_path: Path):
    _metrics(tmp_path)
    payload = json.loads((_ARTIFACT_DIR / 'observed_p027_p028_semantic_claims.json').read_text(encoding='utf-8'))
    claims = payload['claims']
    observed = {(item.get('subject'), item.get('predicate'), item.get('object')) for item in claims}

    assert {
        ('SecurityAwarenessTraining', 'educates', 'User'),
        ('DataHandlingAwareness', 'teaches', 'User'),
        ('AwarenessCampaign', 'reinforces', 'SecureBehavior'),
        ('TrainingCompletionMetric', 'measures', 'UserParticipation'),
        ('SimulatedPhishingExercise', 'measures', 'UserResponse'),
    } <= observed
    taught = {item.get('predicate') for item in claims if item.get('modality') == 'taught_action'}
    assert {'identifies', 'creates', 'protects', 'classifies', 'stores', 'transmits', 'disposes_of', 'recognizes'} <= taught
    assert any(item.get('temporal_relation') == 'before' and item.get('temporal_object') == 'Employment' and item.get('subject') == 'BackgroundCheck' for item in claims)
    assert any(item.get('condition_subject') == 'Employment' and item.get('condition_predicate') == 'ends' for item in claims)
    assert not ({'awareness', 'process', 'campaigns', 'metrics', 'exercises', 'networks', 'applies_before'} & {str(item.get('predicate')) for item in claims})


def test_p027_p028_output_uses_scoped_views_without_unjustified_restrictions(tmp_path: Path):
    _metrics(tmp_path)
    graph = json.loads((_ARTIFACT_DIR / 'observed_p027_p028_graph_model.json').read_text(encoding='utf-8'))
    assert graph.get('restrictions') == []
    assert any(item.get('temporal_relation') == 'before' for item in graph.get('scoped_relations', []))
    assert any(item.get('modality') == 'taught_action' for item in graph.get('scoped_relations', []))
    assert not any(item.get('predicate') in {'orion:awareness', 'orion:campaigns', 'orion:metrics', 'orion:exercises', 'orion:networks'} for item in graph.get('facts', []))


def test_p027_p028_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P027_P028 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0
