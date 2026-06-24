---
id: ADR-002
type: adr
title: Keep Repository Tooling Outside Product Runtime
status: proposed
date: 2026-06-23
deciders: [herodotus]
related_requirements: [CON-001, CON-002, NFR-005]
related_use_cases: []
related_user_stories: []
affected_modules: [MOD-tooling]
supersedes: []
superseded_by: []
---

# ADR-002 — Keep Repository Tooling Outside Product Runtime

## Status

Proposed

## Context

The repository contains internal tooling under `src/tooling/**`. This code supports developer quality checks but is not part of ORION's product runtime contract as an embeddable library.

Without an explicit artifact, tooling code appears as Code -> Knowledge drift: it exists in source but is not explained by product requirements, use cases, or user stories.

## Decision Drivers

- Preserve the no-CLI/no-service product boundary for ORION runtime behavior.
- Keep developer tooling traceable without pretending it is user-facing product functionality.
- Avoid deleting useful tooling solely because it is not part of the runtime pipeline.
- Make it clear that tooling may be changed or removed without changing ORION's public library contract.

## Options Considered

### Option A: Treat tooling as product behavior

Pros:
- Every source file maps to a product requirement.

Cons:
- Misrepresents internal tooling as user-facing behavior.
- Expands the public contract unnecessarily.

### Option B: Delete tooling with no product requirement

Pros:
- Simplifies source tree.
- Avoids traceability questions.

Cons:
- Removes potentially useful quality checks.
- Does not establish a rule for future internal tooling.

### Option C: Track tooling as an internal code module

Pros:
- Provides Code -> Knowledge traceability.
- Keeps runtime/product boundary clear.
- Avoids overfitting product requirements to internal code.

Cons:
- Adds a small amount of documentation for non-product code.

## Decision

We will track repository tooling as an internal `code-module` artifact, not as product-facing ORION behavior. `MOD-tooling` is justified by repository quality/testability concerns and this ADR, not by a host-application user story.

## Consequences

Positive:
- Internal tooling has explicit rationale.
- Product requirements remain clean and user-facing.
- Code -> Knowledge audit can distinguish product modules from support modules.

Negative:
- Tooling changes require keeping `MOD-tooling` current.

Neutral / follow-up:
- If tooling becomes a public CLI or package feature, create separate requirements/use cases before exposing it.

## Traceability

Related artifacts:
- CON-001
- CON-002
- NFR-005
- MOD-tooling

## Review Notes

Revisit if `src/tooling/**` is packaged, invoked by users, or becomes part of CI policy.
