---
id: US-031
type: US
title: Audit Plugin-Derived Claims
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host application can inspect which plugin rule emitted, changed, or rejected a claim.
tags: [user-story, auditability, provenance, plugins]
domain: orion
capability: domain-rule-plugins
actors:
  - Host Application
systems:
  - ORION
source: stakeholder-request
change_ref: CHG-DOMAIN-RULE-PLUGINS
related_ucs:
  - UC-008
related_scenarios: [SCN-008]
related_reqs:
  - FUN-018
  - NFR-009
related_user_stories: []
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# US-031: Audit Plugin-Derived Claims

## Narrative

As a host application, I want plugin-derived claims to identify their rule and evidence so that domain-specific output remains auditable.

## Acceptance Criteria

- AC-1 (NFR-009): Plugin-derived claims include rule or plugin identity.
- AC-2 (NFR-009): Plugin-derived claims preserve source evidence references.
- AC-3 (FUN-018): Rejected claims include rejection reason and responsible rule.

## Traceability

- Related scenario: SCN-008
- Related requirements: FUN-018, NFR-009
- Related ADR: ADR-001
