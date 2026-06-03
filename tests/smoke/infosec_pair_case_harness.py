from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from observability import JsonlFileLogSink
from orion import ORION
from pipeline.step_013_output_generation.rdf_strategy import serialize_graph_to_rdf_xml

_RESOURCE_PREFIX = "https://orion.local/resource/"
_CAMEL_SPLIT = re.compile(r"([a-z])([A-Z])")


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
) -> dict[str, Any]:
    smoke_dir = case_dir.parents[1]
    paragraph_dir = smoke_dir / "fixtures" / "infosec_3k_paragraphs"
    artifact_dir = case_dir / "artifacts"
    case_id = case_id or "_".join(paragraph_ids)
    semantic_path = artifact_dir / f"observed_{case_id}_semantic_claims.json"
    canonical_path = artifact_dir / f"observed_{case_id}_canonical_claims.json"
    graph_path = artifact_dir / f"observed_{case_id}_graph_model.json"
    rdf_path = artifact_dir / f"observed_{case_id}_output.rdf"
    metrics_path = artifact_dir / f"observed_{case_id}_metrics.json"
    for path in (semantic_path, canonical_path, graph_path, rdf_path, metrics_path):
        if path.exists():
            path.unlink()
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
            "canonical_claims": {"artifact_path": canonical_path, "paragraph_asset_ids": paragraph_ids},
        }
    )
    result = sut.process("\n\n".join(paragraph_texts[pid] for pid in paragraph_ids))
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
        "graph_generated": graph_path.exists(),
        **counts,
    }
    metrics_path.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metrics
