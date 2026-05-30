---
id: FUN-008
type: FUN
title: Export serializations as strings
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library exports supported RDF serializations as string values.
tags: [serialization, strings, rdf]
domain: orion
capability: serialization
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [NFR-003, NFR-004]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-008: Export serializations as strings

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library exports supported RDF serializations as string values.

## Context / Scope
ORION shall provide serialized output strings for the supported formats: Turtle, RDF/XML, JSON-LD, and N-Triples.

## Description
ORION shall provide serialized output strings for the supported formats: Turtle, RDF/XML, JSON-LD, and N-Triples.

## Acceptance Criteria
- The result object exposes string serializations for ttl, rdfxml, jsonld, and nt.
- Each serialization value is a string, not a file write or stream-only object.
- All supported formats are available from the same processing result.

## Dependencies
- Requires FUN-007.

## Business Rules
- Supported serializations are ttl, rdfxml, jsonld, and nt.

## Validation Method
- Unit tests assert all four string outputs exist and are strings.

## Technical Notes
Do not couple serialization to file output.

## Traceability
- Upstream source: README.md. Downstream: NFR-003, NFR-004.

## Open questions
None.
