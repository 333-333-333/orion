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
_PARAGRAPH_IDS = ['p041', 'p042']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p041_p042_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P041_P042 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p041_p042_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P041_P042 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def _artifact_json(name: str) -> dict[str, Any]:
    return json.loads((_CASE_DIR / "artifacts" / name).read_text(encoding="utf-8"))


def test_p041_p042_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P041_P042 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_p042_subclasses_of_information_asset_emit_direct_taxonomy(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P041_P042 | AC-P042-TAXONOMY-001 | BR-INFOSEC-PAIR-SMOKE-003
    _metrics(tmp_path)
    semantic = _artifact_json("observed_p041_p042_semantic_claims.json")
    graph = _artifact_json("observed_p041_p042_graph_model.json")

    expected = {
        ("ConfidentialDocument", "InformationAsset"),
        ("CorporateDatabase", "InformationAsset"),
        ("CustomerRecord", "InformationAsset"),
        ("SourceCodeRepository", "InformationAsset"),
    }
    claims = {
        (str(claim.get("subject")), str(claim.get("object")))
        for claim in semantic.get("claims", [])
        if claim.get("paragraph_id") == "p042" and claim.get("predicate") in {"is_a", "type_of"}
    }
    subclass_facts = {
        (str(fact.get("subject", "")).rsplit(":", 1)[-1], str(fact.get("object", "")).rsplit(":", 1)[-1])
        for fact in graph.get("subclass_facts", [])
        if fact.get("predicate") == "rdfs:subClassOf"
    }
    bad_labels = {
        str(value)
        for item in [*semantic.get("claims", []), *graph.get("classes", [])]
        for value in (item.get("subject"), item.get("object"), item.get("label"))
        if value in {
            "ConfidentialDocumentCorporateDatabaseCustomerRecordAndSourceCodeRepositoryAre",
            "OfInformationAsset",
        }
    }

    assert expected <= claims
    assert expected <= subclass_facts
    assert not bad_labels
    assert not any(claim.get("predicate") == "subclasses" for claim in semantic.get("claims", []))


def test_p041_p042_visual_ttl_serializes_information_asset_subclasses(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P041_P042 | AC-P042-TTL-SUBCLASS-001 | BR-INFOSEC-PAIR-SMOKE-003
    _metrics(tmp_path)
    ttl = (_CASE_DIR / "artifacts" / "observed_p041_p042_output.ttl").read_text(encoding="utf-8")

    expected_triples = {
        "orion:ConfidentialDocument rdfs:subClassOf orion:InformationAsset .",
        "orion:CorporateDatabase rdfs:subClassOf orion:InformationAsset .",
        "orion:CustomerRecord rdfs:subClassOf orion:InformationAsset .",
        "orion:SourceCodeRepository rdfs:subClassOf orion:InformationAsset .",
    }
    observed_triples = {
        line.strip()
        for line in ttl.splitlines()
        if " rdfs:subClassOf " in line and "orion:InformationAsset" in line
    }

    assert expected_triples <= observed_triples
    assert len(expected_triples) == len(observed_triples)


def test_p041_p042_filters_orion_meta_instruction_from_semantics_graph_and_ttl(tmp_path: Path):
    # TASK-INFOSEC-P042-META-FILTER | AC-P042-META-FILTER-001 | BR-INFOSEC-PAIR-SMOKE-003
    _metrics(tmp_path)
    semantic = _artifact_json("observed_p041_p042_semantic_claims.json")
    graph = _artifact_json("observed_p041_p042_graph_model.json")
    ttl = (_CASE_DIR / "artifacts" / "observed_p041_p042_output.ttl").read_text(encoding="utf-8")

    forbidden_subject = "OrionShouldBeAbleToIdentifySecurityConceptClassifyHierarchicalRelationshipAndExtractMeaningful"
    forbidden_triple = "orion:orionshouldbeabletoidentifysecurityconceptclassifyhierarchicalrelationshipandextractmeaningful orion:relationships orion:thistext ."

    forbidden_claims = [
        claim
        for claim in semantic.get("claims", [])
        if str(claim.get("paragraph_id")) == "p042"
        and str(claim.get("subject")) == forbidden_subject
        and str(claim.get("predicate")) == "relationships"
        and str(claim.get("object")) == "ThisText"
    ]
    forbidden_facts = [
        fact
        for fact in graph.get("facts", [])
        if str(fact.get("subject", "")).endswith(forbidden_subject)
        and str(fact.get("predicate", "")).endswith("relationships")
        and str(fact.get("object", "")).endswith("ThisText")
    ]

    assert forbidden_claims == []
    assert forbidden_facts == []
    assert forbidden_triple not in ttl
