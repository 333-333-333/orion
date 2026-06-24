---
id: UC-005
type: UC
title: Export Semantic Output
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host Application exports ORION semantic output as a serializable result.
tags: [orion, export, serialization, host-application]
domain: orion
capability: export
actors: [Host Application]
systems: [ORION]
source: docs/user-stories
change_ref: CHG-UC-FROM-US
primary_actor: ACT-001
secondary_actors: []
priority: High
related_acts: [ACT-001]
related_ucm: [UCM-001]
related_reqs: [FUN-008, FUN-010, NFR-003, NFR-004]
related_user_stories: [US-008, US-010]
related_brs: []
related_adrs: []
owner: herodotus
---

# UC-005: Export Semantic Output

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Canonical use case captured from approved user stories | herodotus |

## Summary
Host Application exports ORION semantic output as a serializable result.

## Context / Scope
This use case covers export only. It does not cover generation, parsing, or transport outside the host process.

## Preconditions
- ORION is initialized.
- Semantic output exists.
- The host application knows the desired export shape.

## Postconditions
- ORION returns exported semantic output as a string or Python object as requested.
- Serialization failures return a controlled ORION-specific exception.

## Main Flow
| Step | Actor | Action | Business Rules |
|---|---|---|---|
| 1 | Host Application | Requests export of the current semantic output. | None |
| 2 | ORION | Validates the export target and output state. | None |
| 3 | Host Application | Chooses the export format or result shape. | None |
| 4 | ORION | Serializes the semantic output and returns it. | None |

## Alternative Flows
### AF-1: String export
**Trigger**: Host Application requests a string serialization.
1. ORION serializes the output as a string.
2. Resume at Main Flow step 4.

### AF-2: Python object export
**Trigger**: Host Application requests an in-memory Python object.
1. ORION returns the semantic output as a Python object.
2. Resume at Main Flow step 4.

## Exception Flows
### E1: Serialization failure
**Trigger**: The output cannot be serialized for the requested format.
1. ORION stops export.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

### E2: Unsupported export format
**Trigger**: Host Application requests an unsupported format.
1. ORION rejects the export request.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

### E3: Invalid model/runtime state
**Trigger**: Export depends on invalid or incomplete semantic state.
1. ORION stops export.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

## Business Rules
None; no BR docs exist for this flow.

## Technical Notes
- Export must support stable serialization surfaces for testability.
- Output may be returned as a string or as a Python object depending on the requested shape.
- Use ORION-specific exceptions for serialization and state failures. [FUN-013]

## Traceability
- Related model: UCM-001
- Related reqs: FUN-008, FUN-010, NFR-003, NFR-004
- Related user stories: US-008, US-010
- Related actor: ACT-001
- Related BRs: none

## Open questions
None.

## Cross-References
- UCM: UCM-001
- ACT: ACT-001
- Requirements: FUN-008, FUN-010, NFR-003, NFR-004
- User stories: US-008, US-010
