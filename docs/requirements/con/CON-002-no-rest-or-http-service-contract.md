---
id: CON-002
type: CON
title: No REST or HTTP service contract
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: ORION must not expose a REST or HTTP service contract.
tags: [constraint, rest, http, library-boundary]
domain: orion
capability: boundary
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-001, NFR-004]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# CON-002: No REST or HTTP service contract

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
ORION must not expose a REST or HTTP service contract.

## Context / Scope
ORION shall not provide its own REST endpoint, HTTP server, or network service contract. A host application may call the library internally and expose its own interface if needed.

## Description
ORION shall not provide its own REST endpoint, HTTP server, or network service contract. A host application may call the library internally and expose its own interface if needed.

## Acceptance Criteria
- No ORION-owned HTTP server or endpoint is required to process text.
- Network transport is not part of the ORION contract.
- Documentation frames REST/API systems only as host applications, not as ORION itself.

## Dependencies
- Applies to all processing and output requirements.

## Business Rules
- No REST or HTTP service is part of the ORION boundary.

## Validation Method
- Architecture review confirms no network-service dependency is required.

## Technical Notes
Avoid service scaffolding in the library contract.

## Traceability
- Upstream source: README.md. Downstream: FUN-001, NFR-004.

## Open questions
None.
