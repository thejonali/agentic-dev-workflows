# Changelog

All notable changes to this project are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

No unreleased changes.

## [0.1.0] - 2026-07-06

### Added

- Seven provider-neutral software-development workflows with explicit inputs,
  procedures, outputs, verification, and failure modes.
- Fifteen reusable agent-role definitions, fourteen command specifications, and
  shared authoring and output templates.
- Deterministic Codex, Claude Code, and Cursor adapters generated from the
  canonical core, with checked-in snapshots and drift detection.
- Structural validation for workflow, agent, command, schema, template, and
  local-link contracts.
- A local, read-only MCP server exposing workflow discovery, retrieval,
  provider rendering, validation, and repository health scoring over stdio.
- Reproducible provider-installation examples and illustrative Python CLI and
  React repository guides.
- Deterministic complete-library and provider-specific release archives with a
  SHA-256 checksum manifest.

### Security

- Provider installation and MCP guidance preserve explicit authorization
  boundaries and prohibit implicit access to secrets, deployment, publication,
  or unrelated repository writes.

[Unreleased]: https://github.com/thejonali/agentic-dev-workflows/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/thejonali/agentic-dev-workflows/releases/tag/v0.1.0
