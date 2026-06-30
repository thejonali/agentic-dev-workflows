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

Planned scripts will validate core documents and render repeatable provider
assets. Generated output must be deterministic: identical canonical inputs and
tool versions should produce identical files.

### MCP Server

The planned MCP server will expose structured operations such as listing,
inspecting, validating, and rendering workflows. Static guidance remains in
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

## Phase 0 Boundary

The current phase establishes documentation, repository rules, and tracked
directory scaffolding only. Schemas, workflow specifications, provider assets,
validation scripts, generation tooling, and the MCP server are later phases.
