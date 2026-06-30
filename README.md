# Agentic Developer Workflows

A provider-neutral system for reusable AI-assisted software-development
workflows.

The project will define workflows once in a canonical core and adapt them for
Codex, Claude Code, Cursor, generic `AGENTS.md` consumers, and MCP-compatible
tools. Initial workflow areas include repository setup, safe changes, testing,
reviews, documentation, releases, CI, architecture, and visual design.

## Status

Phase 0 establishes the repository contract and directory scaffolding. Workflow
specifications and provider assets have not been implemented yet.

## Repository Layout

```text
core/       Canonical provider-neutral workflows, agents, commands, and schemas
providers/  Thin provider-specific adapters derived from the core
docs/       Architecture and contributor documentation
```

See [the architecture overview](docs/architecture.md) for dependency rules and
the planned rendering model. Repository-specific guidance for coding agents is
in [AGENTS.md](AGENTS.md).

## Design Principles

- Keep canonical behavior provider-neutral.
- Prefer small, composable workflows over broad prompts.
- Make safety constraints and verification steps explicit.
- Produce readable summaries of actions, results, and remaining risks.
- Design scripts and tools for deterministic, agent-friendly use.

## License

Licensed under the [Apache License 2.0](LICENSE).
