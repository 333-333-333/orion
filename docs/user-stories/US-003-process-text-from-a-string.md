---
id: US-003
type: US
title: Process Text from a String
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application sends a Python string already in memory for processing.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: text-input
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_scenarios: [SCN-002]
related_reqs:
  - FUN-003
  - CON-006
  - NFR-001
  - NFR-005
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-003: Process Text from a String

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application sends a Python string already in memory for processing.

## Context / Scope
The story covers in-memory text input inside the ORION library boundary.

## Narrative
As a host application, I want to send a Python string as input so I can process text already in memory.

## Acceptance Criteria
- AC-1 (FUN-003, CON-006, NFR-001, NFR-005): Input is already available as a Python string.
- AC-2 (FUN-003, CON-006, NFR-001, NFR-005): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-003, CON-006, NFR-001, NFR-005): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-002
- Related requirements: FUN-003, CON-006, NFR-001, NFR-005
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
