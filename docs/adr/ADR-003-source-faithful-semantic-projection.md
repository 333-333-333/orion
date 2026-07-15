---
id: ADR-003
type: adr
title: Preserve source semantics before RDF projection
status: proposed
date: 2026-07-10
deciders: [herodotus]
related_requirements: [FUN-006, FUN-007, FUN-009, NFR-002, NFR-003, NFR-005]
related_use_cases: [UC-004]
related_user_stories: [US-006, US-007, US-009, US-023, US-025]
affected_modules: [MOD-semantic-claims, MOD-semantic-quality]
supersedes: []
superseded_by: []
---

# ADR-003 — Preserve Source Semantics Before RDF Projection

## Status

Proposed

## Context

Structural agreement between semantic claims, triples, graph artifacts, and RDF does not prove that the output represents the source text. Manual comparison exposed missing modal relations, malformed predicates, clause-sized resources, incorrect coordination, and lost passive roles even when every downstream artifact was internally consistent.

The core must remain domain-agnostic. Information-security and pizza fixtures are evidence corpora, not sources of domain vocabulary for production rules.

## Decision Drivers

- Treat source text as the semantic oracle.
- Preserve subject, predicate, object, voice, modality, coordination, and provenance.
- Avoid turning unparsed clauses into ontology resources.
- Keep rules deterministic and domain-agnostic.
- Reject unsupported interpretations explicitly instead of silently projecting them.

## Options Considered

### Option A: Accept downstream structural consistency

Pros:
- No extraction changes.
- Stable current artifacts.

Cons:
- Reproduces semantic errors consistently.
- Cannot support trustworthy querying or reasoning.

### Option B: Add vocabulary-specific corrections

Pros:
- Quickly fixes selected fixtures.

Cons:
- Contaminates core with domain assumptions.
- Does not generalize to other texts.
- Conflicts with ADR-001.

### Option C: Add source-faithful generic English rules and explicit rejection

Pros:
- Improves multiple domains with the same rules.
- Keeps provenance and deterministic behavior.
- Makes unsupported structures observable.

Cons:
- Regex-based extraction remains incomplete.
- Broader parsing rules require source-based regression contracts.

## Decision

ORION should apply generic English construction rules before fallback nominalization. Before acceptance, the implementation needs parsing boundaries that do not regress existing compound-entity and coordination behavior. Core rules must:

1. recognize active and passive modality;
2. decompose coordinated actions and unambiguous coordinated subjects;
3. parse represented/reported SVO clauses with base, inflected, and past-tense verbs;
4. preserve modality in predicate metadata/naming;
5. prefer explicit rejection over clause-sized resources when roles cannot be recovered.

The normative rule catalog is `docs/semantic-rules/CORE-SEMANTIC-RULES.md`.

## Consequences

Positive:
- Modal, passive, coordinated, and reported relations would gain source-faithful RDF projections.
- Rules remain independent of InfoSec vocabulary.
- Source sentences become executable semantic contracts.

Negative:
- Existing artifacts change when prior output encoded malformed semantics.
- Ambiguous coordination still requires conservative handling.
- A regex core cannot fully replace dependency or semantic-role parsing.

Neutral / follow-up:
- Clause-resource rejection and class-versus-individual modeling remain explicit follow-up work.
- Semantic quality must report unsupported constructions rather than score them as perfect.

## Traceability

Related artifacts:
- NFR-002
- NFR-003
- NFR-005
- FUN-006
- FUN-007
- FUN-009
- UC-004
- SCN-004
- MOD-semantic-claims
- MOD-semantic-quality
- ADR-001
- `tests/smoke/test_semantic_claim_acceptance_smoke.py`

## Review Notes

Revisit when dependency-parse or semantic-role evidence can replace regex boundary detection without sacrificing determinism.
