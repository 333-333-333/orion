from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p037', 'p038']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p037_p038_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P037_P038 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p037_p038_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P037_P038 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p037_p038_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P037_P038 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_p037_p038_keeps_example_relations_as_observations_and_instance_types(tmp_path: Path):
    import json

    _metrics(tmp_path)
    claims_payload = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p037_p038_semantic_claims.json").read_text(encoding="utf-8")
    )
    claims = claims_payload["claims"]
    spo = {(claim["subject"], claim["predicate"], claim["object"]) for claim in claims}

    assert ("CustomerDatabase", "hosted_on", "DatabaseServer") in spo
    assert ("DatabaseServer", "runs_inside", "ProductionNetwork") in spo
    assert ("CustomerDatabase", "encrypted_using", "CryptographicKey") in spo
    assert ("AuthorizationService", "grants", "Access") in spo
    assert ("RemoteEmployee", "accesses", "CorporateApplication") in spo
    assert ("Laptop", "accesses", "CorporateApplication") not in spo
    assert ("Laptop", "instance_of", "Endpoint") in spo
    assert ("CorporateApplication", "instance_of", "WebApplication") in spo
    assert all(
        claim.get("observation_scope") == "illustrative_example"
        for claim in claims
        if claim["paragraph_id"] in {"p037", "p038"}
    )

    graph = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p037_p038_graph_model.json").read_text(encoding="utf-8")
    )
    assert len(graph["instance_facts"]) == 2
    assert not any(
        fact["subject"].lower().endswith(("laptop", "corporateapplication"))
        for fact in graph["subclass_facts"]
    )
    assert graph["restrictions"] == []


def test_p037_p038_projects_example_participants_as_individuals_and_keeps_stage_types(tmp_path: Path):
    import json

    _metrics(tmp_path)
    pipeline_dir = _CASE_DIR / "artifacts" / "pipeline_outputs"
    taxonomy = json.loads(
        (pipeline_dir / "observed_p037_p038_13_taxonomy_induction.json").read_text(encoding="utf-8")
    )
    type_stage = json.loads(
        (pipeline_dir / "observed_p037_p038_14_type_assertion.json").read_text(encoding="utf-8")
    )
    quality = json.loads(
        (pipeline_dir / "observed_p037_p038_15_semantic_quality.json").read_text(encoding="utf-8")
    )["semantic_quality_report"]

    assert taxonomy["taxonomy_relations"] == []
    assert {
        (item["instance"], item["class"])
        for item in type_stage["type_assertions"]
    } == {("laptop", "endpoint"), ("corporate application", "web application")}
    assert quality["semantic_integrity_checks"]["canonical_types_projected"]
    assert quality["semantic_integrity_checks"]["instance_taxonomy_consistent"]
    assert quality["quality_score"] < 1.0
    assert "concept_noise_detected" in quality["warnings"]

    graph = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p037_p038_graph_model.json").read_text(encoding="utf-8")
    )
    class_iris = {item["iri"] for item in graph["classes"]}
    instance_iris = {item["subject"] for item in graph["instance_facts"]}
    illustrative_participants = {
        endpoint
        for fact in graph["facts"]
        if fact.get("observation_scope") == "illustrative_example"
        for endpoint in (fact["subject"], fact["object"])
    }

    assert instance_iris == {"orion:laptop", "orion:corporate-application"}
    assert class_iris.isdisjoint(instance_iris)
    assert class_iris.isdisjoint(illustrative_participants)
    assert "orion:Laptop" not in class_iris
    assert "orion:CustomerDatabase" not in class_iris
