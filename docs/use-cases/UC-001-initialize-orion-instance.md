---
id: UC-001
type: UC
title: Initialize ORION Instance
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host Application initializes ORION in-process with a valid configuration object.
tags: [orion, initialization, library-only, host-application]
domain: orion
capability: initialization
actors: [Host Application]
systems: [ORION]
source: docs/user-stories
change_ref: CHG-UC-FROM-US
primary_actor: ACT-001
secondary_actors: []
priority: High
related_acts: [ACT-001]
related_reqs: [FUN-001, FUN-002, FUN-005, CON-001, CON-002, CON-003, CON-004, CON-005, CON-007, CON-008, NFR-004]
related_user_stories: [US-001, US-002, US-005, US-014, US-015, US-016, US-017, US-018, US-020, US-021, US-024]
related_brs: []
related_adrs: []
owner: herodotus
---

# UC-001: Initialize ORION Instance

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Canonical use case captured from approved user stories | herodotus |

## Summary
Host Application initializes ORION in-process with a valid configuration object.

## Context / Scope
This use case stays inside the library-only ORION boundary. It covers startup, configuration handoff, and instance creation only.

## Preconditions
- Host Application can import ORION in the same runtime.
- A configuration object is available.
- No CLI, REST, or HTTP bootstrap is required.

## Postconditions
- ORION instance exists in the host process and is ready for later processing calls.
- If initialization fails, no usable instance is returned and a controlled ORION-specific exception is raised.

## Main Flow
| Step | Actor | Action | Business Rules |
|---|---|---|---|
| 1 | Host Application | Provides the configuration object and requests ORION initialization. | None |
| 2 | ORION | Validates the configuration and library-only boundary constraints. | None |
| 3 | Host Application | Supplies any required initialization values or defaults requested by ORION. | None |
| 4 | ORION | Creates the in-process instance and returns it to the host application. | None |

## Alternative Flows
### AF-1: Default language initialization
**Trigger**: Host Application omits language selection.
1. ORION applies its English default.
2. Resume at Main Flow step 4.

### AF-2: Partial optional configuration
**Trigger**: Optional settings are missing but not required.
1. ORION fills the supported defaults.
2. Resume at Main Flow step 4.

## Exception Flows
### E1: Invalid configuration
**Trigger**: Configuration is malformed, incomplete, or incompatible.
1. ORION rejects initialization.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

### E2: Invalid model setup
**Trigger**: Initialization includes invalid or unavailable model settings.
1. ORION rejects the model setup.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

## Business Rules
None; no BR docs exist for this flow.

## Technical Notes
- Initialization happens in-process only.
- Python dict configuration is the primary expected input shape.
- Failure should use ORION-specific exceptions, not generic runtime errors. [FUN-013]

## Traceability
- Related reqs: FUN-001, FUN-002, FUN-005, CON-001, CON-002, CON-003, CON-004, CON-005, CON-007, CON-008, NFR-004
- Related user stories: US-001, US-002, US-005, US-014, US-015, US-016, US-017, US-018, US-020, US-021, US-024
- Related actor: ACT-001
- Related UCs: UC-002, UC-003, UC-004, UC-005, UC-006
- Related BRs: none

## Open questions
None.

## Cross-References
- ACT: ACT-001
- Requirements: FUN-001, FUN-002, FUN-005, CON-001, CON-002, CON-003, CON-004, CON-005, CON-007, CON-008, NFR-004
- User stories: US-001, US-002, US-005, US-014, US-015, US-016, US-017, US-018, US-020, US-021, US-024
