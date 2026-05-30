---
id: CON-001
type: CON
title: No CLI contract
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: ORION must not be treated as a CLI product.
tags: [constraint, cli, library-boundary]
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

# CON-001: No CLI contract

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
ORION must not be treated as a CLI product.

## Context / Scope
ORION shall not expose a CLI-first or CLI-required contract. The library may be invoked only through Python code by a host application.

## Description
ORION shall not expose a CLI-first or CLI-required contract. The library may be invoked only through Python code by a host application.

## Acceptance Criteria
- Repository documentation and contract artifacts do not require CLI usage for normal operation.
- Tests for the contract do not depend on shell commands to exercise ORION behavior.
- Any CLI mention is limited to non-contract notes or examples outside the product boundary.

## Dependencies
- Applies to all functional and non-functional requirements in this set.

## Business Rules
- No command-line interface is part of the ORION product boundary.

## Validation Method
- Doc review and integration tests confirm no CLI dependency is required.

## Technical Notes
Keep the entrypoint library-first.

## Traceability
- Upstream source: README.md. Downstream: FUN-001, NFR-004.

## Open questions
None.
