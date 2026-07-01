---
name: safe-change
description: Plan, implement, and verify a focused behavior change with minimal scope. Use for features, bug fixes, approved plans, and behavior-preserving refactors; stop after analysis when implementation is not authorized.
---

# Safe Change Workflow

Canonical source in this repository: `core/workflows/safe-change.workflow.md`

## Codex Execution Notes

- Read the applicable repository instructions before acting.
- Treat the required-agent names below as review perspectives. Spawn subagents only when the user explicitly requests subagents or parallel agent work.
- Preserve analysis-only, read-only, and write-authorization boundaries from the request.
- Prefer targeted verification before broader checks and report only checks actually run.
- End with changed files or findings, verification results, assumptions, and remaining risks.

## Canonical Workflow

## Purpose

Plan, implement, and verify a focused code change while minimizing regressions,
scope growth, and unrelated churn.

## When to Use

- Adding a feature or changing behavior.
- Reproducing and fixing a bug.
- Refactoring existing code without intended behavior changes.
- Extracting a module or moving a responsibility.

For analysis-only requests, stop after the plan or reproduction stage unless
implementation is explicitly requested.

## Inputs

- Desired outcome and acceptance criteria.
- Repository instructions and permitted scope.
- Relevant code paths, interfaces, tests, and runtime configuration.
- Known reproduction steps, logs, or failing checks.
- Compatibility, migration, security, and performance constraints.

## Required Agents

- `architect`: plans changes that cross boundaries or alter contracts.
- `implementer`: applies the approved focused change.
- `test-runner`: reproduces behavior and runs verification.
- `reviewer`: checks the completed diff for correctness and scope.

Use `data-contract-reviewer`, `security-reviewer`, or `docs-maintainer` when the
change affects their respective surfaces.

## Commands

- `/new-feature-plan`: define behavior, scope, risks, and implementation order.
- `/implement-plan`: execute an approved plan and verify each increment.
- `/bug-repro`: create a deterministic reproduction before proposing a fix.
- `/fix-bug`: apply the smallest root-cause fix plus regression coverage.
- `/safe-refactor`: preserve behavior while improving structure.
- `/extract-module`: separate a responsibility without changing its contract.

## Procedure

1. Restate the requested outcome, acceptance criteria, scope, and non-goals.
2. Read applicable repository instructions and inspect the current code path.
3. Establish a baseline with a focused test, reproduction, or observable
   behavior. Record environmental blockers instead of inventing results.
4. Trace the root cause or identify the smallest viable design. For contract or
   boundary changes, define compatibility and migration behavior first.
5. Produce an implementation sequence with affected files and verification for
   each meaningful step.
6. Apply the smallest coherent change. Avoid cleanup that is not required for
   the requested outcome.
7. Add or update tests for changed behavior; bug fixes require regression
   coverage when a test harness exists.
8. Run targeted checks first, followed by broader relevant checks in proportion
   to risk.
9. Review the diff for accidental behavior changes, generated-file churn,
   security issues, and documentation drift.
10. Report files changed, behavior changed, checks run, results, assumptions,
    and remaining risks.

## Rules

- Do not edit before understanding the active code path and verification route.
- Preserve public behavior during refactors unless a contract change is explicit.
- Never weaken or delete a failing test merely to make a check pass.
- Do not introduce dependencies or architectural patterns without justification.
- Keep migrations backward compatible or document the required breaking change.
- Stop and re-plan when implementation reveals materially larger scope.
- Preserve user changes and avoid destructive version-control operations.
- Never claim a check passed unless it ran successfully in the current work.

## Outputs

- Scope and acceptance criteria.
- Reproduction or baseline evidence.
- Implementation plan and affected files.
- Focused code and test changes, when authorized.
- Verification commands and results.
- Remaining risks, limitations, and follow-up work.

## Verification

- Confirm the original reproduction now passes for a bug fix.
- Run tests closest to the changed behavior.
- Run applicable lint, format, type, build, and broader test checks.
- Inspect public interfaces, stored data, and generated outputs when affected.
- Review the final diff for unrelated edits and unresolved diagnostics.

Verification depth must match risk; a syntax check alone is insufficient for a
behavior change when runnable tests exist.

## Failure Modes

- If the issue cannot be reproduced, report evidence gathered and do not apply a
  speculative fix without explicit approval.
- If requirements conflict, pause implementation and identify the decision needed.
- If tests expose a pre-existing failure, separate it from change-induced failures.
- If the safe fix requires a breaking change or migration, stop and propose the
  contract and rollout plan.
- If verification cannot run, state why and provide exact commands for completion.

## Provider Notes

Providers may split planning, implementation, testing, and review across isolated
agents, but handoffs must include scope, evidence, changed files, and verification
state. Parallel work must use non-overlapping write scopes. Provider adapters
must not collapse analysis-only and implementation commands into one implicit
write operation.
