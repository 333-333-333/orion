---
id: CON-010
type: CON
title: Logging disabled by default
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: Logging is disabled or no-op by default unless the host configures it.
tags: [logging, default-behavior, constraint]
domain: orion
capability: logging-observability
actors: []
systems: [ORION]
source: stakeholder-input-logging-persistence
change_ref: CHG-LOGGING-REQS
requirement_type: Constraint
subtype: Operational
priority: Critical
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
  - NFR-007
  - NFR-008
owner: herodotus
---

# CON-010: Logging disabled by default

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
Logging is disabled or no-op by default unless the host configures it.

## Context / Scope
ORION shall avoid emitting log output unless the host application explicitly enables logging behavior.

## Description
Logging shall be disabled or no-op by default unless configured by the host application.

## Acceptance Criteria
- Default ORION operation produces no log output unless configured.
- Logging becomes active only after host configuration.
- Default no-op behavior does not block normal processing.

## Dependencies
- Applies to FUN-014, FUN-015, and FUN-016.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests assert no-op default behavior.
- Integration tests confirm logging activates only after explicit host configuration.

## Technical Notes
- Keep default wiring inert.
- Do not require persistence or sink setup for normal processing.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: FUN-014, FUN-015, FUN-016, NFR-007, NFR-008.
- Related requirements: FUN-014, FUN-015, FUN-016, NFR-007, NFR-008.

## Open questions
- None.
