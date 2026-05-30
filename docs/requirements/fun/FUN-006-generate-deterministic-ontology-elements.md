---
id: FUN-006
type: FUN
title: Generate deterministic ontology elements
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library generates ontology elements in a deterministic way for the same input and config.
tags: [ontology, deterministic, nlp]
domain: orion
capability: ontology-generation
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

# FUN-006: Generate deterministic ontology elements

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library generates ontology elements in a deterministic way for the same input and config.

## Context / Scope
ORION shall generate ontology elements from input text deterministically when the same input, configuration, and pinned dependencies are used.

## Description
ORION shall generate ontology elements from input text deterministically when the same input, configuration, and pinned dependencies are used.

## Acceptance Criteria
- Two runs with identical input and config produce the same ontology element set.
- Ontology elements are exposed in a stable structure suitable for comparison tests.
- Non-deterministic variation is not allowed in the deterministic element set.

## Dependencies
- Requires FUN-003 or FUN-004 as input source.

## Business Rules
- Deterministic output is required for ontology elements.

## Validation Method
- Repeatability tests compare ontology outputs across repeated runs with the same pinned environment.

## Technical Notes
Any randomness must be removed from the deterministic path or isolated from it.

## Traceability
- Upstream source: README.md. Downstream: NFR-001, NFR-005.

## Open questions
None.
