---
id: MOD-semantic-quality
type: code-module
title: Semantic Quality Pipeline Step
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-07-10
summary: Quality filtering and reporting for noisy concepts, entities, and semantic structures.
paths:
  - src/pipeline/step_012_semantic_quality/**
implements:
  - US-006
  - US-011
  - US-022
  - US-025
related_requirements:
  - FUN-006
  - FUN-011
  - NFR-002
  - NFR-005
related_adrs:
  - ADR-003
owner: herodotus
---

# MOD-semantic-quality — Semantic Quality Pipeline Step

## Summary

Quality filtering and reporting for noisy concepts, entities, and semantic structures.

## Paths

- `src/pipeline/step_012_semantic_quality/**`

## Implements

- US-006
- US-011
- US-022
- US-025

## Related Requirements

- FUN-006
- FUN-011
- NFR-002
- NFR-005

## Related ADRs

- ADR-003

## Traceability Notes

This artifact provides Code -> Knowledge traceability for the listed source paths. Tests are intentionally not represented as persisted test-result artifacts; validation evidence should come from executable tests and CI/run output.
