---
id: US-011
type: US
title: Record Traceability for Ontology Elements
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host application traces each ontology element back to source text.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: traceability
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_scenarios: [SCN-006]
related_reqs:
  - FUN-011
  - NFR-002
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-011: Record Traceability for Ontology Elements

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application traces each ontology element back to source text.

## Context / Scope
The story covers provenance on ontology elements inside the ORION library boundary.

## Narrative
As a host application, I want ontology elements to carry traceability so I can trace each entity back to source text.

## Acceptance Criteria
- AC-1 (FUN-011, NFR-002): Traceability must point back to source text.
- AC-2 (FUN-011, NFR-002): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (FUN-011, NFR-002): The host application can use the described behavior from Python code.

## Traceability
- Related scenarios: SCN-006
- Related requirements: FUN-011, NFR-002
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
