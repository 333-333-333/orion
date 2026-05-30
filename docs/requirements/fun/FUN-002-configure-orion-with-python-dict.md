---
id: FUN-002
type: FUN
title: Configure ORION with a Python dict
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The host application configures ORION using a Python dictionary before processing text.
tags: [configuration, python-dict, host-application]
domain: orion
capability: configuration
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [CON-007, NFR-004]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-002: Configure ORION with a Python dict

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The host application configures ORION using a Python dictionary before processing text.

## Context / Scope
ORION shall accept its runtime configuration as a Python dict. The configuration shall include, at minimum, language and spaCy model size settings when provided by the host application.

## Description
ORION shall accept its runtime configuration as a Python dict. The configuration shall include, at minimum, language and spaCy model size settings when provided by the host application.

## Acceptance Criteria
- A valid Python dict can be passed at instantiation time without conversion from YAML or CLI flags.
- Invalid or missing required config keys produce ORION-specific validation errors.
- The configuration object controls language and spaCy model size selection.

## Dependencies
- Requires FUN-001 for instantiation and CON-007 for the primary config format.

## Business Rules
- Python dict is the primary configuration format.

## Validation Method
- Unit test passes a Python dict config and verifies deterministic config application and error handling.

## Technical Notes
Avoid making YAML the primary config format.

## Traceability
- Upstream source: README.md. Downstream: CON-007, NFR-004.

## Open questions
None.
