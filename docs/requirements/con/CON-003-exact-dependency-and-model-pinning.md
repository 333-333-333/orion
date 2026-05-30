---
id: CON-003
type: CON
title: Exact dependency and model pinning
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Dependencies and spaCy models must be pinned exactly for reproducibility.
tags: [constraint, pinning, dependencies, spacy]
domain: orion
capability: pinning
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [NFR-001, NFR-003, NFR-005]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# CON-003: Exact dependency and model pinning

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Dependencies and spaCy models must be pinned exactly for reproducibility.

## Context / Scope
ORION shall use exact version pinning for runtime dependencies and selected spaCy model versions.

## Description
ORION shall use exact version pinning for runtime dependencies and selected spaCy model versions.

## Acceptance Criteria
- The project records exact dependency versions in its lock/export workflow.
- Selected spaCy model versions are pinned, not floating.
- Reproducibility tests use the pinned environment, not an unpinned install.

## Dependencies
- Supports deterministic reproducibility and interoperability requirements.

## Business Rules
- Pinned versions are mandatory for the initial contract.

## Validation Method
- Dependency audit verifies exact pins for runtime dependencies and models.

## Technical Notes
Keep dependency and model pins in sync with the lockfile workflow.

## Traceability
- Upstream source: README.md. Downstream: NFR-001, NFR-003, NFR-005.

## Open questions
None.
