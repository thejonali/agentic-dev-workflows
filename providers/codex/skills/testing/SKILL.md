---
name: testing
description: Analyze test gaps and add deterministic behavior-focused coverage. Use for regression tests, fixtures, contract tests, golden tests, or risk-ranked coverage analysis; keep analysis read-only unless test writes are authorized.
---

# Testing Workflow

Canonical source in this repository: `core/workflows/testing.workflow.md`

## Codex Execution Notes

- Read the applicable repository instructions before acting.
- Treat the required-agent names below as review perspectives. Spawn subagents only when the user explicitly requests subagents or parallel agent work.
- Preserve analysis-only, read-only, and write-authorization boundaries from the request.
- Prefer targeted verification before broader checks and report only checks actually run.
- End with changed files or findings, verification results, assumptions, and remaining risks.

## Canonical Workflow

## Purpose

Find meaningful coverage gaps and add stable tests that protect behavior,
contracts, and regressions without overfitting to implementation details.

## When to Use

- Adding regression coverage for a confirmed bug.
- Planning tests for new or changed behavior.
- Auditing risk before a refactor or release.
- Adding fixtures, golden tests, or contract tests.
- Investigating unreliable or incomplete test suites.

## Inputs

- Behavior or contract under test and its acceptance criteria.
- Relevant implementation, existing tests, fixtures, and test configuration.
- Known failures, production incidents, or coverage reports.
- Supported platforms, runtimes, and compatibility requirements.
- Constraints on network, filesystem, time, nondeterminism, and external services.

## Required Agents

- `test-runner`: owns test discovery, execution, and failure interpretation.
- `reviewer`: checks that tests assert meaningful behavior and remain maintainable.

Use `data-contract-reviewer` for schema/API tests, `security-reviewer` for abuse
cases, and `implementer` when production seams must change for testability.

## Commands

- `/test-gap-analysis`: rank missing coverage by behavior and risk.
- `/add-regression-test`: encode a previously failing case.
- `/generate-fixtures`: create minimal deterministic test data.
- `/golden-test`: verify stable, reviewable serialized or rendered output.
- `/contract-test`: protect an interface between components or systems.

## Procedure

1. Define the behavior, risk, and failure that the test should detect.
2. Inspect nearby tests and project conventions before selecting a test level.
3. Establish whether the behavior is already covered; do not duplicate coverage
   solely to increase test count.
4. Choose the lowest test level that exercises the real contract: unit,
   integration, contract, end-to-end, or golden.
5. For bugs, run or create a test that fails for the expected reason before
   applying the fix when practical.
6. Create minimal fixtures with explicit ownership and cleanup. Remove time,
   randomness, network, and ordering dependencies or control them deliberately.
7. Assert observable behavior, boundaries, and error handling instead of private
   implementation details.
8. Run the new test alone, repeat it when flakiness is plausible, then run the
   relevant surrounding suite.
9. Review failure messages, runtime, fixture readability, and portability.
10. Report coverage gained, commands run, results, and gaps intentionally left.

## Rules

- Tests must fail for the intended reason before they are credited as regression
  coverage, unless reproducing the old state is unsafe or impractical.
- Never use real secrets, production data, or uncontrolled external services.
- Prefer deterministic fakes or local fixtures over broad mocks of internal code.
- Do not regenerate or approve golden output without reviewing the semantic diff.
- Test public contracts and user-visible behavior at important boundaries.
- Avoid sleeps; use observable readiness or controlled clocks.
- Keep fixtures minimal and avoid sharing mutable state across tests.
- Do not lower assertions, coverage thresholds, or strictness to hide a failure.

## Outputs

- Risk-ranked coverage-gap analysis.
- Test plan with chosen levels and scenarios.
- Added or updated tests and fixtures, when authorized.
- Regression evidence or contract coverage summary.
- Exact verification commands and results.
- Known untested scenarios and rationale.

## Verification

- Run each new or changed test in isolation.
- Demonstrate regression sensitivity through pre-fix failure or an equivalent
  controlled check when practical.
- Run the nearest relevant suite and any required project-wide checks.
- Repeat timing-, ordering-, or concurrency-sensitive tests.
- Confirm fixtures are cleaned up and tests do not require undeclared state.
- Inspect golden and snapshot diffs manually before acceptance.

## Failure Modes

- If behavior is unspecified, stop and request acceptance criteria before
  encoding an accidental contract.
- If a test is flaky, quarantine is not a fix; identify the uncontrolled input
  and report it if it cannot be stabilized in scope.
- If the harness cannot reproduce the failure, preserve the investigation and
  propose the smallest testability seam.
- If external services are unavoidable, document credentials, availability, and
  cleanup requirements without exposing values.
- If broader tests fail independently, distinguish baseline failures from
  failures introduced by the change.

## Provider Notes

Provider adapters may expose test commands separately, but they must preserve the
fail-for-the-right-reason requirement and exact verification reporting. Tools
that generate fixtures, snapshots, or golden files are write operations and must
make their output reviewable; provider automation should support dry-run where
practical.
