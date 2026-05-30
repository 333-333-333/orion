---
id: FUN-005
type: FUN
title: Support configurable language with English default
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library supports configurable language selection and defaults to English.
tags: [language, english-default, multilingual]
domain: orion
capability: language-selection
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [CON-004, CON-005, NFR-001]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-005: Support configurable language with English default

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library supports configurable language selection and defaults to English.

## Context / Scope
ORION shall let the host application set the processing language, and when no language is provided it shall default to English. Initial supported languages shall include English and Spanish.

## Description
ORION shall let the host application set the processing language, and when no language is provided it shall default to English. Initial supported languages shall include English and Spanish.

## Acceptance Criteria
- If no language is configured, ORION uses English.
- If Spanish is configured and a supported spaCy model is available, processing proceeds without unsupported-language failure.
- Unsupported language values are rejected with a controlled ORION exception.

## Dependencies
- Requires FUN-002 for config input and CON-004/CON-005 for initial language boundaries.

## Business Rules
- Default language is English.
- Initial supported languages are English and Spanish, bounded by spaCy support.

## Validation Method
- Unit tests verify default English, explicit Spanish, and unsupported language failure.

## Technical Notes
Language mapping must align with configured spaCy models.

## Traceability
- Upstream source: README.md. Downstream: CON-004, CON-005, NFR-001.

## Open questions
None.
