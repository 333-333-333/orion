from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest


_NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
}

_RDF_ATTR = {
    "about": f'{{{_NS["rdf"]}}}about',
    "ID": f'{{{_NS["rdf"]}}}ID',
    "resource": f'{{{_NS["rdf"]}}}resource',
}

_LIBRARY_RDF_OUTPUT_ARTIFACT = Path(__file__).parent / "artifacts" / "library_generic_output.rdf"
_LIBRARY_JSON_ARTIFACT = Path(__file__).parent / "artifacts" / "library_generic_output.json"
_INFOSEC_RDF_OUTPUT_ARTIFACT = Path(__file__).parent / "artifacts" / "infosec_3k_output.rdf"
_INFOSEC_JSON_ARTIFACT = Path(__file__).parent / "artifacts" / "infosec_3k_rdf_output.json"

_ALIAS_ONLY_PARENT_LABELS = {
    'advisorydocument',
    'advisory-document',
    'control-document',
    'controldocument',
    'formal-document',
    'formaldocument',
    'foundational-model',
    'foundationalmodel',
    'minimum-set-of-controls',
    'minimumsetofcontrols',
    'operational-document',
    'operationaldocument',
}


def _normalize_label(value: str) -> str:
    token = (value or "").strip()
    if not token:
        return ""
    token = token.rsplit("/", 1)[-1]
    token = token.rsplit("#", 1)[-1]
    if token.startswith("orion:"):
        token = token.split(":", 1)[1]
    return token




def _graph_payload(output_payload: dict) -> dict:
    graph = output_payload.get("graph", {}) if isinstance(output_payload, dict) else {}
    return graph if isinstance(graph, dict) else {}


def _schema_class_rows(output_payload: dict) -> list[dict]:
    graph = _graph_payload(output_payload)
    schema = graph.get("schema", {}) if isinstance(graph.get("schema"), dict) else {}
    raw_classes = schema.get("classes", []) if isinstance(schema, dict) else []
    return [cls for cls in raw_classes if isinstance(cls, dict)] if isinstance(raw_classes, list) else []


def _schema_object_property_links(output_payload: dict) -> set[str]:
    graph = _graph_payload(output_payload)
    schema = graph.get("schema", {}) if isinstance(graph.get("schema"), dict) else {}
    rows = schema.get("object_properties", []) if isinstance(schema, dict) else []
    linked: set[str] = set()
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            linked.add(_normalize_label(str(row.get("domain", ""))))
            linked.add(_normalize_label(str(row.get("range", ""))))
    return {item for item in linked if item}


def _schema_subclass_pairs(output_payload: dict) -> set[tuple[str, str]]:
    graph = _graph_payload(output_payload)
    pairs: set[tuple[str, str]] = set()
    for row in graph.get("subclass_facts", []) if isinstance(graph.get("subclass_facts"), list) else []:
        if isinstance(row, dict):
            pairs.add((_normalize_label(str(row.get("subject") or row.get("subclass") or "")), _normalize_label(str(row.get("object") or row.get("superclass") or ""))))
    for cls in _schema_class_rows(output_payload):
        parent = cls.get("subClassOf") or cls.get("subclass_of") or cls.get("superclass")
        if parent:
            pairs.add((_normalize_label(str(cls.get("iri") or cls.get("label") or "")), _normalize_label(str(parent))))
    return {(child, parent) for child, parent in pairs if child and parent}

def _schema_classes(output_payload: dict) -> dict[str, str]:
    classes: dict[str, str] = {}
    for cls in _schema_class_rows(output_payload):
        iri = str(cls.get("iri", "")).strip()
        label = str(cls.get("label", "")).strip()
        if iri:
            classes[iri] = label
    return classes


def _rdf_classes(root: ET.Element) -> tuple[dict[str, list[str]], list[str], list[str]]:
    rdf_classes: dict[str, list[str]] = {}
    anonymous: list[str] = []
    mute: list[str] = []

    for node in root.findall('.//owl:Class', _NS):
        iri = node.attrib.get(_RDF_ATTR['about'], '').strip() or node.attrib.get(_RDF_ATTR['ID'], '').strip()
        labels = [
            (label.text or '').strip()
            for label in node.findall('rdfs:label', _NS)
            if (label.text or '').strip()
        ]
        if not iri:
            anonymous.append(labels[0] if labels else 'anonymous')
            continue
        if not labels:
            mute.append(iri)
        rdf_classes[iri] = labels

    return rdf_classes, anonymous, mute


@pytest.mark.parametrize(
    'artifact_path,json_path,contract_scope',
    [
        (_LIBRARY_RDF_OUTPUT_ARTIFACT, _LIBRARY_JSON_ARTIFACT, 'library'),
        (_INFOSEC_RDF_OUTPUT_ARTIFACT, _INFOSEC_JSON_ARTIFACT, 'infosec_3k'),
    ],
)
def test_rdf_output_contract_schema_classes_are_visible_red(artifact_path: Path, json_path: Path, contract_scope: str):
    assert artifact_path.exists(), f"artifact RDF ausente para {contract_scope}: {artifact_path}"
    assert json_path.exists(), f"artifact JSON ausente para {contract_scope}: {json_path}"

    output_payload = json.loads(json_path.read_text(encoding='utf-8'))
    expected_classes = _schema_classes(output_payload)
    assert expected_classes, f"{contract_scope}: schema.classes vacio en JSON"

    rdf_xml = artifact_path.read_text(encoding='utf-8')
    root = ET.fromstring(rdf_xml)
    rdf_classes, anonymous_classes, mute_classes = _rdf_classes(root)

    missing_classes = sorted(iri for iri in expected_classes if iri not in rdf_classes)
    assert not missing_classes, (
        f"{contract_scope}: faltan owl:Class para schema.classes en RDF; sample={missing_classes[:8]}"
    )

    label_mismatches = sorted(
        iri for iri, expected_label in expected_classes.items()
        if expected_label and _normalize_label(expected_label) not in {_normalize_label(label) for label in rdf_classes.get(iri, [])}
    )
    assert not label_mismatches, (
        f"{contract_scope}: labels de owl:Class no calzan con schema.classes; sample={label_mismatches[:8]}"
    )

    assert not anonymous_classes, (
        f"{contract_scope}: owl:Class anonimos detectados; sample={anonymous_classes[:8]}"
    )
    assert not mute_classes, (
        f"{contract_scope}: owl:Class mudos detectados; sample={mute_classes[:8]}"
    )



@pytest.mark.parametrize(
    'artifact_path,json_path,contract_scope',
    [
        (_LIBRARY_RDF_OUTPUT_ARTIFACT, _LIBRARY_JSON_ARTIFACT, 'library'),
        (_INFOSEC_RDF_OUTPUT_ARTIFACT, _INFOSEC_JSON_ARTIFACT, 'infosec_3k'),
    ],
)
def test_rdf_output_contract_visible_classes_have_evidence_backed_differentiator_red(artifact_path: Path, json_path: Path, contract_scope: str):
    # TASK-ONT-004 | FUN-SMOKE-001 AC-12 | CON-SMOKE-RDF-004 AC-2 | BR-SMOKE-014
    assert artifact_path.exists(), f"artifact RDF ausente para {contract_scope}: {artifact_path}"
    assert json_path.exists(), f"artifact JSON ausente para {contract_scope}: {json_path}"

    output_payload = json.loads(json_path.read_text(encoding='utf-8'))
    rdf_xml = artifact_path.read_text(encoding='utf-8')
    root = ET.fromstring(rdf_xml)
    rdf_classes, _, _ = _rdf_classes(root)
    object_property_linked = _schema_object_property_links(output_payload)
    subclass_pairs = _schema_subclass_pairs(output_payload)
    superclass_only = {parent for _, parent in subclass_pairs} - {child for child, _ in subclass_pairs}

    leaks = []
    for iri, labels in rdf_classes.items():
        label_tokens = {_normalize_label(iri), *(_normalize_label(label) for label in labels)}
        alias_only = label_tokens & _ALIAS_ONLY_PARENT_LABELS
        has_differentiator = bool(label_tokens & object_property_linked)
        is_superclass_only = bool(label_tokens & superclass_only)
        if alias_only and is_superclass_only and not has_differentiator:
            leaks.append({"iri": iri, "labels": labels, "alias_tokens": sorted(alias_only)})

    assert not leaks, f"{contract_scope}: alias-only visible classes lack evidence-backed differentiator: {leaks[:8]}"
