from __future__ import annotations

from pathlib import Path
import json
import xml.etree.ElementTree as ET
from typing import Any
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p015', 'p016']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p015_p016_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P015_P016 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p015_p016_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P015_P016 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p015_p016_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P015_P016 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0

def _debug_ir_path() -> Path:
    return _CASE_DIR / "artifacts" / "observed_p015_p016_semantic_debug_ir.json"


def _debug_ir(tmp_path: Path) -> dict[str, Any]:
    metrics = _metrics(tmp_path)
    path = _debug_ir_path()
    assert metrics["semantic_debug_ir_generated"], f"missing semantic debug IR artifact: {path}"
    assert path.exists(), f"missing semantic debug IR artifact: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def _term(value: Any) -> str:
    return str(value or "").replace("_", "").replace("-", "").replace(" ", "").lower()


def _field(item: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in item:
            return item[name]
    return None


def test_p015_p016_semantic_debug_ir_contract_shape(tmp_path: Path):
    # TASK-SEMANTIC-DEBUG-IR-001 | FUN-SEMANTIC-DEBUG-IR AC-1 | CON-SEMANTIC-DEBUG-IR-SHAPE AC-1 | BR-SEMANTIC-DEBUG-IR-001
    ir = _debug_ir(tmp_path)

    assert isinstance(ir.get("entities"), list)
    assert isinstance(ir.get("relations"), list)
    if "contexts" in ir:
        assert isinstance(ir["contexts"], list)
    if "rejected" in ir:
        assert isinstance(ir["rejected"], list)

    for entity in ir["entities"]:
        assert isinstance(entity, dict)
        assert entity.get("id")
        assert _field(entity, "label", "canonical", "name")
        if _field(entity, "source", "source_sentence", "evidence") is not None:
            assert str(_field(entity, "source", "source_sentence", "evidence")).strip()

    for relation in ir["relations"]:
        assert isinstance(relation, dict)
        assert relation.get("subject")
        assert relation.get("predicate")
        assert relation.get("object")
        assert _field(relation, "source_sentence", "evidence", "source")


def test_p015_p016_semantic_debug_ir_load_balancer_relation_is_evidence_backed(tmp_path: Path):
    # TASK-SEMANTIC-DEBUG-IR-001 | FUN-SEMANTIC-DEBUG-IR AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-SEMANTIC-DEBUG-IR-002
    ir = _debug_ir(tmp_path)
    relations = ir["relations"]

    matches = [
        relation
        for relation in relations
        if _term(relation.get("subject")) == "loadbalancer"
        and _term(relation.get("predicate")) == "distributes"
        and _term(relation.get("object")) == "traffic"
    ]
    assert matches, "expected evidence-backed LoadBalancer distributes Traffic relation"
    assert any(
        "load balancer distributes traffic across multiple servers"
        in str(_field(relation, "source_sentence", "evidence", "source")).lower()
        for relation in matches
    )


def test_p015_p016_semantic_debug_ir_does_not_promote_across_phrase_noise(tmp_path: Path):
    # TASK-SEMANTIC-DEBUG-IR-001 | FUN-SEMANTIC-DEBUG-IR AC-3 | CON-NO-INVENTED-PROPERTY AC-1 | BR-SEMANTIC-DEBUG-IR-003
    ir = _debug_ir(tmp_path)
    final_entities = {_term(_field(entity, "label", "canonical", "name", "id")) for entity in ir["entities"]}
    final_predicates = {_term(relation.get("predicate")) for relation in ir["relations"]}
    debug_bins = []
    for key in ("rejected", "contexts", "debug"):
        value = ir.get(key)
        if isinstance(value, list):
            debug_bins.extend(value)
        elif isinstance(value, dict):
            debug_bins.append(value)

    assert "flowsacross" not in final_predicates
    assert "trafficacrossmultipleserver" not in final_entities
    if any("trafficacrossmultipleserver" in str(item).replace(" ", "").lower() for item in debug_bins):
        assert True


def _graph_path() -> Path:
    return _CASE_DIR / "artifacts" / "observed_p015_p016_graph_model.json"


def _rdf_path() -> Path:
    return _CASE_DIR / "artifacts" / "observed_p015_p016_output.rdf"


def _local(value: Any) -> str:
    local = str(value or "").rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    if local.startswith("orion:"):
        local = local.split(":", 1)[1]
    return local.replace("_", "").replace("-", "").lower()


def test_p015_p016_prevents_claims_keep_relation_identity_by_source(tmp_path: Path):
    # TASK-THEMIS-PREVENTS-001 | FUN-RDF-CLAIM-IDENTITY AC-1 | BR-RDF-CLAIM-IDENTITY-001
    _metrics(tmp_path)
    graph = json.loads(_graph_path().read_text(encoding="utf-8"))
    facts = [row for row in graph.get("facts", []) if _local(row.get("predicate")) == "prevents"]

    expected = {
        (
            "inputvalidation",
            "malformeddatafromenteringanapplication",
            "input validation prevents malicious or malformed data from entering an application.",
        ),
        (
            "secureerrorhandling",
            "sensitiveinformationfrombeingexposedthrougherrormessage",
            "secure error handling prevents sensitive information from being exposed through error messages.",
        ),
    }
    observed = {
        (_local(row.get("subject")), _local(row.get("object")), str(row.get("source_evidence") or row.get("evidence") or "").lower())
        for row in facts
    }

    assert expected.issubset(observed), f"prevents facts lost claim identity/source metadata: observed={sorted(observed)}"


def _rdf_root() -> ET.Element:
    return ET.fromstring(_rdf_path().read_text(encoding="utf-8"))


def _rdf_ns() -> dict[str, str]:
    return {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
        "meta": "https://orion.local/meta/",
        "skos": "http://www.w3.org/2004/02/skos/core#",
    }


def _resource_attr(node: ET.Element | None, ns: dict[str, str]) -> str:
    if node is None:
        return ""
    return node.get(f"{{{ns['rdf']}}}resource") or ""


def test_p015_p016_relation_metadata_is_not_visible_rdf_statement_fallback(tmp_path: Path):
    # TASK-THEMIS-RDF-VISIBLE-001 | FUN-RDF-RELATION-METADATA AC-1 | BR-RDF-RELATION-METADATA-001
    _metrics(tmp_path)
    graph = json.loads(_graph_path().read_text(encoding="utf-8"))
    sourceful_facts = [row for row in graph.get("facts", []) if row.get("source_evidence") or row.get("evidence")]
    assert sourceful_facts, "relation source metadata must remain in graph/debug artifact, not visible RDF/XML reification"

    root = _rdf_root()
    ns = _rdf_ns()
    assert root.findall(".//rdf:Statement", ns) == [], "rdf:Statement nodes are visible bridge nodes in visualizer RDF/XML"


def test_p015_p016_no_blank_or_metadata_bridge_nodes_connect_domain_entities(tmp_path: Path):
    # TASK-THEMIS-RDF-VISIBLE-001 | FUN-RDF-RELATION-METADATA AC-2 | BR-RDF-RELATION-METADATA-002
    _metrics(tmp_path)
    root = _rdf_root()
    ns = _rdf_ns()
    domain_entities = {"submittedpassword", "fileserver", "compromisedcredential", "unavailableto"}
    leaks: list[dict[str, str]] = []

    for node in root.iter():
        about = node.get(f"{{{ns['rdf']}}}about") or node.get(f"{{{ns['rdf']}}}nodeID") or ""
        has_bridge_shape = node.get(f"{{{ns['rdf']}}}nodeID") is not None or any(
            child.tag in {
                f"{{{ns['rdf']}}}subject",
                f"{{{ns['rdf']}}}predicate",
                f"{{{ns['rdf']}}}object",
                f"{{{ns['meta']}}}evidence",
                f"{{{ns['meta']}}}span",
                f"{{{ns['meta']}}}confidence",
                f"{{{ns['meta']}}}visibility",
            }
            for child in list(node)
        )
        if not has_bridge_shape:
            continue
        refs = {
            _local(child.get(f"{{{ns['rdf']}}}resource"))
            for child in list(node)
            if child.get(f"{{{ns['rdf']}}}resource")
        }
        if refs & domain_entities:
            leaks.append({"node": _local(about), "refs": ",".join(sorted(refs & domain_entities))})

    assert leaks == [], f"visible RDF/XML metadata/reification bridge nodes connected to domain entities: {leaks}"


def test_p015_p016_predicate_labels_are_not_visible_intermediate_nodes(tmp_path: Path):
    # TASK-THEMIS-RDFSTAR-001 | FUN-RDF-RELATION-METADATA AC-2 | BR-RDF-RELATION-METADATA-002
    _metrics(tmp_path)
    root = _rdf_root()
    ns = _rdf_ns()
    forbidden = {"prevents", "submits", "becomes"}
    leaks: list[tuple[str, str]] = []

    visible_node_paths = [".//owl:Class", ".//rdf:Description", ".//rdf:Statement"]
    for path_expr in visible_node_paths:
        for node in root.findall(path_expr, ns):
            labels = node.findall("./rdfs:label", ns) + node.findall("./skos:prefLabel", ns)
            for label in labels:
                if _local(label.text) in forbidden:
                    leaks.append((path_expr, label.text or ""))

    assert leaks == []


def test_p015_p016_same_predicate_relations_remain_distinct_without_visible_middle_node(tmp_path: Path):
    # TASK-THEMIS-RDFSTAR-001 | FUN-RDF-RELATION-METADATA AC-3 | BR-RDF-RELATION-METADATA-003
    _metrics(tmp_path)
    graph = json.loads(_graph_path().read_text(encoding="utf-8"))
    rows = [
        (
            _local(row.get("subject")),
            _local(row.get("object")),
            str(row.get("source_evidence") or row.get("evidence") or "").lower(),
        )
        for row in graph.get("facts", [])
        if _local(row.get("predicate")) == "prevents"
    ]

    expected = {
        (
            "inputvalidation",
            "malformeddatafromenteringanapplication",
            "input validation prevents malicious or malformed data from entering an application.",
        ),
        (
            "secureerrorhandling",
            "sensitiveinformationfrombeingexposedthrougherrormessage",
            "secure error handling prevents sensitive information from being exposed through error messages.",
        ),
    }
    assert expected.issubset(set(rows)), f"same-label prevents relations collapsed or lost metadata: {rows}"
