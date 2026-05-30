---
id: NFR-005
type: NFR
title: Stable comparison testability
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Outputs must stay stable enough for direct comparison in automated tests.
tags: [testing, comparison, stability]
domain: orion
capability: testability
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-006, FUN-007, FUN-009, FUN-013]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# NFR-005: Stable comparison testability

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Outputs must stay stable enough for direct comparison in automated tests.

## Context / Scope
ORION shall expose outputs that can be compared directly in automated tests without relying on visual inspection or manual cleanup.

## Description
ORION shall expose outputs that can be compared directly in automated tests without relying on visual inspection or manual cleanup.

## Acceptance Criteria
- Deterministic output structures are stable enough for equality or deep-compare assertions.
- Known non-deterministic inference data is separated so deterministic tests stay stable.
- Error contracts are stable enough to assert exception type and message category.

## Dependencies
- Requires deterministic output separation and ORION-specific exceptions.

## Business Rules
- Testability depends on stable output boundaries.

## Validation Method
- Automated comparison tests run without flaky output from the deterministic path.

## Technical Notes
Keep comparison surfaces small and typed where possible.

## Traceability
- Upstream source: README.md. Downstream: FUN-006, FUN-007, FUN-009, FUN-013.

## Open questions
None.
