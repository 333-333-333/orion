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
_PARAGRAPH_IDS = ['p013', 'p014']
_METRICS: dict[str, Any] | None = None
_ARTIFACT_DIR = _CASE_DIR / "artifacts"


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p013_p014_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P013_P014 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p013_p014_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P013_P014 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p013_p014_roles_and_coordinated_mechanisms_remain_structured(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p013_p014_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p013_p014_graph_model.json").read_text(encoding="utf-8"))
    claims = semantic["claims"]
    observed = {(claim.get("subject"), claim.get("predicate"), claim.get("object")) for claim in claims}

    assert ("VirtualPrivateNetwork", "creates", "EncryptedCommunicationTunnel") in observed
    assert ("NetworkSegmentation", "separates", "System") in observed
    assert ("ManagementNetwork", "used_for", "AdministrativeAccess") in observed
    assert ("Endpoint", "connected_to", "OrganizationalNetwork") in observed
    assert ("ConfigurationHardening", "disables", "UnnecessaryService") in observed
    assert ("ConfigurationHardening", "applies", "SecureSetting") in observed
    assert not any(claim.get("object") == "NetworkAccessControlSystem" and claim.get("predicate") == "separates" for claim in claims)
    assert not ({"creats", "disabls"} & {str(claim.get("predicate")) for claim in claims})
    assert any(item.get("target") == "orion:DifferentZone" for item in graph.get("facts", []))
    assert not any(item.get("predicate") in {"orion:creats", "orion:disabls"} for item in graph.get("facts", []))


def test_p013_p014_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P013_P014 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0
