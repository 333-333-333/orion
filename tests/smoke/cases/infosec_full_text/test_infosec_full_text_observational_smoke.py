from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case, slug

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_DIR = _SMOKE_DIR / "fixtures" / "infosec_3k_paragraphs"
_ARTIFACT_DIR = _CASE_DIR / "artifacts"
_CASE_ID = "infosec_full_text"
_SEMANTIC_PATH = _ARTIFACT_DIR / "observed_infosec_full_text_semantic_claims.json"
_GRAPH_PATH = _ARTIFACT_DIR / "observed_infosec_full_text_graph_model.json"
_RDF_PATH = _ARTIFACT_DIR / "observed_infosec_full_text_output.rdf"
_METRICS_PATH = _ARTIFACT_DIR / "observed_infosec_full_text_metrics.json"
_PARAGRAPH_IDS = [f"p{index:03d}" for index in range(1, 44)]
_NOUN_CHUNK_RESIDUES = {
    "type-of-",
    "typeofformaldocument",
    "type-of-control-document",
    "resource-for-security-initiative",
    "rules-and-expectations",
    "minimum-set-of-controls-required",
    "technical-environment-that-stores",
    "resource-that",
}
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        assert all((_PARAGRAPH_DIR / f"{pid}.txt").exists() for pid in _PARAGRAPH_IDS)
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path, case_id=_CASE_ID)
    return _METRICS


def _semantic_payload() -> dict[str, Any]:
    return json.loads(_SEMANTIC_PATH.read_text(encoding="utf-8"))


def _graph_payload() -> dict[str, Any]:
    return json.loads(_GRAPH_PATH.read_text(encoding="utf-8"))


def _object_properties(graph: dict[str, Any]) -> list[dict[str, Any]]:
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    return [item for item in schema.get("object_properties", []) if isinstance(item, dict)]


def _rdf_object_property_count() -> int:
    rdf = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
    rdfs = "{http://www.w3.org/2000/01/rdf-schema#}"
    owl = "{http://www.w3.org/2002/07/owl#}"
    root = ET.fromstring(_RDF_PATH.read_text(encoding="utf-8"))
    count = 0
    for prop in root.findall(f"{owl}ObjectProperty"):
        domains = [item.attrib.get(f"{rdf}resource") for item in prop.findall(f"{rdfs}domain")]
        ranges = [item.attrib.get(f"{rdf}resource") for item in prop.findall(f"{rdfs}range")]
        if prop.attrib.get(f"{rdf}about") and any(domains) and any(ranges):
            count += 1
    return count


def test_full_text_pipeline_generates_case_local_artifacts(tmp_path: Path):
    # TASK-INFOSEC-FULL-TEXT-SMOKE | FUN-INFOSEC-FULL-TEXT-SMOKE AC-1 | CON-NO-SRC-CHANGE AC-1 | BR-INFOSEC-FULL-TEXT-SMOKE-001
    metrics = _metrics(tmp_path)

    assert _SEMANTIC_PATH.exists()
    assert _GRAPH_PATH.exists()
    assert _RDF_PATH.exists()
    assert _METRICS_PATH.exists()
    assert metrics["rdf_generated"]
    assert metrics["graph_generated"]
    assert metrics["rdf_bytes"] > 0


def test_full_text_has_semantic_claims_for_every_paragraph(tmp_path: Path):
    # TASK-INFOSEC-FULL-TEXT-SMOKE | FUN-INFOSEC-FULL-TEXT-SMOKE AC-2 | CON-FULL-TEXT-FIXTURES AC-1 | BR-INFOSEC-FULL-TEXT-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["paragraph_ids"] == _PARAGRAPH_IDS
    assert len(metrics["paragraph_claim_distribution"]) == 43
    assert all(metrics["paragraph_claim_distribution"][pid] > 0 for pid in _PARAGRAPH_IDS)
    assert metrics["claim_count"] >= len(_PARAGRAPH_IDS)


def test_full_text_evidence_proxy_and_projection_are_consistent(tmp_path: Path):
    # TASK-INFOSEC-FULL-TEXT-SMOKE | FUN-INFOSEC-FULL-TEXT-SMOKE AC-3 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-FULL-TEXT-SMOKE-003
    metrics = _metrics(tmp_path)
    semantic = _semantic_payload()
    graph = _graph_payload()

    claim_ids = {str(claim.get("claim_id")) for claim in semantic.get("claims", []) if claim.get("claim_id")}
    projection = graph.get("projection") if isinstance(graph.get("projection"), dict) else {}
    projected_ids = {str(item) for item in projection.get("claim_ids", []) if str(item)}
    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert metrics["evidence_precision_proxy"] >= 0.95
    assert not metrics["evidence_unsupported_claim_ids"]
    assert projection.get("source_stage") == "semantic_claims"
    assert claim_ids
    assert claim_ids.issubset(projected_ids)


def test_full_text_rdf_object_properties_have_domain_and_range(tmp_path: Path):
    # TASK-INFOSEC-FULL-TEXT-SMOKE | FUN-INFOSEC-FULL-TEXT-SMOKE AC-4 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-FULL-TEXT-SMOKE-004
    metrics = _metrics(tmp_path)
    graph = _graph_payload()
    object_properties = _object_properties(graph)

    assert metrics["class_count"] >= 40
    assert metrics["object_property_count"] >= 40
    assert object_properties
    assert all(slug(item.get("domain")) and slug(item.get("range")) for item in object_properties)
    assert _rdf_object_property_count() >= max(1, len(object_properties) // 2)


def test_full_text_has_no_known_noun_chunk_residues_and_reasonable_metrics(tmp_path: Path):
    # TASK-INFOSEC-FULL-TEXT-SMOKE | FUN-INFOSEC-FULL-TEXT-SMOKE AC-5 | CON-SMOKE-PROXY AC-1 | BR-INFOSEC-FULL-TEXT-SMOKE-005
    metrics = _metrics(tmp_path)
    graph_text = (_GRAPH_PATH.read_text(encoding="utf-8") + "\n" + _RDF_PATH.read_text(encoding="utf-8")).lower()
    determiner_classes = []
    graph = _graph_payload()
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    for item in schema.get("classes", []):
        if isinstance(item, dict) and re.match(r"^(?:a|an|the)-", slug(item.get("iri") or item.get("label"))):
            determiner_classes.append(item)

    assert not sorted(token for token in _NOUN_CHUNK_RESIDUES if token in graph_text)
    assert not determiner_classes
    assert metrics["claim_count"] >= 100
    assert metrics["subclass_fact_count"] >= 20
    assert metrics["rdf_bytes"] >= 5000
