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
_PARAGRAPH_IDS = ['p035', 'p036']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p035_p036_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P035_P036 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p035_p036_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P035_P036 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p035_p036_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P035_P036 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_p035_p036_audited_modal_and_coordination_claims_are_uniform(tmp_path: Path):
    _metrics(tmp_path)
    payload = json.loads((_CASE_DIR / "artifacts" / "observed_p035_p036_semantic_claims.json").read_text(encoding="utf-8"))
    claims = [item for item in payload.get("claims", []) if isinstance(item, dict)]

    support = [item for item in claims if item.get("predicate") == "supports" and item.get("object") == "Resilience"]
    assert len(support) == 1
    assert support[0].get("subject") == "BackupAndRecovery"
    assert support[0].get("members") == "Backup,Recovery"
    assert support[0].get("coordination_scope") == "subject"
    assert support[0].get("projection_scope") == "scoped"
    assert not any(item.get("subject") in {"Backup", "Recovery"} and item.get("predicate") == "supports" for item in claims)
    assert not any(item.get("object") == "SupportResilience" for item in claims)

    alignment = [item for item in claims if item.get("subject") == "SecureArchitecture" and item.get("predicate") == "aligns_with"]
    assert {item.get("object") for item in alignment} == {"BusinessRequirement", "RiskAppetite", "RegulatoryObligation"}
    assert all(item.get("modality") == "must" for item in alignment)

    can_claims = [item for item in claims if item.get("modality") == "can" and item.get("quantifier") == "one_or_more"]
    assert len(can_claims) == 12
    assert any((item.get("subject"), item.get("predicate"), item.get("object")) == ("System", "canProcess", "InformationAsset") for item in can_claims)
    assert any((item.get("subject"), item.get("predicate"), item.get("object")) == ("User", "canAccess", "System") for item in can_claims)
    assert not any(item.get("subject") in {"SystemCan", "UserCan"} for item in claims)

    negated = next(item for item in claims if item.get("subject") == "ZeroTrust" and item.get("predicate") == "assumes")
    assert (negated.get("object"), negated.get("polarity"), negated.get("basis")) == ("ImplicitTrust", "negative", "NetworkLocation")


def test_p035_p036_modal_relations_are_not_flattened_to_rdf_facts(tmp_path: Path):
    _metrics(tmp_path)
    graph = json.loads((_CASE_DIR / "artifacts" / "observed_p035_p036_graph_model.json").read_text(encoding="utf-8"))
    scoped_modalities = [item.get("modality") for item in graph.get("scoped_relations", [])]
    assert scoped_modalities.count("can") == 12
    assert scoped_modalities.count("must") == 3
    assert graph.get("restrictions") == []


def test_p035_p036_collective_support_is_not_materialized_and_claim_ids_are_stable(tmp_path: Path):
    _metrics(tmp_path)
    payload = json.loads((_CASE_DIR / "artifacts" / "observed_p035_p036_semantic_claims.json").read_text(encoding="utf-8"))
    claims = [item for item in payload.get("claims", []) if isinstance(item, dict)]
    graph = json.loads((_CASE_DIR / "artifacts" / "observed_p035_p036_graph_model.json").read_text(encoding="utf-8"))

    assert not any(
        str(item.get("predicate", "")).lower().endswith("supports")
        and str(item.get("subject", "")).rsplit(":", 1)[-1] in {"Backup", "Recovery"}
        for item in graph.get("facts", [])
    )
    collective = next(
        item for item in graph.get("scoped_relations", [])
        if str(item.get("subject", "")).rsplit(":", 1)[-1] == "BackupAndRecovery"
        and str(item.get("predicate", "")).lower().endswith("supports")
    )
    assert collective.get("coordination_scope") == "subject"
    assert {str(item).rsplit(":", 1)[-1] for item in collective.get("members", [])} == {"Backup", "Recovery"}

    claim_ids = [item.get("claim_id") for item in claims]
    projection = graph.get("projection", {})
    assert projection.get("claim_ids") == claim_ids
    assert [item.get("claim_id") for item in projection.get("claim_dispositions", [])] == claim_ids


def test_p035_p036_quality_detects_the_propositional_concept_candidate(tmp_path: Path):
    _metrics(tmp_path)
    quality = json.loads(
        (_CASE_DIR / "artifacts" / "pipeline_outputs" / "observed_p035_p036_15_semantic_quality.json").read_text(encoding="utf-8")
    )["semantic_quality_report"]
    assert any(
        item.get("reason") == "predicate_absorbed_into_concept"
        and "backup and recovery support resilience" in str(item.get("text", "")).lower()
        for item in quality.get("concept_noise", [])
    )
    assert quality.get("quality_score", 1.0) < 1.0
    assert quality.get("rdf_readiness") is False
