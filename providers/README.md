# Providers

This directory contains thin adapters that expose canonical `core/` behavior in
provider-specific formats.

Adapter layout:

```text
providers/
  codex/
  claude/
  cursor/
  generic/
```

Adapters may add required metadata or translate file structure, but should not
silently redefine core workflow behavior. Generated assets must identify the
canonical source they implement and pass the repository drift check.

The initial Codex adapter is available under `codex/`. Its
[installation guide](codex/install.md) documents supported skills and custom
agents, the deprecated command-prompt compatibility layer, verification, and
current generation limits. Claude, Cursor, and generic adapters are planned for
later phases.

Generation inputs and the safe update procedure are documented in the
[provider adapter guide](../docs/provider-adapters.md).
