---
id: NFR-009
type: NFR
title: Domain Plugin Traceability
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Every claim emitted, changed, or rejected by a domain plugin must include rule, plugin, and source-evidence provenance.
tags: [traceability, plugins, provenance, semantic-claims]
domain: orion
capability: domain-rule-plugins
actors: [Host Application]
systems: [ORION]
source: stakeholder-request
related_ucs: [UC-008]
related_reqs: [FUN-017, FUN-018, NFR-002]
related_user_stories: [US-030, US-031]
related_brs: []
related_adrs: [ADR-001]
owner: herodotus
---

# NFR-009: Domain Plugin Traceability

## Summary

Every claim emitted, changed, or rejected by a domain plugin must include rule, plugin, and source-evidence provenance.

## Acceptance Criteria

- AC-1: Plugin-derived claims include `extracted_by` or equivalent rule ID.
- AC-2: Plugin-derived claims include plugin/rule-pack identity.
- AC-3: Plugin-derived claims preserve source sentence or evidence references.
- AC-4: Rejected claims record rejection reason and responsible rule.

## Traceability

- Related UC: UC-008
- Related ADR: ADR-001
