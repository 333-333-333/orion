from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_CASES_DIR = Path(__file__).parent / "cases"
_REQUIRED_SPO = ("subject", "predicate", "object")


def _label_words(value: Any) -> list[str]:
    text = str(value or "")
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    return [word.casefold() for word in re.sub(r"[^A-Za-z0-9]+", " ", text).split()]


def _is_projection_scaffold(value: Any) -> bool:
    words = _label_words(value)
    return len(words) >= 2 and words[:2] in (
        ["type", "of"],
        ["kind", "of"],
        ["category", "of"],
        ["form", "of"],
    )


def test_all_observed_semantic_claims_are_projection_safe_or_explicitly_rejected():
    artifact_paths = sorted(_CASES_DIR.glob("*/artifacts/*_semantic_claims.json"))
    assert artifact_paths, "semantic→RDF acceptance contract needs generated semantic artifacts"

    violations: list[str] = []
    for path in artifact_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        claims = payload.get("claims") if isinstance(payload.get("claims"), list) else []
        rejected = payload.get("rejected_claims") if isinstance(payload.get("rejected_claims"), list) else []
        accepted_ids = {str(claim.get("claim_id")) for claim in claims if isinstance(claim, dict) and claim.get("claim_id")}
        rejected_ids = {str(claim.get("claim_id")) for claim in rejected if isinstance(claim, dict) and claim.get("claim_id")}

        duplicate_dispositions = sorted(accepted_ids & rejected_ids)
        if duplicate_dispositions:
            violations.append(f"{path.parent.parent.name}: accepted and rejected IDs overlap={duplicate_dispositions[:5]}")

        for claim in claims:
            if not isinstance(claim, dict):
                violations.append(f"{path.parent.parent.name}: accepted claim is not an object")
                continue
            if not str(claim.get("claim_id") or "").strip():
                violations.append(f"{path.parent.parent.name}: accepted claim has no claim_id")
            missing = [field for field in _REQUIRED_SPO if not str(claim.get(field, "")).strip()]
            if missing:
                violations.append(f"{path.parent.parent.name}:{claim.get('claim_id')}: missing accepted SPO={missing}")
            scaffolds = [field for field in ("subject", "object") if _is_projection_scaffold(claim.get(field))]
            if scaffolds:
                violations.append(f"{path.parent.parent.name}:{claim.get('claim_id')}: projection scaffold in={scaffolds}")

        for claim in rejected:
            if not isinstance(claim, dict):
                violations.append(f"{path.parent.parent.name}: rejected claim is not an object")
                continue
            if not str(claim.get("type") or claim.get("rejection_reason") or "").strip():
                violations.append(f"{path.parent.parent.name}:{claim.get('claim_id')}: rejection has no reason")

    assert not violations, "semantic claim acceptance contract broken:\n" + "\n".join(violations[:20])


def test_all_rdf_projections_dispose_every_semantic_claim_with_auditable_output():
    semantic_paths = sorted(_CASES_DIR.glob("*/artifacts/*_semantic_claims.json"))
    violations: list[str] = []

    for semantic_path in semantic_paths:
        prefix = semantic_path.name.removesuffix("_semantic_claims.json")
        graph_path = semantic_path.with_name(f"{prefix}_graph_model.json")
        if not graph_path.exists():
            violations.append(f"{semantic_path.parent.parent.name}: graph artifact missing for semantic projection")
            continue
        semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        claims = [claim for claim in semantic.get("claims", []) if isinstance(claim, dict)]
        claim_ids = {str(claim.get("claim_id")) for claim in claims if claim.get("claim_id")}
        projection = graph.get("projection") if isinstance(graph.get("projection"), dict) else {}
        dispositions = projection.get("claim_dispositions") if isinstance(projection.get("claim_dispositions"), list) else []
        disposition_by_id = {
            str(item.get("claim_id")): item
            for item in dispositions
            if isinstance(item, dict) and item.get("claim_id")
        }
        projected_ids = {str(item) for item in projection.get("claim_ids", []) if str(item)}
        materialized_ids = {str(item) for item in projection.get("materialized_claim_ids", []) if str(item)}
        excluded_ids = {str(item) for item in projection.get("excluded_claim_ids", []) if str(item)}
        graph_spo = {
            (str(item.get("subject")), str(item.get("predicate")), str(item.get("object")))
            for key in ("facts", "subclass_facts")
            for item in graph.get(key, [])
            if isinstance(item, dict)
        }

        if claim_ids != projected_ids or claim_ids != set(disposition_by_id):
            violations.append(
                f"{semantic_path.parent.parent.name}: incomplete disposition "
                f"missing={sorted(claim_ids - set(disposition_by_id))[:5]} "
                f"foreign={sorted(set(disposition_by_id) - claim_ids)[:5]}"
            )

        expected_materialized: set[str] = set()
        expected_excluded: set[str] = set()
        for claim_id, disposition in disposition_by_id.items():
            status = str(disposition.get("status") or "")
            if status in {"materialized", "transformed"}:
                expected_materialized.add(claim_id)
                output = disposition.get("output_spo") if isinstance(disposition.get("output_spo"), dict) else {}
                output_spo = (str(output.get("subject")), str(output.get("predicate")), str(output.get("object")))
                if not all(output_spo) or output_spo not in graph_spo:
                    violations.append(f"{semantic_path.parent.parent.name}:{claim_id}: {status} output is not in graph")
            elif status in {"excluded", "evidence_only"}:
                if status == "excluded":
                    expected_excluded.add(claim_id)
                if not str(disposition.get("reason") or "").strip():
                    violations.append(f"{semantic_path.parent.parent.name}:{claim_id}: {status} disposition has no reason")
            else:
                violations.append(f"{semantic_path.parent.parent.name}:{claim_id}: unknown disposition={status!r}")

        if materialized_ids != expected_materialized:
            violations.append(f"{semantic_path.parent.parent.name}: materialized_claim_ids disagree with dispositions")
        if excluded_ids != expected_excluded:
            violations.append(f"{semantic_path.parent.parent.name}: excluded_claim_ids disagree with dispositions")

    assert not violations, "semantic→RDF disposition contract broken:\n" + "\n".join(violations[:20])


def test_all_semantic_quality_reports_account_for_claim_attrition():
    semantic_paths = sorted(_CASES_DIR.glob("*/artifacts/*_semantic_claims.json"))
    violations: list[str] = []

    for semantic_path in semantic_paths:
        prefix = semantic_path.name.removesuffix("_semantic_claims.json")
        pipeline_dir = semantic_path.parent / "pipeline_outputs"
        triple_path = pipeline_dir / f"{prefix}_12_triple_extraction.json"
        quality_path = pipeline_dir / f"{prefix}_15_semantic_quality.json"
        if not triple_path.exists() or not quality_path.exists():
            violations.append(f"{semantic_path.parent.parent.name}: triple or quality stage artifact missing")
            continue

        semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
        triple_payload = json.loads(triple_path.read_text(encoding="utf-8"))
        quality_payload = json.loads(quality_path.read_text(encoding="utf-8"))
        report = quality_payload.get("semantic_quality_report") if isinstance(quality_payload.get("semantic_quality_report"), dict) else {}
        claims = [item for item in semantic.get("claims", []) if isinstance(item, dict)]
        rejected = [item for item in semantic.get("rejected_claims", []) if isinstance(item, dict)]
        claim_ids = {str(item.get("claim_id")) for item in claims if item.get("claim_id")}
        triple_ids = {
            str(item.get("relation_id"))
            for item in triple_payload.get("triples", [])
            if isinstance(item, dict) and item.get("relation_id")
        }
        rejected_ids = {str(item.get("claim_id")) for item in rejected if item.get("claim_id")}
        invalid_rejected_ids = {
            str(item.get("claim_id"))
            for item in rejected
            if item.get("claim_id") and item.get("type") == "invalid_semantic_claim"
        }

        expected_missing = claim_ids - triple_ids
        expected_foreign = triple_ids - claim_ids
        if report.get("semantic_claim_count") != len(claims):
            violations.append(f"{semantic_path.parent.parent.name}: semantic_claim_count is stale")
        if report.get("rejected_claim_count") != len(rejected):
            violations.append(f"{semantic_path.parent.parent.name}: rejected_claim_count is stale")
        if set(report.get("rejected_claim_ids", [])) != rejected_ids:
            violations.append(f"{semantic_path.parent.parent.name}: rejected IDs are not traceable")
        if set(report.get("invalid_rejected_claim_ids", [])) != invalid_rejected_ids:
            violations.append(f"{semantic_path.parent.parent.name}: invalid rejected IDs are not traceable")
        if set(report.get("claims_without_triple_ids", [])) != expected_missing:
            violations.append(f"{semantic_path.parent.parent.name}: claims_without_triple_ids mismatch")
        if set(report.get("triples_without_claim_ids", [])) != expected_foreign:
            violations.append(f"{semantic_path.parent.parent.name}: triples_without_claim_ids mismatch")
        if (expected_missing or expected_foreign) and report.get("rdf_readiness") is not False:
            violations.append(f"{semantic_path.parent.parent.name}: RDF readiness ignores claim attrition")
        if invalid_rejected_ids:
            if "invalid_semantic_claims_rejected" not in report.get("warnings", []):
                violations.append(f"{semantic_path.parent.parent.name}: invalid rejected claims have no warning")
            if not isinstance(report.get("quality_score"), (int, float)) or report["quality_score"] >= 1.0:
                violations.append(f"{semantic_path.parent.parent.name}: invalid rejected claims do not reduce quality")

    assert not violations, "semantic quality attrition contract broken:\n" + "\n".join(violations[:20])
