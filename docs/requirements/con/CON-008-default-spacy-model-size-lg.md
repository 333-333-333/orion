---
id: CON-008
type: CON
title: Default spaCy model size lg
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The default spaCy model size is lg.
tags: [constraint, spacy, default, lg]
domain: orion
capability: spacy-model-sizing
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-005, NFR-001, NFR-003]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# CON-008: Default spaCy model size lg

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The default spaCy model size is lg.

## Context / Scope
ORION shall default to the lg spaCy model size when the host application does not specify another size.

## Description
ORION shall default to the lg spaCy model size when the host application does not specify another size.

## Acceptance Criteria
- A missing model-size setting results in lg being selected.
- Model-size selection remains configurable by the host application.
- Deterministic tests run against the declared default.

## Dependencies
- Requires spaCy-backed language configuration.

## Business Rules
- Default model size is lg.

## Validation Method
- Configuration tests verify the default model size resolves to lg.

## Technical Notes
Keep model-size defaults explicit in documentation and code.

## Traceability
- Upstream source: README.md. Downstream: FUN-005, NFR-001, NFR-003.

## Open questions
None.
