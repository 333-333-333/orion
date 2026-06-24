---
id: MOD-coreference-resolution
type: code-module
title: Coreference Resolution Pipeline Step
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Domain-agnostic mention/coreference handling used to keep semantic claims connected to evidence.
paths:
  - src/pipeline/step_008_coreference_resolution/**
implements:
  - US-006
  - US-011
  - US-012
  - US-022
  - US-025
  - US-026
related_requirements:
  - FUN-006
  - FUN-011
  - FUN-012
  - NFR-001
  - NFR-002
  - NFR-005
related_adrs:
  []
owner: herodotus
---

# MOD-coreference-resolution — Coreference Resolution Pipeline Step

## Summary

Domain-agnostic mention/coreference handling used to keep semantic claims connected to evidence.

## Paths

- `src/pipeline/step_008_coreference_resolution/**`

## Implements

- US-006
- US-011
- US-012
- US-022
- US-025
- US-026

## Related Requirements

- FUN-006
- FUN-011
- FUN-012
- NFR-001
- NFR-002
- NFR-005

## Related ADRs

- None.

## Traceability Notes

This artifact provides Code -> Knowledge traceability for the listed source paths. Tests are intentionally not represented as persisted test-result artifacts; validation evidence should come from executable tests and CI/run output.
