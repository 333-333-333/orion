---
id: SCN-005
type: SCN
title: Export Semantic Output
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host Application obtains ORION semantic output as Python objects and serialization strings.
tags: [scenario, export, serialization]
domain: orion
capability: output-export
actors: [Host Application]
systems: [ORION]
source: docs/use-cases/UC-005-export-semantic-output.md
change_ref: CHG-SCN-TRACEABILITY-COMPLETE
related_ucs: [UC-005]
related_reqs: [FUN-008, FUN-010, NFR-003, NFR-004, NFR-005]
related_user_stories: [US-008, US-010]
related_brs: []
related_adrs: []
owner: herodotus
---

# SCN-005: Export Semantic Output

## Summary

Host Application obtains processed semantic output as Python objects and serialization strings.

## Preconditions

- ORION has generated semantic output.
- Host Application requests an available output representation.

## Trigger

Host Application reads the ORION result object or serialization fields.

## Scenario Steps

| Step | Actor | Action | References |
|---|---|---|---|
| 1 | Host Application | Requests semantic output from ORION. | UC-005 |
| 2 | ORION | Returns Python objects for host inspection. | FUN-010, US-010 |
| 3 | ORION | Exposes serialization strings. | FUN-008, US-008 |
| 4 | ORION | Keeps exported formats interoperable and stable. | NFR-003, NFR-005 |

## Expected Result

ORION returns semantic output in host-consumable Python objects and supported serialization strings.

## User Stories

- US-008 — Export Serializations as Strings
- US-010 — Return Results as Python Objects
