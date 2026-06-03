from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from observability import JsonlFileLogSink
from orion import ORION
from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

_CASE_DIR = Path(__file__).parent
_SMOKE_DIR = Path(__file__).parents[2]
_PARAGRAPH_DIR = _SMOKE_DIR / "fixtures" / "infosec_3k_paragraphs"
_ARTIFACT_DIR = _CASE_DIR / "artifacts"
_CANONICAL_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p001_p002_canonical_claims.json"
_RDF_ARTIFACT_PATH = _ARTIFACT_DIR / "observed_p001_p002_output.rdf"
_RESOURCE_PREFIX = "https://orion.local/resource/"

_EXPECTED_CLASSES = {
    "information-security",
    "discipline",
    "information-asset",
    "resource",
    "organization",
    "information",
    "threat",
    "internal-threat",
    "external-threat",
    "confidential-document",
    "corporate-database",
    "customer-record",
    "source-code-repository",
    "system-configuration-file",
    "backup-archive",
    "business-report",
    "confidentiality",
    "integrity",
    "availability",
    "security-property",
    "authorized-entity",
    "system",
    "cia-triad",
    "foundational-model",
}

_EXPECTED_DIRECT_SUBCLASSES = {
    ("information-security", "discipline"),
    ("internal-threat", "threat"),
    ("external-threat", "threat"),
    ("confidential-document", "information-asset"),
    ("corporate-database", "information-asset"),
    ("customer-record", "information-asset"),
    ("source-code-repository", "information-asset"),
    ("system-configuration-file", "information-asset"),
    ("backup-archive", "information-asset"),
    ("business-report", "information-asset"),
    ("confidentiality", "security-property"),
    ("integrity", "security-property"),
    ("availability", "security-property"),
    ("cia-triad", "foundational-model"),
}

_EXPECTED_OBJECT_PROPERTIES = {
    ("protects", "information-security", "information-asset"),
    ("protects-against", "information-security", "threat"),
    ("has-value-for", "resource", "organization"),
    ("stores", "information-asset", "information"),
    ("processes", "information-asset", "information"),
    ("transmits", "information-asset", "information"),
    ("represents", "information-asset", "information"),
    ("preserves", "information-security", "security-property"),
    ("ensures-accessible-to", "confidentiality", "authorized-entity"),
    ("ensures-accuracy-of", "integrity", "information"),
    ("ensures-availability-of", "availability", "system"),
    ("forms", "security-property", "cia-triad"),
    ("models", "cia-triad", "information-security"),
}

_EXPECTED_COMMENTS = {
    "information-security": "Information security is a discipline focused on protecting information assets against internal and external threats.",
    "information-asset": "An information asset is any resource that has value for an organization and that stores, processes, transmits, or represents information.",
    "confidentiality": "Confidentiality is a security property that ensures information is accessible only to authorized entities.",
    "integrity": "Integrity is a security property that ensures information is accurate, complete, and protected against unauthorized modification.",
    "availability": "Availability is a security property that ensures information and systems are accessible when needed.",
    "cia-triad": "Confidentiality, integrity, and availability form the CIA triad.",
    "foundational-model": "The CIA triad is a foundational model for information security.",
}

_BANNED_TOKENS = {
    "orion:be",
    "type-of-information-asset",
    "typeofinformationasset",
    "discipline-focused-on-protecting-information-assets",
    "disciplinefocusedonprotectinginformationassets",
    "any-resource-that-has-value-for-an-organization",
    "anyresourcethathasvalueforanorganization",
    "resource-that",
    "resourcethat",
    "value-for-an-organization",
    "valueforanorganization",
}

_DETERMINERS = re.compile(r"^(?:a|an|the|any)-")


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
    text = re.sub(r"-+", "-", text)
    return text


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


def _object_property_triples(graph: dict[str, Any]) -> set[tuple[str, str, str]]:
    schema = graph.get("schema", {}) if isinstance(graph.get("schema"), dict) else {}
    triples: set[tuple[str, str, str]] = set()
    for item in schema.get("object_properties", []):
        if isinstance(item, dict):
            triples.add((_slug(item.get("iri") or item.get("label")), _slug(item.get("domain")), _slug(item.get("range"))))
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
    return "\n".join(chunks).lower()


def _run_p001_p002(tmp_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    paragraph_paths = [_PARAGRAPH_DIR / "p001.txt", _PARAGRAPH_DIR / "p002.txt"]
    text = "\n\n".join(path.read_text(encoding="utf-8").strip() for path in paragraph_paths)
    assert "Information security is a discipline" in text
    assert "The CIA triad is a foundational model" in text
    runtime_log = tmp_path / "p001-p002-runtime-events.jsonl"
    if _CANONICAL_ARTIFACT_PATH.exists():
        _CANONICAL_ARTIFACT_PATH.unlink()
    if _RDF_ARTIFACT_PATH.exists():
        _RDF_ARTIFACT_PATH.unlink()
    _ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf", "canonical_claims": {"artifact_path": _CANONICAL_ARTIFACT_PATH, "paragraph_asset_ids": ["p001", "p002"]}})
    result = sut.process(text)
    graph = _graph(result)
    assert result.get("output", {}).get("strategy") == "rdf"
    assert graph, "graph missing for p001+p002"
    rdf_xml = serialize_graph_to_rdf_xml(graph)
    assert "<rdf:RDF" in rdf_xml
    _RDF_ARTIFACT_PATH.write_text(rdf_xml, encoding="utf-8")
    return result, graph


def test_p001_p002_modular_contract_has_exact_small_deterministic_classes(tmp_path: Path):
    # TASK-SMOKE-P001-P002 | FUN-SMOKE-P001-P002 AC-1 | CON-SMOKE-P001-P002 AC-1 | BR-SMOKE-P001-P002-001
    result, graph = _run_p001_p002(tmp_path)
    classes = _class_slugs(graph)
    graph_text = _combined_graph_text(result, graph)

    assert classes == _EXPECTED_CLASSES
    assert len(classes) == len(_EXPECTED_CLASSES) <= 30
    assert all(not _DETERMINERS.match(item) for item in classes)
    assert not sorted(token for token in _BANNED_TOKENS if token in graph_text)


def test_p001_p002_modular_contract_maps_type_statements_to_direct_subclassof(tmp_path: Path):
    # TASK-SMOKE-P001-P002 | FUN-SMOKE-P001-P002 AC-2 | CON-SMOKE-P001-P002 AC-2 | BR-SMOKE-P001-P002-002
    result, graph = _run_p001_p002(tmp_path)
    actual = _subclass_pairs(result, graph)

    missing = sorted(_EXPECTED_DIRECT_SUBCLASSES - actual)
    assert not missing, f"missing direct subClassOf pairs: {missing}"
    assert not [pair for pair in actual if pair[1].startswith("type-of-") or pair[1] == "type"]


def test_p001_p002_modular_contract_keeps_definitions_as_comments(tmp_path: Path):
    # TASK-SMOKE-P001-P002 | FUN-SMOKE-P001-P002 AC-3 | CON-SMOKE-P001-P002 AC-3 | BR-SMOKE-P001-P002-003
    _, graph = _run_p001_p002(tmp_path)
    comments = _comments_by_class(graph)

    missing = {klass: comment for klass, comment in _EXPECTED_COMMENTS.items() if comment not in comments.get(klass, set())}
    assert not missing, f"missing rdfs:comment definitions: {missing}"


def test_p001_p002_modular_contract_has_expected_object_properties_with_domain_range(tmp_path: Path):
    # TASK-SMOKE-P001-P002 | FUN-SMOKE-P001-P002 AC-4 | CON-SMOKE-P001-P002 AC-4 | BR-SMOKE-P001-P002-004
    _, graph = _run_p001_p002(tmp_path)
    actual = _object_property_triples(graph)

    missing = sorted(_EXPECTED_OBJECT_PROPERTIES - actual)
    assert not missing, f"missing object properties with domain/range: {missing}"
    assert all(predicate not in {"be", "type"} for predicate, _, _ in actual)
