---
id: FUN-015
type: FUN
title: Configure log sink
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: Host application can configure a per-instance log sink.
tags: [logging, sink, configuration]
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
  - FUN-016
  - NFR-006
  - NFR-008
  - CON-009
  - CON-010
owner: herodotus
---

# FUN-015: Configure log sink

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
Host application can configure a per-instance log sink.

## Context / Scope
ORION shall let each ORION instance route its logs to a sink chosen by the host application.

## Description
ORION shall allow the host application to configure a per-instance log sink for structured log events.

## Acceptance Criteria
- The host application can attach a log sink to one ORION instance without changing global logging policy.
- Separate ORION instances can use different sinks.
- If no sink is configured, logging remains disabled or no-op by default.

## Dependencies
- Requires FUN-014.
- Aligns with CON-009 and CON-010.
- Enables FUN-016.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests cover sink attachment and instance isolation.
- Integration tests verify one instance can log while another uses a different sink.

## Technical Notes
- Prefer instance-scoped wiring over module-level logger mutation.
- Sink selection shall remain host-controlled.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: UC-001, UC-002, UC-003, UC-004, UC-005, UC-006.
- Related requirements: FUN-014, FUN-016, NFR-006, NFR-008, CON-009, CON-010.

## Open questions
- None.
