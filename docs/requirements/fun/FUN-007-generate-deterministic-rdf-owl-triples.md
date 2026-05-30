---
id: FUN-007
type: FUN
title: Generate deterministic RDF/OWL triples
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: The library generates deterministic RDF/OWL-oriented triples from processed text.
tags: [rdf, owl, triples, deterministic]
domain: orion
capability: triple-generation
actors: [Host Application]
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [NFR-001, NFR-003, NFR-005]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# FUN-007: Generate deterministic RDF/OWL triples

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
The library generates deterministic RDF/OWL-oriented triples from processed text.

## Context / Scope
ORION shall emit deterministic RDF/OWL-oriented triples as part of the deterministic output set.

## Description
ORION shall emit deterministic RDF/OWL-oriented triples as part of the deterministic output set.

## Acceptance Criteria
- The same input and config yield the same deterministic triple set across repeated runs.
- Triples are represented in a semantically valid RDF/OWL-oriented structure.
- Triple generation does not depend on any non-deterministic inference path.

## Dependencies
- Requires FUN-006 and either FUN-003 or FUN-004.

## Business Rules
- Deterministic triples must be stable across repeated runs.

## Validation Method
- Comparison tests verify equality of generated triples over repeated executions.

## Technical Notes
Triple serialization must remain compatible with semantic web tooling.

## Traceability
- Upstream source: README.md. Downstream: NFR-001, NFR-003, NFR-005.

## Open questions
None.
