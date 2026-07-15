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
_PARAGRAPH_IDS = ['p009', 'p010']
_METRICS: dict[str, Any] | None = None
_ARTIFACT_DIR = _CASE_DIR / "artifacts"


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p009_p010_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P009_P010 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p009_p010_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P009_P010 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p009_p010_quantifiers_definitions_and_causal_roles_survive_projection(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p009_p010_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p009_p010_graph_model.json").read_text(encoding="utf-8"))
    claims = semantic["claims"]
    observed = {(claim.get("subject"), claim.get("predicate"), claim.get("object")) for claim in claims}

    assert ("Credential", "used_to_prove", "Identity") in observed
    assert ("Application", "authenticates", "Request") in observed
    assert ("StolenPassword", "causes", "UnauthorizedAccess") in observed
    assert any(
        claim.get("subject") == "MultiFactorAuthentication"
        and claim.get("predicate") == "requires"
        and claim.get("object") == "VerificationFactor"
        and claim.get("quantifier") == "more_than_one"
        for claim in claims
    )
    assert {"based_on"} <= {claim.get("predicate") for claim in claims}
    assert not {"ThanOneVerificationFactor", "Periodically", "Immediately"} & {
        str(claim.get(endpoint))
        for claim in claims
        if claim.get("visibility") != "internal"
        for endpoint in ("subject", "object")
    }
    graph_classes = {item.get("label") for item in graph.get("classes", [])}
    assert not {"ThanOneVerificationFactor", "Periodically", "Immediately"} & graph_classes
    assert any(item.get("modality") == "must" for item in graph.get("scoped_relations", []))


def test_p009_p010_obligations_and_indefinite_factor_bases_are_qualified(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p009_p010_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p009_p010_graph_model.json").read_text(encoding="utf-8"))
    rdf = (_ARTIFACT_DIR / "observed_p009_p010_output.rdf").read_text(encoding="utf-8")
    claims = semantic["claims"]

    obligations = [
        claim
        for claim in claims
        if claim.get("modality") == "must" and claim.get("rdf_projection") == "qualified_statement"
    ]
    assert len(obligations) == 5
    compatibility = [claim for claim in claims if claim.get("compatibility_only")]
    assert len(compatibility) == 3
    assert all(claim.get("visibility") == "internal" and claim.get("projection") == "internal" for claim in compatibility)

    factor_bases = [claim for claim in claims if claim.get("predicate") == "based_on"]
    assert len(factor_bases) == 3
    assert {claim.get("object") for claim in factor_bases} == {"Something"}
    assert all(claim.get("filler_kind") == "indefinite" for claim in factor_bases)
    assert all(claim.get("filler_quantification") == "existential" for claim in factor_bases)
    assert not any(
        str(claim.get(endpoint, "")).startswith(("UserKnowledge", "UserPossession", "UserInherence"))
        for claim in claims
        for endpoint in ("subject", "object")
    )

    qualified_ids = {
        claim["claim_id"]
        for claim in claims
        if claim.get("rdf_projection") == "qualified_statement"
    }
    qualified_dispositions = {
        row["claim_id"]
        for row in graph["projection"]["claim_dispositions"]
        if row.get("reason") == "represented_as_qualified_rdf_statement"
    }
    assert qualified_ids <= qualified_dispositions
    assert rdf.count("<rdf:Statement ") >= len(qualified_ids)
    assert "<meta:modality>must</meta:modality>" in rdf
    assert "<meta:quantifier>more_than_one</meta:quantifier>" in rdf


def test_p009_p010_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P009_P010 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0
