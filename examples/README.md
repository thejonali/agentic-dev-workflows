# Phase 8 Examples

These examples show canonical workflows installed in provider-native project
paths and two illustrative repository guides rendered from the canonical
`AGENTS.md` template.

## Provider Installations

- [Codex safe-change skill](provider-installations/codex/.agents/skills/safe-change/SKILL.md)
- [Claude Code safe-change skill](provider-installations/claude/.claude/skills/safe-change/SKILL.md)
- [Cursor safe-change rule](provider-installations/cursor/.cursor/rules/safe-change.mdc)
- [Cursor testing rule](provider-installations/cursor/.cursor/rules/testing.mdc)

The nested `.agents/`, `.claude/`, and `.cursor/` directories are the paths a
target repository would use. The example files are byte-for-byte snapshots of
the corresponding generated provider assets.

## Repository Guides

- [Python CLI `AGENTS.md`](repository-guides/python-cli/AGENTS.md)
- [React app `AGENTS.md`](repository-guides/react-app/AGENTS.md)

These guides are illustrative profiles, not complete runnable applications.
Their commands demonstrate coherent contracts for repositories that provide the
corresponding package metadata, lockfiles, dependencies, and scripts. Do not
claim those commands passed until they run in the target repository.

## Reproduce the Examples

The canonical example inputs are [generator.json](generator.json), the generated
provider assets under `providers/`, and `core/templates/AGENTS.template.md`.
Regenerate or check the snapshots from the repository root:

```sh
python3 -B scripts/generate_examples.py
python3 -B scripts/generate_examples.py --check
```

Do not edit files under `provider-installations/` or `repository-guides/`
directly. Change their canonical inputs and regenerate them.

See the [dogfooding report](dogfooding-report.md) for evidence and limitations.
