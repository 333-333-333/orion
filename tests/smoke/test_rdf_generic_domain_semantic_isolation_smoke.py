from __future__ import annotations

import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

from observability import JsonlFileLogSink
from orion import ORION
from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

_FIXTURE = Path(__file__).parent / "fixtures" / "library_generic_input.txt"
_RDF_OUTPUT_ARTIFACT = Path(__file__).parent / "artifacts" / "library_generic_output.rdf"
_RDF_OUTPUT_JSON_ARTIFACT = Path(__file__).parent / "artifacts" / "library_generic_output.json"

_INFOSEC_TERMS = {
    "mfa", "siem", "risk", "control", "threat", "vulnerability", "compliance",
    "evidence", "incident", "securityobjective", "mitigates", "exploits", "exposes",
    "supports", "satisfies", "detects", "owns",
}

_INFOSEC_IRIS = {
    "https://orion.local/resource/SecurityObjective",
    "https://orion.local/resource/Threat",
    "https://orion.local/resource/Vulnerability",
    "https://orion.local/resource/Compliance",
    "https://orion.local/resource/Evidence",
    "https://orion.local/resource/Incident",
    "https://orion.local/resource/Control",
    "https://orion.local/resource/Risk",
    "https://orion.local/resource/SIEM",
    "https://orion.local/resource/MFA",
    "https://orion.local/resource/mitigates",
    "https://orion.local/resource/exploits",
    "https://orion.local/resource/exposes",
    "https://orion.local/resource/supports",
    "https://orion.local/resource/satisfies",
    "https://orion.local/resource/detects",
    "https://orion.local/resource/owns",
}

_LIBRARY_CONCEPT_LABELS = {"Book", "Author", "Library", "Loan", "Reader", "Librarian", "Catalog"}
_LIBRARY_BOOTSTRAP_CLASSES = {"Library", "Book", "Author", "Reader", "Librarian", "Loan"}
_LIBRARY_BOOTSTRAP_PROPERTIES = {"manage", "publish", "request", "record", "have"}
_LIBRARY_BOOTSTRAP_SIGNATURES = {
    "manage": {"subject": "Library", "object": "Book"},
    "publish": {"subject": "Author", "object": "Book"},
    "request": {"subject": "Reader", "object": "Loan"},
    "record": {"subject": "Librarian", "object": "Loan"},
    "have": {"subject": "Book", "object": "Author"},
}


def _normalize_onto_label(value: str) -> str:
    local = str(value or "").strip()
    if not local:
        return ""
    local = local.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    if not local:
        return ""
    if local.startswith("orion:"):
        local = local.split(":", 1)[1]
    if local.islower():
        parts = [part for part in re.split(r"[^a-zA-Z0-9]+", local) if part]
        return "".join(part[:1].upper() + part[1:] for part in parts)
    return local


def _extract_owl_schema(graph_payload: dict) -> tuple[set[str], dict[str, tuple[str, str]]]:
    schema = graph_payload.get("schema", {}) if isinstance(graph_payload, dict) else {}
    if not isinstance(schema, dict):
        return set(), {}

    raw_classes = schema.get("classes", [])
    raw_properties = schema.get("object_properties", [])

    classes = {
        _normalize_onto_label((cls.get("label", "") or cls.get("iri", "")))
        for cls in raw_classes
        if isinstance(cls, dict)
    }

    properties: dict[str, tuple[str, str]] = {}
    if isinstance(raw_properties, list):
        for prop in raw_properties:
            if not isinstance(prop, dict):
                continue
            property_label = _normalize_onto_label(prop.get("label") or prop.get("iri", ""))
            if not property_label:
                continue
            domain = _normalize_onto_label(prop.get("domain", ""))
            range_ = _normalize_onto_label(prop.get("range", ""))
            if domain and range_:
                properties[property_label.casefold()] = (domain, range_)

    return classes, properties


def _extract_owl_schema_from_rdf(rdf_xml: str) -> tuple[set[str], dict[str, tuple[str, str]], set[str]]:
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }
    root = ET.fromstring(rdf_xml)

    classes = set()
    for node in root.findall(".//owl:Class", ns):
        normalized_label = ""
        label_node = node.find("./rdfs:label", ns)
        if label_node is not None:
            normalized_label = _normalize_onto_label(label_node.text or "")

        if not normalized_label:
            normalized_label = _normalize_onto_label(
                node.get(f"{{{ns['rdf']}}}about")
                or node.get(f"{{{ns['rdf']}}}ID")
                or node.get("about")
                or node.get("ID")
            )

        if normalized_label:
            classes.add(normalized_label)

    properties: dict[str, tuple[str, str]] = {}
    for node in root.findall(".//owl:ObjectProperty", ns):
        normalized_label = ""
        label_node = node.find("./rdfs:label", ns)
        if label_node is not None:
            normalized_label = _normalize_onto_label(label_node.text or "")

        if not normalized_label:
            normalized_label = _normalize_onto_label(
                node.get(f"{{{ns['rdf']}}}about")
                or node.get(f"{{{ns['rdf']}}}ID")
                or node.get("about")
                or node.get("ID")
            )

        if not normalized_label:
            continue

        domain_node = node.find("./rdfs:domain", ns)
        range_node = node.find("./rdfs:range", ns)
        domain = _normalize_onto_label(domain_node.get(f"{{{ns['rdf']}}}resource") if domain_node is not None else "")
        range_ = _normalize_onto_label(range_node.get(f"{{{ns['rdf']}}}resource") if range_node is not None else "")
        properties[normalized_label.casefold()] = (domain, range_)

    label_texts = {
        (node.text or "").strip()
        for node in root.findall('.//rdfs:label', ns)
        if (node.text or '').strip()
    }

    return classes, properties, label_texts


def _ensure_generic_rdf_output(tmp_path) -> tuple[dict[str, object], str]:
    if _RDF_OUTPUT_ARTIFACT.exists() and _RDF_OUTPUT_ARTIFACT.stat().st_size > 0:
        output_payload = json.loads(_RDF_OUTPUT_JSON_ARTIFACT.read_text(encoding="utf-8")) if _RDF_OUTPUT_JSON_ARTIFACT.exists() else {}
        return output_payload, _RDF_OUTPUT_ARTIFACT.read_text(encoding="utf-8")

    text = _FIXTURE.read_text(encoding="utf-8")
    runtime_log = tmp_path / "generic-rdf-runtime-events.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})

    result = sut.process(text)
    assert result["output"]["strategy"] == "rdf"
    rdf_xml = serialize_graph_to_rdf_xml(result["output"]["graph"])
    _persist_generic_artifacts(result.get("output", {}), rdf_xml)
    return result.get("output", {}), rdf_xml


def test_rdf_smoke_library_generic_output_rdf_file_contract_red(tmp_path):
    output_payload, rdf_xml = _ensure_generic_rdf_output(tmp_path)
    assert _RDF_OUTPUT_ARTIFACT.exists(), "artifact RDF de salida genérica ausente"

    root = ET.fromstring(rdf_xml)
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    owl_class_count = len(root.findall('.//owl:Class', ns))
    owl_object_property_count = len(root.findall('.//owl:ObjectProperty', ns))
    rdf_class_nodes = root.findall('.//owl:Class/rdfs:label', ns)
    rdf_property_nodes = root.findall('.//owl:ObjectProperty', ns)

    classes_from_xml, properties_from_xml, label_texts = _extract_owl_schema_from_rdf(rdf_xml)

    assert owl_class_count >= len(_LIBRARY_BOOTSTRAP_CLASSES), (
        "owl:Class insuficientes en salida RDF genérica"
        f" observadas={owl_class_count} esperadas={len(_LIBRARY_BOOTSTRAP_CLASSES)}"
    )
    assert owl_object_property_count >= len(_LIBRARY_BOOTSTRAP_PROPERTIES), (
        "owl:ObjectProperty insuficientes en salida RDF genérica"
        f" observadas={owl_object_property_count} esperadas={len(_LIBRARY_BOOTSTRAP_PROPERTIES)}"
    )

    missing_class_labels = sorted(_LIBRARY_BOOTSTRAP_CLASSES.difference(classes_from_xml))
    assert not missing_class_labels, (
        "clases OWL esperadas no encontradas en library_generic_output.rdf: "
        f"{missing_class_labels}"
    )

    missing_property_labels = sorted({_p.casefold() for _p in _LIBRARY_BOOTSTRAP_PROPERTIES}.difference(properties_from_xml))
    assert not missing_property_labels, (
        "object properties OWL esperadas no encontradas en library_generic_output.rdf: "
        f"{missing_property_labels}"
    )

    for prop, expected in _LIBRARY_BOOTSTRAP_SIGNATURES.items():
        prop_key = prop.casefold()
        observed_domain, observed_range = properties_from_xml[prop_key]
        assert observed_domain == expected["subject"], (
            f"domain roto en RDF para '{prop}': observado={observed_domain} esperado={expected['subject']}"
        )
        assert observed_range == expected["object"], (
            f"range roto en RDF para '{prop}': observado={observed_range} esperado={expected['object']}"
        )

    expected_labels = sorted(_LIBRARY_CONCEPT_LABELS)
    observed_expected_labels = sorted(label for label in expected_labels if label in label_texts)
    assert observed_expected_labels == expected_labels, (
        "labels esperadas faltantes en library_generic_output.rdf:"
        f"{[label for label in expected_labels if label not in observed_expected_labels]}"
    )

    assert rdf_class_nodes, "labels OWL Class inexistentes en RDF genérico"
    assert rdf_property_nodes, "ObjectProperty RDF inexistentes en salida genérica"


def _persist_generic_artifacts(output_payload: dict, rdf_xml: str) -> None:
    _RDF_OUTPUT_ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    _RDF_OUTPUT_ARTIFACT.write_text(rdf_xml, encoding="utf-8")
    _RDF_OUTPUT_JSON_ARTIFACT.write_text(
        json.dumps(output_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

# UC-SMOKE-002 MF-1 | FUN-SMOKE-002 AC-1 | CON-SMOKE-RDF-014 AC-1 | BR-SMOKE-042
def test_rdf_smoke_generic_fixture_no_infosec_semantic_contamination_red(tmp_path):
    text = _FIXTURE.read_text(encoding="utf-8")
    runtime_log = tmp_path / "generic-rdf-runtime-events.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})

    result = sut.process(text)

    assert result["output"]["strategy"] == "rdf"
    rdf_xml = serialize_graph_to_rdf_xml(result["output"]["graph"])
    _persist_generic_artifacts(result.get("output", {}), rdf_xml)

    graph_payload = result["output"].get("graph", {})
    fact_count = len(graph_payload.get("facts", []))
    instance_count = len(graph_payload.get("instance_facts", []))
    subclass_count = len(graph_payload.get("subclass_facts", []))

    assert fact_count + instance_count + subclass_count > 0, (
        "grafo RDF vacío: se esperaba mínima semántica para fixture de librería genérica. "
        f"facts={fact_count} instance_facts={instance_count} subclass_facts={subclass_count}"
    )

    root = ET.fromstring(rdf_xml)
    assert root.tag.endswith("RDF")

    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    owl_class_count = len(root.findall('.//owl:Class', ns))
    owl_object_property_count = len(root.findall('.//owl:ObjectProperty', ns))
    rdfs_subclass_count = len(root.findall('.//rdfs:subClassOf', ns))
    rdf_statement_count = len(root.findall('.//rdf:Statement', ns))
    owl_ontology_count = len(root.findall('.//owl:Ontology', ns))
    label_texts = {
        (node.text or '').strip()
        for node in root.findall('.//rdfs:label', ns)
        if (node.text or '').strip()
    }
    concept_labels = sorted(label for label in _LIBRARY_CONCEPT_LABELS if label in label_texts)

    assert owl_ontology_count == 1, (
        'OWL ontology base ausente o duplicada en fixture genérico '
        f'ontology={owl_ontology_count} class={owl_class_count} objectProperty={owl_object_property_count} '
        f'subClassOf={rdfs_subclass_count} statements={rdf_statement_count}'
    )
    assert len(label_texts) >= 3 or (owl_class_count + owl_object_property_count + rdfs_subclass_count == 0), (
        'labels útiles inconsistentes con nodos visibles en RDF genérico '
        f'labels={sorted(label_texts)} class={owl_class_count} objectProperty={owl_object_property_count} subClassOf={rdfs_subclass_count}'
    )

    lowered = rdf_xml.casefold()
    leaked_terms = sorted(term for term in _INFOSEC_TERMS if term in lowered)
    assert leaked_terms == [], f"contaminación InfoSec detectada en dominio genérico: {leaked_terms}"

    leaked_iris = sorted(iri for iri in _INFOSEC_IRIS if iri in rdf_xml)
    assert leaked_iris == [], f"herencia/clases/properties infosec_3k detectadas: {leaked_iris}"


# UC-SMOKE-002 AF-1 | FUN-SMOKE-002 AC-2 | CON-SMOKE-RDF-014 AC-2 | BR-SMOKE-043
def test_rdf_strategy_static_guard_no_domain_semantic_inference_red():
    source = Path("src/pipeline/step_013_output_generation/rdf_strategy.py").read_text(encoding="utf-8")
    lowered = source.casefold()

    predicate_terms = {
        "mitigates", "contributesto", "protects", "exploits", "requires", "affects", "affect",
        "reduce", "manage", "exposes", "satisfies", "supports", "owns", "detects", "generates",
    }
    class_terms = {
        "risk", "control", "threat", "vulnerability", "asset", "incident",
        "policy", "requirement", "compliance", "evidence", "logging", "log",
        "securitycontrol", "securityobjective",
    }

    evidence = []

    for term in sorted(predicate_terms):
        if f"'{term}'" in lowered or f'"{term}"' in lowered:
            evidence.append(f"predicate-term:{term}")

    for term in sorted(class_terms):
        if f"'{term}'" in lowered or f'"{term}"' in lowered:
            evidence.append(f"class-term:{term}")


    lexical_fallback_signals = [
        "risk_synonyms",
        "reduce",
        "manage",
        "affect",
        "mitigates",
        "contributesto",
        "explicit_object_properties.append",
    ]
    if all(signal in lowered for signal in lexical_fallback_signals):
        evidence.append("hardcoded-risk-lexical-fallback")

    semantic_mapping_signals = [
        "domain_range",
        "canonicalizer",
        "synonym",
        "_map_domain_predicate",
        "_pick_domain_range_for_predicate",
        "_predicate_",
    ]
    if any(signal in lowered for signal in semantic_mapping_signals) and any(item.startswith("predicate-term:") for item in evidence):
        evidence.append("semantic-predicate-canonicalization")

    node_type_inference_signals = [
        "rdf:type",
        "_infer_class_from_node_name",
        "endswith('control')",
        "endswith('asset')",
        "endswith('risk')",
        "endswith('vulnerability')",
        "_promote_present_nodes_to_instance_types",
        "type_hints",
    ]
    if any(signal in lowered for signal in node_type_inference_signals):
        evidence.append("node-name-to-rdf-type-inference")

    assert evidence == [], (
        "semántica domain-specific detectada en rdf_strategy.py; "
        f"hallazgos={sorted(set(evidence))}"
    )


# UC-SMOKE-002 AF-2 | FUN-SMOKE-002 AC-3 | CON-SMOKE-RDF-016 AC-2 | BR-SMOKE-048
def test_generic_output_graph_schema_if_present_must_not_leak_infosec_contract():
    assert _RDF_OUTPUT_JSON_ARTIFACT.exists()

    payload = json.loads(_RDF_OUTPUT_JSON_ARTIFACT.read_text(encoding="utf-8"))
    graph = payload.get("graph", {}) if isinstance(payload, dict) else {}

    schema_buckets = {
        "classes": graph.get("classes", []),
        "type_assertions": graph.get("type_assertions", []),
        "subclass_facts": graph.get("subclass_facts", []),
        "object_property_schema": graph.get("object_property_schema", []),
        "restrictions": graph.get("restrictions", []),
    }

    serialized = json.dumps(schema_buckets, ensure_ascii=False).casefold()
    leaked_terms = sorted(term for term in _INFOSEC_TERMS if term in serialized)
    leaked_iris = sorted(iri for iri in _INFOSEC_IRIS if iri.casefold() in serialized)

    assert leaked_terms == [], f"schema contamination terms en generic graph: {leaked_terms}"
    assert leaked_iris == [], f"schema contamination IRIs en generic graph: {leaked_iris}"


# UC-SMOKE-002 AF-3 | FUN-SMOKE-002 AC-4 | CON-SMOKE-RDF-014 AC-4 | BR-SMOKE-060
def test_rdf_smoke_library_generic_owl_bootstrap_from_facts_red(tmp_path):
    text = _FIXTURE.read_text(encoding="utf-8")
    runtime_log = tmp_path / "generic-rdf-bootstrap-runtime-events.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})

    result = sut.process(text)
    assert result["output"]["strategy"] == "rdf"

    graph_payload = result["output"].get("graph", {})
    facts = graph_payload.get("facts", [])
    instance_facts = graph_payload.get("instance_facts", [])
    schema_classes, schema_properties = _extract_owl_schema(graph_payload)

    assert facts, "sin facts en salida RDF de fixture genérica"
    assert instance_facts == [], (
        "esta smoke exige bootstrap OWL desde facts y no requiere type assertions para dominio/rango"
    )

    assert schema_classes.issuperset(_LIBRARY_BOOTSTRAP_CLASSES), (
        f"faltan clases base de bootstrap OWL: observadas={sorted(schema_classes)} esperadas={sorted(_LIBRARY_BOOTSTRAP_CLASSES)}"
    )

    property_keys = set(schema_properties.keys())
    assert property_keys.issuperset({_property.casefold() for _property in _LIBRARY_BOOTSTRAP_PROPERTIES}), (
        f"faltan object properties de bootstrap OWL: observadas={sorted(property_keys)} esperadas={sorted(_LIBRARY_BOOTSTRAP_PROPERTIES)}"
    )

    for prop, expected in _LIBRARY_BOOTSTRAP_SIGNATURES.items():
        prop_key = prop.casefold()
        assert prop_key in schema_properties, f"propiedad {prop} no construida con domain/range"
        observed_domain, observed_range = schema_properties[prop_key]
        assert observed_domain == expected["subject"], (
            f"domain mismatch para {prop}: observado={observed_domain} esperado={expected['subject']}"
        )
        assert observed_range == expected["object"], (
            f"range mismatch para {prop}: observado={observed_range} esperado={expected['object']}"
        )

    serialized = json.dumps(graph_payload.get("schema", {}), ensure_ascii=False).casefold()
    leaked_terms = sorted(term for term in _INFOSEC_TERMS if term in serialized)
    leaked_iris = sorted(iri for iri in _INFOSEC_IRIS if iri.casefold() in serialized)
    assert leaked_terms == [], f"contaminación InfoSec en schema generic bootstrap: {leaked_terms}"
    assert leaked_iris == [], f"IRIs InfoSec en schema generic bootstrap: {leaked_iris}"
