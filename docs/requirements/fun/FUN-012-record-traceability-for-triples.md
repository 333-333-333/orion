---
id: FUN-012
type: FUN
title: Record traceability for triples
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library records traceability metadata for generated triples.
tags: [traceability, triples, audit]
domain: orion
capability: traceability-triples
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [NFR-002]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-012: Record traceability for triples

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library records traceability metadata for generated triples.

## Context / Scope
ORION shall preserve traceability metadata for each deterministic and inferred triple it produces.

## Description
ORION shall preserve traceability metadata for each deterministic and inferred triple it produces.

## Acceptance Criteria
- Each triple can carry source text identifier, sentence identifier, character offsets, and rule identifier when available.
- Traceability metadata is returned alongside both deterministic and inferred triple collections.
- A missing traceability identifier is a failure condition for the traceable output contract.

## Dependencies
- Requires FUN-009 and FUN-010.

## Business Rules
- Triple traceability is mandatory for both deterministic and inferred outputs.

## Validation Method
- Tests assert traceability fields exist for sample triples and map back to source text.

## Technical Notes
Preserve offsets and identifiers without changing output ordering.

## Traceability
- Upstream source: README.md. Downstream: NFR-002.

## Open questions
None.
