---
id: NFR-003
type: NFR
title: Semantic web interoperability
status: draft
version: 0
created_at: 2026-05-29
updated_at: 2026-05-29
summary: Outputs must remain interoperable with RDF/OWL tooling and standard serializations.
tags: [rdf, owl, interoperability, serializations]
domain: orion
capability: interop
actors: []
systems: [ORION]
source: README.md
change_ref: CHG-README-LIBRARY-FIRST
related_ucs: []
related_reqs: [FUN-007, FUN-008, CON-003]
related_user_stories: []
related_brs: []
related_adrs: []
owner: herodotus
---

# NFR-003: Semantic web interoperability

## Version history
| Version | Date | Change | Reason | Author |
|---|---|---|---|---|
| 0 | 2026-05-29 | Added initial draft | Initial requirement capture from README.md | herodotus |

## Summary
Outputs must remain interoperable with RDF/OWL tooling and standard serializations.

## Context / Scope
ORION shall emit semantic-web-oriented outputs that can be consumed by standard RDF/OWL tooling.

## Description
ORION shall emit semantic-web-oriented outputs that can be consumed by standard RDF/OWL tooling.

## Acceptance Criteria
- Supported serializations include ttl, rdfxml, jsonld, and nt.
- Generated triples are structurally valid for the selected serialization format.
- Pinned dependencies preserve output compatibility across runs.

## Dependencies
- Requires serialization support and deterministic triple generation.

## Business Rules
- Semantic web outputs must use standard formats.

## Validation Method
- Format-validation tests load the outputs into compatible RDF tooling or parsers.

## Technical Notes
Do not emit custom-only serialization formats as the primary output.

## Traceability
- Upstream source: README.md. Downstream: FUN-007, FUN-008, CON-003.

## Open questions
None.
