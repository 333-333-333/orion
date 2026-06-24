---
id: SCN-004
type: SCN
title: Generate Deterministic Semantic Output
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: ORION generates deterministic ontology elements, triples, and semantic-web compatible output from processed input.
tags: [scenario, deterministic-output, rdf, owl]
domain: orion
capability: semantic-output-generation
actors: [Host Application]
systems: [ORION]
source: docs/use-cases/UC-004-generate-deterministic-semantic-output.md
change_ref: CHG-SCN-TRACEABILITY-COMPLETE
related_ucs: [UC-004]
related_reqs: [FUN-006, FUN-007, FUN-009, NFR-001, NFR-002, NFR-003, NFR-005]
related_user_stories: [US-006, US-007, US-009, US-023, US-025, US-026]
related_brs: []
related_adrs: []
owner: herodotus
---

# SCN-004: Generate Deterministic Semantic Output

## Summary

ORION converts processed input into deterministic ontology elements, triples, and semantic-web compatible output.

## Preconditions

- ORION has accepted input text.
- Pipeline processing has completed without an exception.

## Trigger

Host Application requests semantic output from processed input.

## Scenario Steps

| Step | Actor | Action | References |
|---|---|---|---|
| 1 | ORION | Extracts deterministic ontology elements. | FUN-006, US-006 |
| 2 | ORION | Generates deterministic RDF/OWL triples. | FUN-007, US-007 |
| 3 | ORION | Separates deterministic triples from inferred triples. | FUN-009, US-009 |
| 4 | ORION | Preserves semantic-web interoperability. | NFR-003, US-023 |
| 5 | ORION | Keeps comparison surfaces stable and reproducible. | NFR-001, NFR-005, US-025, US-026 |

## Expected Result

ORION emits deterministic semantic output suitable for repeatable comparison and semantic-web use.

## User Stories

- US-006 — Generate Deterministic Ontology Elements
- US-007 — Generate Deterministic RDF/OWL Triples
- US-009 — Separate Inferred Triples from Deterministic Triples
- US-023 — Keep Semantic Web Interoperability
- US-025 — Keep Comparison Surfaces Stable
- US-026 — Keep Deterministic Reproducibility
