---
id: US-018
type: US
title: Bound Language Support by spaCy
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application requests only supported languages bounded by spaCy models.
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
  - CON-005
  - FUN-005
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-018: Bound Language Support by spaCy

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application requests only supported languages bounded by spaCy models.

## Context / Scope
The story covers model-bounded language support inside the ORION library boundary.

## Narrative
As a host application, I want language support bounded by spaCy models so I can only request supported languages.

## Acceptance Criteria
- AC-1 (CON-005, FUN-005): Language support follows the available spaCy models.
- AC-2 (CON-005, FUN-005): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (CON-005, FUN-005): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: CON-005, FUN-005
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
