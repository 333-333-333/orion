---
id: FUN-011
type: FUN
title: Record traceability for ontology elements
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library records traceability metadata for ontology elements.
tags: [traceability, ontology, audit]
domain: orion
capability: traceability-ontology
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

# FUN-011: Record traceability for ontology elements

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library records traceability metadata for ontology elements.

## Context / Scope
ORION shall preserve traceability metadata for each generated ontology entity and property.

## Description
ORION shall preserve traceability metadata for each generated ontology entity and property.

## Acceptance Criteria
- Each ontology element can be linked back to its source text context.
- Traceability metadata is available in the returned result object.
- Missing traceability fields are treated as defects, not optional behavior.

## Dependencies
- Requires FUN-006 and FUN-010.

## Business Rules
- Ontology traceability is mandatory for generated elements.

## Validation Method
- Tests verify element-level provenance fields are present and populated for sample inputs.

## Technical Notes
Keep traceability data attached to ontology elements through all processing stages.

## Traceability
- Upstream source: README.md. Downstream: NFR-002.

## Open questions
None.
