# /bug-repro

This Cursor custom command is adapted from `core/commands/bug-repro.command.md`.

Treat task context supplied with the command as additional input. Read applicable
repository instructions, preserve the request's authorization boundaries, and
follow the canonical command contract below. Treat named agent roles as review
perspectives unless the target project defines matching agents.

## Purpose

Reproduce a reported defect deterministically and identify the likely failing code
path before a fix is attempted.

## Inputs

- Error report, observed behavior, logs, or failing test.
- Expected behavior and environmental context.
- Repository root and optional subsystem scope.
- Authorization to add a test or reproduction script, if desired.

## Preconditions

- Expected and observed behavior can be distinguished.
- Reproduction remains read-only unless test or fixture writes are authorized.

## Procedure

1. Record the exact symptom, environment, inputs, and expected result.
2. Inspect relevant entry points, callers, configuration, and existing tests.
3. Minimize the triggering inputs and remove unrelated environmental variables.
4. Reproduce with an existing test or command when possible.
5. Add a minimal failing test or script only when authorized.
6. Confirm that the failure occurs for the expected reason.
7. Trace the failure to the narrowest supported root-cause hypothesis.
8. Report evidence without applying a production fix.

## Output Format

```text
Observed behavior:
Expected behavior:
Environment and inputs:
Minimal reproduction:
Failure evidence:
Likely code path:
Root-cause hypothesis:
Remaining unknowns:
```

## Verification

- Repeat the reproduction when timing or nondeterminism may be involved.
- Confirm control inputs do not trigger the same failure.
- Ensure the reproduction fails at the intended assertion or boundary.
- Confirm no production behavior was changed.

## Failure Behavior

- If reproduction fails, report attempts and evidence rather than proposing a speculative fix.
- If sensitive production data is required, stop and request a safe fixture.
- If expected behavior is unclear, identify the product decision needed.
- Separate environmental or baseline failures from the reported defect.
