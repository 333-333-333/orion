---
id: US-028
type: US
title: Persist Structured Logs
status: draft
version: 0
created_at: 2026-05-30
updated_at: 2026-06-23
summary: Host application opts into JSONL persistence for auditable ORION processing events.
tags:
  - user-story
  - library-only
  - host-application
  - logging-observability
domain: orion
capability: logging-observability
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-LOGGING
related_ucs:
  - UC-001
  - UC-002
  - UC-003
  - UC-004
  - UC-005
  - UC-006
related_scenarios: [SCN-007]
related_reqs:
  - FUN-016
  - NFR-006
  - NFR-007
  - NFR-008
  - CON-011
related_user_stories: []
owner: herodotus
---

# US-028: Persist Structured Logs

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-30 | Added initial draft | User-provided scope captured for the ORION requirement set | herodotus |

## Summary
Host application opts into JSONL persistence for auditable ORION processing events.

## Context / Scope
This story stays inside the ORION library boundary and covers structured log persistence only.

## Narrative
As a host application, I want to opt into JSONL log persistence so I can keep auditable ORION processing events when persistence is required.

## Acceptance Criteria
- AC-1 (FUN-016, NFR-006, NFR-007, NFR-008, CON-011): The host application can opt into JSONL log persistence.
- AC-2 (FUN-016, NFR-006, NFR-007, NFR-008, CON-011): ORION writes auditable processing events in JSONL form when persistence is enabled.
- AC-3 (FUN-016, NFR-006, NFR-007, NFR-008, CON-011): Persistence remains optional and only affects ORION library behavior when requested by the host application.

## Traceability
- Related scenarios: SCN-007
- Related requirements: FUN-016, NFR-006, NFR-007, NFR-008, CON-011
- Related use cases: UC-001, UC-002, UC-003, UC-004, UC-005, UC-006
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only JSONL persistence; keep scope in-process.

## Open questions
None.
