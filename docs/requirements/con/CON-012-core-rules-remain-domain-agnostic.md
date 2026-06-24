---
id: CON-012
type: CON
title: Core Rules Remain Domain-Agnostic
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: ORION core rules must remain domain-agnostic; domain-specific behavior belongs only in explicitly configured plugins or rule packs.
tags: [constraint, domain-agnostic, rule-packs, plugins]
domain: orion
capability: domain-rule-plugins
actors: [Host Application]
systems: [ORION]
source: stakeholder-request
related_ucs: [UC-008]
related_reqs: [FUN-017, FUN-018, NFR-010]
related_user_stories: [US-029, US-030]
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# CON-012: Core Rules Remain Domain-Agnostic

## Summary

ORION core rules must remain domain-agnostic; domain-specific behavior belongs only in explicitly configured plugins or rule packs.

## Acceptance Criteria

- AC-1: A clean ORION configuration does not activate domain-specific rules.
- AC-2: Core rules do not hard-code infosec, library, medical, finance, or other domain vocabularies.
- AC-3: Domain-specific fixtures do not create default ontology vocabulary for unrelated inputs.

## Traceability

- Related UC: UC-008
- Related ADR: ADR-001
