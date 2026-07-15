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
_PARAGRAPH_IDS = ['p029', 'p030']
_METRICS: dict[str, Any] | None = None
_ARTIFACT_DIR = _CASE_DIR / 'artifacts'


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p029_p030_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P029_P030 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p029_p030_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P029_P030 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p029_p030_claims_preserve_compliance_privacy_scope_and_qualifiers(tmp_path: Path):
    _metrics(tmp_path)
    claims = json.loads((_ARTIFACT_DIR / 'observed_p029_p030_semantic_claims.json').read_text(encoding='utf-8'))['claims']
    observed = {(item.get('subject'), item.get('predicate'), item.get('object')) for item in claims}
    assert {
        ('Organization', 'meets', 'LegalRequirement'),
        ('Organization', 'meets', 'RegulatoryRequirement'),
        ('Organization', 'meets', 'ContractualRequirement'),
        ('Organization', 'meets', 'InternalRequirement'),
        ('Control', 'satisfies', 'Requirement'),
        ('DataController', 'determines', 'Purpose'),
        ('DataController', 'determines', 'Means'),
        ('DataProcessor', 'processes', 'PersonalData'),
        ('DataSubject', 'has_personal_data', 'PersonalData'),
        ('Nonconformity', 'fails_to_meet', 'Requirement'),
        ('DataMinimization', 'limits', 'PersonalData'),
        ('RetentionLimitation', 'restricts', 'StorageDuration'),
        ('DataDeletion', 'removes', 'PersonalData'),
    } <= observed
    assert not ({'musts', 'personals', 'means', 'is_processed_for'} & {str(item.get('predicate')) for item in claims})
    assert not any(item.get('subject') == 'Compliance' and item.get('predicate') == 'ensures' for item in claims)
    assert any(item.get('subject') == 'Control' and item.get('modality') == 'whether' for item in claims)
    assert any(item.get('subject') == 'DataDeletion' and item.get('condition_polarity') == 'negative' for item in claims)
    assert any(item.get('subject') == 'DataProcessor' and item.get('on_behalf_of') == 'Controller' for item in claims)
    assert any(item.get('subject') == 'Consent' and item.get('predicate') == 'is_a' and item.get('condition') == 'in some contexts' for item in claims)


def test_p029_p030_output_has_no_pseudo_taxonomies_or_unjustified_restrictions(tmp_path: Path):
    _metrics(tmp_path)
    graph = json.loads((_ARTIFACT_DIR / 'observed_p029_p030_graph_model.json').read_text(encoding='utf-8'))
    assert graph.get('restrictions') == []
    assert any(item.get('modality') == 'whether' for item in graph.get('scoped_relations', []))
    forbidden = {'Necessary', 'Stored', 'NoLongerNeeded'}
    assert not any(str(item.get('object', '')).split(':')[-1] in forbidden for item in graph.get('subclass_facts', []))


def test_p029_p030_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P029_P030 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0
