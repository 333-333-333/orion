---
id: UC-004
type: UC
title: Generate Deterministic Semantic Output
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host Application requests deterministic semantic generation and ORION returns stable semantic output.
tags: [orion, semantic-generation, deterministic, rdf, owl]
domain: orion
capability: semantic-generation
actors: [Host Application]
systems: [ORION]
source: docs/user-stories
change_ref: CHG-UC-FROM-US
primary_actor: ACT-001
secondary_actors: []
priority: High
related_acts: [ACT-001]
related_reqs: [FUN-006, FUN-007, FUN-009, NFR-001, NFR-003, NFR-005]
related_user_stories: [US-006, US-007, US-009, US-023, US-025, US-026]
related_brs: []
related_adrs: []
owner: herodotus
---

# UC-004: Generate Deterministic Semantic Output

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Canonical use case captured from approved user stories | herodotus |

## Summary
Host Application requests deterministic semantic generation and ORION returns stable semantic output.

## Context / Scope
This use case covers deterministic ontology and triple generation only. It stays inside the in-process ORION boundary.

## Preconditions
- ORION is initialized.
- Input has already been processed.
- Required language and model settings are available.

## Postconditions
- ORION produces deterministic semantic output.
- Generated output is stable for the same input and configuration.

## Main Flow
| Step | Actor | Action | Business Rules |
|---|---|---|---|
| 1 | Host Application | Requests semantic generation from ORION. | None |
| 2 | ORION | Loads the deterministic processing setup and validates readiness. | None |
| 3 | Host Application | Confirms the semantic settings or defaults to use. | None |
| 4 | ORION | Generates ontology elements and RDF/OWL triples deterministically. | None |

## Alternative Flows
### AF-1: Default English generation
**Trigger**: Host Application omits language selection.
1. ORION applies English as the default language.
2. Resume at Main Flow step 4.

### AF-2: Stable comparison surface
**Trigger**: Host Application requests output suitable for diff or test comparison.
1. ORION keeps the comparison surface stable.
2. Resume at Main Flow step 4.

## Exception Flows
### E1: Invalid model configuration
**Trigger**: The model setup is invalid, incomplete, or unavailable.
1. ORION stops generation.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

### E2: Input not ready for generation
**Trigger**: Processed input is missing or invalid.
1. ORION rejects the request.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

### E3: Runtime generation failure
**Trigger**: Semantic generation cannot complete because the runtime state is broken.
1. ORION stops generation.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

## Business Rules
None; no BR docs exist for this flow.

## Technical Notes
- Deterministic output must remain reproducible for the same inputs and config.
- Separate inferred and deterministic results remain distinct in the semantic payload.
- Use ORION-specific exceptions for generation failures. [FUN-013]

## Traceability
- Related reqs: FUN-006, FUN-007, FUN-009, NFR-001, NFR-003, NFR-005
- Related user stories: US-006, US-007, US-009, US-023, US-025, US-026
- Related actor: ACT-001
- Related BRs: none

## Open questions
None.

## Cross-References
- ACT: ACT-001
- Requirements: FUN-006, FUN-007, FUN-009, NFR-001, NFR-003, NFR-005
- User stories: US-006, US-007, US-009, US-023, US-025, US-026
