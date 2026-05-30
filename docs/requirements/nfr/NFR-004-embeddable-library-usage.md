---
id: NFR-004
type: NFR
title: Embeddable library usage
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: ORION must be easy to embed inside a host Python application.
tags: [library, embeddable, host-application]
domain: orion
capability: embeddability
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-001, FUN-002, FUN-008, FUN-010]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# NFR-004: Embeddable library usage

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
ORION must be easy to embed inside a host Python application.

## Context / Scope
ORION shall support direct use inside another Python application without requiring ORION-owned process management or service deployment.

## Description
ORION shall support direct use inside another Python application without requiring ORION-owned process management or service deployment.

## Acceptance Criteria
- A host application can call ORION in-process and receive results directly.
- No ORION-specific server, daemon, or CLI process is required for normal use.
- Configuration and outputs stay Python-native at the library boundary.

## Dependencies
- Requires importable entrypoint and Python-native result objects.

## Business Rules
- ORION is a library, not a standalone service contract.

## Validation Method
- Integration test embeds ORION inside a sample host application call path.

## Technical Notes
Keep the public-facing boundary Python-native.

## Traceability
- Upstream source: README.md. Downstream: FUN-001, FUN-002, FUN-008, FUN-010.

## Open questions
None.
