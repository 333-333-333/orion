from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p031', 'p032']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p031_p032_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P031_P032 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p031_p032_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P031_P032 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p031_p032_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P031_P032 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def _artifact_json(name: str) -> dict[str, Any]:
    return json.loads((_CASE_DIR / "artifacts" / name).read_text(encoding="utf-8"))


def test_p031_p032_disjunction_conditions_and_verification_are_structured(tmp_path: Path):
    _metrics(tmp_path)
    semantic = _artifact_json("observed_p031_p032_semantic_claims.json")
    claims = [item for item in semantic.get("claims", []) if isinstance(item, dict)]

    processing = [
        item for item in claims
        if (item.get("source") or {}).get("evidence") == "Data processing transforms or uses information."
    ]
    assert {
        ("DataProcessing", "transforms", "Information"),
        ("DataProcessing", "uses", "Information"),
    } == {(item.get("subject"), item.get("predicate"), item.get("object")) for item in processing}
    assert len({item.get("alternative_group") for item in processing}) == 1
    assert all(item.get("coordination") == "or" for item in processing)

    transmission = [
        item for item in claims
        if (item.get("source") or {}).get("evidence") == "Data transmission moves information between systems or people."
    ]
    assert ("DataTransmission", "moves", "Information") in {
        (item.get("subject"), item.get("predicate"), item.get("object")) for item in transmission
    }
    assert not any(item.get("predicate") == "moves" and item.get("object") == "People" for item in transmission)

    assert any(
        item.get("subject") == "ChangeApproval"
        and item.get("predicate") == "verifies"
        and item.get("object") == "Acceptability"
        for item in claims
    )
    assert not any(item.get("subject") == "ChangeApprovalVerify" for item in claims)
    rollback = next(item for item in claims if item.get("subject") == "ChangeRollback" and item.get("predicate") == "restores")
    assert rollback.get("object") == "PreviousState"
    assert rollback.get("condition") == "Change fails"


def test_p031_p032_quality_gating_and_rdf_do_not_materialize_alternatives_as_facts(tmp_path: Path):
    _metrics(tmp_path)
    quality = _artifact_json("pipeline_outputs/observed_p031_p032_15_semantic_quality.json")["semantic_quality_report"]
    graph = _artifact_json("observed_p031_p032_graph_model.json")

    alternatives = graph.get("logical_alternatives", [])
    assert any(
        {item.get("predicate") for item in group.get("alternatives", [])}
        >= {"orion:transforms", "orion:uses"}
        for group in alternatives
    )
    assert not any(
        item.get("subject") == "orion:DataTransmission"
        and item.get("predicate") == "orion:moves"
        and item.get("object") == "orion:People"
        for item in graph.get("facts", [])
    )
    assert not any(
        item.get("subject") == "orion:ChangeApprovalVerify"
        for item in graph.get("subclass_facts", [])
    )
    assert quality["semantic_integrity_checks"]["logical_scope_structured"]
    assert quality["semantic_integrity_checks"]["claim_scope_preserved_in_triples"]
    assert not any("propositional_resources" in issue for issue in quality["semantic_integrity_issues"])


def test_p031_p032_roles_and_lexical_scope_survive_claims_and_graph_projection(tmp_path: Path):
    _metrics(tmp_path)
    semantic = _artifact_json("observed_p031_p032_semantic_claims.json")
    graph = _artifact_json("observed_p031_p032_graph_model.json")
    claims = [item for item in semantic.get("claims", []) if isinstance(item, dict)]

    classification = next(
        item for item in claims
        if item.get("subject") == "DataClassification" and item.get("predicate") == "applies"
    )
    assert classification.get("object") == "Label"
    assert classification.get("target") == "Information"

    handling = [
        item for item in claims
        if (item.get("source") or {}).get("evidence") == "Data handling rules define how each classification level must be protected."
    ]
    assert {(item.get("subject"), item.get("predicate"), item.get("object")) for item in handling} == {
        ("ClassificationLevel", "mustBeProtectedUnder", "DataHandlingRule")
    }
    assert handling[0].get("modality") == "must"
    assert not any(
        endpoint in {"Protection", "ProtectionRequirement", "IntendedOperation"}
        for item in claims
        for endpoint in (item.get("subject"), item.get("object"))
    )

    emergency = next(item for item in claims if item.get("predicate") == "implementedToResolve")
    assert emergency.get("subject") == "EmergencyChange"
    assert emergency.get("object") == "UrgentIssue"
    assert emergency.get("manner") == "rapidly"
    assert emergency.get("modality") == "purpose"

    testing = next(
        item for item in claims
        if item.get("subject") == "ChangeTesting" and item.get("predicate") == "verifies"
    )
    assert testing.get("object") == "Change"
    assert testing.get("evaluated_outcome") == "works_as_intended"
    lexical_complement = next(item for item in claims if item.get("subject") == "Change" and item.get("predicate") == "works")
    assert lexical_complement.get("object") == "Intended"
    assert lexical_complement.get("projection_scope") == "evidence_only"
    assert not any(item.get("label") in {"Intended", "IntendedOperation"} for item in graph.get("classes", []))

    lifecycle = next(item for item in graph.get("facts", []) if item.get("subject") == "orion:DataLifecycleManagement")
    assert lifecycle.get("scope_from") == "orion:Creation"
    assert lifecycle.get("scope_to") == "orion:Disposal"
    sharing = next(item for item in graph.get("facts", []) if item.get("subject") == "orion:DataSharing")
    assert sharing.get("recipient") == "orion:Party"
