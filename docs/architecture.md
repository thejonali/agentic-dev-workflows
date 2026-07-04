# Architecture

## Objective

Agentic Developer Workflows provides one canonical definition of reusable
software-development workflows and exposes those definitions through multiple
AI coding-agent providers.

The architecture separates behavior from provider packaging:

```text
core definitions
      |
      v
validation and rendering
      |
      +---> Codex assets
      +---> Claude Code assets
      +---> Cursor assets
      +---> Generic AGENTS.md assets
      +---> MCP workflow tools
```

## Components

### Core

`core/` is the source of truth for workflows, agents, commands, templates, and
schemas. A core definition describes intent, inputs, procedure, constraints,
outputs, verification, and failure behavior without assuming a provider.

### Provider Adapters

`providers/` translates core definitions into the structure and metadata each
provider expects. Adapters may add provider-specific instructions, but canonical
behavior remains in `core/`.

### Validation and Rendering

`scripts/validate_workflows.py` validates core document contracts and local
Markdown links against schemas in `core/schemas/`.
`scripts/generate_provider_assets.py` renders Codex assets through strict
provider templates and detects drift against checked-in output. Identical
canonical inputs and tool versions produce identical files.

### MCP Server

The local stdio MCP server exposes structured operations for listing,
inspecting, validating, and rendering workflows plus evidence-based repository
health scoring. It delegates validation and provider rendering to the same
Python functions used by local scripts. The adapter is read-only, bounds large
responses, and returns stable structured errors. Static guidance remains in
Markdown; MCP is reserved for operations that benefit from schemas or runtime
data.

## Dependency Rules

1. Core definitions must not import or require provider adapters.
2. Provider adapters may depend on core definitions.
3. Rendering and validation tooling may read both layers but must not make
   provider output canonical.
4. MCP tools should call the same validation and rendering logic used by local
   scripts rather than duplicate it.
5. Examples may consume public outputs but must not become hidden sources of
   workflow behavior.

## Change Flow

1. Change or add the canonical definition in `core/`.
2. Validate its structure and semantics.
3. Render or update affected provider assets.
4. Verify generated output and examples.
5. Report changed behavior, checks performed, and remaining risks.

## Current Phase Boundary

Phase 7 adds the read-only MCP workflow server while preserving the canonical
core and shared rendering/validation boundaries established in Phase 6. Phase 4
provider adapters remain intentionally deferred, and MCP rendering supports only
the current Codex adapter until those providers exist.
