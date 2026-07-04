# Agentic Developer Workflows

[![Validate workflow specifications](https://github.com/thejonali/agentic-dev-workflows/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/thejonali/agentic-dev-workflows/actions/workflows/validate.yml)
[![License: Apache-2.0](https://img.shields.io/github/license/thejonali/agentic-dev-workflows)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](#verification)
[![MCP workflow server](https://img.shields.io/badge/MCP-workflow%20server-5A45FF)](mcp/workflow-server/README.md)
[![Providers: Codex | Claude Code | Cursor](https://img.shields.io/badge/providers-Codex%20%7C%20Claude%20Code%20%7C%20Cursor-4F46E5)](docs/provider-adapters.md)

A provider-neutral library for maintaining reusable AI-assisted
software-development workflows across Codex, Claude Code, Cursor, and MCP
clients. Canonical definitions live under `core/`; deterministic generators
render provider-native assets, while validation and snapshot checks prevent
those outputs from drifting from their source.

## What It Provides

- Canonical workflows covering repository setup, safe changes, testing,
  reviews, documentation, releases, and visual design.
- Deterministic validation for workflow, command, agent, template, and link
  contracts.
- Generated Codex, Claude Code, and Cursor adapters with checked-in,
  drift-tested provider assets.
- A local, read-only MCP server for workflow discovery, rendering, validation,
  and repository health scoring.
- Reproducible provider-installation and repository-guidance examples.

## Status

The planned implementation through Phase 8 is complete. The library generates
Codex skills, agents, and commands; Claude Code skills and subagents; and Cursor
rules and commands from the same provider-neutral core. A local, read-only MCP
server exposes five structured tools for discovery, rendering, validation, and
repository health scoring. Reproducible installation examples exercise the
generated assets without becoming a second source of workflow behavior. The
generic adapter remains a later phase.

## Use the Library

- Browse the canonical specifications in the [core library](core/README.md).
- Install generated Codex assets with the
  [Codex installation guide](providers/codex/install.md).
- Install generated Claude Code assets with the
  [Claude Code installation guide](providers/claude/install.md).
- Install generated Cursor assets with the
  [Cursor installation guide](providers/cursor/install.md).
- Install and configure the local server with the
  [MCP workflow server guide](mcp/workflow-server/README.md).
- Review installed snapshots and sample repository guidance in the
  [Phase 8 examples](examples/README.md).

## Repository Layout

```text
core/       Canonical provider-neutral workflows, agents, commands, and schemas
providers/  Thin provider-specific adapters derived from the core
mcp/        Local MCP servers that expose shared repository logic
examples/   Reproducible installations and illustrative repository guides
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
python3 -B scripts/generate_examples.py --check
git diff --check
```

The MCP protocol integration test runs when the MCP server package is installed.

## License

Licensed under the [Apache License 2.0](LICENSE).
