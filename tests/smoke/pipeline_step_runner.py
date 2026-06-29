from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import orion as orion_module
from orion import ORION

DEFAULT_PIPELINE_STEP_CONFIG: dict[str, Any] = {
    "spacy_model": "en_core_web_lg",
    "output_strategy": "rdf",
}
_RUNNER_METADATA_TYPES: dict[str, tuple[type[Any], ...]] = {
    "config": (dict,),
    "schema_version": (int,),
    "description": (str,),
}
_FIELD_TYPES: dict[str, tuple[type[Any], ...]] = {
    "input_data": (str,),
    "raw_text": (str,),
    "source_text_id": (str,),
    "metadata": (dict,),
    "preprocessed_text": (str,),
    "operations_applied": (list,),
    "sentences": (list,),
    "tokens": (list,),
    "entities": (list,),
    "concepts": (list,),
    "noun_chunks": (list,),
    "coreferences": (list,),
    "relations": (list,),
    "canonical_claims": (dict,),
    "semantic_claims": (dict,),
    "artifacts": (dict,),
    "triples": (list,),
    "taxonomy_relations": (list,),
    "type_assertions": (list,),
    "semantic_quality_report": (dict,),
    "excluded_entities": (list,),
    "excluded_concepts": (list,),
}


@dataclass(frozen=True)
class PipelineStepInputContract:
    sequence: int
    stage: str
    required: tuple[str, ...]
    optional: tuple[str, ...] = ()
    description: str = ""

    @property
    def allowed_payload_keys(self) -> set[str]:
        return set(self.required) | set(self.optional)

    def as_json(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "stage": self.stage,
            "required": list(self.required),
            "optional": list(self.optional),
            "runner_optional": sorted(_RUNNER_METADATA_TYPES),
            "description": self.description,
        }


class PipelineStepInputValidationError(ValueError):
    pass


_BASE_TEXT_PAYLOAD = ("raw_text", "source_text_id", "metadata")
_PREPROCESSED_PAYLOAD = (*_BASE_TEXT_PAYLOAD, "preprocessed_text", "operations_applied")
_SENTENCE_PAYLOAD = (*_PREPROCESSED_PAYLOAD, "sentences")
_TOKEN_PAYLOAD = (*_SENTENCE_PAYLOAD, "tokens")
_ENTITY_PAYLOAD = (*_TOKEN_PAYLOAD, "entities")
_CONCEPT_PAYLOAD = (*_ENTITY_PAYLOAD, "concepts")
_COREFERENCE_PAYLOAD = (*_CONCEPT_PAYLOAD, "coreferences")
_RELATION_PAYLOAD = (*_COREFERENCE_PAYLOAD, "relations")
_CANONICAL_PAYLOAD = (*_RELATION_PAYLOAD, "canonical_claims")
_TRIPLE_PAYLOAD = (*_CANONICAL_PAYLOAD, "triples")
_TAXONOMY_PAYLOAD = (*_TRIPLE_PAYLOAD, "taxonomy_relations")
_TYPE_PAYLOAD = (*_TAXONOMY_PAYLOAD, "type_assertions")
_QUALITY_PAYLOAD = (*_TYPE_PAYLOAD, "semantic_quality_report", "excluded_entities", "excluded_concepts")
_SEMANTIC_OPTIONAL = ("semantic_claims", "artifacts", "noun_chunks")

PIPELINE_STEP_INPUT_CONTRACTS: tuple[PipelineStepInputContract, ...] = (
    PipelineStepInputContract(
        1,
        "input_intake",
        required=("input_data",),
        description="Runner input document for raw text or a .txt path before ORION intake.",
    ),
    PipelineStepInputContract(
        2,
        "preprocessing",
        required=_BASE_TEXT_PAYLOAD,
        description="Cumulative intake payload produced by input_intake.",
    ),
    PipelineStepInputContract(
        3,
        "sentence_segmentation",
        required=_PREPROCESSED_PAYLOAD,
        description="Cumulative preprocessed payload before sentence segmentation.",
    ),
    PipelineStepInputContract(
        4,
        "tokenization",
        required=_SENTENCE_PAYLOAD,
        description="Cumulative sentence payload before tokenization.",
    ),
    PipelineStepInputContract(
        5,
        "linguistic_annotation",
        required=_TOKEN_PAYLOAD,
        description="Cumulative token payload before spaCy-backed annotation.",
    ),
    PipelineStepInputContract(
        6,
        "entity_extraction",
        required=_TOKEN_PAYLOAD,
        description="Cumulative annotated-token payload before entity extraction.",
    ),
    PipelineStepInputContract(
        7,
        "concept_extraction",
        required=_ENTITY_PAYLOAD,
        description="Cumulative entity payload before concept extraction.",
    ),
    PipelineStepInputContract(
        8,
        "coreference_resolution",
        required=_CONCEPT_PAYLOAD,
        optional=("noun_chunks",),
        description="Cumulative concept payload before coreference resolution.",
    ),
    PipelineStepInputContract(
        9,
        "relation_extraction",
        required=_COREFERENCE_PAYLOAD,
        optional=("noun_chunks",),
        description="Cumulative coreference payload before relation extraction.",
    ),
    PipelineStepInputContract(
        10,
        "canonical_claims",
        required=_RELATION_PAYLOAD,
        optional=("artifacts", "noun_chunks"),
        description="Cumulative relation payload before canonical/semantic claim extraction.",
    ),
    PipelineStepInputContract(
        11,
        "semantic_debug_ir",
        required=_CANONICAL_PAYLOAD,
        optional=_SEMANTIC_OPTIONAL,
        description="Cumulative claim payload before optional semantic debug IR materialization.",
    ),
    PipelineStepInputContract(
        12,
        "triple_extraction",
        required=_CANONICAL_PAYLOAD,
        optional=_SEMANTIC_OPTIONAL,
        description="Cumulative claim payload before deterministic triple extraction.",
    ),
    PipelineStepInputContract(
        13,
        "taxonomy_induction",
        required=_TRIPLE_PAYLOAD,
        optional=_SEMANTIC_OPTIONAL,
        description="Cumulative triple payload before taxonomy induction.",
    ),
    PipelineStepInputContract(
        14,
        "type_assertion",
        required=_TAXONOMY_PAYLOAD,
        optional=_SEMANTIC_OPTIONAL,
        description="Cumulative taxonomy payload before type assertion.",
    ),
    PipelineStepInputContract(
        15,
        "semantic_quality",
        required=_TYPE_PAYLOAD,
        optional=_SEMANTIC_OPTIONAL,
        description="Cumulative type-asserted semantic payload before semantic quality checks.",
    ),
    PipelineStepInputContract(
        16,
        "output_generation",
        required=_QUALITY_PAYLOAD,
        optional=_SEMANTIC_OPTIONAL,
        description="Cumulative quality-assessed payload before final output projection.",
    ),
)
_PIPELINE_STEP_CONTRACT_BY_STAGE = {contract.stage: contract for contract in PIPELINE_STEP_INPUT_CONTRACTS}
_STAGE_METHODS: dict[str, str] = {
    "sentence_segmentation": "_run_sentence_segmentation",
    "tokenization": "_run_tokenization",
    "linguistic_annotation": "_run_linguistic_annotation",
    "entity_extraction": "_run_entity_extraction",
    "concept_extraction": "_run_concept_extraction",
    "coreference_resolution": "_run_coreference_resolution",
    "relation_extraction": "_run_relation_extraction",
    "canonical_claims": "_run_canonical_claims",
    "semantic_debug_ir": "_run_semantic_debug_ir",
    "triple_extraction": "_run_triple_extraction",
    "taxonomy_induction": "_run_taxonomy_induction",
    "type_assertion": "_run_type_assertion",
    "semantic_quality": "_run_semantic_quality",
    "output_generation": "_run_output_generation",
}
_STAGE_ALIASES: dict[str, str] = {}
for _contract in PIPELINE_STEP_INPUT_CONTRACTS:
    _STAGE_ALIASES[_contract.stage] = _contract.stage
    _STAGE_ALIASES[str(_contract.sequence)] = _contract.stage
    _STAGE_ALIASES[f"{_contract.sequence:02d}"] = _contract.stage
    _STAGE_ALIASES[f"{_contract.sequence:02d}_{_contract.stage}"] = _contract.stage


def normalize_pipeline_stage(stage: str | int) -> str:
    normalized = str(stage).strip().casefold().replace("-", "_")
    if normalized in _STAGE_ALIASES:
        return _STAGE_ALIASES[normalized]
    available = ", ".join(contract.stage for contract in PIPELINE_STEP_INPUT_CONTRACTS)
    raise PipelineStepInputValidationError(f"unknown pipeline stage '{stage}'. Available stages: {available}")


def pipeline_step_contracts_json() -> dict[str, Any]:
    return {contract.stage: contract.as_json() for contract in PIPELINE_STEP_INPUT_CONTRACTS}


def _type_names(types: tuple[type[Any], ...]) -> str:
    return " or ".join(type_.__name__ for type_ in types)


def _validate_metadata(document: dict[str, Any], source: str) -> None:
    errors = []
    for key, expected_types in _RUNNER_METADATA_TYPES.items():
        if key in document and not isinstance(document[key], expected_types):
            errors.append(f"{source}: {key} must be {_type_names(expected_types)}")
    if errors:
        raise PipelineStepInputValidationError("; ".join(errors))


def validate_step_input(stage: str | int, payload: dict[str, Any]) -> None:
    normalized_stage = normalize_pipeline_stage(stage)
    contract = _PIPELINE_STEP_CONTRACT_BY_STAGE[normalized_stage]
    if not isinstance(payload, dict):
        raise PipelineStepInputValidationError(f"input JSON for {normalized_stage} must be an object")

    missing = [key for key in contract.required if key not in payload]
    unknown = sorted(set(payload) - contract.allowed_payload_keys)
    type_errors = []
    for key in sorted(contract.allowed_payload_keys & set(payload)):
        expected_types = _FIELD_TYPES.get(key)
        if expected_types is not None and not isinstance(payload[key], expected_types):
            type_errors.append(f"{key} must be {_type_names(expected_types)}")

    messages = []
    if missing:
        messages.append(f"missing required attributes for {normalized_stage}: {', '.join(missing)}")
    if unknown:
        messages.append(f"unknown attributes for {normalized_stage}: {', '.join(unknown)}")
    if type_errors:
        messages.append(f"invalid attribute types for {normalized_stage}: {', '.join(type_errors)}")
    if messages:
        raise PipelineStepInputValidationError("; ".join(messages))


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PipelineStepInputValidationError(f"{path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise PipelineStepInputValidationError(f"{path}: input JSON must be an object")
    _validate_metadata(payload, str(path))
    return payload


def load_step_input_documents(paths: list[Path]) -> tuple[dict[str, Any], dict[str, Any]]:
    if not paths:
        raise PipelineStepInputValidationError("at least one --input-json file is required")
    merged_payload: dict[str, Any] = {}
    embedded_config: dict[str, Any] = {}
    for path in paths:
        document = _read_json_object(path)
        config = document.get("config")
        if isinstance(config, dict):
            embedded_config.update(config)
        for key, value in document.items():
            if key not in _RUNNER_METADATA_TYPES:
                merged_payload[key] = value
    return merged_payload, embedded_config


def _read_config_file(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    config = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise PipelineStepInputValidationError(f"{path}: config JSON must be an object")
    return config


def _effective_config(*configs: dict[str, Any] | None) -> dict[str, Any]:
    merged = dict(DEFAULT_PIPELINE_STEP_CONFIG)
    for config in configs:
        if config is None:
            continue
        if not isinstance(config, dict):
            raise PipelineStepInputValidationError("config must be an object")
        merged.update(config)
    return merged


def execute_pipeline_step(stage: str | int, payload: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    normalized_stage = normalize_pipeline_stage(stage)
    validate_step_input(normalized_stage, payload)
    effective_config = _effective_config(config)
    if normalized_stage == "input_intake":
        return orion_module.process_input_intake(input_data=payload["input_data"], config=effective_config)
    if normalized_stage == "preprocessing":
        return orion_module.preprocess_input(payload)
    sut = ORION(config=effective_config)
    method_name = _STAGE_METHODS[normalized_stage]
    return getattr(sut, method_name)(payload)


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


def execute_pipeline_step_from_files(
    stage: str | int,
    input_json_paths: list[Path],
    output_json_path: Path,
    config_json_path: Path | None = None,
    output_mode: str = "stage-only",
) -> dict[str, Any]:
    payload, embedded_config = load_step_input_documents(input_json_paths)
    file_config = _read_config_file(config_json_path)
    result = execute_pipeline_step(stage, payload, config=_effective_config(embedded_config, file_config))
    if output_mode == "stage-only":
        output_payload = _stage_output_only(payload, result)
    elif output_mode == "payload":
        output_payload = result
    else:
        raise PipelineStepInputValidationError("output_mode must be 'stage-only' or 'payload'")
    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    safe_output = _json_safe(output_payload)
    output_json_path.write_text(json.dumps(safe_output, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return safe_output


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one ORION pipeline step from validated JSON input files.")
    parser.add_argument("stage", nargs="?", help="Stage name, sequence number, or NN_stage alias.")
    parser.add_argument("--input-json", action="append", type=Path, default=[], help="Input JSON file. Repeat to shallow-merge stage-only files in order.")
    parser.add_argument("--output-json", type=Path, help="Output JSON file to write.")
    parser.add_argument("--config-json", type=Path, help="Optional config JSON. Overrides config embedded in input files.")
    parser.add_argument("--output-mode", choices=("stage-only", "payload"), default="stage-only", help="Write only this stage's delta or the full cumulative payload.")
    parser.add_argument("--contracts", action="store_true", help="Print required/optional JSON attributes for every stage and exit.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.contracts:
        print(json.dumps(pipeline_step_contracts_json(), indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if not args.stage:
        print("ERROR: stage is required unless --contracts is used", file=sys.stderr)
        return 2
    if not args.input_json:
        print("ERROR: at least one --input-json file is required", file=sys.stderr)
        return 2
    if args.output_json is None:
        print("ERROR: --output-json is required", file=sys.stderr)
        return 2
    try:
        execute_pipeline_step_from_files(
            args.stage,
            args.input_json,
            args.output_json,
            config_json_path=args.config_json,
            output_mode=args.output_mode,
        )
    except PipelineStepInputValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - preserves CLI diagnostics for real stage failures.
        print(f"ERROR: pipeline step execution failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
