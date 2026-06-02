from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET


_ORION_NS = 'https://orion.local/resource/'


_RDF_ARTIFACT = Path(__file__).parent / "artifacts" / "infosec_3k_output.rdf"
_JSON_ARTIFACT = Path(__file__).parent / "artifacts" / "infosec_3k_rdf_output.json"


def _leaf(iri: str) -> str:
    return iri.rsplit('/', 1)[-1].lower()


def _label_matches_leaf(label: str, leaf: str) -> bool:
    normalized = (label or '').strip().casefold()
    leaf = (leaf or '').strip().casefold()
    if not normalized or not leaf:
        return False
    return (
        normalized == leaf
        or normalized.startswith(f"{leaf} ")
        or normalized.startswith(f"{leaf}(")
        or normalized.startswith(f"{leaf}[")
    )


def _label_contains_roles(label: str, roles: set[str]) -> bool:
    normalized = (label or '').casefold()
    if not normalized:
        return False
    return all(role in normalized for role in roles)


def _normalize_roles(raw: set[str]) -> list[str]:
    return [role for role in ('subject', 'predicate', 'object') if role in raw]


# UC-SMOKE-001 AF-20 | FUN-SMOKE-001 AC-22 | CON-SMOKE-RDF-018 AC-1 | BR-SMOKE-051
def test_contextual_entities_contract_red_for_polysemy_pronouns_and_generic_nodes():
    assert _RDF_ARTIFACT.exists(), "falta artifact RDF infosec_3k_output.rdf"
    assert _JSON_ARTIFACT.exists(), "falta artifact JSON infosec_3k_rdf_output.json"

    payload = json.loads(_JSON_ARTIFACT.read_text(encoding="utf-8"))
    facts = payload.get("graph", {}).get("facts", [])

    assert facts, "fixture inválido: graph.facts vacío"

    by_leaf_roles: dict[str, set[str]] = {}
    by_leaf_role_by_iri: dict[str, dict[str, set[str]]] = {}
    bad_pronouns: list[str] = []
    bad_generic_type: list[str] = []

    for fact in facts:
        s = str(fact.get("subject", ""))
        p = str(fact.get("predicate", ""))
        o = str(fact.get("object", ""))
        span = fact.get("evidence_span", {})
        if _leaf(s) in {"that", "which", "who"} or _leaf(o) in {"that", "which", "who"}:
            bad_pronouns.append(f"{s}|{p}|{o}")

        if o.endswith('/type'):
            bad_generic_type.append(f"{s}|{p}|{o}|span={span}")

        if s.startswith('https://orion.local/resource/'):
            leaf = _leaf(s)
            by_leaf_roles.setdefault(leaf, set()).add('subject')
            by_leaf_role_by_iri.setdefault(leaf, {}).setdefault(s, set()).add('subject')
        if o.startswith('https://orion.local/resource/'):
            leaf = _leaf(o)
            by_leaf_roles.setdefault(leaf, set()).add('object')
            by_leaf_role_by_iri.setdefault(leaf, {}).setdefault(o, set()).add('object')
        if p.startswith('orion:'):
            leaf = p.split(':', 1)[1].lower()
            by_leaf_roles.setdefault(leaf, set()).add('predicate')
            by_leaf_role_by_iri.setdefault(leaf, {}).setdefault(f"{_ORION_NS}{leaf}", set()).add('predicate')
        elif p.startswith('https://orion.local/resource/'):
            leaf = _leaf(p)
            by_leaf_roles.setdefault(leaf, set()).add('predicate')
            by_leaf_role_by_iri.setdefault(leaf, {}).setdefault(p, set()).add('predicate')

    ambiguous = {k: sorted(v) for k, v in by_leaf_roles.items() if k in {"access", "process"} and len(v) > 1}

    root = ET.fromstring(_RDF_ARTIFACT.read_text(encoding="utf-8"))
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    }

    labels_by_iri: dict[str, set[str]] = {}
    for node in list(root):
        iri = node.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
        if not iri:
            continue
        current = labels_by_iri.setdefault(iri, set())
        for child in node.findall('rdfs:label', ns):
            if child.text and child.text.strip():
                current.add(child.text.strip().lower())

    for node in root.findall('.//rdf:Description', ns):
        iri = node.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
        if not iri:
            continue
        for child in node.findall('rdfs:label', ns):
            if child.text and child.text.strip():
                labels_by_iri.setdefault(iri, set()).add(child.text.strip().lower())

    referenced = set()
    for stmt in root.findall('.//rdf:Statement', ns):
        for tag in ('subject', 'predicate', 'object'):
            obj = stmt.find(f'rdf:{tag}', ns)
            if obj is None:
                continue
            iri = obj.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
            if iri:
                referenced.add(iri)

    unlabeled_refs = sorted(
        [iri for iri in referenced if not any(_label_matches_leaf(label, _leaf(iri)) for label in labels_by_iri.get(iri, set()))]
    )

    missing_role_labels = []
    for leaf, roles in ambiguous.items():
        leaf = str(leaf)
        needed = set(_normalize_roles(set(roles)))
        labeled_ok = False
        for iri, iri_roles in by_leaf_role_by_iri.get(leaf, {}).items():
            if not needed.issubset(iri_roles):
                continue
            if any(_label_contains_roles(label, needed) for label in labels_by_iri.get(iri, set())):
                labeled_ok = True
                break
        if not labeled_ok:
            missing_role_labels.append(f"{leaf}:{sorted(roles)}")

    assert not missing_role_labels, (
        "contrato contextual roto: access/process sigue multi-rol sin etiqueta contextual por rol; "
        f"hallazgos={missing_role_labels}, ambigüedad={ambiguous}"
    )
    assert bad_pronouns == [], f"pronombre relativo visible como resource RDF: {bad_pronouns[:8]}"
    assert bad_generic_type == [], f"nodo genérico type usado sin evidencia nominal concreta: {bad_generic_type[:8]}"
    assert unlabeled_refs == [], f"resources referenciados por rdf:Statement sin label visible: {unlabeled_refs[:8]}"


# UC-SMOKE-001 AF-21 | FUN-SMOKE-001 AC-23 | CON-SMOKE-RDF-019 AC-1 | BR-SMOKE-052
def test_contextual_schema_domain_range_must_trace_real_fact_direction_red():
    assert _RDF_ARTIFACT.exists(), "falta artifact RDF infosec_3k_output.rdf"
    assert _JSON_ARTIFACT.exists(), "falta artifact JSON infosec_3k_rdf_output.json"

    payload = json.loads(_JSON_ARTIFACT.read_text(encoding="utf-8"))
    facts = payload.get("graph", {}).get("facts", []) if isinstance(payload, dict) else []

    root = ET.fromstring(_RDF_ARTIFACT.read_text(encoding="utf-8"))
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    rdf_about = f'{{{ns["rdf"]}}}about'
    rdf_res = f'{{{ns["rdf"]}}}resource'

    def _local(value: str) -> str:
        return str(value or "").strip().rsplit('/', 1)[-1].split(':')[-1].casefold()

    fact_pairs = set()
    for f in facts:
        if not isinstance(f, dict):
            continue
        pred = _local(f.get("predicate", ""))
        subj = _local(f.get("subject", ""))
        obj = _local(f.get("object", ""))
        if pred and subj and obj:
            fact_pairs.add((pred, subj, obj))

    stale_mitigates = []
    for op in root.findall('.//owl:ObjectProperty', ns):
        piri = op.attrib.get(rdf_about, '').strip()
        pred = _local(piri)
        if pred != 'mitigates':
            continue
        domains = [
            _local(d.attrib.get(rdf_res, '').strip())
            for d in op.findall('rdfs:domain', ns)
            if d.attrib.get(rdf_res, '').strip()
        ]
        ranges = [
            _local(r.attrib.get(rdf_res, '').strip())
            for r in op.findall('rdfs:range', ns)
            if r.attrib.get(rdf_res, '').strip()
        ]
        for domain in domains:
            for rng in ranges:
                if (pred, domain, rng) not in fact_pairs:
                    stale_mitigates.append((pred, domain, rng))

    assert not stale_mitigates, (
        "schema stale: domain/range no sale de facts reales ni dirección textual; "
        f"stale_mitigates={stale_mitigates[:8]}"
    )


# UC-SMOKE-001 AF-22 | FUN-SMOKE-001 AC-24 | CON-SMOKE-RDF-019 AC-2 | BR-SMOKE-053
def test_contextual_nodes_must_have_visible_identity_in_local_name_red():
    assert _RDF_ARTIFACT.exists(), "falta artifact RDF infosec_3k_output.rdf"

    root = ET.fromstring(_RDF_ARTIFACT.read_text(encoding="utf-8"))
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    }

    rdf_about = f'{{{ns["rdf"]}}}about'
    weak_context_nodes = []

    for node in root.findall('.//*[@rdf:about]', ns):
        iri = node.attrib.get(rdf_about, '').strip()
        if not iri.startswith(_ORION_NS):
            continue
        labels = [(lbl.text or '').strip().casefold() for lbl in node.findall('rdfs:label', ns) if (lbl.text or '').strip()]
        if not labels:
            continue
        if not any('subject|predicate|object' in lbl or '(subject|' in lbl for lbl in labels):
            continue

        local = iri.rsplit('/', 1)[-1].casefold()
        has_role_slug = any(role in local for role in ('subject', 'predicate', 'object'))
        has_spo_slug = ('__' in local and any(token in local for token in ('subj', 'pred', 'obj', 'subject', 'predicate', 'object')))

        if not has_role_slug and not has_spo_slug:
            weak_context_nodes.append((iri, labels[0]))

    assert not weak_context_nodes, (
        "nodo contextual sin identidad visible en local-name; usar slug determinista por role o SPO además de rdfs:label; "
        f"sample={weak_context_nodes[:8]}"
    )


# UC-SMOKE-001 AF-23 | FUN-SMOKE-001 AC-25 | CON-SMOKE-RDF-020 AC-1 | BR-SMOKE-054
def test_reified_statement_local_name_and_class_description_label_contract_red():
    assert _RDF_ARTIFACT.exists(), "falta artifact RDF infosec_3k_output.rdf"

    root = ET.fromstring(_RDF_ARTIFACT.read_text(encoding="utf-8"))
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }

    rdf_about = f'{{{ns["rdf"]}}}about'

    long_or_opaque_reified = []
    for stmt in root.findall('.//rdf:Statement', ns):
        iri = stmt.attrib.get(rdf_about, '').strip()
        if not iri or '/statement/' not in iri:
            continue
        local = iri.rsplit('/', 1)[-1]
        if len(local) > 48 or 'subject__' in local or '__predicate__' in local or '__object__' in local:
            long_or_opaque_reified.append(local)

    class_labels = {}
    for cls in root.findall('.//owl:Class', ns):
        iri = cls.attrib.get(rdf_about, '').strip()
        if not iri:
            continue
        labels = [
            (c.text or '').strip()
            for c in cls.findall('rdfs:label', ns)
            if (c.text or '').strip()
        ]
        class_labels[iri] = labels

    mute_duplicate_descriptions = []
    for desc in root.findall('.//rdf:Description', ns):
        iri = desc.attrib.get(rdf_about, '').strip()
        if not iri or iri not in class_labels:
            continue
        desc_labels = [
            (c.text or '').strip()
            for c in desc.findall('rdfs:label', ns)
            if (c.text or '').strip()
        ]
        has_subclass = desc.find('rdfs:subClassOf', ns) is not None
        if has_subclass and class_labels[iri] and not desc_labels:
            mute_duplicate_descriptions.append(iri)

    assert not long_or_opaque_reified, (
        'rdf:Statement visible con local-name largo/opaco; usar slug corto deterministico SPO tipo management-protect-token; '
        f'sample={long_or_opaque_reified[:8]}'
    )
    assert not mute_duplicate_descriptions, (
        'rdf:Description duplicada muda para IRI owl:Class con label; mover subClassOf al owl:Class con label o repetir label en description; '
        f'sample={mute_duplicate_descriptions[:8]}'
    )
