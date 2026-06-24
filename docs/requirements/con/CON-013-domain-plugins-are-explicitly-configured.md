---
id: CON-013
type: CON
title: Domain Plugins Are Explicitly Configured
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Domain plugins must be opt-in through Python dict configuration and must not be auto-loaded by text-domain guessing.
tags: [constraint, opt-in, configuration, plugins]
domain: orion
capability: domain-rule-plugins
actors: [Host Application]
systems: [ORION]
source: stakeholder-request
related_ucs: [UC-008]
related_reqs: [FUN-017, FUN-018, CON-007, CON-012]
related_user_stories: [US-029]
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# CON-013: Domain Plugins Are Explicitly Configured

## Summary

Domain plugins must be opt-in through Python dict configuration and must not be auto-loaded by text-domain guessing.

## Acceptance Criteria

- AC-1: The primary configuration shape remains a Python dict.
- AC-2: ORION does not infer a domain and load plugins implicitly.
- AC-3: Enabled plugin identifiers, paths, and modes are auditable from configuration.

## Traceability

- Related UC: UC-008
- Related ADR: ADR-001
