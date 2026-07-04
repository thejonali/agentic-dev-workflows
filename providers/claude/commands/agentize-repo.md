# /agentize-repo

This Claude Code compatibility command is adapted from `core/commands/agentize-repo.command.md`. Skills are
the preferred reusable workflow surface; existing `.claude/commands/` files
remain supported for explicit invocation.

Treat task context supplied after the command as additional input. Read
applicable repository instructions, preserve the request's authorization
boundaries, and follow the canonical command contract below. Named agent roles
require matching installed subagents; otherwise treat them as review
perspectives.

## Purpose

Inspect a repository and create or update approved agent instructions and
workflow scaffolding. Implements the repository-agentization workflow.

## Inputs

- Repository root.
- Optional provider target: `codex`, `claude`, `cursor`, `generic`, or `all`.
- Requested output files and allowed write scope.
- Optional focus: setup, testing, release, security, or open-source readiness.

## Preconditions

- The repository root is identified and readable.
- Applicable instruction files and user-owned changes are known.
- Writes to guidance or provider files are explicitly authorized.

## Procedure

1. Read existing contributor and agent instructions.
2. Map the stack, entry points, package managers, modules, and generated files.
3. Derive setup, build, test, lint, format, type-check, development, and release
   commands from repository configuration and CI.
4. Identify conflicting guidance, missing prerequisites, unsafe defaults, and
   undocumented workflows.
5. Propose the smallest useful agent instruction set.
6. Create or update approved `AGENTS.md`, `PLANS.md`, documentation, or provider
   assets without changing application behavior.
7. Verify documented paths and commands where the environment permits.
8. Review the diff and report follow-up work separately.

## Output Format

```text
Repository summary:
Detected stack:
Commands confirmed:
Files created:
Files updated:
Verification:
Risks and unknowns:
Recommended next actions:
```

## Verification

- Confirm all referenced paths exist.
- Compare commands with manifests and CI.
- Run the narrowest practical documented commands.
- Check the diff for secrets, machine-specific values, and unrelated edits.

## Failure Behavior

- Stop writes when repository instructions conflict or the write scope is unclear.
- Mark unavailable commands unverified and state the exact missing prerequisite.
- Redact any suspected secret and report only its location.
- Return a partial analysis with explicit omissions when repository access is incomplete.
