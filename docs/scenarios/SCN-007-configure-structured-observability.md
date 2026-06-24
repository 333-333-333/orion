---
id: SCN-007
type: SCN
title: Configure Structured Observability
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host Application configures structured logging and optional JSONL persistence for ORION events.
tags: [scenario, observability, logging]
domain: orion
capability: logging-observability
actors: [Host Application]
systems: [ORION]
source: docs/use-cases/UC-007-configure-structured-observability.md
change_ref: CHG-SCN-TRACEABILITY-COMPLETE
related_ucs: [UC-007]
related_reqs: [FUN-014, FUN-015, FUN-016, CON-009, CON-010, CON-011, NFR-006, NFR-007, NFR-008]
related_user_stories: [US-027, US-028]
related_brs: []
related_adrs: []
owner: herodotus
---

# SCN-007: Configure Structured Observability

## Summary

Host Application configures structured logging and optional JSONL persistence for ORION events.

## Preconditions

- ORION is initialized or about to be initialized with a Python dict config.
- Host Application chooses no-op, memory, or JSONL logging behavior.

## Trigger

Host Application supplies logging configuration to ORION.

## Scenario Steps

| Step | Actor | Action | References |
|---|---|---|---|
| 1 | Host Application | Configures or omits a log sink. | FUN-015, CON-010, US-027 |
| 2 | ORION | Emits structured events when a sink is configured. | FUN-014, NFR-006, NFR-008 |
| 3 | ORION | Avoids raw input text and sensitive full content in events. | NFR-007 |
| 4 | ORION | Avoids global/root logging mutation. | CON-009 |
| 5 | ORION | Persists JSONL events only when explicitly configured. | FUN-016, CON-011, US-028 |

## Expected Result

ORION observability is opt-in, structured, deterministic, privacy-safe, and persistence-capable only by explicit configuration.

## User Stories

- US-027 — Configure Structured Logging
- US-028 — Persist Structured Logs
