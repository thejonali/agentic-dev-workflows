---
description: "Improve internal structure while preserving observable behavior and public contracts."
argument-hint: "[TASK_CONTEXT]"
---

# /safe-refactor

This is a legacy explicit-invocation Codex prompt adapted from `core/commands/safe-refactor.command.md`.
Custom prompts are deprecated; prefer the matching shared skill when one exists.

Treat `$ARGUMENTS` as additional task context. Read applicable repository
instructions, preserve the authorization boundaries in the request, and follow
the canonical command contract below.

## Purpose

Improve internal structure while preserving observable behavior and public contracts.

## Inputs

- Refactoring goal and explicit boundaries.
- Current implementation, callers, tests, and public interfaces.
- Allowed files and required verification commands.

## Preconditions

- No intentional behavior change is included.
- Existing behavior is covered or can be characterized safely.
- Refactoring writes are authorized.

## Procedure

1. Define the structural problem, target boundary, and non-goals.
2. Identify public behavior, callers, side effects, and data contracts to preserve.
3. Run existing tests and add characterization coverage when needed.
4. Refactor in small mechanically reviewable steps.
5. Run targeted tests after each meaningful step.
6. Avoid mixing renames, formatting churn, and functional changes unnecessarily.
7. Run the relevant broader suite and compare observable outputs.
8. Review the diff for accidental behavior or contract changes.

## Output Format

```text
Refactoring goal:
Behavior preserved:
Files changed:
Structural improvement:
Characterization coverage:
Commands run and results:
Remaining risks:
```

## Verification

- Run the same focused checks before and after the refactor.
- Confirm public signatures, serialized output, and side effects remain stable.
- Run applicable lint, type, build, and broader tests.
- Inspect the diff separately from formatting or generated-file changes.

## Failure Behavior

- Stop and split out any newly required behavior change.
- If current behavior is unknown, add characterization or narrow the scope.
- If tests fail before the change, record the baseline and avoid masking it.
- If safe extraction requires a new architecture decision, return to planning.
