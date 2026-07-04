# Provider Adapter Generation

## Purpose

Provider adapters package canonical `core/` behavior without becoming a second
source of truth. The Phase 6 generator targets Codex, Claude Code, and Cursor;
generic generation remains deferred.

## Inputs and Outputs

The generator reads:

- Canonical workflows, agents, and commands under `core/`.
- Codex skill-selection descriptions in `providers/codex/generator.json`.
- Provider packaging templates under each generated provider's `templates/`
  directory.

It writes only these provider surfaces:

- `providers/codex/skills/*/SKILL.md`
- `providers/codex/agents/*.toml`
- `providers/codex/commands/*.md`
- `providers/claude/skills/*/SKILL.md`
- `providers/claude/agents/*.md`
- `providers/claude/commands/*.md`
- `providers/cursor/rules/*.mdc`
- `providers/cursor/commands/*.md`

Install guides, generator metadata, and templates remain maintained inputs.
Claude Code and Cursor descriptions are derived from canonical Purpose sections;
Codex retains explicit selection descriptions because its adapter already uses a
provider-specific selection contract. Generation does not delete unexpected
files; drift checks report them for explicit review.

## Check for Drift

Run the read-only check used by CI:

```sh
python3 -B scripts/generate_provider_assets.py --check
```

Use `--json` when another tool needs structured status. A clean check exits 0;
missing, changed, unexpected, or invalid assets exit 1; invalid CLI usage exits
2.

## Regenerate Provider Assets

After an approved canonical or packaging change:

1. Run `python3 -B scripts/validate_workflows.py`.
2. Run `python3 -B scripts/generate_provider_assets.py`.
3. Inspect every generated diff for behavior and packaging changes.
4. Treat the checked-in generated assets as the reviewable golden snapshots;
   do not approve their changes without comparing them to canonical inputs.
5. Run the unit suite and drift check from `AGENTS.md`.

Use `--output <directory>` to render into a temporary provider root when testing
one explicit `--provider`. The default target is `all`; use `--provider codex`,
`--provider claude`, or `--provider cursor` for a focused operation.

## Provider Compatibility Decisions

- Codex uses skills, standalone TOML agents, and deprecated prompt compatibility
  commands.
- Claude Code uses Agent Skills, Markdown custom subagents, and compatibility
  commands. Skills are preferred because Claude Code has merged custom commands
  into the skill system.
- Cursor uses one agent-requested `.mdc` rule per canonical workflow and plain
  Markdown custom commands. Rules are not always-on, so the full workflow library
  does not consume context on every request.
- Cursor does not receive generated agent-role files because the planned Cursor
  adapter contract maps workflows to rules and commands, not provider subagents.

## Strict Template Rendering

`scripts/render_templates.py` replaces `{{lower_snake_case}}` placeholders in
one pass. It fails on malformed placeholders, missing values, and unused values;
inserted content is never recursively interpreted. Run it with `--help` for the
standalone file-rendering interface.

## Adding Another Provider

A new provider target requires an explicit compatibility design, provider-owned
templates and metadata, deterministic output paths, drift detection, snapshots,
tests, installation guidance, and CI coverage. Do not copy Codex-specific
frontmatter or agent formats into the canonical core.
