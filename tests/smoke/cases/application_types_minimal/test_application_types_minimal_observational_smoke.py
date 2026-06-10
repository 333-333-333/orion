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
_PARAGRAPH_IDS = ["application_types_001"]
_CASE_ID = "application_types_minimal"
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(
            _CASE_DIR,
            _PARAGRAPH_IDS,
            tmp_path,
            case_id=_CASE_ID,
            fixture_dir=_CASE_DIR / "fixtures",
        )
    return _METRICS


def _artifact_json(name: str) -> dict[str, Any]:
    return json.loads((_CASE_DIR / "artifacts" / name).read_text(encoding="utf-8"))


def _class_slugs(graph: dict[str, Any]) -> set[str]:
    classes: list[Any] = []
    if isinstance(graph.get("classes"), list):
        classes.extend(graph["classes"])
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    if isinstance(schema.get("classes"), list):
        classes.extend(schema["classes"])
    values: set[str] = set()
    for item in classes:
        if not isinstance(item, dict):
            continue
        for key in ("label", "iri", "id", "name"):
            if item.get(key):
                values.add(slug(item[key]))
    return values


def _subclass_pairs(graph: dict[str, Any]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for item in graph.get("subclass_facts", []):
        if isinstance(item, dict):
            pairs.add((slug(item.get("subject") or item.get("subclass")), slug(item.get("object") or item.get("superclass"))))
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    for item in schema.get("classes", []):
        if isinstance(item, dict):
            parent = item.get("subClassOf") or item.get("subclass_of") or item.get("superclass")
            if parent:
                pairs.add((slug(item.get("iri") or item.get("label") or item.get("id")), slug(parent)))
    return pairs


def test_application_types_minimal_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-APP-TYPES-RED-001 | FUN-APP-TYPES AC-1 | CON-SMOKE-MODULAR AC-1 | BR-APP-TYPES-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_application_types_minimal_preserves_source_evidence(tmp_path: Path):
    # TASK-APP-TYPES-RED-001 | FUN-APP-TYPES AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-APP-TYPES-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert metrics["paragraph_claim_distribution"]["application_types_001"] > 0


def test_application_types_minimal_emits_application_taxonomy(tmp_path: Path):
    # TASK-APP-TYPES-RED-001 | FUN-APP-TYPES AC-3 | CON-APP-TAXONOMY AC-1 | BR-APP-TYPES-003
    _metrics(tmp_path)
    graph = _artifact_json("observed_application_types_minimal_graph_model.json")
    classes = _class_slugs(graph)
    pairs = _subclass_pairs(graph)

    missing_classes = {"application", "web-application", "mobile-application"} - classes
    missing_pairs = {
        ("web-application", "application"),
        ("mobile-application", "application"),
    } - pairs

    assert not missing_classes, f"missing application taxonomy classes: {sorted(missing_classes)}; classes={sorted(classes)}"
    assert not missing_pairs, f"missing direct application subClassOf pairs: {sorted(missing_pairs)}; pairs={sorted(pairs)}"


def test_application_types_minimal_does_not_cross_subclass_siblings(tmp_path: Path):
    # TASK-APP-TYPES-RED-001 | FUN-APP-TYPES AC-4 | CON-APP-TAXONOMY AC-2 | BR-APP-TYPES-004
    _metrics(tmp_path)
    graph = _artifact_json("observed_application_types_minimal_graph_model.json")
    pairs = _subclass_pairs(graph)
    forbidden = {
        ("mobile-application", "web-application"),
        ("web-application", "mobile-application"),
    }
    leaked = sorted(forbidden & pairs)

    assert not leaked, f"sibling application types leaked as cross subClassOf pairs: {leaked}"
