---
id: FUN-013
type: FUN
title: Raise ORION-specific exceptions
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library raises ORION-specific exceptions for expected failure modes.
tags: [exceptions, validation, errors]
domain: orion
capability: error-handling
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [NFR-005]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-013: Raise ORION-specific exceptions

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library raises ORION-specific exceptions for expected failure modes.

## Context / Scope
ORION shall raise its own exception types for validation, parsing, model, and serialization failures instead of leaking raw implementation exceptions as the primary contract.

## Description
ORION shall raise its own exception types for validation, parsing, model, and serialization failures instead of leaking raw implementation exceptions as the primary contract.

## Acceptance Criteria
- Invalid config, invalid input, unsupported language, model failure, and serialization failure each raise an ORION-specific exception category.
- The host application can catch ORION exceptions without depending on internal third-party exception classes.
- Successful processing does not emit exceptions.

## Dependencies
- Requires FUN-001, FUN-002, FUN-003, FUN-004, and FUN-008.

## Business Rules
- Failure modes must be surfaced through ORION-specific exceptions.

## Validation Method
- Tests force each failure mode and assert the exception type and message contract.

## Technical Notes
Wrap third-party errors at the library boundary where appropriate.

## Traceability
- Upstream source: README.md. Downstream: NFR-005.

## Open questions
None.
