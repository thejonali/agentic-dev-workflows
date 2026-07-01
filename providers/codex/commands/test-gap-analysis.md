---
description: "Identify and rank meaningful untested behavior by impact and regression likelihood."
argument-hint: "[TASK_CONTEXT]"
---

# /test-gap-analysis

This is a legacy explicit-invocation Codex prompt adapted from `core/commands/test-gap-analysis.command.md`.
Custom prompts are deprecated; prefer the matching shared skill when one exists.

Treat `$ARGUMENTS` as additional task context. Read applicable repository
instructions, preserve the authorization boundaries in the request, and follow
the canonical command contract below.

## Purpose

Identify and rank meaningful untested behavior by impact and regression likelihood.

## Inputs

- Repository root or requested subsystem.
- Existing tests, coverage reports, incidents, and acceptance criteria.
- Optional focus: unit, integration, contract, end-to-end, security, or performance.

## Preconditions

- The analysis is read-only unless test creation is separately authorized.
- Relevant production and test code can be inspected.

## Procedure

1. Map public behavior, critical paths, boundaries, and failure modes.
2. Inventory existing tests by behavior and test level.
3. Review coverage data as supporting evidence, not the sole metric.
4. Identify missing happy paths, edge cases, error handling, and contracts.
5. Rank gaps by impact, likelihood, change frequency, and test feasibility.
6. Recommend the lowest effective test level and likely test location.
7. Separate high-value gaps from low-value implementation-detail coverage.

## Output Format

```text
Scope analyzed:
Existing coverage:
High-risk untested behavior:
Missing edge and failure cases:
Missing integration or contract tests:
Suggested test files and levels:
Priority ranking:
Analysis limitations:
```

## Verification

- Confirm proposed scenarios are not already covered elsewhere.
- Cite production and test paths supporting each priority gap.
- Tie each high-priority gap to a plausible regression or incident.
- Ensure no file was modified.

## Failure Behavior

- If behavior is unspecified, mark it as a contract question rather than a test gap.
- If coverage tooling is unavailable, continue with code-path analysis and label the limitation.
- If scope is too broad, return the highest-risk areas and explicit omissions.
- Do not recommend tests solely to increase a percentage.
