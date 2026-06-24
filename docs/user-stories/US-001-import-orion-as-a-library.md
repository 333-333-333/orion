---
id: US-001
type: US
title: Import ORION as a Library
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application imports and instantiates ORION in-process without a separate process.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: library-embedding
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_scenarios: [SCN-001]
related_reqs:
  - FUN-001
  - CON-001
  - CON-002
  - NFR-004
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-001: Import ORION as a Library

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application imports and instantiates ORION in-process without a separate process.

## Context / Scope
The story stays inside the ORION library boundary and covers in-process use only.

## Narrative
As a host application, I want to import and instantiate ORION in-process so I can use it without starting a separate process.

## Acceptance Criteria
- AC-1 (FUN-001, CON-001, CON-002, NFR-004): No separate process is required to begin normal ORION use.
- AC-2 (FUN-001, CON-001, CON-002, NFR-004): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-001, CON-001, CON-002, NFR-004): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-001
- Related requirements: FUN-001, CON-001, CON-002, NFR-004
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
