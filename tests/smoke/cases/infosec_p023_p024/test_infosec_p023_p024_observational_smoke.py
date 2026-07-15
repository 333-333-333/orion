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
_PARAGRAPH_IDS = ['p023', 'p024']
_METRICS: dict[str, Any] | None = None
_ARTIFACT_DIR = _CASE_DIR / "artifacts"


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p023_p024_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P023_P024 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p023_p024_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P023_P024 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p023_p024_conditions_temporal_scope_and_definition_content_are_preserved(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p023_p024_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p023_p024_graph_model.json").read_text(encoding="utf-8"))
    claims = semantic["claims"]
    observed = {(claim.get("subject"), claim.get("predicate"), claim.get("object")) for claim in claims}

    assert ("UnauthorizedAccess", "involves", "Access") in observed
    assert ("InsiderMisuse", "caused_by", "InternalActor") in observed
    assert ("BusinessContinuity", "continues", "CriticalOperation") in observed
    assert ("DisasterRecovery", "restores", "TechnologyService") in observed
    assert {("BusinessImpactAnalysis", "identifies", obj) for obj in ("CriticalProcess", "Dependency", "RecoveryPriority")} <= observed
    assert ("Backup", "used_for", "Recovery") in observed
    assert not any(claim.get("subject") == "Capability" and claim.get("predicate") == "continues" for claim in claims)
    assert not any(claim.get("object") == "WhetherRecoveryProcedureWorkAsExpected" for claim in claims)
    test_claim = next(claim for claim in claims if claim.get("subject") == "DisasterRecoveryTest")
    assert test_claim["object"] == "RecoveryProcedure"
    assert test_claim["modality"] == "whether"
    assert test_claim["expected_state"] == "as_expected"
    assert any(item.get("temporal_relation") == "during" for item in graph.get("scoped_relations", []))
    assert any(item.get("modality") == "whether" and item.get("expected_state") == "as_expected" for item in graph.get("scoped_relations", []))


def test_p023_p024_collective_subject_and_backup_attachment_remain_scoped(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p023_p024_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p023_p024_graph_model.json").read_text(encoding="utf-8"))
    quality = json.loads(
        (_ARTIFACT_DIR / "pipeline_outputs" / "observed_p023_p024_15_semantic_quality.json").read_text(encoding="utf-8")
    )["semantic_quality_report"]
    rdf = (_ARTIFACT_DIR / "observed_p023_p024_output.rdf").read_text(encoding="utf-8")
    claims = semantic["claims"]

    protection = [claim for claim in claims if claim.get("predicate") == "protects"]
    assert len(protection) == 1
    assert protection[0]["subject"] == "BusinessContinuityAndDisasterRecovery"
    assert protection[0]["coordination_scope"] == "subject"
    assert protection[0]["members"] == "BusinessContinuity,DisasterRecovery"
    assert protection[0]["projection_scope"] == "scoped"

    backup_use = next(
        claim
        for claim in claims
        if claim.get("subject") == "Backup" and claim.get("predicate") == "used_for"
    )
    assert backup_use["interpretation_status"] == "ambiguous_attachment"
    assert backup_use["attachment_scope"] == "unresolved"
    assert backup_use["candidate_subjects"] == "Backup,CopyOfData,Data"
    assert backup_use["projection_scope"] == "scoped"
    assert quality["semantic_ambiguities"]
    assert "source_ambiguity_preserved" in quality["warnings"]
    assert quality["quality_score"] < 1.0
    assert quality["semantic_integrity_checks"]["ambiguous_interpretations_scoped"]

    assert not any(
        item.get("predicate", "").rsplit(":", 1)[-1] in {"protects", "usedFor"}
        for item in graph.get("facts", [])
    )
    qualified_dispositions = {
        row["claim_id"]
        for row in graph["projection"]["claim_dispositions"]
        if row.get("reason") == "represented_as_qualified_rdf_statement"
    }
    assert {protection[0]["claim_id"], backup_use["claim_id"]} <= qualified_dispositions
    assert "<meta:coordinationScope>subject</meta:coordinationScope>" in rdf
    assert "<meta:interpretationStatus>ambiguous_attachment</meta:interpretationStatus>" in rdf


def test_p023_p024_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P023_P024 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def test_p023_p024_disjunction_and_identity_participant_keep_explicit_roles(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p023_p024_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p023_p024_graph_model.json").read_text(encoding="utf-8"))
    rdf = (_ARTIFACT_DIR / "observed_p023_p024_output.rdf").read_text(encoding="utf-8")

    alternatives = [
        claim
        for claim in semantic["claims"]
        if claim.get("subject") == "DataBreach" and claim.get("alternative_group")
    ]
    assert {claim["object"] for claim in alternatives} == {"UnauthorizedAccess", "Disclosure"}
    assert all(claim.get("patient") == "Data" for claim in alternatives)
    assert all(claim.get("coordination_ellipsis") == "shared_object" for claim in alternatives)
    assert any(
        claim.get("subject") == "Access"
        and claim.get("predicate") == "has_actor"
        and claim.get("object") == "UnapprovedIdentity"
        for claim in semantic["claims"]
    )

    graph_alternatives = graph["logical_alternatives"][0]["alternatives"]
    assert all(item.get("patient") == "orion:Data" for item in graph_alternatives)
    assert "orion:UnapprovedIdentity" in {item["iri"] for item in graph["classes"]}
    assert any(
        item.get("subject") == "orion:Access"
        and item.get("predicate") == "orion:hasActor"
        and item.get("object") == "orion:UnapprovedIdentity"
        for item in graph["facts"]
    )
    assert "hasActor" in rdf and "UnapprovedIdentity" in rdf


def test_p023_p024_unresolved_scope_does_not_create_ontology_commitments(tmp_path: Path):
    _metrics(tmp_path)
    graph = json.loads((_ARTIFACT_DIR / "observed_p023_p024_graph_model.json").read_text(encoding="utf-8"))

    class_iris = {item["iri"] for item in graph["classes"]}
    assert "orion:BusinessContinuityAndDisasterRecovery" not in class_iris
    protection = next(item for item in graph["scoped_relations"] if item.get("relation_role") == "coordinated_subject")
    assert protection["members"] == ["orion:BusinessContinuity", "orion:DisasterRecovery"]
    backup_use = next(item for item in graph["scoped_relations"] if item.get("attachment_scope") == "unresolved")
    assert backup_use["candidate_subjects"] == "Backup,CopyOfData,Data"

    scoped_schema = {
        row["predicate"]: row
        for row in graph["object_property_schema"]
        if row["predicate"] in {"orion:protects", "orion:usedFor"}
    }
    assert scoped_schema["orion:protects"]["scoped_pairs"] == []
    assert scoped_schema["orion:usedFor"]["scoped_pairs"] == []
    assert scoped_schema["orion:usedFor"]["observed_pairs"] == []


def test_p023_p024_quality_gate_validates_roles_refs_and_ambiguity_confidence(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p023_p024_semantic_claims.json").read_text(encoding="utf-8"))
    triples_payload = json.loads(
        (_ARTIFACT_DIR / "pipeline_outputs" / "observed_p023_p024_12_triple_extraction.json").read_text(encoding="utf-8")
    )
    quality = json.loads(
        (_ARTIFACT_DIR / "pipeline_outputs" / "observed_p023_p024_15_semantic_quality.json").read_text(encoding="utf-8")
    )["semantic_quality_report"]

    repaired_ids = {
        claim["claim_id"]
        for claim in semantic["claims"]
        if claim.get("extracted_by") == "RULE-SEMANTIC-REMEDIATION-D3-001"
    }
    repaired_triples = [triple for triple in triples_payload["triples"] if triple.get("relation_id") in repaired_ids]
    assert len(repaired_triples) == len(repaired_ids)
    assert all(
        len({triple.get("subject_ref"), triple.get("predicate_ref"), triple.get("object_ref")}) == 3
        for triple in repaired_triples
    )
    ambiguous = next(triple for triple in repaired_triples if triple.get("attachment_scope") == "unresolved")
    assert ambiguous["confidence"] == 0.65
    checks = quality["semantic_integrity_checks"]
    assert checks["required_claim_roles_complete"]
    assert checks["claim_term_references_distinct"]
    assert not any(gap.startswith(("required_claim_roles_missing", "claim_term_references_conflated")) for gap in quality["relation_gaps"])


def test_p023_p024_ambiguous_type_and_anonymous_referent_do_not_become_classes(tmp_path: Path):
    _metrics(tmp_path)
    semantic = json.loads((_ARTIFACT_DIR / "observed_p023_p024_semantic_claims.json").read_text(encoding="utf-8"))
    graph = json.loads((_ARTIFACT_DIR / "observed_p023_p024_graph_model.json").read_text(encoding="utf-8"))
    quality = json.loads(
        (_ARTIFACT_DIR / "pipeline_outputs" / "observed_p023_p024_15_semantic_quality.json").read_text(encoding="utf-8")
    )["semantic_quality_report"]
    rdf = (_ARTIFACT_DIR / "observed_p023_p024_output.rdf").read_text(encoding="utf-8")

    lost_device = next(
        claim for claim in semantic["claims"]
        if claim.get("subject") == "LostDeviceIncident" and claim.get("predicate") == "is_a"
    )
    assert lost_device["extracted_by"] == "RULE-SEMANTIC-REMEDIATION-D4-001"
    assert lost_device["interpretation_status"] == "ambiguous_coordination"
    assert lost_device["coordination_scope"] == "object_type_modifiers"
    assert lost_device["coordination_members"] == "Physical,InformationSecurity"
    assert lost_device["candidate_interpretations"] == "compound_type,coordinated_type_modifiers"
    assert lost_device["projection_scope"] == "scoped"
    assert lost_device["rdf_projection"] == "qualified_statement"

    class_iris = {item["iri"] for item in graph["classes"]}
    assert "orion:PhysicalAndInformationSecurityIncident" not in class_iris
    assert "orion:Organization" not in class_iris
    assert not any(
        item.get("subject") == "orion:LostDeviceIncident"
        and item.get("predicate") == "rdfs:subClassOf"
        for item in graph["subclass_facts"]
    )

    scoped_lost_device = next(item for item in graph["scoped_relations"] if item.get("claim_id") == lost_device["claim_id"])
    assert scoped_lost_device["object_resource_kind"] == "unresolved_type_expression"
    assert scoped_lost_device["candidate_interpretations"] == "compound_type,coordinated_type_modifiers"
    assert any(item.get("claim_id") == lost_device["claim_id"] for item in quality["semantic_ambiguities"])

    protection = next(item for item in graph["scoped_relations"] if item.get("relation_role") == "coordinated_subject")
    assert protection["object"] == "orion:organization"
    assert protection["object_resource_kind"] == "anonymous_referent"
    assert protection["object_quantification"] == "definite"

    assert '<owl:Class rdf:about="https://orion.local/resource/Organization">' not in rdf
    assert '<owl:Class rdf:about="https://orion.local/resource/PhysicalAndInformationSecurityIncident">' not in rdf
    assert "<meta:candidateInterpretations>compound_type,coordinated_type_modifiers</meta:candidateInterpretations>" in rdf
    assert "<meta:objectResourceKind>anonymous_referent</meta:objectResourceKind>" in rdf
