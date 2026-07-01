---
description: "Turn a feature request into an implementation-ready plan with explicit behavior, scope, contracts, verification, rollout, and rollback."
argument-hint: "[TASK_CONTEXT]"
---

# /new-feature-plan

This is a legacy explicit-invocation Codex prompt adapted from `core/commands/new-feature-plan.command.md`.
Custom prompts are deprecated; prefer the matching shared skill when one exists.

Treat `$ARGUMENTS` as additional task context. Read applicable repository
instructions, preserve the authorization boundaries in the request, and follow
the canonical command contract below.

## Purpose

Turn a feature request into an implementation-ready plan with explicit behavior,
scope, contracts, verification, rollout, and rollback.

## Inputs

- Feature goal and intended users.
- Acceptance criteria or known product constraints.
- Repository root and relevant existing behavior.
- Compatibility, security, performance, and delivery requirements.

## Preconditions

- The request is planning-only unless implementation is separately authorized.
- Relevant repository instructions and current code can be inspected.

## Procedure

1. Clarify the user-visible outcome, scope, and non-goals.
2. Inspect existing implementations, patterns, interfaces, tests, and documentation.
3. Trace affected flows and identify reusable components.
4. Define contract, data-model, migration, configuration, and UI-state changes.
5. Compare alternatives when a material design decision exists.
6. Break implementation into reviewable steps with file-level impact.
7. Define tests, validation commands, rollout, observability, and rollback.
8. Record assumptions, unresolved decisions, and risks that block implementation.

## Output Format

```text
Feature summary:
Acceptance criteria:
Scope and non-goals:
Current behavior:
Proposed design:
Files likely affected:
Data or contract changes:
Implementation steps:
Tests and verification:
Risk areas:
Rollout and rollback:
Open decisions:
```

## Verification

- Tie each acceptance criterion to an implementation step and check.
- Confirm referenced files and patterns exist.
- Validate migration and compatibility assumptions against current contracts.
- Ensure the plan does not contain unauthorized implementation changes.

## Failure Behavior

- If requirements materially conflict, stop at the decision and present the tradeoff.
- If current behavior cannot be established, mark the affected plan steps provisional.
- If scope is too broad for a reliable plan, split it into ordered milestones.
- Do not invent product requirements to fill material gaps.
