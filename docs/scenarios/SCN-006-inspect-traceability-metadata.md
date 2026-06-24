---
id: SCN-006
type: SCN
title: Inspect Traceability Metadata
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host Application inspects traceability metadata for ontology elements and triples.
tags: [scenario, traceability, metadata]
domain: orion
capability: traceability
actors: [Host Application]
systems: [ORION]
source: docs/use-cases/UC-006-inspect-traceability-metadata.md
change_ref: CHG-SCN-TRACEABILITY-COMPLETE
related_ucs: [UC-006]
related_reqs: [FUN-011, FUN-012, NFR-002]
related_user_stories: [US-011, US-012, US-022]
related_brs: []
related_adrs: []
owner: herodotus
---

# SCN-006: Inspect Traceability Metadata

## Summary

Host Application inspects traceability metadata attached to ORION ontology elements and triples.

## Preconditions

- ORION has produced semantic output.
- Traceability metadata exists for the requested output.

## Trigger

Host Application requests metadata for output inspection or verification.

## Scenario Steps

| Step | Actor | Action | References |
|---|---|---|---|
| 1 | Host Application | Requests ontology-element traceability metadata. | FUN-011, US-011 |
| 2 | Host Application | Requests triple-level traceability metadata. | FUN-012, US-012 |
| 3 | ORION | Returns metadata suitable for verification. | NFR-002, US-022 |

## Expected Result

ORION returns traceability metadata that the host application can inspect and verify.

## User Stories

- US-011 — Record Traceability for Ontology Elements
- US-012 — Record Traceability for Triples
- US-022 — Make Traceability Verifiable
