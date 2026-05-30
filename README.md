# ORION

Ontology Recognition and Inference from Open Narratives

ORION is a Python library for extracting ontology elements from natural language text and producing RDF/OWL-oriented outputs with traceability and deterministic behavior.

It is designed to be imported and used by a host application. For example, a traditional REST API can call ORION internally, but ORION itself is not a CLI, not a REST API, and not an HTTP service.

## What ORION does

- Accepts input as a Python string or a path to a `.txt` file.
- Processes text through a deterministic NLP pipeline.
- Extracts ontology candidates, relations, and triples.
- Keeps deterministic triples separate from inferred triples.
- Exposes Python objects and serializable outputs.
- Preserves traceability per entity, property, and triple.

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
    "language": "en",
    "spacy_model_size": "lg",
    "output_formats": ["ttl", "rdfxml", "jsonld", "nt"],
    "traceability": True,
}

orion = ORION(config=config)

result = orion.process("A customer creates a reservation.")
# orion.process(Path("input.txt"))

print(result.ontology)          # Python objects
print(result.serialized["ttl"]) # string serialization
print(result.deterministic_triples)
print(result.inferred_triples)
```

### Host app example

A host app, including a REST API backend, can instantiate ORION inside a request handler or job worker and return the produced Python objects or serialized strings to its own callers.

## Input contract

- Accepted input types: `str` and `.txt` file path.
- Language is part of config.
- Config is passed as a Python `dict`.

## Output contract

ORION returns Python objects plus serialized strings in:

- `ttl`
- `rdfxml`
- `jsonld`
- `nt`

Deterministic triples and inferred triples are separated.

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
