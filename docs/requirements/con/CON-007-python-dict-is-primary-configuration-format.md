---
id: CON-007
type: CON
title: Python dict is primary configuration format
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Python dict is the primary runtime configuration format.
tags: [constraint, configuration, python-dict]
domain: orion
capability: configuration-format
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-002]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# CON-007: Python dict is primary configuration format

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Python dict is the primary runtime configuration format.

## Context / Scope
ORION shall treat Python dict as the primary supported configuration shape for the initial contract.

## Description
ORION shall treat Python dict as the primary supported configuration shape for the initial contract.

## Acceptance Criteria
- The main documented configuration path uses a Python dict.
- Alternative config formats are not required for the initial contract.
- Tests use Python dict configuration as the default contract path.

## Dependencies
- Applies to the configuration entrypoint.

## Business Rules
- Primary config format is Python dict.

## Validation Method
- API/contract tests verify dict-based configuration is accepted.

## Technical Notes
Keep config parsing simple and Python-native.

## Traceability
- Upstream source: README.md. Downstream: FUN-002.

## Open questions
None.
