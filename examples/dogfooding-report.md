# Phase 8 Dogfooding Report

## Scope

Phase 8 exercises the provider-generation and repository-guidance paths without
creating untracked behavior outside the canonical core:

- Install `safe-change` into Codex and Claude Code project skill paths.
- Install `safe-change` and `testing` into Cursor project rule paths.
- Render Python CLI and React app repository guides from the canonical
  `AGENTS.md` template.

## Evidence

| Example | Source | Verification |
| --- | --- | --- |
| Codex skill | `providers/codex/skills/safe-change/SKILL.md` | Byte equality and drift test |
| Claude Code skill | `providers/claude/skills/safe-change/SKILL.md` | Byte equality and drift test |
| Cursor rules | `providers/cursor/rules/safe-change.mdc`, `testing.mdc` | Byte equality, frontmatter contract, drift test, and authenticated Cursor Agent discovery |
| Python CLI guide | `core/templates/AGENTS.template.md`, `examples/generator.json` | Strict template rendering and placeholder test |
| React app guide | `core/templates/AGENTS.template.md`, `examples/generator.json` | Strict template rendering and placeholder test |

The checked-in examples are regenerated before comparison, so a canonical
workflow, provider template, installation selection, or guide-profile change
causes an explicit drift failure.

## Repository Dogfooding

This repository is the concrete dogfooding target for the example pipeline. The
Phase 8 change uses its canonical safe-change procedure, strict template
renderer, standard-library tests, link validator, provider drift check, and CI
workflow. The installed snapshots therefore exercise the same files and commands
that maintain the library rather than a separate example-only implementation.

## Cursor Runtime Check

Cursor Desktop 3.9.16 and Cursor Agent `2026.07.01-41b2de7` were detected. An
authenticated Cursor Agent request ran in read-only `ask` mode with sandboxing
against `examples/provider-installations/cursor` and discovered exactly:

- `.cursor/rules/safe-change.mdc` with `alwaysApply: false` and canonical source
  `core/workflows/safe-change.workflow.md`.
- `.cursor/rules/testing.mdc` with `alwaysApply: false` and canonical source
  `core/workflows/testing.workflow.md`.

SHA-256 hashes for both rule files were identical before and after the request,
confirming that runtime discovery did not modify the example fixture.

## Findings

- Provider examples can remain exact installed snapshots without becoming a
  second source of workflow behavior.
- Cursor benefits from multiple scoped, agent-requested rules instead of one
  large always-on rule.
- The canonical `AGENTS.md` template supports both Python and JavaScript command
  contracts without provider-specific behavior.
- Example drift needs a dedicated check because provider drift alone cannot
  detect stale installed snapshots.

## Limitations

- Cursor project-rule discovery was runtime-tested through Cursor Agent; visual
  listing in Cursor Settings and custom-command discovery in the editor UI were
  not automated.
- Claude Code subagents were runtime-discovered during provider verification,
  but this skill-only installation snapshot was not invoked against a model.
- The Python CLI and React app profiles are illustrative; no sample application
  or dependency tree is included, so their documented commands were not run.
- Phase 8 does not publish examples to external repositories or authorize any
  provider to write, deploy, or access secrets.
