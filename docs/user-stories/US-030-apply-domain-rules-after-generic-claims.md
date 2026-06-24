---
id: US-030
type: US
title: Apply Domain Rules After Generic Claims
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host application runs domain rules after ORION has produced generic semantic claims.
tags: [user-story, semantic-claims, plugins, domain-specific]
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
  - CON-012
  - NFR-010
related_user_stories: []
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# US-030: Apply Domain Rules After Generic Claims

## Narrative

As a host application, I want domain rules to run after generic semantic claims exist so that domain logic enriches ORION output without replacing the core pipeline.

## Acceptance Criteria

- AC-1 (FUN-018): Domain rules receive generic semantic claims and evidence as input.
- AC-2 (CON-012): Domain rules do not become part of the default core behavior.
- AC-3 (NFR-010): Domain rule execution order is deterministic.

## Traceability

- Related scenario: SCN-008
- Related requirements: FUN-018, CON-012, NFR-010
- Related ADR: ADR-001
