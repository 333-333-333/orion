---
id: UC-006
type: UC
title: Inspect Traceability Metadata
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-06-23
summary: Host Application inspects traceability metadata attached to ORION outputs.
tags: [orion, traceability, metadata, host-application]
domain: orion
capability: traceability
actors: [Host Application]
systems: [ORION]
source: docs/user-stories
change_ref: CHG-UC-FROM-US
primary_actor: ACT-001
secondary_actors: []
priority: High
related_acts: [ACT-001]
related_ucm: [UCM-001]
related_reqs: [FUN-011, FUN-012, NFR-002]
related_user_stories: [US-011, US-012, US-022]
related_brs: []
related_adrs: []
owner: herodotus
---

# UC-006: Inspect Traceability Metadata

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Canonical use case captured from approved user stories | herodotus |

## Summary
Host Application inspects traceability metadata attached to ORION outputs.

## Context / Scope
This use case covers metadata inspection only. It does not change generated content or export format.

## Preconditions
- ORION is initialized.
- A traceable output exists.
- The host application can request metadata from the current ORION state.

## Postconditions
- ORION returns traceability metadata that the host application can inspect or verify.
- Missing metadata results in a controlled ORION-specific exception or empty traceable response when allowed by contract.

## Main Flow
| Step | Actor | Action | Business Rules |
|---|---|---|---|
| 1 | Host Application | Requests traceability metadata from ORION. | None |
| 2 | ORION | Locates the metadata for the current semantic output. | None |
| 3 | Host Application | Chooses whether to inspect ontology-element or triple-level traceability. | None |
| 4 | ORION | Returns the requested traceability metadata. | None |

## Alternative Flows
### AF-1: Ontology-element traceability
**Trigger**: Host Application requests ontology-element metadata.
1. ORION returns ontology-element traceability data.
2. Resume at Main Flow step 4.

### AF-2: Triple-level traceability
**Trigger**: Host Application requests triple-level metadata.
1. ORION returns triple traceability data.
2. Resume at Main Flow step 4.

## Exception Flows
### E1: Missing traceability metadata
**Trigger**: No traceability metadata exists for the current output.
1. ORION rejects the request or returns no metadata according to contract.
2. If rejected, ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

### E2: Corrupt metadata state
**Trigger**: Traceability data cannot be read or verified.
1. ORION stops inspection.
2. ORION raises a controlled ORION-specific exception. [FUN-013]
3. Use case ends.

## Business Rules
None; no BR docs exist for this flow.

## Technical Notes
- Traceability must be inspectable and verifiable by the host application.
- Keep metadata consistent with deterministic outputs.
- Use ORION-specific exceptions for traceability failures. [FUN-013]

## Traceability
- Related model: UCM-001
- Related reqs: FUN-011, FUN-012, NFR-002
- Related user stories: US-011, US-012, US-022
- Related actor: ACT-001
- Related BRs: none

## Open questions
None.

## Cross-References
- UCM: UCM-001
- ACT: ACT-001
- Requirements: FUN-011, FUN-012, NFR-002
- User stories: US-011, US-012, US-022
