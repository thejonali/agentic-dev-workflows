# Roadmap

This roadmap records likely product directions, not delivery commitments.
Canonical workflow behavior remains under `core/`; future provider integrations
must continue to derive from that source.

## v0.1.0: Initial Stable Workflow Pack

Release scope:

- Provider-neutral workflows, agents, commands, schemas, and templates.
- Generated Codex, Claude Code, and Cursor adapters.
- Validation, snapshot, and example drift checks in CI.
- Local read-only MCP workflow server.
- Reproducible examples and release archives.

See the [v0.1.0 release notes](docs/releases/v0.1.0.md) for the complete release
contract and known limitations.

## v0.1.x: Compatibility and Maintenance

- Correct provider packaging when upstream formats change.
- Improve validation diagnostics without weakening existing contracts.
- Expand verified installation and troubleshooting guidance.
- Fix defects in MCP tools while preserving their read-only boundary.

## Candidate v0.2.0 Scope

- Design and generate a generic provider adapter only after defining a concrete
  portable contract.
- Add an installer CLI with dry-run, collision detection, selective asset
  installation, and explicit overwrite confirmation.
- Define compatibility metadata for workflow and provider versions.

## Later Exploration

- A marketplace-style workflow index with provenance metadata.
- Project-specific workflow packs built on the canonical core.
- Visual regression utilities for provider-facing examples and documentation.
- Additional providers after their native packaging contracts are verified.

## Non-Goals

- Automatically granting agents permission to write, publish, deploy, or read
  secrets.
- Moving provider-specific behavior into the canonical core.
- Operating a hosted MCP service or collecting repository contents.
- Claiming support for provider formats that are not generated and tested.
