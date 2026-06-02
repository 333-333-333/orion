from __future__ import annotations

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
    "resource": f'{{{_NS["rdf"]}}}resource',
}

_LIBRARY_RDF_OUTPUT_ARTIFACT = Path(__file__).parent / "artifacts" / "library_generic_output.rdf"
_INFOSEC_RDF_OUTPUT_ARTIFACT = Path(__file__).parent / "artifacts" / "infosec_3k_output.rdf"


def _local_name(iri: str) -> str:
    token = (iri or "").strip()
    if not token:
        return ""
    token = token.rsplit("#", 1)[-1]
    token = token.rsplit("/", 1)[-1]
    return token


def _domain_nodes(root: ET.Element) -> set[str]:
    nodes: set[str] = set()
    for xpath in (".//owl:Class", ".//owl:ObjectProperty"):
        for node in root.findall(xpath, _NS):
            iri = node.attrib.get(_RDF_ATTR["about"], "").strip()
            if iri.startswith("https://orion.local/resource/"):
                nodes.add(iri)
    return nodes


def _add_edge(edges: dict[str, set[str]], left: str, right: str) -> None:
    if left in edges and right in edges and left != right:
        edges[left].add(right)
        edges[right].add(left)


def _isolated_visible_nodes(root: ET.Element) -> tuple[int, list[str]]:
    visible_nodes = _domain_nodes(root)
    edges: dict[str, set[str]] = {iri: set() for iri in visible_nodes}

    # taxonomía
    for cls in root.findall('.//owl:Class', _NS):
        c = cls.attrib.get(_RDF_ATTR["about"], "").strip()
        if c not in visible_nodes:
            continue
        for sub in cls.findall('rdfs:subClassOf', _NS):
            parent = sub.attrib.get(_RDF_ATTR["resource"], "").strip()
            if parent:
                _add_edge(edges, c, parent)

        for restriction in cls.findall('rdfs:subClassOf/owl:Restriction', _NS):
            on_property = restriction.find('owl:onProperty', _NS)
            on_iri = on_property.attrib.get(_RDF_ATTR["resource"], "").strip() if on_property is not None else ""
            if on_iri:
                _add_edge(edges, c, on_iri)

            for child in ('owl:someValuesFrom', 'owl:allValuesFrom'):
                obj_node = restriction.find(child, _NS)
                obj_iri = obj_node.attrib.get(_RDF_ATTR["resource"], "").strip() if obj_node is not None else ""
                if obj_iri:
                    _add_edge(edges, c, obj_iri)

    # propiedades semánticas
    for prop in root.findall('.//owl:ObjectProperty', _NS):
        p = prop.attrib.get(_RDF_ATTR["about"], "").strip()
        if p not in visible_nodes:
            continue
        for domain in prop.findall('rdfs:domain', _NS):
            _add_edge(edges, p, domain.attrib.get(_RDF_ATTR["resource"], "").strip())
        for rng in prop.findall('rdfs:range', _NS):
            _add_edge(edges, p, rng.attrib.get(_RDF_ATTR["resource"], "").strip())

    # conexiones explícitas por statements reificados
    for stmt in root.findall('.//rdf:Statement', _NS):
        subject_node = stmt.find('rdf:subject', _NS)
        predicate_node = stmt.find('rdf:predicate', _NS)
        object_node = stmt.find('rdf:object', _NS)

        subject = subject_node.attrib.get(_RDF_ATTR["resource"], "").strip() if subject_node is not None else ""
        predicate = predicate_node.attrib.get(_RDF_ATTR["resource"], "").strip() if predicate_node is not None else ""
        object_ = object_node.attrib.get(_RDF_ATTR["resource"], "").strip() if object_node is not None else ""

        if subject in edges and predicate in edges:
            _add_edge(edges, subject, predicate)
        if predicate in edges and object_ in edges:
            _add_edge(edges, predicate, object_)
        if subject in edges and object_ in edges:
            _add_edge(edges, subject, object_)

    isolated = sorted(
        iri
        for iri, neighbors in edges.items()
        if not neighbors
    )

    return len(visible_nodes), isolated


@pytest.mark.parametrize(
    "artifact_path,contract_scope",
    [
        (_LIBRARY_RDF_OUTPUT_ARTIFACT, "library"),
        (_INFOSEC_RDF_OUTPUT_ARTIFACT, "infosec_3k"),
    ],
)
def test_rdf_output_contract_no_visible_isolated_nodes_red(artifact_path: Path, contract_scope: str):
    assert artifact_path.exists(), f"artifact RDF ausente para {contract_scope}: {artifact_path}"

    rdf_xml = artifact_path.read_text(encoding="utf-8")
    root = ET.fromstring(rdf_xml)

    visible_total, isolated_nodes = _isolated_visible_nodes(root)
    local_examples = [_local_name(iri) for iri in isolated_nodes[:12]]

    assert not isolated_nodes, (
        f"{contract_scope}: publicó {len(isolated_nodes)} nodos visibles aislados en RDF (total visibles={visible_total}); "
        f"ejemplos_locales={local_examples}"
    )
