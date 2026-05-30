---
id: FUN-010
type: FUN
title: Return results as Python objects
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library returns Python objects in addition to serialized strings.
tags: [python-objects, result-model, host-application]
domain: orion
capability: result-object
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [NFR-004, NFR-003]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-010: Return results as Python objects

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library returns Python objects in addition to serialized strings.

## Context / Scope
ORION shall return a Python result object that exposes ontology data and output collections directly to the host application.

## Description
ORION shall return a Python result object that exposes ontology data and output collections directly to the host application.

## Acceptance Criteria
- The host application receives a Python object from processing, not only a serialized blob.
- The object contains structured access to ontology data, deterministic triples, inferred triples, and serializations.
- The object can be used without additional parsing step by the host application.

## Dependencies
- Requires FUN-006, FUN-007, FUN-008, and FUN-009.

## Business Rules
- Python objects are part of the primary output contract.

## Validation Method
- Unit tests assert the returned value is a Python object with the expected attributes or keys.

## Technical Notes
The object schema should stay stable enough for comparison tests.

## Traceability
- Upstream source: README.md. Downstream: NFR-003, NFR-004.

## Open questions
None.
