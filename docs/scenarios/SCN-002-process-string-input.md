---
id: SCN-002
type: SCN
title: Process Text from a String
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host Application submits an in-memory string and ORION processes it without file or service bootstrap.
tags: [scenario, processing, string-input, library-only]
domain: orion
capability: input-processing
actors: [Host Application]
systems: [ORION]
source: docs/use-cases/UC-002-process-string-input.md
change_ref: CHG-SCN-TRACEABILITY-COMPLETE
related_ucs: [UC-002]
related_reqs: [FUN-003, FUN-010, FUN-013, NFR-001, NFR-002, NFR-005]
related_user_stories: [US-003, US-013]
related_brs: []
related_adrs: []
owner: herodotus
---

# SCN-002: Process Text from a String

## Summary

Host Application submits an in-memory string and ORION returns a Python object containing processed semantic output.

## Preconditions

- ORION is initialized in-process.
- Host Application has a non-empty text string.

## Trigger

Host Application calls the processing API with a string input.

## Scenario Steps

| Step | Actor | Action | References |
|---|---|---|---|
| 1 | Host Application | Calls ORION with string input. | UC-002, US-003, FUN-003 |
| 2 | ORION | Validates the input shape. | FUN-013, NFR-005 |
| 3 | ORION | Processes the text through the pipeline. | NFR-001, NFR-002 |
| 4 | ORION | Returns a Python result object. | FUN-010 |

## Expected Result

ORION processes the string input deterministically and returns a structured Python object.

## User Stories

- US-003 — Process Text from a String
- US-013 — Raise ORION-Specific Exceptions
