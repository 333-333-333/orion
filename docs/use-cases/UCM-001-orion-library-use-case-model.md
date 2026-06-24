---
id: UCM-001
type: use-case-model
title: ORION Library Use Case Model
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
scope: orion-library
actors: [ACT-001]
use_cases: [UC-001, UC-002, UC-003, UC-004, UC-005, UC-006, UC-007, UC-008]
requirements: [FUN-001, FUN-002, FUN-003, FUN-004, FUN-005, FUN-006, FUN-007, FUN-008, FUN-009, FUN-010, FUN-011, FUN-012, FUN-013, FUN-014, FUN-015, FUN-016, FUN-017, FUN-018, CON-001, CON-002, CON-003, CON-004, CON-005, CON-006, CON-007, CON-008, CON-009, CON-010, CON-011, CON-012, CON-013, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009, NFR-010]
owner: herodotus
---

# UCM-001 — ORION Library Use Case Model

## Scope

ORION as an embeddable Python library used by a host application to process text and inspect deterministic semantic outputs.

## Actors

- ACT-001 — Host Application

## Use Cases

- UC-001 — Initialize ORION Instance
- UC-002 — Process String Input
- UC-003 — Process TXT File Input
- UC-004 — Generate Deterministic Semantic Output
- UC-005 — Export Semantic Output
- UC-006 — Inspect Traceability Metadata
- UC-007 — Configure Structured Observability
- UC-008 — Configure Domain Rule Plugins

## Invariants

- ORION stays library-only and in-process.
- ORION does not expose a CLI, REST API, or HTTP service contract.
- Deterministic outputs and traceability metadata remain verifiable.
- Logging is opt-in and must not expose raw input text by default.
- Domain-specific rules are opt-in plugins and never part of the default core behavior.
