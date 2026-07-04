# /make-agent-friendly-cli

This Claude Code compatibility command is adapted from `core/commands/make-agent-friendly-cli.command.md`. Skills are
the preferred reusable workflow surface; existing `.claude/commands/` files
remain supported for explicit invocation.

Treat task context supplied after the command as additional input. Read
applicable repository instructions, preserve the request's authorization
boundaries, and follow the canonical command contract below. Named agent roles
require matching installed subagents; otherwise treat them as review
perspectives.

## Purpose

Assess and improve a command-line interface for safe, deterministic use by coding
agents and automation while preserving human usability.

## Inputs

- Existing CLI entry points, help output, implementation, and tests.
- Target agent workflows and compatibility constraints.
- Allowed design-only or implementation scope.

## Preconditions

- Existing command behavior and consumers can be inspected.
- Breaking output or exit-code changes require an explicit migration decision.
- Writes are authorized before implementation begins.

## Procedure

1. Inventory commands, arguments, defaults, prompts, output streams, and exit codes.
2. Identify ambiguous input, unbounded output, hidden state, and unsafe writes.
3. Specify structured `--json` output and machine-readable errors where useful.
4. Specify `--dry-run` for write operations and non-interactive behavior.
5. Evaluate `--quiet`, `--verbose`, `--output`, and `--config` based on concrete needs.
6. Define stable exit codes, deterministic ordering, and output-size controls.
7. Implement the approved compatibility-safe subset when authorized.
8. Add tests for human output, JSON, errors, dry-run, and exit codes.

## Output Format

```text
Current CLI contract:
Automation risks:
Proposed command and flags:
JSON and error schemas:
Exit codes:
Compatibility impact:
Changes implemented:
Tests and verification:
```

## Verification

- Test help, successful output, empty results, invalid input, and failures.
- Confirm JSON is valid, stable, bounded, and free of mixed diagnostics.
- Confirm dry-run performs no writes and reports intended changes.
- Verify exit codes and non-interactive behavior through subprocess tests.

## Failure Behavior

- Do not change a public output contract without a migration path.
- If behavior cannot be made non-interactive safely, report the blocking prompt or state.
- If dry-run cannot model writes accurately, document the limitation rather than faking it.
- Preserve the design specification when implementation is outside scope.
