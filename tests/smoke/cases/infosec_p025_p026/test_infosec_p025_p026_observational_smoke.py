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
_PARAGRAPH_IDS = ['p025', 'p026']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p025_p026_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P025_P026 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p025_p026_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P025_P026 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p025_p026_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P025_P026 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_p025_p026_audited_deontic_roles_and_complements_are_preserved(tmp_path: Path):
    _metrics(tmp_path)
    payload = json.loads((_CASE_DIR / "artifacts" / "observed_p025_p026_semantic_claims.json").read_text(encoding="utf-8"))
    claims = [item for item in payload.get("claims", []) if isinstance(item, dict)]

    contract = next(item for item in claims if item.get("subject") == "Contract")
    assert (contract.get("predicate"), contract.get("object")) == ("defines", "Obligation")
    assert (contract.get("participant_a"), contract.get("participant_b")) == ("Organization", "Supplier")
    assert not any(item.get("subject") == "Contract" and item.get("object") == "Supplier" for item in claims)

    alternatives = [item for item in claims if item.get("subject") == "Supplier" and item.get("predicate") == "provides"]
    assert {item.get("object") for item in alternatives} == {"Good", "Service"}
    assert len({item.get("alternative_group") for item in alternatives}) == 1

    access_claims = [item for item in claims if item.get("subject") in {"ThirdPartyAccess", "PhysicalAccess"}]
    assert len(access_claims) == 5
    assert all(item.get("modality") == "must" for item in access_claims)
    revoked = next(item for item in access_claims if item.get("predicate") == "beRevoked")
    assert revoked.get("condition") == "ThirdPartyAccess is no longer required"

    environmental = [item for item in claims if item.get("subject") == "EnvironmentalControl"]
    assert any(item.get("object") == "Equipment" for item in environmental)
    assert {item.get("object") for item in environmental if item.get("predicate") == "protects_against"} == {
        "Fire", "Humidity", "Temperature", "PowerFailure",
    }


def test_p025_p026_deontic_claims_are_scoped_not_materialized_as_facts(tmp_path: Path):
    _metrics(tmp_path)
    graph = json.loads((_CASE_DIR / "artifacts" / "observed_p025_p026_graph_model.json").read_text(encoding="utf-8"))
    scoped_subjects = {
        str(item.get("subject", "")).rsplit("/", 1)[-1].split(":", 1)[-1].lower()
        for item in graph.get("scoped_relations", [])
    }
    assert {"thirdpartyaccess", "physicalaccess"}.issubset(scoped_subjects)
    assert graph.get("restrictions") == []
