---
id: US-007
type: US
title: Generate Deterministic RDF/OWL Triples
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application compares semantic-web triples across repeated runs.
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
  - FUN-007
  - NFR-001
  - NFR-003
  - NFR-005
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-007: Generate Deterministic RDF/OWL Triples

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application compares semantic-web triples across repeated runs.

## Context / Scope
The story covers repeatable RDF/OWL triple generation inside the ORION library boundary.

## Narrative
As a host application, I want deterministic RDF/OWL triples so I can use semantic-web outputs repeatably.

## Acceptance Criteria
- AC-1 (FUN-007, NFR-001, NFR-003, NFR-005): The output must stay compatible with semantic-web tooling.
- AC-2 (FUN-007, NFR-001, NFR-003, NFR-005): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-007, NFR-001, NFR-003, NFR-005): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-004
- Related requirements: FUN-007, NFR-001, NFR-003, NFR-005
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
