---
id: NFR-002
type: NFR
title: Verifiable traceability
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Traceability metadata must be present and testable for ontology elements and triples.
tags: [traceability, auditability, verification]
domain: orion
capability: traceability
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-011, FUN-012]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# NFR-002: Verifiable traceability

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Traceability metadata must be present and testable for ontology elements and triples.

## Context / Scope
ORION shall make traceability data verifiable for generated ontology elements and triples.

## Description
ORION shall make traceability data verifiable for generated ontology elements and triples.

## Acceptance Criteria
- Traceability fields are available in the returned result object for inspection by tests or the host application.
- Traceability data must support source reconstruction to the documented level.
- Missing traceability data fails validation.

## Dependencies
- Requires traceability-capable output models.

## Business Rules
- Traceability is mandatory for generated ontology elements and triples.

## Validation Method
- Automated tests validate traceability fields on generated outputs.

## Technical Notes
Keep provenance data stable across serializations and object views.

## Traceability
- Upstream source: README.md. Downstream: FUN-011, FUN-012.

## Open questions
None.
