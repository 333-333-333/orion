---
id: FUN-016
type: FUN
title: Persist log events
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: ORION provides an optional built-in JSONL log sink for persistence.
tags: [logging, persistence, jsonl]
domain: orion
capability: logging-observability
actors: [Host Application]
systems: [ORION]
source: stakeholder-input-logging-persistence
change_ref: CHG-LOGGING-REQS
requirement_type: Functional
subtype: Logging
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
  - NFR-006
  - NFR-007
  - NFR-008
  - CON-010
  - CON-011
owner: herodotus
---

# FUN-016: Persist log events

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
ORION provides an optional built-in JSONL log sink for persistence.

## Context / Scope
ORION shall persist structured log events only when the host application opts into persistence.

## Description
ORION shall provide an optional built-in JSONL log sink for persistence of structured log events.

## Acceptance Criteria
- The host application can enable built-in JSONL persistence explicitly.
- JSONL output contains one structured log event per line.
- Persistence is optional and does not change normal processing behavior when unused.
- Persistence tests verify emitted JSONL records match the structured event contract.

## Dependencies
- Requires FUN-014 and FUN-015.
- Requires CON-010 and CON-011.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests cover JSONL record formatting.
- Integration tests verify optional persistence writes expected JSONL output.

## Technical Notes
- Keep JSONL output stable and machine-readable.
- Persistence sink shall not be required for core processing.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: UC-001, UC-002, UC-003, UC-004, UC-005, UC-006.
- Related requirements: FUN-014, FUN-015, NFR-006, NFR-007, NFR-008, CON-010, CON-011.

## Open questions
- None.
