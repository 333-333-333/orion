# Core Semantic Projection Rules

These rules are normative for ORION core. They are domain-agnostic; fixtures supply evidence, never production vocabulary.

## Status legend

- **ENFORCED**: implemented and covered by source-based smoke contracts.
- **PARTIAL**: implemented for deterministic unambiguous forms; ambiguous forms remain unsupported.
- **PLANNED**: required but not completed by the current change.

## CORE-SEM-001 — Source text is the semantic oracle

**Status:** ENFORCED

Downstream agreement does not establish correctness. Accepted claims must preserve a defensible reading of their source evidence. Unsupported readings must be rejected with a reason.

## CORE-SEM-002 — Preserve required SPO roles

**Status:** ENFORCED

Every accepted relation has non-empty subject, predicate, and object. Missing roles produce `rejected_claims`, never visible RDF.

## CORE-SEM-003 — Preserve modality

**Status:** PARTIAL — dependency-backed active/passive forms are enforced; unsupported parses remain explicit gaps

Modal words (`may`, `must`, `can`, `could`, `should`, `would`, `might`) qualify the action and must not become entities. Examples:

- `X may detect Y` → `X mayDetect Y`
- `X can be affected by Y` → `X canBeAffectedBy Y`
- `X must be stored in Y` → `X mustBeStoredIn Y`

## CORE-SEM-004 — Preserve passive roles

**Status:** PARTIAL

Passive constructions retain the grammatical patient as subject and the agent/context as object unless a later semantic rule explicitly normalizes direction. They must not become `is_a` clause resources.

## CORE-SEM-005 — Decompose coordination conservatively

**Status:** PARTIAL

- `X may detect and block Y` emits both actions with shared subject and object.
- `X and Y support Z` emits one relation per subject only when the plural/base verb makes coordination unambiguous.
- Comma lists are not treated as two-subject coordination by this rule.

## CORE-SEM-006 — Parse represented and reported clauses

**Status:** PARTIAL — finite-verb coverage is restricted and past/base forms need a safer parser

Clauses under `represent that`, `states that`, `reports that`, and equivalent supported reporting forms are decomposed into their own claims. Base verbs and past-tense verbs are accepted; the reporting pronoun is not projected as the domain subject.

## CORE-SEM-007 — Ontology resources must be atomic concepts

**Status:** PARTIAL

Definition parents are cut at generic relative, causal, provenance, and contextual markers. Other fallbacks can still emit clause-sized resources. A resource must not encode a complete clause, modal phrase, temporal statement, or discourse frame.

## CORE-SEM-008 — Discourse context is not a domain entity

**Status:** ENFORCED for recognized generic discourse frames

Prefixes such as `for example`, contextual `inside/outside` frames, `another example`, and `these relationships` do not become part of resource identity or domain facts.

## CORE-SEM-009 — Preserve entity identity across mentions

**Status:** PLANNED

Names and shortened mentions must resolve to one identity when evidence supports it. Pronoun resolution must not replace a person with an event or object phrase.

## CORE-SEM-010 — Distinguish classes from individuals

**Status:** PLANNED

Generic concepts belong in OWL classes. Concrete actors, systems, documents, orders, devices, and named objects in scenarios should be individuals with `rdf:type` where the text supports that distinction.

## Current implementation

Affected core modules:

- `src/pipeline/step_009_canonical_claims/orchestrator.py`
- `src/pipeline/step_009_canonical_claims/rules/dependency_svo.py`
- `src/pipeline/step_012_semantic_quality/orchestrator.py`
- `src/pipeline/step_013_output_generation/rdf_strategy.py`

Source-based verification:

- `tests/smoke/test_semantic_claim_acceptance_smoke.py`

Architecture decision:

- `docs/adr/ADR-003-source-faithful-semantic-projection.md`
