---
id: US-006
type: US
title: Generate Deterministic Ontology Elements
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application compares ontology elements across repeated runs.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: deterministic-output
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_scenarios: [SCN-004]
related_reqs:
  - FUN-006
  - NFR-001
  - NFR-005
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-006: Generate Deterministic Ontology Elements

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application compares ontology elements across repeated runs.

## Context / Scope
The story covers repeatable ontology element generation inside the ORION library boundary.

## Narrative
As a host application, I want deterministic ontology elements so I can compare runs reliably.

## Acceptance Criteria
- AC-1 (FUN-006, NFR-001, NFR-005): Determinism matters for direct run-to-run comparison.
- AC-2 (FUN-006, NFR-001, NFR-005): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-006, NFR-001, NFR-005): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-004
- Related requirements: FUN-006, NFR-001, NFR-005
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
