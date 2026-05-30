---
id: US-016
type: US
title: Pin Dependencies and Models Exactly
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application gets reproducible results from exact dependency and model pinning.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: reproducibility
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_reqs:
  - CON-003
  - NFR-001
  - NFR-003
  - NFR-005
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-016: Pin Dependencies and Models Exactly

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application gets reproducible results from exact dependency and model pinning.

## Context / Scope
The story covers exact pinning inside the ORION library boundary.

## Narrative
As a host application, I want exact dependency and model pinning so I can get reproducible results.

## Acceptance Criteria
- AC-1 (CON-003, NFR-001, NFR-003, NFR-005): Reproducibility depends on pinned dependencies and models.
- AC-2 (CON-003, NFR-001, NFR-003, NFR-005): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (CON-003, NFR-001, NFR-003, NFR-005): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: CON-003, NFR-001, NFR-003, NFR-005
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
