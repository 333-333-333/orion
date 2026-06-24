---
id: US-014
type: US
title: Stay Library-Only
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application uses ORION without a CLI contract.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: boundary
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_scenarios: [SCN-001]
related_reqs:
  - CON-001
  - FUN-001
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-014: Stay Library-Only

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application uses ORION without a CLI contract.

## Context / Scope
The story keeps ORION inside the importable library boundary only.

## Narrative
As a host application, I want ORION to stay library-only so I can avoid a CLI contract.

## Acceptance Criteria
- AC-1 (CON-001, FUN-001): No CLI contract is part of the product boundary.
- AC-2 (CON-001, FUN-001): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (CON-001, FUN-001): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-001
- Related requirements: CON-001, FUN-001
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
