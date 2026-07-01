---
description: "Fix a confirmed defect with the smallest root-cause change and regression coverage."
argument-hint: "[TASK_CONTEXT]"
---

# /fix-bug

This is a legacy explicit-invocation Codex prompt adapted from `core/commands/fix-bug.command.md`.
Custom prompts are deprecated; prefer the matching shared skill when one exists.

Treat `$ARGUMENTS` as additional task context. Read applicable repository
instructions, preserve the authorization boundaries in the request, and follow
the canonical command contract below.

## Purpose

Fix a confirmed defect with the smallest root-cause change and regression coverage.

## Inputs

- Confirmed reproduction or failing test.
- Expected behavior and acceptance criteria.
- Relevant code, configuration, and allowed write scope.
- Required verification commands.

## Preconditions

- The defect is reproduced or the user explicitly accepts a documented exception.
- Implementation writes are authorized.
- The expected contract is known.

## Procedure

1. Reconfirm the reproduction against the current state.
2. Trace the failure to its root cause and identify affected callers or data.
3. Add or preserve regression coverage that detects the old failure.
4. Apply the smallest coherent production fix.
5. Run the targeted regression test.
6. Check adjacent edge cases and relevant integration boundaries.
7. Run broader verification proportional to risk.
8. Review the diff for unrelated refactoring and documentation drift.

## Output Format

```text
Root cause:
Fix applied:
Files changed:
Regression coverage:
Commands run and results:
Compatibility impact:
Remaining risks:
```

## Verification

- Demonstrate that the original reproduction passes after the fix.
- Confirm the regression test detects the pre-fix behavior when practical.
- Run the nearest relevant suite and required static checks.
- Inspect public contracts, persisted data, and error behavior when affected.

## Failure Behavior

- Do not apply a speculative fix when the issue cannot be reproduced without approval.
- Stop and propose a migration or design decision if the fix is breaking.
- Distinguish baseline failures from fix-induced failures.
- If checks cannot run, state the blocker and exact commands still required.
