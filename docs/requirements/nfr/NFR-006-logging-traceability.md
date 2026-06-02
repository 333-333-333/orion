---
id: NFR-006
type: NFR
title: Logging traceability
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: Log events remain traceable to phase, event type, status, and source, use-case, and requirement context.
tags: [logging, traceability, observability]
domain: orion
capability: logging-observability
actors: []
systems: [ORION]
source: stakeholder-input-logging-persistence
change_ref: CHG-LOGGING-REQS
requirement_type: Non-Functional
subtype: Traceability
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
owner: herodotus
---

# NFR-006: Logging traceability

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
Log events remain traceable to phase, event type, status, source context identifier, related use-case identifier, related requirement identifier, operation name, and ORION exception category.

## Context / Scope
ORION shall preserve enough contextual detail in logs to support debugging, audit, and test traceability.

## Description
Log events shall be traceable to phase, event type, status, source context identifier when available, related use-case identifier when configured, related requirement identifier when configured, operation name when applicable, and ORION exception category when failed.

## Acceptance Criteria
- Log events can be associated with phase, event type, and status.
- Log events can be associated with source context identifier when available.
- Log events can include related use-case identifier when configured.
- Log events can include related requirement identifier when configured.
- Log events can include operation name when applicable.
- Failed log events include ORION exception category.

## Dependencies
- Requires FUN-014.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests assert phase, event type, status, source context identifier when available, related use-case identifier when configured, related requirement identifier when configured, operation name when applicable, and ORION exception category when failed.
- Integration tests confirm end-to-end event traceability across the structured event contract.

## Technical Notes
- Keep traceability fields stable and machine-readable.
- Avoid coupling traceability to global logging state.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: FUN-014, FUN-015, FUN-016, UC-001, UC-002, UC-003, UC-004, UC-005, UC-006.
- Related requirements: FUN-014, FUN-015, FUN-016.

## Open questions
- None.
