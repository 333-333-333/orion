---
id: FUN-018
type: FUN
title: Execute Domain-Specific Rules as Plugins
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: ORION can execute domain-specific user rules as opt-in plugins after the core semantic pipeline produces generic claims.
tags: [rule-engine, plugins, semantic-claims, domain-specific]
domain: orion
capability: domain-rule-plugins
actors: [Host Application]
systems: [ORION]
source: stakeholder-request
related_ucs: [UC-008]
related_reqs: [FUN-017, CON-012, CON-013, NFR-009, NFR-010]
related_user_stories: [US-030, US-031]
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# FUN-018: Execute Domain-Specific Rules as Plugins

## Summary

ORION can execute domain-specific user rules as opt-in plugins after the core semantic pipeline produces generic claims.

## Description

Domain plugins may enrich, normalize, reject, or validate semantic claims, but they shall not silently replace core extraction behavior or contaminate unrelated domains.

## Acceptance Criteria

- AC-1: Domain rules run only when explicitly enabled.
- AC-2: Domain rules receive generic semantic claims and source evidence as input.
- AC-3: Domain rules can emit accepted and rejected claims with provenance.
- AC-4: Domain rules cannot remove required core provenance fields.

## Traceability

- Related UC: UC-008
- Related user stories: US-030, US-031
- Related ADR: ADR-001
