---
id: UC-007
type: UC
title: Configure Structured Observability
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host Application configures structured ORION log events and optional JSONL persistence without global logging side effects.
tags: [orion, observability, logging, host-application]
domain: orion
capability: logging-observability
actors: [Host Application]
systems: [ORION]
source: docs/user-stories
change_ref: CHG-UC-OBSERVABILITY
primary_actor: ACT-001
secondary_actors: []
priority: High
related_ucm: [UCM-001]
related_acts: [ACT-001]
related_reqs: [FUN-014, FUN-015, FUN-016, CON-009, CON-010, CON-011, NFR-006, NFR-007, NFR-008]
related_user_stories: [US-027, US-028]
related_brs: []
related_adrs: []
owner: herodotus
---

# UC-007: Configure Structured Observability

## Summary

Host Application configures structured ORION log events and optional JSONL persistence without global logging side effects.

## Context / Scope

This use case covers observability configuration only. Logging is disabled/no-op by default unless the host application supplies a sink or persistence configuration.

## Preconditions

- Host Application can instantiate ORION with a Python dict config.
- Host Application has selected the desired logging sink or no-op default.

## Postconditions

- ORION emits structured, deterministic, privacy-safe events when configured.
- ORION can persist JSONL events only when explicitly configured.
- ORION does not mutate Python global/root logging configuration.

## Main Flow

| Step | Actor | Action | Business Rules |
|---|---|---|---|
| 1 | Host Application | Provides logging configuration in the ORION config dict. | None |
| 2 | ORION | Validates the sink or persistence settings. | None |
| 3 | ORION | Uses no-op logging when no sink is configured. | None |
| 4 | ORION | Emits structured safe events during initialization and processing when a sink is configured. | None |
| 5 | ORION | Persists JSONL events only when explicitly configured. | None |

## Alternative Flows

### AF-1: Memory sink
1. Host Application provides an in-memory sink.
2. ORION appends structured events in deterministic order.

### AF-2: JSONL persistence
1. Host Application provides a JSONL file sink.
2. ORION writes one structured event per line.

## Exception Flows

### E1: Invalid sink
1. ORION rejects the logging configuration.
2. ORION raises a controlled ORION-specific exception. [FUN-013]

## Traceability

- Related model: UCM-001
- Related reqs: FUN-014, FUN-015, FUN-016, CON-009, CON-010, CON-011, NFR-006, NFR-007, NFR-008
- Related user stories: US-027, US-028
- Related actor: ACT-001

## Open questions

None.
