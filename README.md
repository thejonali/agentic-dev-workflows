# Agentic Developer Workflows

[![Validate workflow specifications](https://github.com/thejonali/agentic-dev-workflows/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/thejonali/agentic-dev-workflows/actions/workflows/validate.yml)
[![License: Apache-2.0](https://img.shields.io/github/license/thejonali/agentic-dev-workflows)](LICENSE)

A provider-neutral library of reusable AI-assisted software-development
workflows. Canonical behavior lives in one core and is rendered into thin
provider adapters or exposed through structured MCP tools.

## What It Provides

- Canonical workflows covering repository setup, safe changes, testing,
  reviews, documentation, releases, and visual design.
- Deterministic validation for workflow, command, agent, template, and link
  contracts.
- A generated Codex adapter with checked-in, drift-tested skills, agents, and
  commands.
- A local, read-only MCP server for workflow discovery, rendering, validation,
  and repository health scoring.

## Status

Phase 7 exposes the canonical library through a local, read-only MCP workflow
server. Its five tools reuse the existing validator and Codex renderer, apply
bounded outputs, and include deterministic service and stdio protocol coverage.
Provider rendering currently supports Codex only; other provider adapters remain
later phases.

## Use the Library

- Browse the canonical specifications in the [core library](core/README.md).
- Install generated Codex assets with the
  [Codex installation guide](providers/codex/install.md).
- Install and configure the local server with the
  [MCP workflow server guide](mcp/workflow-server/README.md).

## Repository Layout

```text
core/       Canonical provider-neutral workflows, agents, commands, and schemas
providers/  Thin provider-specific adapters derived from the core
mcp/        Local MCP servers that expose shared repository logic
docs/       Architecture and contributor documentation
```

See [the architecture overview](docs/architecture.md) for dependency rules and
the rendering model. Repository-specific guidance for coding agents is in
[AGENTS.md](AGENTS.md).

See the [provider adapter guide](docs/provider-adapters.md) before regenerating
or changing provider packaging.

## Design Principles

- Keep canonical behavior provider-neutral.
- Prefer small, composable workflows over broad prompts.
- Make safety constraints and verification steps explicit.
- Produce readable summaries of actions, results, and remaining risks.
- Design scripts and tools for deterministic, agent-friendly use.

## Verification

Python 3.11 or newer is required for the complete validation and MCP workflow.
Run the same checks used by CI from the repository root:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_workflows.py
python3 -B scripts/generate_provider_assets.py --check
git diff --check
```

The MCP protocol integration test runs when the MCP server package is installed.

## License

Licensed under the [Apache License 2.0](LICENSE).
