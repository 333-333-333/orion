from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import orion as orion_module
from observability import JsonlFileLogSink
from orion import ORION
from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

_RESOURCE_PREFIX = "https://orion.local/resource/"
_RDFS_SUBCLASS_OF = "rdfs:subClassOf"
_CAMEL_SPLIT = re.compile(r"([a-z])([A-Z])")
_PIPELINE_MODULE_STAGE_ARTIFACTS: tuple[tuple[int, str, str], ...] = (
    (1, "input_intake", "process_input_intake"),
    (2, "preprocessing", "preprocess_input"),
)
_PIPELINE_METHOD_STAGE_ARTIFACTS: tuple[tuple[int, str, str], ...] = (
    (3, "sentence_segmentation", "_run_sentence_segmentation"),
    (4, "tokenization", "_run_tokenization"),
    (5, "linguistic_annotation", "_run_linguistic_annotation"),
    (6, "entity_extraction", "_run_entity_extraction"),
    (7, "concept_extraction", "_run_concept_extraction"),
    (8, "coreference_resolution", "_run_coreference_resolution"),
    (9, "relation_extraction", "_run_relation_extraction"),
    (10, "canonical_claims", "_run_canonical_claims"),
    (11, "semantic_debug_ir", "_run_semantic_debug_ir"),
    (12, "triple_extraction", "_run_triple_extraction"),
    (13, "taxonomy_induction", "_run_taxonomy_induction"),
    (14, "type_assertion", "_run_type_assertion"),
    (15, "semantic_quality", "_run_semantic_quality"),
    (16, "output_generation", "_run_output_generation"),
)
PIPELINE_JSON_STAGES: tuple[tuple[int, str], ...] = tuple(
    (sequence, stage)
    for sequence, stage, _ in _PIPELINE_MODULE_STAGE_ARTIFACTS + _PIPELINE_METHOD_STAGE_ARTIFACTS
)


def slug(value: Any) -> str:
    text = str(value or "").strip()
    if text.startswith("orion:"):
        text = text[len("orion:"):]
    if text.startswith(_RESOURCE_PREFIX):
        text = text[len(_RESOURCE_PREFIX):]
    text = text.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    text = _CAMEL_SPLIT.sub(r"\1-\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-+", "-", text)


def pipeline_json_artifact_path(artifact_dir: Path, case_id: str, sequence: int, stage: str) -> Path:
    return artifact_dir / "pipeline_outputs" / f"observed_{case_id}_{sequence:02d}_{stage}.json"


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items() if not str(key).startswith("_spacy")}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return [_json_safe(item) for item in sorted(value, key=repr)]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _stage_output_only(previous_payload: Any, output: Any) -> Any:
    if not isinstance(previous_payload, dict) or not isinstance(output, dict):
        return output
    delta: dict[str, Any] = {}
    for key, value in output.items():
        key_text = str(key)
        if key_text.startswith("_spacy"):
            continue
        if key not in previous_payload:
            delta[key_text] = value
            continue
        previous_value = previous_payload[key]
        if value == previous_value:
            continue
        if isinstance(previous_value, dict) and isinstance(value, dict):
            nested_delta = _stage_output_only(previous_value, value)
            if nested_delta:
                delta[key_text] = nested_delta
        else:
            delta[key_text] = value
    return delta


def _write_pipeline_json_artifact(
    artifact_dir: Path,
    case_id: str,
    sequence: int,
    stage: str,
    previous_payload: Any,
    output: Any,
) -> Path:
    path = pipeline_json_artifact_path(artifact_dir, case_id, sequence, stage)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _json_safe(_stage_output_only(previous_payload, output))
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _clear_pipeline_json_artifacts(artifact_dir: Path, case_id: str) -> None:
    pipeline_dir = artifact_dir / "pipeline_outputs"
    if not pipeline_dir.exists():
        return
    for path in pipeline_dir.glob(f"observed_{case_id}_*.json"):
        path.unlink()


def process_with_pipeline_json_artifacts(
    sut: ORION,
    input_data: Any,
    artifact_dir: Path,
    case_id: str,
) -> tuple[dict[str, Any], list[Path]]:
    _clear_pipeline_json_artifacts(artifact_dir, case_id)
    pipeline_paths: list[Path] = []
    original_module_functions: dict[str, Any] = {}
    original_methods: dict[str, Any] = {}

    def capture(sequence: int, stage: str, previous_payload: Any, output: Any) -> Any:
        pipeline_paths.append(_write_pipeline_json_artifact(artifact_dir, case_id, sequence, stage, previous_payload, output))
        return output

    for sequence, stage, function_name in _PIPELINE_MODULE_STAGE_ARTIFACTS:
        original = getattr(orion_module, function_name)
        original_module_functions[function_name] = original

        def wrapped_module_function(*args: Any, _original: Any = original, _sequence: int = sequence, _stage: str = stage, **kwargs: Any) -> Any:
            previous_payload = None if _stage == "input_intake" else (args[0] if args else kwargs.get("input_payload"))
            return capture(_sequence, _stage, previous_payload, _original(*args, **kwargs))

        setattr(orion_module, function_name, wrapped_module_function)

    for sequence, stage, method_name in _PIPELINE_METHOD_STAGE_ARTIFACTS:
        original = getattr(sut, method_name)
        original_methods[method_name] = original

        def wrapped_method(*args: Any, _original: Any = original, _sequence: int = sequence, _stage: str = stage, **kwargs: Any) -> Any:
            previous_payload = args[0] if args else kwargs.get("payload") or kwargs.get("input_payload")
            return capture(_sequence, _stage, previous_payload, _original(*args, **kwargs))

        setattr(sut, method_name, wrapped_method)

    try:
        return sut.process(input_data), pipeline_paths
    finally:
        for function_name, original in original_module_functions.items():
            setattr(orion_module, function_name, original)
        for method_name, original in original_methods.items():
            setattr(sut, method_name, original)


def _observed_payload(result: dict[str, Any], semantic_path: Path, canonical_path: Path) -> dict[str, Any]:
    if isinstance(result.get("semantic_claims"), dict):
        payload = dict(result["semantic_claims"])
        payload["observed_stage"] = "semantic_claims"
        return payload
    artifacts = result.get("artifacts") if isinstance(result.get("artifacts"), dict) else {}
    if isinstance(artifacts.get("semantic_claims"), dict):
        payload = dict(artifacts["semantic_claims"])
        payload["observed_stage"] = "semantic_claims"
        return payload
    if semantic_path.exists():
        payload = json.loads(semantic_path.read_text(encoding="utf-8"))
        payload["observed_stage"] = payload.get("observed_stage", "semantic_claims_artifact")
        return payload
    if isinstance(result.get("canonical_claims"), dict):
        payload = dict(result["canonical_claims"])
        payload["observed_stage"] = "canonical_claims"
        return payload
    if canonical_path.exists():
        payload = json.loads(canonical_path.read_text(encoding="utf-8"))
        payload["observed_stage"] = "canonical_claims_artifact"
        return payload
    return {"observed_stage": "missing", "claims": []}


def _graph(result: dict[str, Any]) -> dict[str, Any]:
    output = result.get("output") if isinstance(result.get("output"), dict) else {}
    graph = output.get("graph") if isinstance(output.get("graph"), dict) else {}
    return graph if isinstance(graph, dict) else {}


def _claims(payload: dict[str, Any]) -> list[dict[str, Any]]:
    claims = payload.get("claims")
    if not isinstance(claims, list):
        return []
    return [item for item in claims if isinstance(item, dict)]


def _claim_source(claim: dict[str, Any]) -> dict[str, Any]:
    return claim.get("source") if isinstance(claim.get("source"), dict) else {}


def _supported_claims(claims: list[dict[str, Any]], paragraph_texts: dict[str, str]) -> tuple[list[str], list[str]]:
    supported: list[str] = []
    unsupported: list[str] = []
    combined = "\n\n".join(paragraph_texts.values()).lower()
    for index, claim in enumerate(claims):
        source = _claim_source(claim)
        evidence = str(source.get("evidence") or "").strip()
        claim_id = str(claim.get("claim_id") or f"claim-{index}")
        if evidence and evidence.lower() in combined:
            supported.append(claim_id)
        else:
            unsupported.append(claim_id)
    return supported, unsupported


def _ttl_local_name(value: Any) -> str:
    text = _ttl_resource_name(value)
    return text.lower()


def _ttl_resource_name(value: Any) -> str:
    text = str(value or "").strip()
    if text.startswith("orion:"):
        text = text[len("orion:"):]
    if text.startswith(_RESOURCE_PREFIX):
        text = text[len(_RESOURCE_PREFIX):]
    text = text.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return re.sub(r"[^A-Za-z0-9]", "", text)


def _serialize_visual_turtle(graph: dict[str, Any]) -> str:
    lines = [
        "@prefix orion: <https://orion.local/resource/> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
    ]
    facts = graph.get("facts") if isinstance(graph.get("facts"), list) else []
    subclass_facts = graph.get("subclass_facts") if isinstance(graph.get("subclass_facts"), list) else []
    triples: set[tuple[str, str, str]] = set()
    subclass_triples: set[tuple[str, str]] = set()
    for fact in facts:
        if not isinstance(fact, dict):
            continue
        subject = _ttl_local_name(fact.get("subject"))
        predicate = _ttl_local_name(fact.get("predicate"))
        obj = _ttl_local_name(fact.get("object"))
        if subject and predicate and obj:
            triples.add((subject, predicate, obj))
    for fact in subclass_facts:
        if not isinstance(fact, dict) or fact.get("predicate") != _RDFS_SUBCLASS_OF:
            continue
        subject = _ttl_resource_name(fact.get("subject"))
        obj = _ttl_resource_name(fact.get("object"))
        if subject and obj:
            subclass_triples.add((subject, obj))
    lines.extend(
        f"orion:{subject} orion:{predicate} orion:{obj} ."
        for subject, predicate, obj in sorted(triples)
    )
    lines.extend(
        f"orion:{subject} {_RDFS_SUBCLASS_OF} orion:{obj} ."
        for subject, obj in sorted(subclass_triples)
    )
    return "\n".join(lines) + "\n"


def _schema_counts(graph: dict[str, Any]) -> dict[str, int]:
    schema = graph.get("schema") if isinstance(graph.get("schema"), dict) else {}
    return {
        "class_count": len([item for item in schema.get("classes", []) if isinstance(item, dict)]),
        "object_property_count": len([item for item in schema.get("object_properties", []) if isinstance(item, dict)]),
        "subclass_fact_count": len([item for item in graph.get("subclass_facts", []) if isinstance(item, dict)]),
    }


def run_pair_case(
    case_dir: Path,
    paragraph_ids: list[str],
    tmp_path: Path,
    case_id: str | None = None,
    fixture_dir: Path | None = None,
) -> dict[str, Any]:
    smoke_dir = case_dir.parents[1]
    paragraph_dir = fixture_dir or smoke_dir / "fixtures" / "infosec_3k_paragraphs"
    artifact_dir = case_dir / "artifacts"
    case_id = case_id or "_".join(paragraph_ids)
    semantic_path = artifact_dir / f"observed_{case_id}_semantic_claims.json"
    canonical_path = artifact_dir / f"observed_{case_id}_canonical_claims.json"
    graph_path = artifact_dir / f"observed_{case_id}_graph_model.json"
    debug_ir_path = artifact_dir / f"observed_{case_id}_semantic_debug_ir.json"
    rdf_path = artifact_dir / f"observed_{case_id}_output.rdf"
    ttl_path = artifact_dir / f"observed_{case_id}_output.ttl"
    metrics_path = artifact_dir / f"observed_{case_id}_metrics.json"
    pipeline_json_dir = artifact_dir / "pipeline_outputs"
    for path in (semantic_path, canonical_path, graph_path, debug_ir_path, rdf_path, ttl_path, metrics_path):
        if path.exists():
            path.unlink()
    _clear_pipeline_json_artifacts(artifact_dir, case_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    paragraph_texts = {
        pid: (paragraph_dir / f"{pid}.txt").read_text(encoding="utf-8").strip()
        for pid in paragraph_ids
    }
    runtime_log = tmp_path / f"{case_id}-runtime-events.jsonl"
    sut = ORION(
        config={
            "logging": {"sink": JsonlFileLogSink(runtime_log)},
            "spacy_model": "en_core_web_lg",
            "output_strategy": "rdf",
            "semantic_claims": {"artifact_path": semantic_path, "paragraph_asset_ids": paragraph_ids},
            "semantic_debug_ir": {"artifact_path": debug_ir_path, "paragraph_asset_ids": paragraph_ids},
            "canonical_claims": {"artifact_path": canonical_path, "paragraph_asset_ids": paragraph_ids},
        }
    )
    result, pipeline_json_paths = process_with_pipeline_json_artifacts(
        sut,
        "\n\n".join(paragraph_texts[pid] for pid in paragraph_ids),
        artifact_dir,
        case_id,
    )
    payload = _observed_payload(result, semantic_path, canonical_path)
    payload.setdefault("contract_required_stage", "semantic_claims")
    payload.setdefault("paragraph_asset_ids", paragraph_ids)
    semantic_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    graph = _graph(result)
    if graph:
        graph_path.write_text(
            json.dumps(graph, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        rdf_xml = serialize_graph_to_rdf_xml(graph)
        if "<rdf:RDF" in rdf_xml:
            rdf_path.write_text(rdf_xml, encoding="utf-8")
        ttl_path.write_text(_serialize_visual_turtle(graph), encoding="utf-8")
    claims = _claims(payload)
    supported, unsupported = _supported_claims(claims, paragraph_texts)
    counts = _schema_counts(graph)
    paragraph_distribution: dict[str, int] = {pid: 0 for pid in paragraph_ids}
    for claim in claims:
        source = _claim_source(claim)
        pid = str(claim.get("paragraph_id") or source.get("paragraph_id") or source.get("asset_id") or "")
        if pid in paragraph_distribution:
            paragraph_distribution[pid] += 1
    metrics = {
        "case_id": case_id,
        "paragraph_ids": paragraph_ids,
        "claim_count": len(claims),
        "evidence_supported_claim_count": len(supported),
        "evidence_unsupported_claim_ids": unsupported,
        "evidence_precision_proxy": round(len(supported) / max(1, len(claims)), 4),
        "paragraph_claim_distribution": paragraph_distribution,
        "observed_stage": payload.get("observed_stage"),
        "rdf_generated": rdf_path.exists(),
        "rdf_bytes": rdf_path.stat().st_size if rdf_path.exists() else 0,
        "ttl_generated": ttl_path.exists(),
        "ttl_bytes": ttl_path.stat().st_size if ttl_path.exists() else 0,
        "graph_generated": graph_path.exists(),
        "semantic_debug_ir_generated": debug_ir_path.exists(),
        "semantic_debug_ir_path": str(debug_ir_path.relative_to(case_dir)),
        "pipeline_output_json_generated": len(pipeline_json_paths) == len(PIPELINE_JSON_STAGES),
        "pipeline_output_json_count": len(pipeline_json_paths),
        "pipeline_output_json_expected_count": len(PIPELINE_JSON_STAGES),
        "pipeline_output_json_dir": str(pipeline_json_dir.relative_to(case_dir)),
        "pipeline_output_json_paths": [str(path.relative_to(case_dir)) for path in pipeline_json_paths],
        **counts,
    }
    metrics_path.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metrics
