---
id: US-010
type: US
title: Return Results as Python Objects
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application reads results directly without parsing blobs.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: python-results
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_reqs:
  - FUN-010
  - NFR-003
  - NFR-004
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-010: Return Results as Python Objects

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application reads results directly without parsing blobs.

## Context / Scope
The story covers Python-native result handling inside the ORION library boundary.

## Narrative
As a host application, I want Python result objects so I can read output directly without parsing blobs.

## Acceptance Criteria
- AC-1 (FUN-010, NFR-003, NFR-004): Results should stay usable from host Python code.
- AC-2 (FUN-010, NFR-003, NFR-004): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-010, NFR-003, NFR-004): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: FUN-010, NFR-003, NFR-004
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
