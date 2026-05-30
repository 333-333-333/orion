---
id: FUN-001
type: FUN
title: Instantiate ORION as a library
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The host application can instantiate ORION as an importable Python library object before use.
tags: [library, instantiation, host-application]
domain: orion
capability: library-instantiation
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [CON-001, CON-002, NFR-004]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-001: Instantiate ORION as a library

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The host application can instantiate ORION as an importable Python library object before use.

## Context / Scope
ORION shall be importable and instantiable from Python code by a host application. The library shall not require CLI startup, HTTP startup, or any external service wrapper before use.

## Description
ORION shall be importable and instantiable from Python code by a host application. The library shall not require CLI startup, HTTP startup, or any external service wrapper before use.

## Acceptance Criteria
- The host application can import ORION from Python and create an instance without launching a process, server, or shell command.
- Instantiation succeeds with a valid configuration object and fails with a controlled ORION exception for invalid setup.
- The instantiated object can be used directly to process input in the same runtime.

## Dependencies
- Requires FUN-002 for configuration input and CON-001/CON-002 for the no-CLI/no-service boundary.

## Business Rules
- No CLI contract applies.
- No REST or HTTP service contract applies.

## Validation Method
- Unit test imports ORION, instantiates it, and verifies no CLI or network bootstrap is needed.

## Technical Notes
Library entrypoint must stay importable from Python and usable inside another process.

## Traceability
- Upstream source: README.md. Downstream: CON-001, CON-002, NFR-004.

## Open questions
None.
