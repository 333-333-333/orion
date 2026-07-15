from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case, slug

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p043']
_METRICS: dict[str, Any] | None = None


def _artifact(name: str) -> Path:
    return _CASE_DIR / "artifacts" / name


def _load_json_artifact(name: str) -> dict[str, Any]:
    return json.loads(_artifact(name).read_text(encoding="utf-8"))


def _class_slugs(graph: dict[str, Any]) -> set[str]:
    classes: list[Any] = []
    classes.extend(graph.get("classes", []))
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    classes.extend(schema.get("classes", []))
    values: set[str] = set()
    for item in classes:
        if not isinstance(item, dict):
            continue
        for key in ("label", "iri", "id", "name"):
            if item.get(key):
                values.add(slug(item[key]))
    return values


def _object_property_edges(graph: dict[str, Any]) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for key in ("object_property_facts", "object_property_schema"):
        for item in graph.get(key, []):
            if isinstance(item, dict):
                edges.append((slug(item.get("domain")), slug(item.get("predicate")), slug(item.get("range"))))
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    for item in schema.get("object_properties", []):
        if isinstance(item, dict):
            edges.append((slug(item.get("domain")), slug(item.get("predicate") or item.get("iri") or item.get("label")), slug(item.get("range"))))
    for item in graph.get("scoped_relations", []):
        if isinstance(item, dict):
            edges.append((slug(item.get("subject")), slug(item.get("predicate")), slug(item.get("object"))))
    return edges


def _claim_edges(payload: dict[str, Any]) -> list[tuple[str, str, str]]:
    claims = payload.get("claims") if isinstance(payload.get("claims"), list) else []
    return [
        (slug(claim.get("subject")), slug(claim.get("predicate")), slug(claim.get("object")))
        for claim in claims
        if isinstance(claim, dict)
    ]


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p043_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P043 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p043_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P043 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p043_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P043 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0

def test_p043_task_001_explicit_svo_entities_are_separate_classes(tmp_path: Path):
    # TASK-001 p043 | FUN-P043-SVO AC-1 | CON-P043-EXPLICIT-SVO AC-1 | BR-P043-SVO-001
    _metrics(tmp_path)
    graph = _load_json_artifact("observed_p043_graph_model.json")
    classes = _class_slugs(graph)
    expected_entity_groups = {
        "users": {"user", "users"},
        "systems": {"system", "systems"},
        "roles": {"role", "roles"},
        "permissions": {"permission", "permissions"},
        "controls": {"control", "controls"},
        "risks": {"risk", "risks"},
        "threats": {"threat", "threats"},
        "vulnerabilities": {"vulnerability", "vulnerabilities"},
        "incidents": {"incident", "incidents"},
        "assets": {"asset", "assets"},
        "information assets": {"information-asset", "information-assets"},
        "policies": {"policy", "policies"},
        "requirements": {"requirement", "requirements"},
        "suppliers": {"supplier", "suppliers"},
        "services": {"service", "services"},
        "auditors": {"auditor", "auditors"},
        "compliance": {"compliance"},
    }
    missing = [name for name, aliases in expected_entity_groups.items() if classes.isdisjoint(aliases)]
    assert not missing, f"p043 explicit SVO entities missing as separate classes/nodes: {missing}; classes={sorted(classes)}"


def test_p043_task_001_access_is_object_property_between_users_and_systems(tmp_path: Path):
    # TASK-001 p043 | FUN-P043-SVO AC-2 | CON-P043-EXPLICIT-SVO AC-2 | BR-P043-SVO-002
    _metrics(tmp_path)
    graph = _load_json_artifact("observed_p043_graph_model.json")
    edges = _object_property_edges(graph)
    assert any(
        domain in {"user", "users"}
        and predicate in {"access", "accesses"}
        and range_ in {"system", "systems"}
        for domain, predicate, range_ in edges
    ), f"missing explicit users access systems object property; edges={edges}"


def test_p043_audited_relations_keep_should_scope_and_discourse_closure(tmp_path: Path):
    _metrics(tmp_path)
    payload = _load_json_artifact("observed_p043_semantic_claims.json")
    claims = [item for item in payload.get("claims", []) if isinstance(item, dict)]

    represented = [item for item in claims if item.get("relation_role") == "represented_content"]
    assert len(represented) == 14
    assert all(item.get("modality") == "should" and item.get("scope") == "ResultingOntology" for item in represented)
    assert ("backup", "supports", "availability") in {
        (slug(item.get("subject")), slug(item.get("predicate")), slug(item.get("object"))) for item in represented
    }
    assert not any(item.get("subject") == "Encryption" and item.get("predicate") == "backups" for item in claims)
    requirement_claims = [item for item in represented if item.get("subject") == "Requirement"]
    assert [(item.get("predicate"), item.get("object")) for item in requirement_claims] == [("beSatisfiedBy", "Control")]

    assert not any(item.get("subject") == "RelationshipSet" for item in claims)
    suitability = [
        item for item in claims
        if item.get("subject") == "GeneratedGraph"
        and item.get("predicate") == "suitable_for"
        and item.get("relation_role") == "discourse_consequence"
    ]
    assert {item.get("object") for item in suitability} == {"Querying", "Validation", "Reasoning", "Mining"}
    assert all(
        item.get("graph_format_alternatives") == "RDF,OWL"
        and item.get("graph_format_operator") == "or"
        and item.get("antecedent_scope") == "represented_relationships"
        for item in suitability
    )

    graph = _load_json_artifact("observed_p043_graph_model.json")
    assert any(
        slug(item.get("subject")) == "backup"
        and slug(item.get("predicate")) == "supports"
        and slug(item.get("object")) == "availability"
        for item in graph.get("scoped_relations", [])
    )
    assert graph.get("restrictions") == []


def test_p043_suitability_and_support_pairs_survive_projection(tmp_path: Path):
    _metrics(tmp_path)
    graph = _load_json_artifact("observed_p043_graph_model.json")
    suitability_relations = [
        item for item in graph.get("scoped_relations", [])
        if slug(item.get("subject")) == "generated-graph"
        and slug(item.get("predicate")) == "suitable-for"
    ]
    assert {slug(item.get("object")) for item in suitability_relations} == {
        "querying", "validation", "reasoning", "mining",
    }
    assert all(
        item.get("graph_format_alternatives") == "RDF,OWL"
        and item.get("graph_format_operator") == "or"
        and item.get("relation_role") == "discourse_consequence"
        for item in suitability_relations
    )
    assert not any(slug(item.get("predicate")) == "suitable-for" for item in graph.get("facts", []))

    supports_schema = next(
        item for item in graph.get("object_property_schema", [])
        if slug(item.get("predicate")) == "supports"
    )
    scoped_pairs = {
        (slug(item.get("domain")), slug(item.get("range")))
        for item in supports_schema.get("scoped_pairs", [])
    }
    assert scoped_pairs == {("backup", "availability"), ("logging", "accountability")}

    quality = _load_json_artifact("pipeline_outputs/observed_p043_15_semantic_quality.json")["semantic_quality_report"]
    assert "missing_graph_suitability_inventory" not in quality.get("semantic_integrity_issues", [])
    assert any(item.get("reason") == "predicate_absorbed_into_concept" for item in quality.get("concept_noise", []))
    assert quality.get("quality_score", 1.0) < 1.0
    assert quality.get("rdf_readiness") is False


def test_p043_task_001_no_compound_relation_classes_or_meta_hub(tmp_path: Path):
    # TASK-001 p043 | FUN-P043-SVO AC-3 | CON-P043-NO-COMPOUND-CLASS AC-1 | BR-P043-SVO-003
    _metrics(tmp_path)
    graph = _load_json_artifact("observed_p043_graph_model.json")
    payload = _load_json_artifact("observed_p043_semantic_claims.json")
    classes = _class_slugs(graph)
    forbidden_classes = {
        "access-system",
        "control-reduce-risk",
        "threat-exploit-vulnerability",
        "incident-affect-asset",
        "system-process-information-asset",
        "policy-define-requirement",
        "requirement-are-satisfied-by-control",
        "supplier-provide-service",
        "resulting-ontology",
        "resulting-ontology-should-represent",
    }
    present_forbidden = sorted(classes.intersection(forbidden_classes))
    assert not present_forbidden, f"compound relation/meta-hub classes present: {present_forbidden}"

    edges = _claim_edges(payload) + _object_property_edges(graph)
    hub_subject_edges = [edge for edge in edges if edge[0] in {"resulting-ontology", "resulting-ontology-should-represent"}]
    assert not hub_subject_edges, f"anonymous/meta hub replaces explicit p043 SVO edges: {hub_subject_edges}"

