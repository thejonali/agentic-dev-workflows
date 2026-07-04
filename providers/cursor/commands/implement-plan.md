# /implement-plan

This Cursor custom command is adapted from `core/commands/implement-plan.command.md`.

Treat task context supplied with the command as additional input. Read applicable
repository instructions, preserve the request's authorization boundaries, and
follow the canonical command contract below. Treat named agent roles as review
perspectives unless the target project defines matching agents.

## Purpose

Execute an approved plan as a focused change while preserving scope, recording
deviations, and producing verification evidence.

## Inputs

- Approved `PLANS.md` entry or supplied implementation plan.
- Acceptance criteria, scope, and non-goals.
- Repository root and allowed write surface.
- Required validation commands and environmental constraints.

## Preconditions

- The plan is sufficiently specific to implement safely.
- Material architecture and product decisions are resolved.
- Implementation writes are authorized.
- Applicable repository instructions are available.

## Procedure

1. Reconcile the plan with the current repository state and user changes.
2. Establish a test or behavior baseline.
3. Implement steps in dependency order using the smallest coherent diffs.
4. Add or update tests for changed behavior.
5. Update documentation and migrations required by the plan.
6. Run targeted verification after each meaningful increment.
7. Stop and re-plan if a material contract, risk, or scope change appears.
8. Run broader relevant checks and review the complete diff.

## Output Format

```text
Plan implemented:
Files changed:
Behavior changed:
Plan deviations:
Tests added or updated:
Commands run and results:
Remaining risks:
Follow-up work:
```

## Verification

- Map completed work back to every acceptance criterion.
- Run targeted tests, then applicable lint, type, build, and broader test checks.
- Inspect migrations, public interfaces, docs, and generated files when affected.
- Check the final diff for unrelated edits and unresolved diagnostics.

## Failure Behavior

- Stop when the plan is stale, contradictory, or materially incomplete.
- Preserve user changes and report overlapping edits rather than overwriting them.
- If verification cannot run, explain why and give exact completion commands.
- Never silently omit a failed plan step or claim partial work is complete.
