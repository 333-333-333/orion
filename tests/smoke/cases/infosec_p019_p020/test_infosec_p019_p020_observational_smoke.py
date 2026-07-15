from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p019', 'p020']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p019_p020_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P019_P020 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p019_p020_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P019_P020 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p019_p020_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P019_P020 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_p019_p020_preserves_service_coordination_modality_and_negation(tmp_path: Path):
    import json

    _metrics(tmp_path)
    claims_payload = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p019_p020_semantic_claims.json").read_text(encoding="utf-8")
    )
    claims = claims_payload["claims"]
    service_spo = {
        (claim["predicate"], claim["object"])
        for claim in claims
        if claim["subject"] == "KeyManagementService"
    }

    assert service_spo == {
        ("stores", "CryptographicKey"),
        ("controls_access_to", "CryptographicKey"),
    }
    assert not any(claim.get("object") == "ControlAccess" for claim in claims)
    assert any(claim["subject"] == "PoorKeyManagement" and claim.get("modality") == "can" for claim in claims)
    assert any(claim["subject"] == "SecurityEvent" and claim.get("modality") == "may" for claim in claims)
    assert any(claim["subject"] == "FalsePositive" and claim.get("polarity") == "negative" for claim in claims)
    assert not any(claim["predicate"] in {"does", "maies"} for claim in claims)

    graph = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p019_p020_graph_model.json").read_text(encoding="utf-8")
    )
    scoped_ids = {item["claim_id"] for item in graph["scoped_relations"]}
    false_positive = next(claim for claim in claims if claim["subject"] == "FalsePositive" and claim["predicate"] == "represents")
    assert false_positive["claim_id"] in scoped_ids
    assert graph["restrictions"] == []


def test_p019_p020_preserves_generic_event_and_when_condition_without_agent_inference(tmp_path: Path):
    import json

    _metrics(tmp_path)
    claims = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p019_p020_semantic_claims.json").read_text(encoding="utf-8")
    )["claims"]
    spo = {(claim["subject"], claim["predicate"], claim["object"]) for claim in claims}

    assert ("LogRecord", "records", "Event") in spo
    assert ("Event", "generated_by", "System") in spo
    assert ("LogRecord", "records", "SecurityEvent") not in spo
    assert ("DetectionRule", "identifies", "SuspiciousActivity") in spo
    assert ("SecurityAlert", "generated_by", "DetectionRule") not in spo
    condition_claim = next(claim for claim in claims if claim["subject"] == "DetectionRule")
    assert condition_claim["relation_role"] == "generation_condition"
    assert condition_claim["context"] == "SecurityAlert"
    assert condition_claim["state"] == "generated_when"

    graph = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p019_p020_graph_model.json").read_text(encoding="utf-8")
    )
    facts = {(item["subject"], item["predicate"], item["object"]) for item in graph["facts"]}
    assert ("orion:LogRecord", "orion:records", "orion:Event") in facts
    assert ("orion:Event", "orion:generatedBy", "orion:System") in facts
    assert ("orion:DetectionRule", "orion:identifies", "orion:SuspiciousActivity") in facts
    assert not any(item["predicate"] == "orion:generatedBy" and item["subject"] == "orion:SecurityAlert" for item in graph["facts"])

    quality = json.loads(
        (_CASE_DIR / "artifacts" / "pipeline_outputs" / "observed_p019_p020_15_semantic_quality.json").read_text(encoding="utf-8")
    )["semantic_quality_report"]
    assert quality["semantic_integrity_checks"]["source_connectors_grounded"]
