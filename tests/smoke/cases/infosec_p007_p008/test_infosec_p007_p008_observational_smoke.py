from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

_SMOKE_DIR = Path(__file__).parents[2]
if str(_SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(_SMOKE_DIR))

from infosec_pair_case_harness import run_pair_case

_CASE_DIR = Path(__file__).parent
_PARAGRAPH_IDS = ['p007', 'p008']
_METRICS: dict[str, Any] | None = None


def _metrics(tmp_path: Path) -> dict[str, Any]:
    global _METRICS
    if _METRICS is None:
        _METRICS = run_pair_case(_CASE_DIR, _PARAGRAPH_IDS, tmp_path)
    return _METRICS


def test_p007_p008_observed_artifacts_are_generated_case_local(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P007_P008 | FUN-INFOSEC-PAIR-SMOKE AC-1 | CON-NO-INFOSEC-3K AC-1 | BR-INFOSEC-PAIR-SMOKE-001
    metrics = _metrics(tmp_path)

    assert metrics["claim_count"] > 0
    assert metrics["graph_generated"]
    assert metrics["rdf_generated"]
    assert metrics["rdf_bytes"] > 0


def test_p007_p008_semantic_claims_preserve_source_evidence(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P007_P008 | FUN-INFOSEC-PAIR-SMOKE AC-2 | CON-SOURCE-EVIDENCE AC-1 | BR-INFOSEC-PAIR-SMOKE-002
    metrics = _metrics(tmp_path)

    assert metrics["observed_stage"] in {"semantic_claims", "semantic_claims_artifact"}
    assert not metrics["evidence_unsupported_claim_ids"]
    assert all(count > 0 for count in metrics["paragraph_claim_distribution"].values())


def test_p007_p008_rdf_projection_has_visible_structure(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P007_P008 | FUN-INFOSEC-PAIR-SMOKE AC-3 | CON-RDF-VISIBILITY AC-1 | BR-INFOSEC-PAIR-SMOKE-003
    metrics = _metrics(tmp_path)

    assert metrics["class_count"] > 0
    assert metrics["object_property_count"] > 0


def _artifact_path(name: str) -> Path:
    return _CASE_DIR / "artifacts" / name


def _debug_ir_path() -> Path:
    return _artifact_path("observed_p007_p008_semantic_debug_ir.json")


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


def _debug_bins(ir: dict[str, Any]) -> list[Any]:
    bins: list[Any] = []
    for key in ("rejected", "contexts", "debug"):
        value = ir.get(key)
        if isinstance(value, list):
            bins.extend(value)
        elif isinstance(value, dict):
            bins.append(value)
    return bins


def test_p007_p008_rdf_does_not_emit_nominalized_ability_phrase_as_visible_class(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P007_P008 | FUN-SEMANTIC-DEBUG-IR AC-3 | CON-RDF-VISIBILITY AC-1 | BR-NO-NOMINALIZED-GIANT-CLASS-001
    _metrics(tmp_path)
    target = "AbilityToTraceActionToASpecificIdentity"
    rdf_path = _artifact_path("observed_p007_p008_output.rdf")
    graph_path = _artifact_path("observed_p007_p008_graph_model.json")
    rdf_text = rdf_path.read_text(encoding="utf-8")
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    class_labels = {
        _term(_field(item, "label", "canonical", "name", "iri", "id"))
        for item in schema.get("classes", [])
        if isinstance(item, dict)
    }

    assert target not in rdf_text
    assert _term(target) not in class_labels


def test_p007_p008_semantic_debug_ir_rejects_or_decomposes_nominalized_ability_phrase(tmp_path: Path):
    # TASK-INFOSEC-PAIR-SMOKE-P007_P008 | FUN-SEMANTIC-DEBUG-IR AC-3 | CON-SOURCE-EVIDENCE AC-1 | BR-NO-NOMINALIZED-GIANT-CLASS-001
    ir = _debug_ir(tmp_path)
    target = "AbilityToTraceActionToASpecificIdentity"
    source_sentence = "Accountability is the ability to trace actions to a specific identity."
    final_entities = {
        _term(_field(entity, "label", "canonical", "name", "id")): entity
        for entity in ir.get("entities", [])
        if isinstance(entity, dict)
    }
    debug_contains_target = any(_term(target) in _term(item) for item in _debug_bins(ir))

    assert _term(target) not in final_entities
    assert debug_contains_target or all(name in final_entities for name in ("ability", "action", "identity"))

    assert "ability" in final_entities
    assert any(name in final_entities for name in ("action", "actions"))
    assert "identity" in final_entities
    for name in ("ability", "identity"):
        assert source_sentence in str(_field(final_entities[name], "source_sentence", "evidence", "source"))
    action_entity = final_entities.get("action") or final_entities.get("actions")
    assert source_sentence in str(_field(action_entity, "source_sentence", "evidence", "source"))

