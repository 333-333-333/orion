---
id: US-005
type: US
title: Select Language with English Default
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application chooses a processing language with English as the default.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: language-selection
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_reqs:
  - FUN-005
  - CON-004
  - CON-005
  - NFR-001
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-005: Select Language with English Default

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application chooses a processing language with English as the default.

## Context / Scope
The story covers language selection and default behavior inside the ORION library boundary.

## Narrative
As a host application, I want to choose the processing language and get English by default so I can control language behavior predictably.

## Acceptance Criteria
- AC-1 (FUN-005, CON-004, CON-005, NFR-001): English is the default when the host application does not override the language.
- AC-2 (FUN-005, CON-004, CON-005, NFR-001): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-005, CON-004, CON-005, NFR-001): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: FUN-005, CON-004, CON-005, NFR-001
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
