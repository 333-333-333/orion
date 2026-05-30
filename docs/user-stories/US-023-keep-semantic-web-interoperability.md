---
id: US-023
type: US
title: Keep Semantic Web Interoperability
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host application uses standard RDF/OWL tooling with ORION output.
tags:
  - user-story
  - library-only
  - host-application
domain: orion
capability: interoperability
actors:
  - Host Application
systems:
  - ORION
source: docs/requirements
change_ref: CHG-US-FROM-REQS
related_ucs: []
related_reqs:
  - NFR-003
  - FUN-007
  - FUN-008
  - CON-003
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# US-023: Keep Semantic Web Interoperability

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Approved user story preview captured from the ORION requirement set | herodotus |

## Summary
Host application uses standard RDF/OWL tooling with ORION output.

## Context / Scope
The story covers semantic-web interoperability inside the ORION library boundary.

## Narrative
As a host application, I want semantic-web interoperable outputs so I can use standard RDF/OWL tools.

## Acceptance Criteria
- AC-1 (NFR-003, FUN-007, FUN-008, CON-003): Standard RDF/OWL tools should consume the outputs.
- AC-2 (NFR-003, FUN-007, FUN-008, CON-003): The story stays inside the ORION library boundary and avoids scope outside the listed requirements.
- AC-3 (NFR-003, FUN-007, FUN-008, CON-003): The host application can use the described behavior from Python code.

## Traceability
- Related requirements: NFR-003, FUN-007, FUN-008, CON-003
- Source: docs/requirements
- Related user stories: None

## Notes
Library-only boundary; keep use in-process.

## Open questions
None.
