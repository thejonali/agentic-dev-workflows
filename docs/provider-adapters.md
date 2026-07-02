# Provider Adapter Generation

## Purpose

Provider adapters package canonical `core/` behavior without becoming a second
source of truth. Phase 6 generates the Codex adapter; Claude, Cursor, and generic
generation remain deferred.

## Codex Inputs and Outputs

The generator reads:

- Canonical workflows, agents, and commands under `core/`.
- Codex skill-selection descriptions in `providers/codex/generator.json`.
- Provider packaging templates in `providers/codex/templates/`.

It writes only these generated surfaces:

- `providers/codex/skills/*/SKILL.md`
- `providers/codex/agents/*.toml`
- `providers/codex/commands/*.md`

The install guide, generator manifest, and templates remain maintained inputs.
Generation does not delete unexpected files; drift checks report them for
explicit review.

## Check for Drift

Run the read-only check used by CI:

```sh
python3 -B scripts/generate_provider_assets.py --check
```

Use `--json` when another tool needs structured status. A clean check exits 0;
missing, changed, unexpected, or invalid assets exit 1; invalid CLI usage exits
2.

## Regenerate Codex Assets

After an approved canonical or packaging change:

1. Run `python3 -B scripts/validate_workflows.py`.
2. Run `python3 -B scripts/generate_provider_assets.py`.
3. Inspect every generated diff for behavior and packaging changes.
4. Treat the checked-in generated assets as the reviewable golden snapshots;
   do not approve their changes without comparing them to canonical inputs.
5. Run the unit suite and drift check from `AGENTS.md`.

Use `--output <directory>` to render into a temporary provider root when testing
generation without touching checked-in assets.

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
