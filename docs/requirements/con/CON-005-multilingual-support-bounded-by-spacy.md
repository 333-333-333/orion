---
id: CON-005
type: CON
title: Multilingual support bounded by spaCy
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Language support is limited by what spaCy models can support.
tags: [constraint, multilingual, spacy]
domain: orion
capability: language-boundary
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

# CON-005: Multilingual support bounded by spaCy

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Language support is limited by what spaCy models can support.

## Context / Scope
ORION shall only claim multilingual support to the extent that compatible spaCy models exist and are configured.

## Description
ORION shall only claim multilingual support to the extent that compatible spaCy models exist and are configured.

## Acceptance Criteria
- Supported language behavior depends on available spaCy models.
- Unsupported spaCy-backed languages are rejected or left unclaimed.
- The contract does not promise universal language coverage.

## Dependencies
- Requires spaCy model selection and pinning.

## Business Rules
- Language support is bounded by spaCy capability.

## Validation Method
- Docs review and language tests confirm support is limited to declared models.

## Technical Notes
Language feature expansion must follow spaCy model support.

## Traceability
- Upstream source: README.md. Downstream: FUN-005.

## Open questions
None.
