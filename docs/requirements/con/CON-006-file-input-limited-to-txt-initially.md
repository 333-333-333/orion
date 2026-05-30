---
id: CON-006
type: CON
title: File input limited to TXT initially
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Initial file input is limited to .txt files.
tags: [constraint, file-input, txt]
domain: orion
capability: file-input
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-003, FUN-004]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# CON-006: File input limited to TXT initially

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Initial file input is limited to .txt files.

## Context / Scope
ORION shall initially accept only .txt files as file-based input. Other file types are out of scope for the initial contract.

## Description
ORION shall initially accept only .txt files as file-based input. Other file types are out of scope for the initial contract.

## Acceptance Criteria
- .txt file paths are accepted by the initial file input contract.
- .pdf, .docx, and other formats are rejected or unsupported initially.
- String input remains separate from file input and is still allowed.

## Dependencies
- Applies to file-based input handling only.

## Business Rules
- Initial file input scope is .txt only.

## Validation Method
- Input tests verify accepted .txt and rejected non-.txt paths.

## Technical Notes
Do not infer future file-type support from the initial contract.

## Traceability
- Upstream source: README.md. Downstream: FUN-003, FUN-004.

## Open questions
None.
