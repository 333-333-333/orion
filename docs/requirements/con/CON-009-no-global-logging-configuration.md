---
id: CON-009
type: CON
title: No global logging configuration
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: ORION does not configure Python global logging or root handlers.
tags: [logging, constraint, global-state]
domain: orion
capability: logging-observability
actors: []
systems: [ORION]
source: stakeholder-input-logging-persistence
change_ref: CHG-LOGGING-REQS
requirement_type: Constraint
subtype: Architecture
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
owner: herodotus
---

# CON-009: No global logging configuration

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
ORION does not configure Python global logging or root handlers.

## Context / Scope
ORION shall leave host application logging policy untouched and avoid global logging side effects.

## Description
ORION shall not configure Python global logging, root handlers, or host logging policy.

## Acceptance Criteria
- ORION does not mutate Python root logging configuration.
- ORION does not install global handlers on import or normal execution.
- Host logging policy remains under host application control.

## Dependencies
- Applies to FUN-014 and FUN-015.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests assert no root-handler mutation.
- Integration tests confirm host logging policy remains unchanged.

## Technical Notes
- Use instance-scoped wiring only.
- Avoid import-time logging setup.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: FUN-014, FUN-015.
- Related requirements: FUN-014, FUN-015.

## Open questions
- None.
