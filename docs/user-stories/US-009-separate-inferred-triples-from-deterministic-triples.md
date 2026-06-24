---
id: US-009
type: US
title: Separate Inferred Triples from Deterministic Triples
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application inspects stable output without inferred triples mixed in.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: triple-separation
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_scenarios: [SCN-004]
related_reqs:
  - FUN-009
  - NFR-001
  - NFR-005
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-009: Separate Inferred Triples from Deterministic Triples

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application inspects stable output without inferred triples mixed in.

## Context / Scope
The story covers separation of stable and inferred semantic output inside the ORION library boundary.

## Narrative
As a host application, I want inferred triples kept separate from deterministic triples so I can inspect stable output alone.

## Acceptance Criteria
- AC-1 (FUN-009, NFR-001, NFR-005): Stable output must remain inspectable on its own.
- AC-2 (FUN-009, NFR-001, NFR-005): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-009, NFR-001, NFR-005): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-004
- Related requirements: FUN-009, NFR-001, NFR-005
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
