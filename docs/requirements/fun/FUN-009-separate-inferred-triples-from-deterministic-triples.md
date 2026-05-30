---
id: FUN-009
type: FUN
title: Separate inferred triples from deterministic triples
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library keeps inferred triples separate from deterministic triples.
tags: [triples, inference, deterministic]
domain: orion
capability: triple-separation
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [NFR-001, NFR-005]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-009: Separate inferred triples from deterministic triples

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library keeps inferred triples separate from deterministic triples.

## Context / Scope
ORION shall expose deterministic triples and inferred triples as separate result collections.

## Description
ORION shall expose deterministic triples and inferred triples as separate result collections.

## Acceptance Criteria
- Deterministic triples and inferred triples are returned in separate fields or collections.
- A consumer can inspect deterministic output without mixing inferred output.
- The separation is preserved in repeat runs with the same input and config.

## Dependencies
- Requires FUN-007.

## Business Rules
- Inferred triples must not be merged into the deterministic triple set.

## Validation Method
- Unit tests verify two distinct output collections exist and remain distinct.

## Technical Notes
Any non-deterministic reasoning output must be isolated from deterministic output.

## Traceability
- Upstream source: README.md. Downstream: NFR-001, NFR-005.

## Open questions
None.
