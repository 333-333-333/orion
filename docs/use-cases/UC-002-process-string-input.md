---
id: UC-002
type: UC
title: Process String Input
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host Application submits a text string and ORION processes it in-process.
tags: [orion, string-input, text-processing, host-application]
domain: orion
capability: input-processing
actors: [Host Application]
systems: [ORION]
source: docs/user-stories
change_ref: CHG-UC-FROM-US
primary_actor: ACT-001
secondary_actors: []
priority: High
related_acts: [ACT-001]
related_ucm: [UCM-001]
related_reqs: [FUN-003, NFR-001, NFR-005]
related_user_stories: [US-003]
related_brs: []
related_adrs: []
owner: herodotus
---

# UC-002: Process String Input

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Canonical use case captured from approved user stories | herodotus |

## Summary
Host Application submits a text string and ORION processes it in-process.

## Context / Scope
This use case covers direct string input only. It remains inside the library-only boundary and does not require file, CLI, or service invocation.

## Preconditions
- ORION is already initialized.
- Host Application has a string payload.
- The runtime is ready for deterministic processing.

## Postconditions
- ORION produces a processed text result for downstream semantic work.
- Invalid input results in a controlled ORION-specific exception.

## Main Flow
| Step | Actor | Action | Business Rules |
|---|---|---|---|
| 1 | Host Application | Sends a text string to ORION for processing. | None |
| 2 | ORION | Validates the string content and runtime readiness. | None |
| 3 | Host Application | Confirms the processing settings to use for the input. | None |
| 4 | ORION | Returns the processed text result. | None |

## Alternative Flows
### AF-1: Empty but accepted text wrapper
**Trigger**: Input wrapper exists but the text payload is blank after trimming.
1. ORION treats the input as invalid.
2. Jump to Exception Flow E1.

## Exception Flows
### E1: Invalid string input
**Trigger**: Input is empty, unsupported, or otherwise unusable.
1. ORION rejects the input.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

### E2: Invalid model/runtime state
**Trigger**: The processing path depends on an invalid model or broken runtime setup.
1. ORION stops processing.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

## Business Rules
None; no BR docs exist for this flow.

## Technical Notes
- Input is plain text string only.
- Processing stays in-process and must not assume serialization or export.
- Use ORION-specific exceptions for validation and runtime failures. [FUN-013]

## Traceability
- Related model: UCM-001
- Related reqs: FUN-003, NFR-001, NFR-005
- Related user stories: US-003
- Related actor: ACT-001
- Related BRs: none

## Open questions
None.

## Cross-References
- UCM: UCM-001
- ACT: ACT-001
- Requirements: FUN-003, NFR-001, NFR-005
- User stories: US-003
