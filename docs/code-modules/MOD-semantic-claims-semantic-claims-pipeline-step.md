---
id: MOD-semantic-claims
type: code-module
title: Semantic Claims Pipeline Step
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Canonical and semantic claim extraction, generic claim normalization, and hook point for domain rule behavior.
paths:
  - src/pipeline/step_009_canonical_claims/**
implements:
  - US-006
  - US-007
  - US-009
  - US-011
  - US-012
  - US-022
  - US-029
  - US-030
  - US-031
related_requirements:
  - FUN-006
  - FUN-007
  - FUN-009
  - FUN-011
  - FUN-012
  - FUN-017
  - FUN-018
  - CON-012
  - CON-013
  - NFR-002
  - NFR-009
  - NFR-010
related_adrs:
  - ADR-001
owner: herodotus
---

# MOD-semantic-claims — Semantic Claims Pipeline Step

## Summary

Canonical and semantic claim extraction, generic claim normalization, and hook point for domain rule behavior.

## Paths

- `src/pipeline/step_009_canonical_claims/**`

## Implements

- US-006
- US-007
- US-009
- US-011
- US-012
- US-022
- US-029
- US-030
- US-031

## Related Requirements

- FUN-006
- FUN-007
- FUN-009
- FUN-011
- FUN-012
- FUN-017
- FUN-018
- CON-012
- CON-013
- NFR-002
- NFR-009
- NFR-010

## Related ADRs

- ADR-001

## Traceability Notes

This artifact provides Code -> Knowledge traceability for the listed source paths. Tests are intentionally not represented as persisted test-result artifacts; validation evidence should come from executable tests and CI/run output.
