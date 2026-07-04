# /review-council

This Claude Code compatibility command is adapted from `core/commands/review-council.command.md`. Skills are
the preferred reusable workflow surface; existing `.claude/commands/` files
remain supported for explicit invocation.

Treat task context supplied after the command as additional input. Read
applicable repository instructions, preserve the request's authorization
boundaries, and follow the canonical command contract below. Named agent roles
require matching installed subagents; otherwise treat them as review
perspectives.

## Purpose

Review a defined change through distinct correctness, testing, security,
documentation, contract, and UI perspectives, then synthesize one recommendation.

## Inputs

- Review target and baseline.
- Change intent, acceptance criteria, and relevant design decisions.
- Requested specialist scopes and verification budget.

## Preconditions

- The target and baseline are unambiguous.
- Review remains read-only unless fixes are separately authorized.
- Every participating reviewer receives the same change intent and baseline.

## Procedure

1. Inspect the complete diff and classify changed surfaces.
2. Assign non-overlapping scopes to `reviewer`, `test-runner`,
   `security-reviewer`, and `docs-maintainer`.
3. Add `data-contract-reviewer` for contract changes and UI/accessibility roles for
   rendered interface changes.
4. Have each role validate actionable findings against the current target.
5. Run focused checks for material claims where practical.
6. Deduplicate findings and reconcile severity using impact and likelihood.
7. Confirm every retained finding has a location, trigger, impact, and remediation.
8. Produce a recommendation that follows from unresolved findings.

## Output Format

```text
Review target and baseline:
Perspectives completed:
Blockers:
High-priority fixes:
Medium-priority improvements:
Optional polish:
Open questions:
Verification performed:
Final recommendation:
```

## Verification

- Confirm all changed files and applicable specialist surfaces were reviewed.
- Recheck findings against the final target and remove stale or duplicate items.
- Distinguish verified defects from questions and unverified risks.
- Ensure the recommendation matches the highest unresolved severity.

## Failure Behavior

- Stop if the review baseline cannot be established.
- Report unavailable specialist or runtime coverage as an explicit gap.
- If scope exceeds reliable review capacity, list reviewed and omitted areas.
- Do not let consensus downgrade evidence-backed blockers.
