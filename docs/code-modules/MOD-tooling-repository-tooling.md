---
id: MOD-tooling
type: code-module
title: Repository Tooling
status: draft
version: 0
created_at: 2026-06-23
updated_at: 2026-06-23
summary: Internal developer tooling for static analysis and repository quality checks; not part of ORION runtime product behavior.
paths:
  - src/tooling/**
implements:
  []
related_requirements:
  - NFR-005
related_adrs:
  - ADR-002
owner: herodotus
---

# MOD-tooling — Repository Tooling

## Summary

Internal developer tooling for static analysis and repository quality checks; not part of ORION runtime product behavior.

## Paths

- `src/tooling/**`

## Implements

- None; internal tooling or support module.

## Related Requirements

- NFR-005

## Related ADRs

- ADR-002

## Traceability Notes

This artifact provides Code -> Knowledge traceability for the listed source paths. Tests are intentionally not represented as persisted test-result artifacts; validation evidence should come from executable tests and CI/run output.
