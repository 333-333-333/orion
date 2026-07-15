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
_PARAGRAPH_IDS = ['p017', 'p018']
_METRICS: dict[str, Any] | None = None
_ARTIFACT_DIR = _CASE_DIR / "artifacts"


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p017_p018_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P017_P018 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p017_p018_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P017_P018 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p017_p018_subjects_sources_destinations_and_key_coordination_are_faithful(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p017_p018_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p017_p018_graph_model.json").read_text(encoding="utf-8"))
    claims = semantic["claims"]
    observed = {(claim.get("subject"), claim.get("predicate"), claim.get("object")) for claim in claims}

    assert ("CloudAccessSecurityBroker", "monitors", "CloudServiceUsage") in observed
    assert ("CloudAccessSecurityBroker", "controls", "CloudServiceUsage") in observed
    assert ("CloudIdentity", "used_to_access", "CloudService") in observed
    assert ("CryptographicKey", "used_by", "CryptographicAlgorithm") in observed
    assert ("HashFunction", "uses", "InputData") in observed
    assert ("AsymmetricEncryption", "uses", "PublicKey") in observed
    assert ("AsymmetricEncryption", "uses", "PrivateKey") in observed
    conversion = next(claim for claim in claims if claim.get("subject") == "Decryption" and claim.get("predicate") == "converts")
    assert conversion["object"] == "EncryptedData"
    assert conversion["target"] == "ReadableData"
    assert not ({"Cloud", "SecurityBrokerMonitor", "PublicKeyAndAPrivateKey", "EncryptedDataBackIntoReadableData"} & {
        str(claim.get(endpoint)) for claim in claims for endpoint in ("subject", "object")
    })
    graph_classes = {item.get("label") for item in graph.get("classes", [])}
    assert "SecurityBrokerMonitor" not in graph_classes
    assert any(item.get("target") == "orion:ReadableData" for item in graph.get("facts", []))


def test_p017_p018_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P017_P018 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0
