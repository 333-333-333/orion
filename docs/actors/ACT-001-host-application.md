---
id: ACT-001
type: ACT
title: Host Application
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: External system or application that imports and uses ORION in-process as a library.
tags: [actor, host-application, library-only, in-process, boundary]
domain: orion
capability: host-integration
actors: [Host Application]
systems: [ORION]
source: docs/user-stories
change_ref: CHG-ACT-FROM-US
related_ucs: [UC-001, UC-002, UC-003, UC-004, UC-005, UC-006]
related_reqs: [FUN-001, FUN-002, FUN-003, FUN-004, FUN-005, FUN-006, FUN-007, FUN-008, FUN-009, FUN-010, FUN-011, FUN-012, FUN-013, CON-001, CON-002, CON-003, CON-004, CON-005, CON-006, CON-007, CON-008, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005]
related_user_stories: [US-001, US-002, US-003, US-004, US-005, US-006, US-007, US-008, US-009, US-010, US-011, US-012, US-014, US-015, US-016, US-017, US-018, US-019, US-020, US-021, US-022, US-023, US-024, US-025, US-026]
related_brs: []
related_adrs: []
owner: herodotus
---

# ACT-001: Host Application

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Canonical actor captured from approved ORION user stories | herodotus |

## Summary
Host Application is the external application that imports ORION and uses it in-process as a library.

## Actor profile
- Type: external software system/application
- Role: boundary actor that owns the runtime and calls ORION from inside its own process
- Identity: singular canonical actor for all in-process ORION interactions
- Alias: host app, host application

## Boundary
- In scope: importing ORION, configuring it, sending text/file input, requesting semantic generation, exporting results, and inspecting traceability metadata.
- Out of scope: CLI startup, REST/HTTP service usage, and any wording that implies ORION is a separate service.
- Constraint: ORION stays library-only and runs inside the host process.

## Relationships
- Interacts with ORION only through in-process library calls.
- Drives UC-001 through UC-006.
- Relies on the approved ORION requirements set for configuration, input processing, deterministic output, export, and traceability.
- No BR or ADR artifacts are linked for this actor yet.

## Traceability
- Source: docs/user-stories
- Related UCs: UC-001, UC-002, UC-003, UC-004, UC-005, UC-006
- Related reqs: FUN-001 through FUN-013, CON-001 through CON-008, NFR-001 through NFR-005
- Related user stories: US-001 through US-012, US-014 through US-026

## Open questions
None.
