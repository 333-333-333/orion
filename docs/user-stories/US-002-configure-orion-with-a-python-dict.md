---
id: US-002
type: US
title: Configure ORION with a Python Dict
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application configures ORION natively with a Python dict.
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
related_scenarios: [SCN-001]
related_reqs:
  - FUN-002
  - CON-007
  - NFR-004
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-002: Configure ORION with a Python Dict

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application configures ORION natively with a Python dict.

## Context / Scope
The story stays inside the ORION library boundary and covers native Python setup only.

## Narrative
As a host application, I want to pass a Python dict at setup so I can configure ORION natively.

## Acceptance Criteria
- AC-1 (FUN-002, CON-007, NFR-004): Configuration happens through Python objects already available in the host app.
- AC-2 (FUN-002, CON-007, NFR-004): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-002, CON-007, NFR-004): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-001
- Related requirements: FUN-002, CON-007, NFR-004
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
