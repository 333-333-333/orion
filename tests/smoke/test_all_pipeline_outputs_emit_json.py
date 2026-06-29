from __future__ import annotations

import json
from pathlib import Path

from infosec_pair_case_harness import PIPELINE_JSON_STAGES, pipeline_json_artifact_path

_INHERITED_KEYS_BY_SEQUENCE = {
    1: set(),
    2: {"raw_text", "source_text_id", "metadata"},
    3: {"raw_text", "source_text_id", "metadata", "preprocessed_text", "operations_applied"},
    4: {"raw_text", "source_text_id", "metadata", "preprocessed_text", "operations_applied", "sentences"},
    5: {"raw_text", "source_text_id", "metadata", "preprocessed_text", "operations_applied", "sentences"},
}
_DEFAULT_INHERITED_KEYS = {
    "raw_text",
    "source_text_id",
    "metadata",
    "preprocessed_text",
    "operations_applied",
    "sentences",
    "tokens",
}


def test_all_smoke_cases_emit_json_for_each_pipeline_output() -> None:
    cases_dir = Path(__file__).parent / "cases"
    rdf_paths = sorted(cases_dir.glob("*/artifacts/observed_*_output.rdf"))
    assert rdf_paths, "smoke suite should generate RDF artifacts before pipeline JSON audit"

    missing: list[str] = []
    invalid: list[str] = []
    incremental: list[str] = []
    for rdf_path in rdf_paths:
        case_id = rdf_path.name.removeprefix("observed_").removesuffix("_output.rdf")
        for sequence, stage in PIPELINE_JSON_STAGES:
            json_path = pipeline_json_artifact_path(rdf_path.parent, case_id, sequence, stage)
            if not json_path.exists():
                missing.append(str(json_path))
                continue
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                invalid.append(str(json_path))
                continue
            inherited_keys = _INHERITED_KEYS_BY_SEQUENCE.get(sequence, _DEFAULT_INHERITED_KEYS)
            leaked_keys = sorted(inherited_keys & payload.keys())
            if leaked_keys:
                incremental.append(f"{json_path}: {leaked_keys}")

    assert not missing, "missing per-stage pipeline JSON artifacts: " + ", ".join(missing)
    assert not invalid, "invalid per-stage pipeline JSON artifacts: " + ", ".join(invalid)
    assert not incremental, "pipeline JSON artifacts must contain only their stage output, not cumulative payloads: " + ", ".join(incremental)
