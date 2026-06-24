---
id: UC-008
type: UC
title: Configure Domain Rule Plugins
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Host Application configures optional domain-specific rule packs while ORION preserves domain-agnostic defaults.
tags: [orion, rule-packs, plugins, domain-specific]
domain: orion
capability: domain-rule-plugins
actors: [Host Application]
systems: [ORION]
source: stakeholder-request
change_ref: CHG-DOMAIN-RULE-PLUGINS
primary_actor: ACT-001
secondary_actors: []
priority: High
related_ucm: [UCM-001]
related_acts: [ACT-001]
related_reqs: [FUN-017, FUN-018, CON-012, CON-013, NFR-009, NFR-010]
related_user_stories: [US-029, US-030, US-031]
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# UC-008: Configure Domain Rule Plugins

## Summary

Host Application configures optional domain-specific rule packs while ORION preserves domain-agnostic defaults.

## Context / Scope

This use case covers plugin/rule-pack configuration and execution boundaries. It does not require ORION to ship domain-specific rules by default.

## Preconditions

- ORION is configured through a Python dict.
- A user-provided rule pack or plugin is available when domain-specific behavior is desired.

## Postconditions

- If no plugin is configured, ORION remains domain-agnostic.
- If a plugin is configured, ORION applies it only in the configured stages and records provenance.

## Main Flow

| Step | Actor | Action | Business Rules |
|---|---|---|---|
| 1 | Host Application | Provides plugin or rule-pack configuration. | None |
| 2 | ORION | Validates plugin identity, mode, and target stages. | None |
| 3 | ORION | Runs the core domain-agnostic pipeline. | None |
| 4 | ORION | Runs enabled domain rules against generic semantic claims. | None |
| 5 | ORION | Emits enriched or rejected claims with plugin provenance. | None |

## Alternative Flows

### AF-1: No plugins configured
1. ORION skips domain-specific rule execution.
2. ORION output remains produced only by core rules.

### AF-2: Assist mode
1. ORION applies plugin rules as suggestions or enrichments.
2. ORION preserves original generic claims and marks plugin-derived claims.

### AF-3: Enforce mode
1. ORION applies plugin validation and rejection rules.
2. ORION records rejection reasons and responsible rule IDs.

## Exception Flows

### E1: Invalid plugin configuration
1. ORION rejects the configuration.
2. ORION raises a controlled ORION-specific exception. [FUN-013]

## Traceability

- Related model: UCM-001
- Related reqs: FUN-017, FUN-018, CON-012, CON-013, NFR-009, NFR-010
- Related user stories: US-029, US-030, US-031
- Related ADR: ADR-001

## Open questions

None.
