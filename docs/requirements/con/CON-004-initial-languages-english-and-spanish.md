---
id: CON-004
type: CON
title: Initial languages English and Spanish
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Initial supported languages are bounded to English and Spanish.
tags: [constraint, language, english, spanish]
domain: orion
capability: language-scope
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-005]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# CON-004: Initial languages English and Spanish

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Initial supported languages are bounded to English and Spanish.

## Context / Scope
ORION shall initially support only English and Spanish languages as the declared starting language set.

## Description
ORION shall initially support only English and Spanish languages as the declared starting language set.

## Acceptance Criteria
- English is available by default.
- Spanish is available when the corresponding supported model is configured.
- Other languages are out of scope for the initial contract.

## Dependencies
- Depends on spaCy language model availability.

## Business Rules
- The initial language scope is English plus Spanish only.

## Validation Method
- Configuration tests verify English and Spanish succeed while another language fails.

## Technical Notes
Keep language expansion explicit, not implicit.

## Traceability
- Upstream source: README.md. Downstream: FUN-005.

## Open questions
None.
