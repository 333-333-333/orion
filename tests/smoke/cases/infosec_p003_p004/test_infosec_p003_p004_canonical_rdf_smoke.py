from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from observability import JsonlFileLogSink
from orion import ORION
from infosec_pair_case_harness import _serialize_visual_turtle, process_with_pipeline_json_artifacts
from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

_CASE_DIR = Path(__file__).parent
_SMOKE_DIR = Path(__file__).parents[2]
_PARAGRAPH_DIR = _SMOKE_DIR / "fixtures" / "infosec_3k_paragraphs"
_CONTRACT_PATH = _CASE_DIR / "expected_contract.json"
_ARTIFACT_DIR = _CASE_DIR / "artifacts"
_CANONICAL_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p003_p004_canonical_claims.json"
_SEMANTIC_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p003_p004_semantic_claims.json"
_RDF_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p003_p004_output.rdf"
_TTL_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p003_p004_output.ttl"
_GRAPH_MODEL_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p003_p004_graph_model.json"
_RESOURCE_PREFIX = "https://orion.local/resource/"
_DETERMINERS = re.compile(r"^(?:a|an|the|any)-")

_ALIAS_ONLY_DEFINITIONAL_CLASS_SLUGS = {
    "advisory-document",
    "control-document",
    "formal-document",
    "minimum-set-of-controls",
    "operational-document",
}

_ALIAS_ONLY_DEFINITIONAL_SUBCLASS_PAIRS = {
    ("security-baseline", "minimum-set-of-controls"),
    ("security-guideline", "advisory-document"),
    ("security-policy", "formal-document"),
    ("security-procedure", "operational-document"),
    ("security-standard", "control-document"),
}

_KNOWN_TERM_SLUGS = {
    "advisorydocument": "advisory-document",
    "assetcustodian": "asset-custodian",
    "assetowner": "asset-owner",
    "boardofdirectors": "board-of-directors",
    "controldocument": "control-document",
    "enduser": "end-user",
    "formaldocument": "formal-document",
    "goodpractice": "good-practice",
    "incidentresponseprocess": "incident-response-process",
    "informationasset": "information-asset",
    "informationsecurity": "information-security",
    "informationsecuritymanager": "information-security-manager",
    "informationsecurityprogram": "information-security-program",
    "infrastructurecomponent": "infrastructure-component",
    "mandatoryrequirement": "mandatory-requirement",
    "minimumsetofcontrols": "minimum-set-of-controls",
    "monitoringmechanism": "monitoring-mechanism",
    "operatingsystem": "operating-system",
    "operationaldocument": "operational-document",
    "protectionrequirement": "protection-requirement",
    "securityanalyst": "security-analyst",
    "securitybaseline": "security-baseline",
    "securityevent": "security-event",
    "securityguideline": "security-guideline",
    "securityinitiative": "security-initiative",
    "securitypolicy": "security-policy",
    "securityprocedure": "security-procedure",
    "securityrequirement": "security-requirement",
    "securitystandard": "security-standard",
    "seniormanagement": "senior-management",
    "stepbystepactivity": "step-by-step-activity",
    "suspiciousactivity": "suspicious-activity",
    "systemadministrator": "system-administrator",
    "technicalenvironment": "technical-environment",
    "technicalservice": "technical-service",
}


def _contract() -> dict[str, Any]:
    return json.loads(_CONTRACT_PATH.read_text(encoding="utf-8"))


def _paragraph_texts() -> dict[str, str]:
    texts = {
        "p003": (_PARAGRAPH_DIR / "p003.txt").read_text(encoding="utf-8").strip(),
        "p004": (_PARAGRAPH_DIR / "p004.txt").read_text(encoding="utf-8").strip(),
    }
    assert "A security policy is a formal document" in texts["p003"]
    assert "The board of directors provides strategic oversight" in texts["p004"]
    return texts


def _slug(value: Any) -> str:
    text = str(value or "").strip()
    if text.startswith("orion:"):
        text = text[len("orion:"):]
    if text.startswith(_RESOURCE_PREFIX):
        text = text[len(_RESOURCE_PREFIX):]
    text = text.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    text = re.sub(r"([a-z])([A-Z])", r"\1-\2", text)
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return _KNOWN_TERM_SLUGS.get(re.sub(r"-+", "-", text), re.sub(r"-+", "-", text))


def _run_p003_p004(tmp_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    for path in (_CANONICAL_ARTIFACT_PATH, _SEMANTIC_ARTIFACT_PATH, _RDF_ARTIFACT_PATH, _TTL_ARTIFACT_PATH, _GRAPH_MODEL_ARTIFACT_PATH):
        if path.exists():
            path.unlink()
    _ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    paragraph_texts = _paragraph_texts()
    text = "\n\n".join(paragraph_texts[key] for key in ("p003", "p004"))
    runtime_log = tmp_path / "p003-p004-runtime-events.jsonl"
    sut = ORION(config={
        "logging": {"sink": JsonlFileLogSink(runtime_log)},
        "spacy_model": "en_core_web_lg",
        "output_strategy": "rdf",
        "semantic_claims": {"artifact_path": _SEMANTIC_ARTIFACT_PATH, "paragraph_asset_ids": ["p003", "p004"]},
        "canonical_claims": {"artifact_path": _CANONICAL_ARTIFACT_PATH, "paragraph_asset_ids": ["p003", "p004"]},
    })
    result, _ = process_with_pipeline_json_artifacts(sut, text, _ARTIFACT_DIR, "p003_p004")
    graph = _graph(result)
    if graph:
        _GRAPH_MODEL_ARTIFACT_PATH.write_text(json.dumps(graph, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        rdf_xml = serialize_graph_to_rdf_xml(graph)
        if "<rdf:RDF" in rdf_xml:
            _RDF_ARTIFACT_PATH.write_text(rdf_xml, encoding="utf-8")
            _TTL_ARTIFACT_PATH.write_text(_serialize_visual_turtle(graph), encoding="utf-8")
    return result, graph


def _canonical_claims_payload(result: dict[str, Any]) -> dict[str, Any]:
    candidates = [
        result.get("semantic_claims"),
        result.get("canonical_claims"),
        result.get("canonical_claims_artifact"),
        result.get("artifacts", {}).get("canonical_claims") if isinstance(result.get("artifacts"), dict) else None,
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            return candidate
    if _SEMANTIC_ARTIFACT_PATH.exists():
        return json.loads(_SEMANTIC_ARTIFACT_PATH.read_text(encoding="utf-8"))
    if _CANONICAL_ARTIFACT_PATH.exists():
        return json.loads(_CANONICAL_ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert False, "canonical_claims payload missing for p003+p004"


def _claims(payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("claims")
    assert isinstance(raw, list) and raw, "canonical_claims.claims must be a non-empty list"
    assert all(isinstance(item, dict) for item in raw), "each canonical claim must be an object"
    return raw


def _statement(claim: dict[str, Any]) -> str:
    value = claim.get("statement") or claim.get("normalized_statement")
    assert isinstance(value, str) and value.strip(), "each canonical claim must expose a normalized statement string"
    return value.strip()


def _paragraph_id(claim: dict[str, Any]) -> str:
    source = claim.get("source") if isinstance(claim.get("source"), dict) else {}
    value = claim.get("paragraph_id") or source.get("paragraph_id") or source.get("asset_id")
    assert value in {"p003", "p004"}, "each canonical claim must preserve source paragraph asset p003 or p004"
    return str(value)


def _graph(result: dict[str, Any]) -> dict[str, Any]:
    output = result.get("output", {})
    graph = output.get("graph", {}) if isinstance(output, dict) else {}
    assert isinstance(graph, dict), "graph must be a dict"
    return graph


def _class_slugs(graph: dict[str, Any]) -> set[str]:
    schema = graph.get("schema", {}) if isinstance(graph.get("schema"), dict) else {}
    classes = schema.get("classes", [])
    return {_slug(item.get("iri") or item.get("id") or item.get("label")) for item in classes if isinstance(item, dict)}


def _subclass_pairs(result: dict[str, Any], graph: dict[str, Any]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for item in result.get("taxonomy_relations", []):
        if isinstance(item, dict):
            pairs.add((_slug(item.get("subclass")), _slug(item.get("superclass"))))
    for item in graph.get("subclass_facts", []):
        if isinstance(item, dict):
            pairs.add((_slug(item.get("subject") or item.get("subclass")), _slug(item.get("object") or item.get("superclass"))))
    schema = graph.get("schema", {}) if isinstance(graph.get("schema"), dict) else {}
    for item in schema.get("classes", []):
        if isinstance(item, dict):
            parent = item.get("subClassOf") or item.get("subclass_of") or item.get("superclass")
            if parent:
                pairs.add((_slug(item.get("iri") or item.get("label")), _slug(parent)))
    return pairs


def _object_property_rows(graph: dict[str, Any]) -> list[dict[str, Any]]:
    schema = graph.get("schema", {}) if isinstance(graph.get("schema"), dict) else {}
    return [item for item in schema.get("object_properties", []) if isinstance(item, dict)]


def _object_property_triples(graph: dict[str, Any]) -> set[tuple[str, str, str]]:
    triples: set[tuple[str, str, str]] = set()
    for item in _object_property_rows(graph):
        triples.add((_slug(item.get("iri") or item.get("label")), _slug(item.get("domain")), _slug(item.get("range"))))
    return triples


def _serialized_object_property_triples() -> set[tuple[str, str, str]]:
    if not _RDF_ARTIFACT_PATH.exists():
        return set()
    rdf = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
    rdfs = "{http://www.w3.org/2000/01/rdf-schema#}"
    owl = "{http://www.w3.org/2002/07/owl#}"
    root = ET.fromstring(_RDF_ARTIFACT_PATH.read_text(encoding="utf-8"))
    triples: set[tuple[str, str, str]] = set()
    for prop in root.findall(f"{owl}ObjectProperty"):
        predicate = _slug(prop.attrib.get(f"{rdf}about"))
        domains = [_slug(item.attrib.get(f"{rdf}resource")) for item in prop.findall(f"{rdfs}domain")]
        ranges = [_slug(item.attrib.get(f"{rdf}resource")) for item in prop.findall(f"{rdfs}range")]
        triples.update((predicate, domain, range_) for domain in domains for range_ in ranges if predicate and domain and range_)
    return triples


def _comments_by_class(graph: dict[str, Any]) -> dict[str, set[str]]:
    schema = graph.get("schema", {}) if isinstance(graph.get("schema"), dict) else {}
    comments: dict[str, set[str]] = {}
    for item in schema.get("classes", []):
        if not isinstance(item, dict):
            continue
        key = _slug(item.get("iri") or item.get("label"))
        raw_comments = item.get("comments") or item.get("comment") or item.get("rdfs:comment") or []
        if isinstance(raw_comments, str):
            raw_comments = [raw_comments]
        comments[key] = {str(comment).strip() for comment in raw_comments if str(comment).strip()}
    return comments


def _combined_graph_text(result: dict[str, Any], graph: dict[str, Any]) -> str:
    output = result.get("output", {})
    chunks = [str(graph), str(output)]
    if isinstance(output, dict):
        for key in ("rdf", "rdf_xml", "serialized", "content", "text"):
            if key in output:
                chunks.append(str(output[key]))
    if _RDF_ARTIFACT_PATH.exists():
        chunks.append(_RDF_ARTIFACT_PATH.read_text(encoding="utf-8"))
    return "\n".join(chunks).lower()


def _semantic_claim_ids(result: dict[str, Any]) -> set[str]:
    payload = _canonical_claims_payload(result)
    return {str(claim.get("claim_id")) for claim in _claims(payload) if claim.get("claim_id")}


def _projection_claim_ids(graph: dict[str, Any]) -> set[str]:
    projection = graph.get("projection", {}) if isinstance(graph.get("projection"), dict) else {}
    raw = projection.get("claim_ids", [])
    assert isinstance(raw, list), "RDF projection must expose claim_ids list"
    return {str(item) for item in raw if str(item)}


def _taxonomy_density(classes: set[str], pairs: set[tuple[str, str]]) -> float:
    return len(pairs) / max(1, len(classes))


def _unjustified_subclass_orphans(classes: set[str], pairs: set[tuple[str, str]], allowed: set[str]) -> list[str]:
    linked = {item for pair in pairs for item in pair}
    return sorted(item for item in classes - linked if item not in allowed)


def test_p003_p004_rdf_artifact_is_generated_case_local(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-2 | CON-CANONICAL-RDF-P003-P004 AC-2 | BR-CANONICAL-RDF-P003-P004-002
    result, graph = _run_p003_p004(tmp_path)
    rdf_xml = _RDF_ARTIFACT_PATH.read_text(encoding="utf-8") if _RDF_ARTIFACT_PATH.exists() else ""

    assert graph, "pipeline/test must produce inspectable RDF graph for p003+p004"
    assert _RDF_ARTIFACT_PATH.exists(), "pipeline/test must persist observed p003+p004 RDF artifact case-local"
    assert _GRAPH_MODEL_ARTIFACT_PATH.exists(), "test harness must persist observed p003+p004 graph/model artifact case-local"
    assert _RDF_ARTIFACT_PATH == _ARTIFACT_DIR / "observed_p003_p004_output.rdf"
    assert "<rdf:RDF" in rdf_xml
    assert "SecurityPolicy" in rdf_xml and "BoardOfDirectors" in rdf_xml
    assert _paragraph_texts()["p003"] and _paragraph_texts()["p004"]


def test_p003_p004_canonical_claims_are_deterministic_and_asset_scoped(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-1 | CON-CANONICAL-RDF-P003-P004 AC-1 | BR-CANONICAL-RDF-P003-P004-001
    result, _ = _run_p003_p004(tmp_path)
    expected = {key: set(value) for key, value in _contract()["expected_statements_by_paragraph"].items()}
    claims = _claims(_canonical_claims_payload(result))
    actual: dict[str, set[str]] = {"p003": set(), "p004": set()}
    for claim in claims:
        actual[_paragraph_id(claim)].add(_statement(claim))

    assert actual == expected
    assert _SEMANTIC_ARTIFACT_PATH.exists(), "test must persist observed semantic_claims artifact from pipeline"


def test_p003_p004_rdf_has_exact_small_class_contract(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-2 | CON-CANONICAL-RDF-P003-P004 AC-2 | BR-CANONICAL-RDF-P003-P004-002
    result, graph = _run_p003_p004(tmp_path)
    classes = _class_slugs(graph)
    expected = {_slug(item) for item in _contract()["rdf"]["classes"]}
    graph_text = _combined_graph_text(result, graph)

    quality = _contract()["rdf_quality"]
    violations = []
    if len(classes) > quality["max_class_count"]:
        violations.append(f"class count too high: {len(classes)} > {quality['max_class_count']}")
    prohibited = sorted({_slug(item) for item in quality["prohibited_classes"]} & classes)
    if prohibited:
        violations.append(f"prohibited generic classes: {prohibited}")
    determiner_classes = sorted(item for item in classes if _DETERMINERS.match(item))
    if determiner_classes:
        violations.append(f"determiner-prefixed classes: {determiner_classes}")
    banned = sorted(token for token in _contract()["banned_tokens"] if token in graph_text)
    if banned:
        violations.append(f"banned graph tokens: {banned}")
    missing = sorted(expected - classes)
    unexpected = sorted(classes - expected)
    if missing or unexpected:
        violations.append(f"class contract mismatch missing={missing} unexpected={unexpected}")
    assert not violations, "; ".join(violations)
    assert _RDF_ARTIFACT_PATH.exists(), "test must persist observed p003+p004 RDF artifact from pipeline"


def test_p003_p004_rdf_maps_type_definitions_to_direct_subclassof(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-3 | CON-CANONICAL-RDF-P003-P004 AC-3 | BR-CANONICAL-RDF-P003-P004-003
    result, graph = _run_p003_p004(tmp_path)
    actual = _subclass_pairs(result, graph)
    expected = {tuple(item) for item in _contract()["rdf"]["direct_subclasses"]}

    quality = _contract()["rdf_quality"]
    classes = _class_slugs(graph)
    density = _taxonomy_density(classes, actual)

    missing = sorted(expected - actual)
    assert not missing, f"missing direct subClassOf pairs: {missing}"
    assert len(actual) >= quality["min_subclass_count"], f"subClassOf count too low: {len(actual)}"
    assert density >= quality["min_subclass_density"], f"taxonomy density too low: {density:.3f}"
    assert not [pair for pair in actual if pair[1].startswith("type-of-") or pair[1] == "type"]


def test_p003_p004_rdf_preserves_definition_sentences_as_comments(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-4 | CON-CANONICAL-RDF-P003-P004 AC-4 | BR-CANONICAL-RDF-P003-P004-004
    _, graph = _run_p003_p004(tmp_path)
    comments = _comments_by_class(graph)
    expected = _contract()["rdf"]["comments"]

    rdf_xml = _RDF_ARTIFACT_PATH.read_text(encoding="utf-8") if _RDF_ARTIFACT_PATH.exists() else ""
    missing = {klass: comment for klass, comment in expected.items() if comment not in comments.get(klass, set())}
    missing_serialized = {klass: comment for klass, comment in expected.items() if comment not in rdf_xml}
    assert not missing, f"missing graph rdfs:comment definitions: {missing}"
    assert not missing_serialized, f"missing serialized RDF rdfs:comment definitions: {missing_serialized}"


def test_p003_p004_rdf_has_expected_object_properties_with_domain_range(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-5 | CON-CANONICAL-RDF-P003-P004 AC-5 | BR-CANONICAL-RDF-P003-P004-004
    _, graph = _run_p003_p004(tmp_path)
    actual = _object_property_triples(graph)
    serialized = _serialized_object_property_triples()
    expected = {tuple(item) for item in _contract()["rdf"]["object_properties"]}

    rows = _object_property_rows(graph)
    malformed = [row for row in rows if not _slug(row.get("iri") or row.get("label")) or not _slug(row.get("domain")) or not _slug(row.get("range"))]
    missing_graph = sorted(expected - actual)
    missing_serialized = sorted(expected - serialized)
    assert not malformed, f"object properties missing predicate/domain/range: {malformed}"
    assert not missing_graph, f"missing graph object properties with domain/range: {missing_graph}"
    assert not missing_serialized, f"missing serialized RDF object properties with domain/range: {missing_serialized}"
    assert all(predicate not in {"be", "type"} for predicate, _, _ in actual | serialized)


def test_p003_p004_rdf_keeps_central_entities_relation_connected(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-5 | CON-CANONICAL-RDF-P003-P004 AC-5 | BR-CANONICAL-RDF-P003-P004-004
    _, graph = _run_p003_p004(tmp_path)
    quality = _contract()["rdf_quality"]
    expected_central = {_slug(item) for item in quality["central_connected_classes"]}
    relation_linked = {item for triple in _object_property_triples(graph) for item in triple[1:]}
    missing = sorted(expected_central - relation_linked)

    assert len(missing) <= quality["max_unjustified_connectivity_orphans"], f"central classes missing object-property connectivity: {missing}"


def test_p003_p004_rdf_projection_comes_only_from_semantic_claims(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-6 | CON-CANONICAL-RDF-P003-P004 AC-6 | BR-CANONICAL-RDF-P003-P004-005
    result, graph = _run_p003_p004(tmp_path)
    projection = graph.get("projection", {}) if isinstance(graph.get("projection"), dict) else {}

    assert projection.get("source_stage") == "semantic_claims"
    assert _projection_claim_ids(graph) == _semantic_claim_ids(result)


def test_p003_p004_rdf_has_no_noun_chunk_residue(tmp_path: Path):
    # TASK-CANONICAL-RDF-P003-P004 | FUN-CANONICAL-RDF-P003-P004 AC-7 | CON-CANONICAL-RDF-P003-P004 AC-7 | BR-CANONICAL-RDF-P003-P004-006
    result, graph = _run_p003_p004(tmp_path)
    graph_text = _combined_graph_text(result, graph)
    residues = _contract()["rdf_quality"]["noun_chunk_residue_tokens"]

    assert not sorted(token for token in residues if token in graph_text), "RDF contains noun-chunk residue tokens"



def test_p003_p004_rdf_rejects_definition_only_taxonomy_without_differentiator(tmp_path: Path):
    # TASK-ONT-003 | FUN-CANONICAL-RDF-P003-P004 AC-8 | CON-CANONICAL-RDF-P003-P004 AC-8 | BR-CANONICAL-RDF-P003-P004-007
    result, graph = _run_p003_p004(tmp_path)
    classes = _class_slugs(graph)
    subclass_pairs = _subclass_pairs(result, graph)

    leaked_classes = sorted(_ALIAS_ONLY_DEFINITIONAL_CLASS_SLUGS & classes)
    leaked_pairs = sorted(_ALIAS_ONLY_DEFINITIONAL_SUBCLASS_PAIRS & subclass_pairs)

    assert not leaked_classes, f"definition-only taxonomy leaked as owl:Class: {leaked_classes}"
    assert not leaked_pairs, f"definition-only taxonomy leaked as rdfs:subClassOf: {leaked_pairs}"
