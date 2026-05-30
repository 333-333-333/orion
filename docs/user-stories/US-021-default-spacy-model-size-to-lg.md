---
id: US-021
type: US
title: Default spaCy Model Size to lg
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application gets explicit default runs with lg model size.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: configuration
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_reqs:
  - CON-008
  - FUN-005
  - NFR-001
  - NFR-003
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-021: Default spaCy Model Size to lg

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application gets explicit default runs with lg model size.

## Context / Scope
The story covers the default spaCy model size inside the ORION library boundary.

## Narrative
As a host application, I want lg to be the default spaCy model size so I can run with an explicit default.

## Acceptance Criteria
- AC-1 (CON-008, FUN-005, NFR-001, NFR-003): Default runs should not rely on an implicit model size.
- AC-2 (CON-008, FUN-005, NFR-001, NFR-003): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (CON-008, FUN-005, NFR-001, NFR-003): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: CON-008, FUN-005, NFR-001, NFR-003
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
