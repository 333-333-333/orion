from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys
import xml.etree.ElementTree as ET

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p039', 'p040']
_METRICS: dict[str, Any] | None = None


_RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
_RDFS_NS = "http://www.w3.org/2000/01/rdf-schema#"
_OWL_NS = "http://www.w3.org/2002/07/owl#"
_ORION_NS = "https://orion.local/resource/"
_NS = {"rdf": _RDF_NS, "rdfs": _RDFS_NS, "owl": _OWL_NS}


def _artifact_path(name: str) -> Path:
    return _CASE_DIR / "artifacts" / name


def _rdf_root() -> ET.Element:
    return ET.parse(_artifact_path("observed_p039_p040_output.rdf")).getroot()


def _ttl_text() -> str:
    return _artifact_path("observed_p039_p040_output.ttl").read_text(encoding="utf-8")


def _has_direct_orion_triple(root: ET.Element, subject: str, predicate: str, obj: str) -> bool:
    subject_iri = f"{_ORION_NS}{subject}"
    object_iri = f"{_ORION_NS}{obj}"
    predicate_tag = f"{{{_ORION_NS}}}{predicate}"
    for desc in root.findall("rdf:Description", _NS):
        if desc.attrib.get(f"{{{_RDF_NS}}}about") != subject_iri:
            continue
        for child in desc:
            if child.tag == predicate_tag and child.attrib.get(f"{{{_RDF_NS}}}resource") == object_iri:
                return True
    return False


_PHISHING_SCENARIO_EVIDENCE = "A phishing scenario illustrates how threats, vulnerabilities, controls, and incidents relate to each other."
_PHISHING_SCENARIO_RELATIONS = {
    ("PhishingScenario", "illustrates", "Threat"),
    ("PhishingScenario", "illustrates", "Vulnerability"),
    ("PhishingScenario", "illustrates", "Control"),
    ("PhishingScenario", "illustrates", "Incident"),
}
_EVENT_MODAL_COORDINATION_EVIDENCE = "The event affects availability and may affect integrity."
_EVENT_MODAL_COORDINATION_RELATIONS = {
    ("Event", "affects", "Availability"),
    ("Event", "mayAffect", "Integrity"),
}
_FORBIDDEN_MODAL_COORDINATION_NODE = "MayAffectIntegrity"
_CORRECTIVE_ACTIONS_EVIDENCE = "Corrective actions may include patch deployment, privilege reduction, and improved detection rules."
_CORRECTIVE_ACTIONS_RELATIONS = {
    ("Corrective", "actions", "PatchDeployment"),
    ("Corrective", "actions", "PrivilegeReduction"),
    ("Corrective", "actions", "ImprovedDetectionRule"),
}
_FORBIDDEN_CORRECTIVE_ACTIONS_NODE = "MayIncludePatchDeployment"
_LOG_MONITORING_EVIDENCE = "Log monitoring may identify suspicious login activity."
_LOG_MONITORING_RELATIONS = {("LogMonitoring", "mayIdentify", "SuspiciousLoginActivity")}
_POST_INCIDENT_REVIEW_EVIDENCE = "The post-incident review may identify missing patches, weak access controls, or insufficient monitoring."
_POST_INCIDENT_REVIEW_RELATIONS = {
    ("PostIncidentReview", "mayIdentify", "MissingPatch"),
    ("PostIncidentReview", "mayIdentify", "WeakAccessControl"),
    ("PostIncidentReview", "mayIdentify", "InsufficientMonitoring"),
}
_SECURITY_AWARENESS_TRAINING_EVIDENCE = "Security awareness training may reduce the likelihood of clicking the malicious link."
_SECURITY_AWARENESS_TRAINING_RELATIONS = {("SecurityAwarenessTraining", "mayReduce", "MaliciousLinkClickingLikelihood")}
_FORBIDDEN_SECURITY_AWARENESS_TRAINING_OBJECT = "LikelihoodOfClickingTheMaliciousLink"
_COMPROMISED_CREDENTIAL_EVIDENCE = "The attacker uses the compromised credential to access a cloud account."
_COMPROMISED_CREDENTIAL_RELATIONS = {
    ("Attacker", "uses", "CompromisedCredential"),
    ("CompromisedCredential", "accesses", "CloudAccount"),
}
_FORBIDDEN_OBSERVATIONAL_NODES = {
    "LogMonitoringMayIdentify",
    "PostIncidentReviewMayIdentify",
    "SecurityAwarenessTrainingMayReduce",
    "SecurityAwarenessTrainingmayReduceTheLikelihoodOfClickingTheMaliciousLink",
    _FORBIDDEN_SECURITY_AWARENESS_TRAINING_OBJECT,
    "CompromisedCredentialToAccessACloudAccount",
}
_FORBIDDEN_OBSERVATIONAL_PREDICATES = {"suspicious", "access"}


def _semantic_claims() -> list[dict[str, Any]]:
    payload = json.loads(_artifact_path("observed_p039_p040_semantic_claims.json").read_text(encoding="utf-8"))
    claims = payload.get("claims")
    return [claim for claim in claims if isinstance(claim, dict)] if isinstance(claims, list) else []


def _graph_facts() -> list[dict[str, Any]]:
    graph = json.loads(_artifact_path("observed_p039_p040_graph_model.json").read_text(encoding="utf-8"))
    facts = graph.get("facts")
    return [fact for fact in facts if isinstance(fact, dict)] if isinstance(facts, list) else []


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p039_p040_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p039_p040_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p039_p040_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["claim_count"] > 0



def test_p039_p040_rdf_visual_uses_direct_facts_not_predicate_bridge_nodes(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | CON-RDF-VISIBILITY AC-2 | BR-INFOSEC-PAIR-SMOKE-003
    _metrics(tmp_path)
    root = _rdf_root()

    assert _has_direct_orion_triple(root, "submittedpassword", "becomes", "compromisedcredential")
    assert _has_direct_orion_triple(root, "fileserver", "becomes", "unavailabletobusinessuser")

    becomes_iri = f"{_ORION_NS}becomes"
    becomes_properties = [
        prop for prop in root.findall("owl:ObjectProperty", _NS)
        if prop.attrib.get(f"{{{_RDF_NS}}}about") == becomes_iri
    ]
    assert not becomes_properties
    assert root.findall("rdf:Statement", _NS) == []
    assert root.findall(".//owl:Restriction", _NS) == []
    assert all(f"{{{_RDF_NS}}}nodeID" not in element.attrib for element in root.iter())


def test_p039_p040_visual_artifact_is_turtle_with_direct_triples(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | CON-RDF-VISIBILITY AC-5 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)
    ttl = _ttl_text()

    assert metrics["ttl_generated"]
    assert metrics["ttl_bytes"] > 0
    assert "@prefix orion: <https://orion.local/resource/> ." in ttl
    assert "orion:submittedpassword orion:becomes orion:compromisedcredential ." in ttl
    assert "orion:fileserver orion:becomes orion:unavailabletobusinessuser ." in ttl
    assert "orion:phishingscenario orion:illustrates orion:threat ." in ttl
    assert "orion:phishingscenario orion:illustrates orion:vulnerability ." in ttl
    assert "orion:phishingscenario orion:illustrates orion:control ." in ttl
    assert "orion:phishingscenario orion:illustrates orion:incident ." in ttl
    assert "[]" not in ttl
    assert "rdf:Statement" not in ttl
    assert "owl:ObjectProperty" not in ttl


def test_p039_p040_relation_evidence_remains_in_sidecars(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | CON-SOURCE-EVIDENCE AC-2 | BR-INFOSEC-PAIR-SMOKE-002
    _metrics(tmp_path)
    graph = json.loads(_artifact_path("observed_p039_p040_graph_model.json").read_text(encoding="utf-8"))
    debug_ir = json.loads(_artifact_path("observed_p039_p040_semantic_debug_ir.json").read_text(encoding="utf-8"))

    graph_facts = graph.get("facts", [])
    assert any(
        fact.get("subject") == "orion:SubmittedPassword"
        and fact.get("predicate") == "orion:becomes"
        and fact.get("object") == "orion:CompromisedCredential"
        and fact.get("source_evidence") == "The submitted password becomes a compromised credential."
        for fact in graph_facts
    )
    assert any(
        fact.get("subject") == "orion:FileServer"
        and fact.get("predicate") == "orion:becomes"
        and fact.get("object") == "orion:UnavailableToBusinessUser"
        and fact.get("source_evidence") == "The file server becomes unavailable to business users."
        for fact in graph_facts
    )

    relations = debug_ir.get("relations", [])
    assert any(
        rel.get("subject") == "SubmittedPassword"
        and rel.get("predicate") == "becomes"
        and rel.get("object") == "CompromisedCredential"
        and rel.get("source", {}).get("evidence") == "The submitted password becomes a compromised credential."
        for rel in relations
    )
    assert any(
        rel.get("subject") == "FileServer"
        and rel.get("predicate") == "becomes"
        and rel.get("object") == "UnavailableToBusinessUser"
        and rel.get("source", {}).get("evidence") == "The file server becomes unavailable to business users."
        for rel in relations
    )


def test_p039_p040_event_modal_coordination_semantic_claims_use_shared_subject_direct_relation(tmp_path: Path):
    # TASK-NLP-MODAL-COORDINATION-P040 | FUN-NLP-MODAL-COORDINATION AC-1 | BR-NLP-MODAL-COORDINATION-001
    _metrics(tmp_path)
    claims = _semantic_claims()
    observed = {
        (claim.get("subject"), claim.get("predicate"), claim.get("object"))
        for claim in claims
        if claim.get("source", {}).get("evidence") == _EVENT_MODAL_COORDINATION_EVIDENCE
    }

    assert _EVENT_MODAL_COORDINATION_RELATIONS <= observed
    assert ("Event", "affects", _FORBIDDEN_MODAL_COORDINATION_NODE) not in observed
    assert all(claim.get("object") != _FORBIDDEN_MODAL_COORDINATION_NODE for claim in claims)
    assert all(claim.get("subject") != _FORBIDDEN_MODAL_COORDINATION_NODE for claim in claims)


def test_p039_p040_event_modal_coordination_graph_model_uses_direct_relation_not_node(tmp_path: Path):
    # TASK-NLP-MODAL-COORDINATION-P040 | CON-RDF-VISIBILITY AC-6 | BR-NLP-MODAL-COORDINATION-001
    _metrics(tmp_path)
    facts = _graph_facts()
    observed = {
        (fact.get("subject"), fact.get("predicate"), fact.get("object"))
        for fact in facts
        if fact.get("source_evidence") == _EVENT_MODAL_COORDINATION_EVIDENCE
    }
    expected = {
        (f"orion:{subject}", f"orion:{predicate}", f"orion:{obj}")
        for subject, predicate, obj in _EVENT_MODAL_COORDINATION_RELATIONS
    }

    assert expected <= observed
    assert ("orion:Event", "orion:affects", f"orion:{_FORBIDDEN_MODAL_COORDINATION_NODE}") not in observed
    assert all(fact.get("object") != f"orion:{_FORBIDDEN_MODAL_COORDINATION_NODE}" for fact in facts)
    assert all(fact.get("subject") != f"orion:{_FORBIDDEN_MODAL_COORDINATION_NODE}" for fact in facts)


def test_p039_p040_event_modal_coordination_rdf_and_ttl_use_direct_relation_not_node(tmp_path: Path):
    # TASK-NLP-MODAL-COORDINATION-P040 | CON-RDF-VISIBILITY AC-7 | BR-NLP-MODAL-COORDINATION-001
    _metrics(tmp_path)
    root = _rdf_root()
    ttl = _ttl_text()

    assert _has_direct_orion_triple(root, "event", "affects", "availability")
    assert _has_direct_orion_triple(root, "event", "mayaffect", "integrity")
    assert not _has_direct_orion_triple(root, "event", "affects", "mayaffectintegrity")
    assert "MayAffectIntegrity" not in ET.tostring(root, encoding="unicode")
    assert "orion:event orion:affects orion:availability ." in ttl
    assert "orion:event orion:mayaffect orion:integrity ." in ttl
    assert "mayaffectintegrity" not in ttl.casefold()


def test_p039_p040_phishing_scenario_semantic_claims_decompose_illustrates_how_list(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | FUN-INFOSEC-PAIR-SMOKE AC-4 | BR-INFOSEC-PAIR-SMOKE-004
    _metrics(tmp_path)
    claims = _semantic_claims()
    observed = {
        (claim.get("subject"), claim.get("predicate"), claim.get("object"))
        for claim in claims
        if claim.get("source", {}).get("evidence") == _PHISHING_SCENARIO_EVIDENCE
    }

    assert _PHISHING_SCENARIO_RELATIONS <= observed
    assert ("PhishingScenario", "incidents", "RelateToEachOther") not in observed
    assert all(claim.get("object") != "RelateToEachOther" for claim in claims)
    assert all(claim.get("predicate") != "incidents" for claim in claims)


def test_p039_p040_phishing_scenario_graph_model_uses_direct_illustrates_facts(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | CON-RDF-VISIBILITY AC-3 | BR-INFOSEC-PAIR-SMOKE-004
    _metrics(tmp_path)
    facts = _graph_facts()
    observed = {
        (fact.get("subject"), fact.get("predicate"), fact.get("object"))
        for fact in facts
        if fact.get("source_evidence") == _PHISHING_SCENARIO_EVIDENCE
    }
    expected = {
        (f"orion:{subject}", f"orion:{predicate}", f"orion:{obj}")
        for subject, predicate, obj in _PHISHING_SCENARIO_RELATIONS
    }

    assert expected <= observed
    assert ("orion:PhishingScenario", "orion:incidents", "orion:RelateToEachOther") not in observed
    assert all(fact.get("object") != "orion:RelateToEachOther" for fact in facts)
    assert all(fact.get("predicate") != "orion:incidents" for fact in facts)


def test_p039_p040_phishing_scenario_rdf_uses_direct_illustrates_triples(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P039_P040 | CON-RDF-VISIBILITY AC-4 | BR-INFOSEC-PAIR-SMOKE-004
    _metrics(tmp_path)
    root = _rdf_root()

    assert _has_direct_orion_triple(root, "phishingscenario", "illustrates", "threat")
    assert _has_direct_orion_triple(root, "phishingscenario", "illustrates", "vulnerability")
    assert _has_direct_orion_triple(root, "phishingscenario", "illustrates", "control")
    assert _has_direct_orion_triple(root, "phishingscenario", "illustrates", "incident")
    assert not _has_direct_orion_triple(root, "phishingscenario", "incidents", "relatetoeachother")
    incidents_iri = f"{_ORION_NS}incidents"
    assert all(
        prop.attrib.get(f"{{{_RDF_NS}}}about") != incidents_iri
        for prop in root.findall("owl:ObjectProperty", _NS)
    )

def test_p039_p040_corrective_actions_semantic_claims_use_direct_action_objects(tmp_path: Path):
    # TASK-NLP-MAY-INCLUDE-ACTIONS-P040 | FUN-NLP-MAY-INCLUDE-ACTIONS AC-1 | BR-NLP-MAY-INCLUDE-ACTIONS-001
    _metrics(tmp_path)
    claims = _semantic_claims()
    observed = {
        (claim.get("subject"), claim.get("predicate"), claim.get("object"))
        for claim in claims
        if claim.get("source", {}).get("evidence") == _CORRECTIVE_ACTIONS_EVIDENCE
    }

    assert _CORRECTIVE_ACTIONS_RELATIONS <= observed
    assert ("Corrective", "actions", _FORBIDDEN_CORRECTIVE_ACTIONS_NODE) not in observed
    assert all(claim.get("object") != _FORBIDDEN_CORRECTIVE_ACTIONS_NODE for claim in claims)
    assert all(claim.get("subject") != _FORBIDDEN_CORRECTIVE_ACTIONS_NODE for claim in claims)


def test_p039_p040_corrective_actions_graph_model_uses_direct_action_facts(tmp_path: Path):
    # TASK-NLP-MAY-INCLUDE-ACTIONS-P040 | CON-RDF-VISIBILITY AC-8 | BR-NLP-MAY-INCLUDE-ACTIONS-001
    _metrics(tmp_path)
    facts = _graph_facts()
    observed = {
        (fact.get("subject"), fact.get("predicate"), fact.get("object"))
        for fact in facts
        if fact.get("source_evidence") == _CORRECTIVE_ACTIONS_EVIDENCE
    }
    expected = {
        (f"orion:{subject}", f"orion:{predicate}", f"orion:{obj}")
        for subject, predicate, obj in _CORRECTIVE_ACTIONS_RELATIONS
    }

    assert expected <= observed
    assert ("orion:Corrective", "orion:actions", f"orion:{_FORBIDDEN_CORRECTIVE_ACTIONS_NODE}") not in observed
    assert all(fact.get("object") != f"orion:{_FORBIDDEN_CORRECTIVE_ACTIONS_NODE}" for fact in facts)
    assert all(fact.get("subject") != f"orion:{_FORBIDDEN_CORRECTIVE_ACTIONS_NODE}" for fact in facts)


def test_p039_p040_corrective_actions_rdf_and_ttl_use_direct_action_objects(tmp_path: Path):
    # TASK-NLP-MAY-INCLUDE-ACTIONS-P040 | CON-RDF-VISIBILITY AC-9 | BR-NLP-MAY-INCLUDE-ACTIONS-001
    _metrics(tmp_path)
    root = _rdf_root()
    ttl = _ttl_text()

    assert _has_direct_orion_triple(root, "corrective", "actions", "patchdeployment")
    assert _has_direct_orion_triple(root, "corrective", "actions", "privilegereduction")
    assert _has_direct_orion_triple(root, "corrective", "actions", "improveddetectionrule")
    assert not _has_direct_orion_triple(root, "corrective", "actions", "mayincludepatchdeployment")
    assert _FORBIDDEN_CORRECTIVE_ACTIONS_NODE not in ET.tostring(root, encoding="unicode")
    assert "orion:corrective orion:actions orion:patchdeployment ." in ttl
    assert "orion:corrective orion:actions orion:privilegereduction ." in ttl
    assert "orion:corrective orion:actions orion:improveddetectionrule ." in ttl
    assert "mayincludepatchdeployment" not in ttl.casefold()

def _claims_for_evidence(evidence: str) -> set[tuple[Any, Any, Any]]:
    return {
        (claim.get("subject"), claim.get("predicate"), claim.get("object"))
        for claim in _semantic_claims()
        if claim.get("source", {}).get("evidence") == evidence
    }


def _facts_for_evidence(evidence: str) -> set[tuple[Any, Any, Any]]:
    return {
        (fact.get("subject"), fact.get("predicate"), fact.get("object"))
        for fact in _graph_facts()
        if fact.get("source_evidence") == evidence
    }


def test_p039_p040_observational_modal_svo_semantic_claims_stay_clean(tmp_path: Path):
    # TASK-NLP-P039-P040-OBSERVATIONAL-CLEANUP | FUN-NLP-OBSERVATIONAL-CLEANUP AC-1
    _metrics(tmp_path)
    claims = _semantic_claims()

    assert _LOG_MONITORING_RELATIONS <= _claims_for_evidence(_LOG_MONITORING_EVIDENCE)
    assert _POST_INCIDENT_REVIEW_RELATIONS <= _claims_for_evidence(_POST_INCIDENT_REVIEW_EVIDENCE)
    assert _SECURITY_AWARENESS_TRAINING_RELATIONS <= _claims_for_evidence(_SECURITY_AWARENESS_TRAINING_EVIDENCE)
    assert _COMPROMISED_CREDENTIAL_RELATIONS <= _claims_for_evidence(_COMPROMISED_CREDENTIAL_EVIDENCE)
    assert all(claim.get("subject") not in _FORBIDDEN_OBSERVATIONAL_NODES for claim in claims)
    assert all(claim.get("object") not in _FORBIDDEN_OBSERVATIONAL_NODES for claim in claims)
    assert all(claim.get("predicate") not in _FORBIDDEN_OBSERVATIONAL_PREDICATES for claim in claims)


def test_p039_p040_observational_modal_svo_graph_and_ttl_stay_clean(tmp_path: Path):
    # TASK-NLP-P039-P040-OBSERVATIONAL-CLEANUP | CON-RDF-VISIBILITY AC-10
    _metrics(tmp_path)
    root = _rdf_root()
    ttl = _ttl_text()
    expected_facts = {
        (f"orion:{subject}", f"orion:{predicate}", f"orion:{obj}")
        for subject, predicate, obj in (
            _LOG_MONITORING_RELATIONS
            | _POST_INCIDENT_REVIEW_RELATIONS
            | _SECURITY_AWARENESS_TRAINING_RELATIONS
            | _COMPROMISED_CREDENTIAL_RELATIONS
        )
    }
    observed_facts = (
        _facts_for_evidence(_LOG_MONITORING_EVIDENCE)
        | _facts_for_evidence(_POST_INCIDENT_REVIEW_EVIDENCE)
        | _facts_for_evidence(_SECURITY_AWARENESS_TRAINING_EVIDENCE)
        | _facts_for_evidence(_COMPROMISED_CREDENTIAL_EVIDENCE)
    )

    assert expected_facts <= observed_facts
    assert _has_direct_orion_triple(root, "logmonitoring", "mayidentify", "suspiciousloginactivity")
    assert _has_direct_orion_triple(root, "postincidentreview", "mayidentify", "missingpatch")
    assert _has_direct_orion_triple(root, "postincidentreview", "mayidentify", "weakaccesscontrol")
    assert _has_direct_orion_triple(root, "postincidentreview", "mayidentify", "insufficientmonitoring")
    assert _has_direct_orion_triple(root, "securityawarenesstraining", "mayreduce", "maliciouslinkclickinglikelihood")
    assert not _has_direct_orion_triple(root, "securityawarenesstraining", "mayreduce", "likelihoodofclickingthemaliciouslink")
    assert _has_direct_orion_triple(root, "attacker", "uses", "compromisedcredential")
    assert _has_direct_orion_triple(root, "compromisedcredential", "accesses", "cloudaccount")
    rdf_text = ET.tostring(root, encoding="unicode")
    assert all(node not in rdf_text for node in _FORBIDDEN_OBSERVATIONAL_NODES)
    assert "orion:securityawarenesstraining orion:mayreduce orion:maliciouslinkclickinglikelihood ." in ttl
    assert all(node.casefold() not in ttl.casefold() for node in _FORBIDDEN_OBSERVATIONAL_NODES)

