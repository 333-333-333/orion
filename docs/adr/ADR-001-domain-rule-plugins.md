---
id: ADR-001
type: adr
title: Support Domain Rules as Opt-In Plugins
status: proposed
date: 2026-06-23
deciders: [herodotus]
related_requirements: [FUN-017, FUN-018, CON-012, CON-013, NFR-009, NFR-010]
related_use_cases: [UC-008]
related_user_stories: [US-029, US-030, US-031]
affected_modules: [MOD-rule-engine, MOD-semantic-claims]
supersedes: []
superseded_by: []
---

# ADR-001 — Support Domain Rules as Opt-In Plugins

## Status

Proposed

## Context

ORION's core rule behavior must remain domain-agnostic. At the same time, host applications may need user-provided, domain-specific rules for vocabularies such as information security, healthcare, finance, or internal enterprise taxonomies.

The main risk is contaminating generic output with domain assumptions. A second risk is losing traceability when plugin logic enriches or rejects claims.

## Decision Drivers

- Keep ORION's default behavior domain-agnostic.
- Allow users to add domain-specific behavior without modifying core rules.
- Preserve deterministic output and stable comparison surfaces.
- Require provenance for every plugin-derived accepted or rejected claim.
- Keep configuration explicit and auditable.

## Options Considered

### Option A: Hard-code common domain rules in core

Pros:
- Simple runtime path.
- No plugin loading mechanism needed.

Cons:
- Violates the domain-agnostic core constraint.
- Risks domain vocabulary leaking into unrelated outputs.
- Makes user-specific domains hard to support.

### Option B: Auto-detect domain and auto-load rules

Pros:
- Convenient for demos.
- Less configuration for host applications.

Cons:
- Non-deterministic and difficult to audit.
- Unexpected behavior when domain detection is wrong.
- Violates explicit opt-in configuration.

### Option C: Opt-in plugin/rule-pack layer after generic semantic claims

Pros:
- Preserves generic core behavior.
- Keeps domain behavior isolated and configurable.
- Allows provenance on every plugin-derived claim.
- Supports declarative rule packs first and code plugins later.

Cons:
- Requires a plugin/rule-pack contract.
- Requires validation and deterministic execution order.

## Decision

We will support domain-specific rules as explicitly configured plugins or rule packs that run after ORION produces generic semantic claims. The core pipeline remains domain-agnostic by default.

Plugins may enrich, normalize, validate, or reject claims, but must preserve source evidence and record rule/plugin provenance. ORION must not infer domains and load plugins implicitly.

## Consequences

Positive:
- Domain-specific behavior becomes possible without contaminating core rules.
- Users can audit which rule pack produced each domain claim.
- Generic-domain isolation remains testable.

Negative:
- Plugin configuration and validation add implementation complexity.
- Domain plugin authors need a stable rule-pack contract.

Neutral / follow-up:
- Start with declarative rule packs for simple extraction/normalization/validation.
- Add Python plugin hooks only when declarative rules are insufficient.
- Future tests should verify disabled-plugin isolation, enabled-plugin provenance, invalid config rejection, and deterministic plugin order.

## Traceability

Related artifacts:
- FUN-017
- FUN-018
- CON-012
- CON-013
- NFR-009
- NFR-010
- UC-008
- SCN-008
- US-029
- US-030
- US-031
- MOD-rule-engine
- MOD-semantic-claims

## Review Notes

Revisit if plugin execution needs sandboxing, third-party package loading, or cross-language rule-pack support.
