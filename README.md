# Agentic Developer Workflows

A provider-neutral system for reusable AI-assisted software-development
workflows.

The project will define workflows once in a canonical core and adapt them for
Codex, Claude Code, Cursor, generic `AGENTS.md` consumers, and MCP-compatible
tools. Initial workflow areas include repository setup, safe changes, testing,
reviews, documentation, releases, CI, architecture, and visual design.

## Status

Phase 5 adds machine-readable schemas and automated validation on top of the
canonical library and the Phase 3 Codex adapter. The validator enforces document
structure, naming, non-empty sections, and repository-local Markdown links in
CI. Provider generation and runtime tooling remain later phases.

## Repository Layout

```text
core/       Canonical provider-neutral workflows, agents, commands, and schemas
providers/  Thin provider-specific adapters derived from the core
docs/       Architecture and contributor documentation
```

See [the architecture overview](docs/architecture.md) for dependency rules and
the planned rendering model. Repository-specific guidance for coding agents is
in [AGENTS.md](AGENTS.md).

The current specifications are indexed in [the core README](core/README.md).
Codex assets and their current limitations are documented in the
[Codex installation guide](providers/codex/install.md).

Run the same validation used by CI with:

```sh
python3 -B scripts/validate_workflows.py
```

Use `--json` for deterministic machine-readable output. Validation failures
exit with status 1; invalid command-line usage exits with status 2.

## Design Principles

- Keep canonical behavior provider-neutral.
- Prefer small, composable workflows over broad prompts.
- Make safety constraints and verification steps explicit.
- Produce readable summaries of actions, results, and remaining risks.
- Design scripts and tools for deterministic, agent-friendly use.

## License

Licensed under the [Apache License 2.0](LICENSE).
