from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p011', 'p012']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p011_p012_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P011_P012 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p011_p012_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P011_P012 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p011_p012_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P011_P012 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_p011_p012_preserves_normative_alternative_and_condition_scope(tmp_path: Path):
    import json

    _metrics(tmp_path)
    claims_payload = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p011_p012_semantic_claims.json").read_text(encoding="utf-8")
    )
    claims = claims_payload["claims"]
    spo = {(claim["subject"], claim["predicate"], claim["object"]) for claim in claims}

    assert ("IdentityAndAccessManagement", "controls", "Lifecycle") in spo
    assert not any(claim["subject"] == "IdentityAnd" or claim["predicate"] == "access" for claim in claims)
    deprovisioning = [claim for claim in claims if claim["subject"] == "UserDeprovisioning"]
    assert {claim["predicate"] for claim in deprovisioning} == {"disables", "removes"}
    assert len({claim["alternative_group"] for claim in deprovisioning}) == 1
    assert all(claim["condition_polarity"] == "negative" for claim in deprovisioning)
    assert any(claim.get("modality") == "must" and claim.get("quantifier") == "only" for claim in claims)

    graph = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p011_p012_graph_model.json").read_text(encoding="utf-8")
    )
    assert graph["logical_alternatives"]
    assert graph["restrictions"] == []


def test_p011_p012_keeps_generic_access_and_modifier_condition_targets(tmp_path: Path):
    import json

    _metrics(tmp_path)
    claims = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p011_p012_semantic_claims.json").read_text(encoding="utf-8")
    )["claims"]
    p012_access_claims = [
        claim for claim in claims
        if claim["paragraph_id"] == "p012" and claim["subject"] in {
            "UserDeprovisioning", "AccessCertification", "JoinerProcess", "MoverProcess", "LeaverProcess"
        }
    ]

    assert p012_access_claims
    assert {claim["object"] for claim in p012_access_claims} == {"Access"}
    assert not any(claim["object"] == "DormantAccountAccess" for claim in p012_access_claims)
    assert all(
        claim.get("condition_object") == "Access"
        for claim in p012_access_claims
        if claim["subject"] == "UserDeprovisioning"
    )
    joiner = next(claim for claim in p012_access_claims if claim["subject"] == "JoinerProcess")
    assert joiner["qualifier"] == "new"
    assert joiner["qualifier_target"] == "Employee"

    graph = json.loads(
        (_CASE_DIR / "artifacts" / "observed_p011_p012_graph_model.json").read_text(encoding="utf-8")
    )
    projected_access_objects = [
        item.get("object")
        for collection in (graph["facts"], graph["scoped_relations"])
        for item in collection
        if item.get("subject") in {
            "orion:UserDeprovisioning", "orion:AccessCertification", "orion:JoinerProcess",
            "orion:MoverProcess", "orion:LeaverProcess",
        }
    ]
    projected_access_objects.extend(
        item["object"]
        for group in graph["logical_alternatives"]
        for item in group["alternatives"]
        if item["subject"] == "orion:UserDeprovisioning"
    )
    assert projected_access_objects and set(projected_access_objects) == {"orion:Access"}
    assert {item.get("condition_object") for item in graph["scoped_relations"] if item.get("condition")} >= {
        "orion:Role", "orion:Organization"
    }
