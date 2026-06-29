from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from pipeline_step_runner import (
    PipelineStepInputValidationError,
    execute_pipeline_step_from_files,
    pipeline_step_contracts_json,
    validate_step_input,
)


def test_pipeline_step_contracts_expose_required_and_optional_json_attributes() -> None:
    contracts = pipeline_step_contracts_json()

    assert contracts["preprocessing"]["required"] == ["raw_text", "source_text_id", "metadata"]
    assert contracts["sentence_segmentation"]["required"] == [
        "raw_text",
        "source_text_id",
        "metadata",
        "preprocessed_text",
        "operations_applied",
    ]
    assert "noun_chunks" in contracts["coreference_resolution"]["optional"]
    assert "semantic_claims" in contracts["triple_extraction"]["optional"]
    assert "config" in contracts["output_generation"]["runner_optional"]


def test_pipeline_step_input_validation_rejects_missing_required_attribute() -> None:
    with pytest.raises(PipelineStepInputValidationError, match="missing required attributes for preprocessing: source_text_id"):
        validate_step_input("preprocessing", {"raw_text": "Hello.", "metadata": {}})


def test_pipeline_step_input_validation_rejects_unknown_attribute() -> None:
    with pytest.raises(PipelineStepInputValidationError, match="unknown attributes for preprocessing: tokens"):
        validate_step_input(
            "preprocessing",
            {"raw_text": "Hello.", "source_text_id": "source-1", "metadata": {}, "tokens": []},
        )


def test_pipeline_step_runner_cli_executes_specific_step_from_json_file(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    input_json = tmp_path / "preprocessing-input.json"
    output_json = tmp_path / "preprocessing-output.json"
    input_json.write_text(
        json.dumps({"raw_text": "Hello    world.", "source_text_id": "source-1", "metadata": {}}),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(repo_root / "tests/smoke/pipeline_step_runner.py"),
            "preprocessing",
            "--input-json",
            str(input_json),
            "--output-json",
            str(output_json),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload == {
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "preprocessed_text": "Hello world.",
    }


def test_pipeline_step_runner_merges_stage_only_json_inputs_for_next_step(tmp_path: Path) -> None:
    intake_output = tmp_path / "01-input-intake.json"
    preprocessing_output = tmp_path / "02-preprocessing.json"
    output_json = tmp_path / "03-sentence-segmentation.json"
    intake_output.write_text(
        json.dumps({"raw_text": "Hello world. Bye.", "source_text_id": "source-1", "metadata": {}}),
        encoding="utf-8",
    )
    preprocessing_output.write_text(
        json.dumps({"preprocessed_text": "Hello world. Bye.", "operations_applied": ["manual"]}),
        encoding="utf-8",
    )

    payload = execute_pipeline_step_from_files(
        "03_sentence_segmentation",
        [intake_output, preprocessing_output],
        output_json,
    )

    assert sorted(payload) == ["sentences"]
    assert [sentence["text"] for sentence in payload["sentences"]] == ["Hello world.", "Bye."]
    assert "raw_text" not in json.loads(output_json.read_text(encoding="utf-8"))
