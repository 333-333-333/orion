---
id: CON-011
type: CON
title: Persistence is optional
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: Log persistence is opt-in and not required for normal processing.
tags: [logging, persistence, opt-in, constraint]
domain: orion
capability: logging-observability
actors: []
systems: [ORION]
source: stakeholder-input-logging-persistence
change_ref: CHG-LOGGING-REQS
requirement_type: Constraint
subtype: Operational
priority: High
related_ucs:
  - UC-001
  - UC-002
  - UC-003
  - UC-004
  - UC-005
  - UC-006
related_reqs:
  - FUN-016
  - CON-010
owner: herodotus
---

# CON-011: Persistence is optional

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
Log persistence is opt-in and not required for normal processing.

## Context / Scope
ORION shall support log persistence only when the host application explicitly enables it.

## Description
Persistence is optional; normal processing must not require persistence.

## Acceptance Criteria
- ORION can process normally without persistence enabled.
- Built-in JSONL persistence activates only when configured.
- Persistence does not become a mandatory dependency of the core flow.

## Dependencies
- Applies to FUN-016.
- Aligns with CON-010.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests assert persistence is off unless enabled.
- Integration tests confirm normal processing works without persistence.
- JSONL persistence tests verify opt-in output when enabled.

## Technical Notes
- Keep persistence wiring separate from core execution.
- Host application remains responsible for choosing persistence.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: FUN-016.
- Related requirements: FUN-016, CON-010.

## Open questions
- None.
