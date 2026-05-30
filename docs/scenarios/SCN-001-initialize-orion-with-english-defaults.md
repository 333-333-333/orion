---
id: SCN-001
type: SCN
title: Initialize ORION with English Defaults
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Host Application initializes ORION in-process with English defaults and optional overrides.
tags: [scenario, initialization, english-default, library-only]
domain: orion
capability: initialization
actors: [Host Application]
systems: [ORION]
source: docs/use-cases/UC-001-initialize-orion-instance.md
change_ref: CHG-SCN-FROM-UC
related_ucs: [UC-001]
related_reqs: [FUN-001, FUN-002, FUN-005, CON-001, CON-002, CON-007, CON-008, NFR-004]
related_user_stories: [US-001, US-002, US-005, US-014, US-015, US-017, US-020, US-021]
related_brs: []
related_adrs: []
owner: herodotus
---

# SCN-001: Initialize ORION with English Defaults

## Version history
- v0 (2026-05-29): Initial draft from UC-001 trace.

## Summary
Host Application imports ORION and initializes it as a library-only, in-process instance using English by default.

## Context / Scope
This scenario covers initialization only. It stays inside the in-process library boundary and does not cover CLI, REST, HTTP, or service startup.

## Preconditions
- Host Application can import ORION.
- Host Application can pass a Python dict config.
- No language is provided in the config for the default path.

## Trigger
Host Application calls ORION initialization with a config dict.

## Scenario Steps
| Step | Actor | Action | References |
|---|---|---|---|
| 1 | Host Application | Imports ORION. | ACT-001, UC-001 |
| 2 | Host Application | Provides a Python dict config without language. | FUN-001, CON-001 |
| 3 | ORION | Validates library-only boundary and configuration format. | CON-002, CON-007, CON-008 |
| 4 | ORION | Applies default language English. | FUN-002, US-001, US-002 |
| 5 | ORION | Applies default spaCy model size lg. | FUN-005, NFR-004 |
| 6 | ORION | Returns initialized in-process instance. | UC-001, US-005 |

## Expected Result
ORION returns an initialized in-process instance with English as the default language and spaCy model size lg when no overrides are provided.

## Alternative Paths
- Explicit language configured Spanish: ORION accepts the config language value Spanish and initializes with that language instead of English.
- Explicit model size override: ORION accepts a supported model size override and initializes with that configured model size instead of lg.

## Exception Paths
- Invalid config -> ORION-specific exception.
- Unsupported model setup -> ORION-specific exception.
- Attempted CLI/REST/HTTP service startup -> out of contract.

## Acceptance Checks
- ORION initializes successfully from a Python dict config.
- ORION defaults language to English when language is omitted.
- ORION defaults spaCy model size to lg when model size is omitted.
- ORION accepts explicit Spanish language configuration.
- ORION accepts supported model size overrides.
- ORION rejects invalid config with an ORION-specific exception.
- ORION rejects unsupported model setups with an ORION-specific exception.
- ORION stays library-only and in-process.

## Traceability
- ACT-001
- UC-001
- US-001
- US-002
- US-005
- US-014
- US-015
- US-017
- US-020
- US-021
- FUN-001
- FUN-002
- FUN-005
- CON-001
- CON-002
- CON-007
- CON-008
- NFR-004

## Open questions
None.
