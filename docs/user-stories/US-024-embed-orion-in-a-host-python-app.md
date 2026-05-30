---
id: US-024
type: US
title: Embed ORION in a Host Python App
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application calls ORION in-process from another Python app.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: embedding
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_reqs:
  - NFR-004
  - FUN-001
  - FUN-002
  - FUN-008
  - FUN-010
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-024: Embed ORION in a Host Python App

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application calls ORION in-process from another Python app.

## Context / Scope
The story covers host-application embedding inside the ORION library boundary.

## Narrative
As a host application, I want ORION to be easy to embed in another Python app so I can call it in-process.

## Acceptance Criteria
- AC-1 (NFR-004, FUN-001, FUN-002, FUN-008, FUN-010): In-process use should stay simple for Python hosts.
- AC-2 (NFR-004, FUN-001, FUN-002, FUN-008, FUN-010): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (NFR-004, FUN-001, FUN-002, FUN-008, FUN-010): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: NFR-004, FUN-001, FUN-002, FUN-008, FUN-010
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
