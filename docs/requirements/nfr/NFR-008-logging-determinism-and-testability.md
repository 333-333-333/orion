---
id: NFR-008
type: NFR
title: Logging determinism and testability
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: Logging behavior is deterministic enough for stable automated tests.
tags: [logging, determinism, testability]
domain: orion
capability: logging-observability
actors: []
systems: [ORION]
source: stakeholder-input-logging-persistence
change_ref: CHG-LOGGING-REQS
requirement_type: Non-Functional
subtype: Testability
priority: High
related_ucs:
  - UC-001
  - UC-002
  - UC-003
  - UC-004
  - UC-005
  - UC-006
related_reqs:
  - FUN-014
  - FUN-015
  - FUN-016
  - CON-010
owner: herodotus
---

# NFR-008: Logging determinism and testability

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
Logging behavior is deterministic enough for stable automated tests.

## Context / Scope
ORION shall keep logging behavior predictable so tests can assert structure without brittle cleanup.

## Description
Logging must be testable and deterministic enough; volatile fields shall be off or controllable in tests.

## Acceptance Criteria
- Volatile fields can be disabled or controlled in tests.
- Structured log events remain stable enough for equality or deep-compare assertions.
- JSONL persistence tests can assert exact records when configured deterministically.
- Logging tests do not require manual inspection.

## Dependencies
- Requires FUN-014 and FUN-015.
- Applies alongside FUN-016 and CON-010.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests cover deterministic event payloads.
- Integration tests verify controllable volatile fields and stable JSONL output.

## Technical Notes
- Provide test hooks for volatile fields where needed.
- Keep default event payloads stable and repeatable.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: FUN-014, FUN-015, FUN-016, CON-010.
- Related requirements: FUN-014, FUN-015, FUN-016, CON-010.

## Open questions
- None.
