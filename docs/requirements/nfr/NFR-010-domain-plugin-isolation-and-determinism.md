---
id: NFR-010
type: NFR
title: Domain Plugin Isolation and Determinism
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Domain plugins must be isolated from the core default behavior and deterministic for stable comparison.
tags: [determinism, isolation, plugins, rule-packs]
domain: orion
capability: domain-rule-plugins
actors: [Host Application]
systems: [ORION]
source: stakeholder-request
related_ucs: [UC-008]
related_reqs: [FUN-017, FUN-018, CON-012, CON-013, NFR-001, NFR-005]
related_user_stories: [US-029, US-030]
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# NFR-010: Domain Plugin Isolation and Determinism

## Summary

Domain plugins must be isolated from the core default behavior and deterministic for stable comparison.

## Acceptance Criteria

- AC-1: A domain plugin affects only configured stages and configured executions.
- AC-2: Plugin execution order is deterministic.
- AC-3: Plugin output is stable for the same input, configuration, and rule-pack version.
- AC-4: Domain-specific vocabulary does not leak into outputs when the plugin is disabled.

## Traceability

- Related UC: UC-008
- Related ADR: ADR-001
