---
id: NFR-007
type: NFR
title: Logging privacy
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-05-30
summary: Logs do not include raw input text or sensitive full input content by default.
tags: [logging, privacy, security]
domain: orion
capability: logging-observability
actors: []
systems: [ORION]
source: stakeholder-input-logging-persistence
change_ref: CHG-LOGGING-REQS
requirement_type: Non-Functional
subtype: Security
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
  - FUN-016
  - CON-010
owner: herodotus
---

# NFR-007: Logging privacy

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | Initial specification capture for logging observability | herodotus |

## Summary
Logs do not include raw input text or sensitive full input content by default.

## Context / Scope
ORION shall keep log output privacy-safe by default while still supporting debugging metadata.

## Description
Logs shall not include raw input text or sensitive full input content by default.

## Acceptance Criteria
- raw input text is not written to logs by default.
- Full sensitive input content is not written to logs by default.
- Safe metadata may be logged when needed for observability.
- Privacy behavior is consistent across structured events and JSONL persistence.

## Dependencies
- Requires FUN-014.
- Applies alongside CON-010.

## Business Rules
- None currently.

## Validation Method
- Traceable unit tests assert excluded fields stay absent by default.
- Integration tests verify JSONL persistence also omits raw input text and sensitive full input content.

## Technical Notes
- Prefer redaction or omission over storage of raw input text.
- Keep privacy-safe metadata explicit and minimal.

## Traceability
- Upstream source: stakeholder-input-logging-persistence.
- Downstream: FUN-014, FUN-016, CON-010.
- Related requirements: FUN-014, FUN-016, CON-010.

## Open questions
- None.
