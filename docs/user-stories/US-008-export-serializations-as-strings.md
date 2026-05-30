---
id: US-008
type: US
title: Export Serializations as Strings
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application consumes serializations without writing files.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: serialization
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_reqs:
  - FUN-008
  - NFR-003
  - NFR-004
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-008: Export Serializations as Strings

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application consumes serializations without writing files.

## Context / Scope
The story covers string-based export inside the ORION library boundary.

## Narrative
As a host application, I want serializations as strings so I can consume results without file writes.

## Acceptance Criteria
- AC-1 (FUN-008, NFR-003, NFR-004): File writes are not part of the normal consumption flow.
- AC-2 (FUN-008, NFR-003, NFR-004): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-008, NFR-003, NFR-004): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: FUN-008, NFR-003, NFR-004
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
