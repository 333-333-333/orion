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
_PARAGRAPH_IDS = ['p021', 'p022']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p021_p022_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P021_P022 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p021_p022_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P021_P022 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p021_p022_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P021_P022 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def _artifact_json(name: str) -> dict[str, Any]:
    return json.loads((_CASE_DIR / "artifacts" / name).read_text(encoding="utf-8"))


def test_p021_p022_coordination_modality_and_process_scope_are_source_faithful(tmp_path: Path):
    _metrics(tmp_path)
    semantic = _artifact_json("observed_p021_p022_semantic_claims.json")
    claims = [item for item in semantic.get("claims", []) if isinstance(item, dict)]
    by_evidence: dict[str, list[dict[str, Any]]] = {}
    for claim in claims:
        by_evidence.setdefault(str((claim.get("source") or {}).get("evidence")), []).append(claim)

    siem = by_evidence["A security information and event management system collects, normalizes, correlates, and analyzes security logs."]
    assert {
        ("SecurityInformationAndEventManagementSystem", predicate, "SecurityLog")
        for predicate in ("collects", "normalizes", "correlates", "analyzes")
    } <= {(item.get("subject"), item.get("predicate"), item.get("object")) for item in siem}

    use_case = by_evidence["A use case describes a scenario that monitoring should detect."]
    assert any(
        item.get("subject") == "Monitoring"
        and item.get("predicate") == "shouldDetect"
        and item.get("object") == "Scenario"
        and item.get("modality") == "should"
        for item in use_case
    )
    assert not any(item.get("subject") == "Scenario" and item.get("predicate") == "monitors" for item in claims)

    process = by_evidence["Incident response is the process of preparing for, detecting, analyzing, containing, eradicating, and recovering from security incidents."]
    assert ("IncidentResponse", "is_a", "Process") in {
        (item.get("subject"), item.get("predicate"), item.get("object")) for item in process
    }
    assert len([item for item in process if item.get("predicate") == "has_activity"]) == 6


def test_p021_p022_quality_and_rdf_keep_obligations_scoped_and_bad_roles_out(tmp_path: Path):
    _metrics(tmp_path)
    quality = _artifact_json("pipeline_outputs/observed_p021_p022_15_semantic_quality.json")["semantic_quality_report"]
    graph = _artifact_json("observed_p021_p022_graph_model.json")

    scoped = {
        (item.get("subject"), item.get("predicate"), item.get("object"), item.get("modality"))
        for item in graph.get("scoped_relations", [])
    }
    assert ("orion:Monitoring", "orion:shouldDetect", "orion:Scenario", "should") in scoped
    assert ("orion:LogRetentionPolicy", "orion:requiresStorageOf", "orion:Log", "must") in scoped
    assert not any(item.get("predicate") == "orion:services" for item in graph.get("facts", []))
    assert not any(item.get("label") == "Storage" for item in graph.get("classes", []))
    assert quality["semantic_integrity_checks"]["logical_scope_structured"]
    assert quality["semantic_integrity_checks"]["claim_scope_preserved_in_triples"]
    assert not any("propositional_resources" in issue for issue in quality["semantic_integrity_issues"])


def test_p021_p022_retention_and_plan_claims_avoid_invented_or_truncated_resources(tmp_path: Path):
    _metrics(tmp_path)
    semantic = _artifact_json("observed_p021_p022_semantic_claims.json")
    claims = [item for item in semantic.get("claims", []) if isinstance(item, dict)]

    retention = [
        item for item in claims
        if (item.get("source") or {}).get("evidence") == "A log retention policy defines how long logs must be stored."
    ]
    assert any(
        item.get("subject") == "LogRetentionPolicy"
        and item.get("predicate") == "requiresStorageOf"
        and item.get("object") == "Log"
        and item.get("modality") == "must"
        for item in retention
    )
    assert all(item.get("object") != "Storage" for item in retention)

    plan = [
        item for item in claims
        if (item.get("source") or {}).get("evidence") == "An incident response plan is a document that defines the process for handling incidents."
    ]
    assert ("IncidentResponsePlan", "is_a", "Document") in {
        (item.get("subject"), item.get("predicate"), item.get("object")) for item in plan
    }
    assert ("Process", "handles", "Incident") in {
        (item.get("subject"), item.get("predicate"), item.get("object")) for item in plan
    }
    assert not any("Handl" in str(item.get("predicate")) for item in claims)
