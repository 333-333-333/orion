---
id: US-017
type: US
title: Use English and Spanish Initially
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application uses the declared initial language set.
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
  - CON-004
  - FUN-005
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-017: Use English and Spanish Initially

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application uses the declared initial language set.

## Context / Scope
The story covers the initial supported language set inside the ORION library boundary.

## Narrative
As a host application, I want English and Spanish as the initial languages so I can use the declared language set.

## Acceptance Criteria
- AC-1 (CON-004, FUN-005): Initial support is limited to the declared language set.
- AC-2 (CON-004, FUN-005): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (CON-004, FUN-005): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: CON-004, FUN-005
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
