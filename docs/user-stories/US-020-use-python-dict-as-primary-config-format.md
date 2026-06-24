---
id: US-020
type: US
title: Use Python Dict as Primary Config Format
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application configures ORION with Python-native data.
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
  - CON-007
  - FUN-002
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-020: Use Python Dict as Primary Config Format

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application configures ORION with Python-native data.

## Context / Scope
The story covers the primary configuration shape inside the ORION library boundary.

## Narrative
As a host application, I want Python dict to be the primary config format so I can configure ORION in Python.

## Acceptance Criteria
- AC-1 (CON-007, FUN-002): Python dict is the native setup format.
- AC-2 (CON-007, FUN-002): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (CON-007, FUN-002): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-001
- Related requirements: CON-007, FUN-002
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
