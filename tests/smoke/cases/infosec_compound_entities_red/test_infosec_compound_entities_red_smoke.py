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
_PARAGRAPH_IDS = ["p044"]
_CASE_ID = "compound_entities_red"
_METRICS: dict[str, Any] | None = None
_RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
_ORION_NS = "https://orion.local/resource/"
_NS = {"rdf": _RDF_NS}

_EXPECTED_COMPOUNDS = {
    "IdentityAndAccessManagement",
    "PhysicalAccess",
    "UnauthorizedAccess",
    "RecoveryPointObjective",
    "KeyManagementService",
}
_EXPECTED_TTL_TRIPLES = {
    "orion:identityandaccessmanagement orion:governs orion:accessdecision .",
    "orion:physicalaccess orion:requires orion:badgeapproval .",
    "orion:unauthorizedaccess orion:triggers orion:securityincident .",
    "orion:recoverypointobjective orion:defines orion:maximumtolerabledataloss .",
    "orion:keymanagementservice orion:stores orion:cryptographickey .",
}
_FORBIDDEN_COMPOUND_RESIDUES = {
    "AccessManagementGoverns",
    "ManagementGovernsAccessDecision",
    "PhysicalAccessRequires",
    "AccessRequiresBadgeApproval",
    "UnauthorizedAccessTriggers",
    "AccessTriggersASecurityIncident",
    "RecoveryPointObjectiveDefines",
    "PointObjectiveDefinesMaximum",
    "KeyManagementServiceStores",
    "ManagementServiceStoresACryptographicKey",
}


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path, case_id=_CASE_ID)
    return _METRICS


def _artifact_json(name: str) -> dict[str, Any]:
    return json.loads((_CASE_DIR / "artifacts" / name).read_text(encoding="utf-8"))


def _rdf_root() -> ET.Element:
    return ET.parse(_CASE_DIR / "artifacts" / "observed_compound_entities_red_output.rdf").getroot()


def _ttl_text() -> str:
    return (_CASE_DIR / "artifacts" / "observed_compound_entities_red_output.ttl").read_text(encoding="utf-8")


def _local(value: Any) -> str:
    text = str(value or "").rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    if text.startswith("orion:"):
        text = text.split(":", 1)[1]
    return text


def _graph_labels(graph: dict[str, Any]) -> set[str]:
    labels: set[str] = set()
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    for bucket_name in ("classes", "object_properties"):
        for item in graph.get(bucket_name, []) + schema.get(bucket_name, []):
            if isinstance(item, dict):
                labels.add(_local(item.get("label") or item.get("iri")))
    for bucket_name in ("facts", "subclass_facts"):
        for item in graph.get(bucket_name, []):
            if isinstance(item, dict):
                labels.update({_local(item.get("subject")), _local(item.get("predicate")), _local(item.get("object"))})
    return {label for label in labels if label}


def test_compound_entities_are_atomic_in_semantic_and_graph_layers(tmp_path: Path):
    # TB-ORION-COMPOUND-ENTITY-RED | FUN-COMPOUND-ENTITY AC-1 | CON-RDF-VISIBILITY AC-1 | BR-COMPOUND-ENTITY-001
    _metrics(tmp_path)
    semantic = _artifact_json("observed_compound_entities_red_semantic_claims.json")
    graph = _artifact_json("observed_compound_entities_red_graph_model.json")

    semantic_terms = {
        _local(value)
        for claim in semantic.get("claims", [])
        if isinstance(claim, dict)
        for value in (claim.get("subject"), claim.get("predicate"), claim.get("object"))
    }
    graph_terms = _graph_labels(graph)
    observed = semantic_terms | graph_terms

    assert _EXPECTED_COMPOUNDS <= observed, f"compound entities lost or split before RDF projection: missing={sorted(_EXPECTED_COMPOUNDS - observed)}"
    assert not (_FORBIDDEN_COMPOUND_RESIDUES & observed), f"compound entity phrase residues reached semantic/graph output: {sorted(_FORBIDDEN_COMPOUND_RESIDUES & observed)}"


def test_compound_entities_emit_direct_visible_rdf_triples_not_split_nodes(tmp_path: Path):
    # TB-ORION-COMPOUND-ENTITY-RED | FUN-COMPOUND-ENTITY AC-2 | CON-RDF-VISIBILITY AC-2 | BR-COMPOUND-ENTITY-002
    _metrics(tmp_path)
    root = _rdf_root()
    ttl = _ttl_text()
    rdf_text = ET.tostring(root, encoding="unicode")

    missing = sorted(triple for triple in _EXPECTED_TTL_TRIPLES if triple not in ttl)
    leaked = sorted(residue for residue in _FORBIDDEN_COMPOUND_RESIDUES if residue in rdf_text or residue.casefold() in ttl.casefold())

    assert not missing, f"compound entities must survive as direct RDF triples; missing={missing}"
    assert not leaked, f"split compound residues must not become visible RDF/NLP nodes: {leaked}"
    assert all(f"{_ORION_NS}{compound.lower()}" in rdf_text.casefold() for compound in _EXPECTED_COMPOUNDS)
