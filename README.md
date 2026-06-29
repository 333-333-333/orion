# ORION

Ontology Recognition and Inference from Open Narratives

ORION is a Python library for extracting ontology elements from natural language text and producing RDF/OWL-oriented outputs with traceability and deterministic behavior.

It is designed to be imported and used by a host application. For example, a traditional REST API can call ORION internally, but ORION itself is not a CLI, not a REST API, and not an HTTP service.

## What ORION does

- Accepts input as a Python string or a path to a `.txt` file.
- Processes text through a deterministic NLP pipeline.
- Extracts ontology candidates, relations, semantic claims, and triples.
- Keeps deterministic triples separate from inferred triples.
- Exposes Python objects and serializable outputs.
- Preserves traceability per entity, property, and triple.

## Current quality / smoke status

- Pipeline order now is `semantic_claims` first, then triple extraction, then RDF.
- Smoke is modular by case directory under `tests/smoke/cases/...`.
- One runner: `python3 tests/smoke/run_infosec_smoke_suite.py`.
- Artifacts tracked: per-step `pipeline_outputs/*.json`, `semantic_claims`, `graph_model`, RDF, TTL, and metrics.
- Legacy `infosec_3k` smoke stays disabled.
- Full-text modular smoke is observational/proxy.
- Strict contracts stay on `p001-p002` and `p003-p004`.
- Latest validation: `145 passed`.
- No hardcode in `src`; contract and smoke truth live in docs and tests.

## Pipeline contract

ORION runs a deterministic, library-only pipeline. Internally each step receives the current pipeline payload and returns a new payload for downstream steps. When smoke artifacts persist per-step JSON files, each file contains only the output introduced or changed by that step, not the full cumulative payload.

| # | Step | Role | Input contract | Step output contract |
|---|------|------|----------------|----------------------|
| 1 | `input_intake` | Convert supported host input into an ORION source payload. | `str` text, `str` path ending in `.txt`, or `Path` to `.txt`; config is a Python `dict`. | `raw_text`, `source_text_id`, `metadata.source`. |
| 2 | `preprocessing` | Normalize Unicode, repeated spaces, and newlines without changing source identity. | Intake payload with `raw_text`, `source_text_id`, `metadata`. | `preprocessed_text`, `operations_applied`. |
| 3 | `sentence_segmentation` | Split normalized text into deterministic sentence spans. | Preprocessed payload. | `sentences[]` with `sentence_id`, index, text, offsets, and `source_text_id`. |
| 4 | `tokenization` | Split sentences into deterministic token spans. | Sentence payload. | `tokens[]` with token id/text, sentence id, offsets, and index. |
| 5 | `linguistic_annotation` | Add spaCy-backed linguistic evidence. | Token payload and configured spaCy model. | Annotated `tokens[]` with lemma, POS, tag, dependency, and head text. |
| 6 | `entity_extraction` | Produce generic entity observations without domain hardcoding. | Annotated token payload and active spaCy doc. | `entities[]` with entity id, label, span, sentence, and source id. |
| 7 | `concept_extraction` | Propose ontology concept candidates from linguistic evidence. | Entity/annotation payload. | `concepts[]` with concept id, label/text, source span, confidence/evidence metadata. |
| 8 | `coreference_resolution` | Resolve supported references while keeping traceability. | Concept payload. | `coreferences[]` with mention, antecedent/resolution, and confidence metadata. |
| 9 | `relation_extraction` | Extract candidate semantic relations from explicit linguistic patterns. | Concept/coreference payload. | `relations[]` with relation id, subject, predicate, object, references, and evidence span. |
| 10 | `canonical_claims` / `semantic_claims` | Convert observed relations/definitions into explicit, evidence-backed claims before triples/RDF. | Relation payload plus optional claim artifact config. | `canonical_claims`; when semantic mode is enabled, `semantic_claims`; `artifacts` entries for claim payloads/paths. |
| 11 | `semantic_debug_ir` | Optional sidecar for debugging semantic claim projection. | Claim payload plus optional debug artifact config. | `artifacts.semantic_debug_ir`, `artifacts.semantic_debug_ir_path`; empty output when not configured. |
| 12 | `triple_extraction` | Convert claims or relations into deterministic SPO triples. | Claim payload. | `triples[]` with subject, predicate, object, refs/evidence, confidence. |
| 13 | `taxonomy_induction` | Derive direct class hierarchy facts. | Triple/claim payload. | `taxonomy_relations[]` with subclass/superclass relation metadata. |
| 14 | `type_assertion` | Derive class membership assertions. | Taxonomy/triple payload. | `type_assertions[]` with entity/instance and type/class metadata. |
| 15 | `semantic_quality` | Assess noise, RDF readiness, and exclusions before projection. | Semantic payload with concepts/entities/relations/triples. | `semantic_quality_report`, `excluded_entities`, `excluded_concepts`. |
| 16 | `output_generation` | Project semantic payload into the configured output graph/model. | Quality-assessed payload and `output_strategy`. | `output.strategy`, `output.format`, `output.graph`, `output.metadata`; RDF/OWL strategy decides graph shape. |

Per-step smoke JSON artifacts use this naming convention:

```txt
tests/smoke/cases/<case>/artifacts/pipeline_outputs/observed_<case>_<NN>_<stage>.json
```

### Pipeline step runner contracts and execution

Specific steps can be executed from validated JSON input files without changing `src`.

Print the machine-readable contract for every stage:

```bash
python3 tests/smoke/pipeline_step_runner.py --contracts
```

Contract JSON excerpt:

```json
{
  "sentence_segmentation": {
    "sequence": 3,
    "stage": "sentence_segmentation",
    "required": [
      "raw_text",
      "source_text_id",
      "metadata",
      "preprocessed_text",
      "operations_applied"
    ],
    "optional": [],
    "runner_optional": ["config", "description", "schema_version"],
    "description": "Cumulative preprocessed payload before sentence segmentation."
  }
}
```

Runnable input JSON example for the first step:

```json
{
  "schema_version": 1,
  "description": "Minimal ORION pipeline-step runner input.",
  "config": {
    "spacy_model": "en_core_web_lg",
    "output_strategy": "rdf"
  },
  "input_data": "Mario's Pizzeria serves a Vesuvio pie."
}
```

Runner metadata keys (`schema_version`, `description`, `config`) are allowed in input files but are not passed as pipeline payload fields. `config` can also be provided with `--config-json`.

#### Execute every step linearly

Use `--output-mode payload` when you want each step output to be the complete cumulative payload for the next step:

```bash
WORK=/tmp/orion-step-demo
RUN="python3 tests/smoke/pipeline_step_runner.py"
mkdir -p "$WORK"

cat > "$WORK/00-input.json" <<'JSON'
{
  "schema_version": 1,
  "description": "Minimal ORION pipeline-step runner input.",
  "config": {
    "spacy_model": "en_core_web_lg",
    "output_strategy": "rdf"
  },
  "input_data": "Mario's Pizzeria serves a Vesuvio pie."
}
JSON

$RUN 01_input_intake --input-json "$WORK/00-input.json" --output-json "$WORK/01_input_intake.json" --output-mode payload
$RUN 02_preprocessing --input-json "$WORK/01_input_intake.json" --output-json "$WORK/02_preprocessing.json" --output-mode payload
$RUN 03_sentence_segmentation --input-json "$WORK/02_preprocessing.json" --output-json "$WORK/03_sentence_segmentation.json" --output-mode payload
$RUN 04_tokenization --input-json "$WORK/03_sentence_segmentation.json" --output-json "$WORK/04_tokenization.json" --output-mode payload
$RUN 05_linguistic_annotation --input-json "$WORK/04_tokenization.json" --output-json "$WORK/05_linguistic_annotation.json" --output-mode payload
$RUN 06_entity_extraction --input-json "$WORK/05_linguistic_annotation.json" --output-json "$WORK/06_entity_extraction.json" --output-mode payload
$RUN 07_concept_extraction --input-json "$WORK/06_entity_extraction.json" --output-json "$WORK/07_concept_extraction.json" --output-mode payload
$RUN 08_coreference_resolution --input-json "$WORK/07_concept_extraction.json" --output-json "$WORK/08_coreference_resolution.json" --output-mode payload
$RUN 09_relation_extraction --input-json "$WORK/08_coreference_resolution.json" --output-json "$WORK/09_relation_extraction.json" --output-mode payload
$RUN 10_canonical_claims --input-json "$WORK/09_relation_extraction.json" --output-json "$WORK/10_canonical_claims.json" --output-mode payload
$RUN 11_semantic_debug_ir --input-json "$WORK/10_canonical_claims.json" --output-json "$WORK/11_semantic_debug_ir.json" --output-mode payload
$RUN 12_triple_extraction --input-json "$WORK/11_semantic_debug_ir.json" --output-json "$WORK/12_triple_extraction.json" --output-mode payload
$RUN 13_taxonomy_induction --input-json "$WORK/12_triple_extraction.json" --output-json "$WORK/13_taxonomy_induction.json" --output-mode payload
$RUN 14_type_assertion --input-json "$WORK/13_taxonomy_induction.json" --output-json "$WORK/14_type_assertion.json" --output-mode payload
$RUN 15_semantic_quality --input-json "$WORK/14_type_assertion.json" --output-json "$WORK/15_semantic_quality.json" --output-mode payload
$RUN 16_output_generation --input-json "$WORK/15_semantic_quality.json" --output-json "$WORK/16_output_generation.json" --output-mode payload
```

Stage names, numbers, and aliases are accepted; for example `sentence_segmentation`, `3`, `03`, and `03_sentence_segmentation` all refer to the same step.

#### Execute one step from stage-only JSON artifacts

By default the runner writes only the selected step's own output. In that mode, repeat `--input-json` to shallow-merge prior stage-only files into the cumulative payload required by the target step:

```bash
python3 tests/smoke/pipeline_step_runner.py preprocessing \
  --input-json input_intake.json \
  --output-json preprocessing.json

python3 tests/smoke/pipeline_step_runner.py sentence_segmentation \
  --input-json input_intake.json \
  --input-json preprocessing.json \
  --output-json sentences.json
```

Per-step smoke JSON artifacts use the same stage-only convention.

## Quality entrypoints

- `docs/core/quality/TR-ORION-INFOSEC-FULL-TEXT-SMOKE.md`
- `docs/core/quality/TR-ORION-INFOSEC-PAIR-SMOKE-REMAINING.md`

## Supported languages

- Language is configurable.
- Default language: English.
- Initial supported languages, based on spaCy models: English and Spanish.

## spaCy models

- Model family is configurable by size.
- Default size: `lg`.
- Exact model versions must be pinned.
- Example families: `en_core_web_lg`, `es_core_news_lg`.
- Install the selected model versions through the project lock/export workflow.

## Installation

```bash
uv sync
uv export --frozen --no-dev --no-editable -o requirements.txt
```

If your environment needs the selected spaCy models, install the pinned model versions required by the project lockfile.

## Use from Python

```python
from orion import ORION

config = {
    "spacy_model": "en_core_web_lg",
    "output_strategy": "rdf",
}

orion = ORION(config=config)

result = orion.process("A customer creates a reservation.")
# orion.process(Path("input.txt"))

print(result.get("semantic_claims") or result["canonical_claims"])  # evidence-backed claims
print(result["triples"])                                      # deterministic SPO triples
print(result["output"]["graph"])                             # graph model for RDF/OWL projection
```

### Host app example

A host app, including a REST API backend, can instantiate ORION inside a request handler or job worker and return the produced Python objects or serialized strings to its own callers.

## Input contract

- `ORION(config=...)` requires a Python `dict` config.
- Accepted `process(...)` input types: Python `str` text, `str` path ending in `.txt`, or `Path` to a `.txt` file.
- Empty text is rejected.
- `.txt` paths must exist and are read as UTF-8.
- `spacy_model`, `output_strategy`, `base_iri`, `prefixes`, and optional artifact paths are config-driven.

## Output contract

`ORION.process(...)` returns a dict-like `ORIONResult` containing the final payload.

Primary final output lives under `result["output"]`:

- `strategy`: selected strategy, for example `rdf`.
- `format`: emitted graph/model format.
- `graph`: deterministic graph model used for RDF/OWL projection.
- `metadata`: source metadata propagated from intake.

Intermediate semantic outputs may also be present for host inspection and smoke contracts:

- `semantic_claims` / `canonical_claims`
- `triples`
- `taxonomy_relations`
- `type_assertions`
- `semantic_quality_report`
- `artifacts`

Deterministic pipeline outputs are generated before output projection; inferred output remains separate when a strategy or host layer adds it.

## Traceability

Traceability is preserved for ontology entities, properties, and triples.

Each generated triple can carry:

- `source_text_id`
- `sentence_id`
- character offsets
- `rule_id`

## Errors

ORION raises its own exceptions for validation, parsing, model, and serialization failures.

## Determinism

The same input, same config, and same pinned dependencies must produce the same deterministic output.

## Project setup

- Python package management: UV
- Requirements export: `uv export --frozen --no-dev --no-editable -o requirements.txt`
- Runtime dependency pinning: required

## Notes

- YAML is not the main configuration format.
- CLI usage is not part of the contract.
- ORION is meant to be embedded in other Python systems.

## Developer static linter

Optional static check for Python source:

```bash
python3 src/tooling/python_ast_linter.py src tests
```

Rules:
- function/async function longer than 30 lines
- control-flow depth greater than 4
- missing docstring in function/async function

Exit code is non-zero when warnings exist.
