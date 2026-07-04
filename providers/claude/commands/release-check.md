# /release-check

This Claude Code compatibility command is adapted from `core/commands/release-check.command.md`. Skills are
the preferred reusable workflow surface; existing `.claude/commands/` files
remain supported for explicit invocation.

Treat task context supplied after the command as additional input. Read
applicable repository instructions, preserve the request's authorization
boundaries, and follow the canonical command contract below. Named agent roles
require matching installed subagents; otherwise treat them as review
perspectives.

## Purpose

Determine whether a defined version and artifact set is ready to release without
performing publication, tagging, or deployment.

## Inputs

- Target version, baseline, and release range.
- Versioning policy and required release checks.
- Package metadata, changelog, documentation, and candidate artifacts.
- CI/test evidence and supported platform matrix.

## Preconditions

- The exact release range and candidate version are known.
- The command is read-only unless preparation edits are separately authorized.
- Publishing credentials are neither required nor inspected.

## Procedure

1. Confirm version consistency and derive changes from the exact release range.
2. Check required tests and CI status, preserving unknown states.
3. Verify README setup, usage, migrations, known limitations, and changelog.
4. Validate package metadata, dependency locks, licenses, and provenance.
5. Build or inspect candidate artifacts and compare their contents with expectations.
6. Scan the change and artifact list for secrets or local/private files.
7. Identify rollout monitoring, compatibility requirements, and rollback steps.
8. Classify readiness as ready, ready with documented follow-up, or blocked.

## Output Format

```text
Version and release range:
Tests and CI:
Documentation and changelog:
Package metadata:
Artifacts and provenance:
Security and secret hygiene:
Compatibility and migrations:
Rollout and rollback:
Blockers and unknowns:
Readiness decision:
```

## Verification

- Run required local release checks supported by the environment.
- Inspect candidate artifact contents rather than only source files.
- Confirm notes and changelog match the release range.
- Verify that no external publish, tag, or deployment action occurred.

## Failure Behavior

- Mark the release blocked when required checks fail.
- Mark unavailable evidence unknown rather than passing.
- Stop if version or release range is ambiguous.
- If artifacts are not reproducible or inspectable, report provenance as unresolved.
