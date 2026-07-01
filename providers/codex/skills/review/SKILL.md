---
name: review
description: Review a diff, commit range, branch, or pull request for actionable defects and risks. Use for read-only correctness, security, contract, testing, or pre-merge review; do not implement fixes unless asked.
---

# Review Workflow

Canonical source in this repository: `core/workflows/review.workflow.md`

## Codex Execution Notes

- Read the applicable repository instructions before acting.
- Treat the required-agent names below as review perspectives. Spawn subagents only when the user explicitly requests subagents or parallel agent work.
- Preserve analysis-only, read-only, and write-authorization boundaries from the request.
- Prefer targeted verification before broader checks and report only checks actually run.
- End with changed files or findings, verification results, assumptions, and remaining risks.

## Canonical Workflow

## Purpose

Evaluate a proposed change for correctness, regressions, security, contracts,
operability, and maintainability, then provide prioritized actionable findings.

## When to Use

- Reviewing a working-tree diff, commit range, or pull request.
- Performing a pre-merge or pre-release quality gate.
- Running focused security, performance, or error-handling reviews.
- Combining specialist reviews into one recommendation.

Review is read-only unless the user separately authorizes fixes.

## Inputs

- Review target and baseline: diff, commit range, branch, or pull request.
- Intended behavior, acceptance criteria, and linked design decisions.
- Repository instructions and relevant build/test commands.
- Changed code, tests, schemas, documentation, and generated artifacts.
- Requested focus areas and risk tolerance.

## Required Agents

- `reviewer`: owns correctness, maintainability, and final prioritization.
- `test-runner`: evaluates coverage and verifies suspicious behavior.

Add `security-reviewer`, `data-contract-reviewer`, `docs-maintainer`,
`accessibility-reviewer`, `visual-qa-reviewer`, or `release-manager` according to
the changed surfaces. A council must have distinct scopes to avoid duplicate
feedback.

## Commands

- `/review-diff`: review a defined change against its baseline.
- `/review-council`: combine independent specialist reviews.
- `/security-sweep`: inspect practical security boundaries and abuse cases.
- `/performance-pass`: identify material performance regressions and hot paths.
- `/error-handling-pass`: inspect failure behavior, diagnostics, and recovery.

## Procedure

1. Confirm the review target, baseline, intent, and requested depth.
2. Read repository guidance and inspect the complete diff before individual files.
3. Trace changed behavior through callers, state transitions, data boundaries,
   tests, and user-facing documentation.
4. Run focused checks or construct minimal reproductions for suspected defects
   when safe and proportionate.
5. Evaluate correctness first, then security, compatibility, reliability,
   performance, maintainability, documentation, and style.
6. For each finding, verify that it is introduced or exposed by the reviewed
   change and is not merely a general preference.
7. Record a precise location, impact, triggering conditions, evidence, and a
   concrete remediation direction.
8. Deduplicate specialist findings and resolve conflicting severity assessments.
9. Report findings in severity order, followed by open questions, verification,
   and a clear merge recommendation.

## Rules

- Prioritize defects and operational risks over style preferences.
- Do not report a finding without a plausible failure mode or maintenance cost.
- Keep findings scoped to the reviewed change unless a pre-existing blocker is
  directly relevant and clearly labeled.
- Do not infer passing tests from the presence of test files or CI configuration.
- Treat missing tests as a finding only when a meaningful regression path exists.
- Never expose secrets encountered during review.
- Avoid duplicate findings and bundled findings with unrelated root causes.
- If no findings remain, say so and identify residual verification gaps.

## Outputs

- Blockers, high-priority, and medium-priority findings.
- Optional polish separated from required changes.
- Open questions and assumptions affecting the review.
- Commands run and verification results.
- Final recommendation: approve, approve with follow-up, or request changes.

Each finding must include a location, impact, evidence or trigger, and actionable
remediation direction.

## Verification

- Confirm the baseline and inspect all changed files, including tests and docs.
- Re-read relevant callers and contracts outside the diff.
- Run targeted tests or static checks for material claims when available.
- Confirm every finding is still present in the final reviewed state.
- Check that severity reflects impact and likelihood rather than reviewer effort.
- Ensure the final recommendation follows from the reported findings.

## Failure Modes

- If the baseline is missing or ambiguous, do not guess; state the exact target
  required for a reliable review.
- If generated or binary artifacts cannot be inspected, report the blind spot and
  identify their source inputs.
- If tests cannot run, continue static review but label runtime claims unverified.
- If a specialist review conflicts with repository evidence, preserve the evidence
  and explain the resolved severity.
- If scope is too large for reliable coverage, return reviewed areas and explicit
  omissions rather than claiming completeness.

## Provider Notes

Provider adapters may run specialist reviews in parallel when their scopes do not
overlap. The coordinating reviewer must receive the same baseline and intent,
deduplicate results, and verify findings against the final state. Review commands
remain read-only unless a distinct fix command is authorized.
