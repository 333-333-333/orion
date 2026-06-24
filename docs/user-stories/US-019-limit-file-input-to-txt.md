---
id: US-019
type: US
title: Limit File Input to TXT
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application fails early on unsupported file types.
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
related_scenarios: [SCN-003]
related_reqs:
  - CON-006
  - FUN-004
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-019: Limit File Input to TXT

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application fails early on unsupported file types.

## Context / Scope
The story covers file input validation inside the ORION library boundary.

## Narrative
As a host application, I want file input limited to .txt so I can fail early on unsupported file types.

## Acceptance Criteria
- AC-1 (CON-006, FUN-004): Only .txt files are in scope.
- AC-2 (CON-006, FUN-004): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (CON-006, FUN-004): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-003
- Related requirements: CON-006, FUN-004
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
