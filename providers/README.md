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
silently redefine core workflow behavior. Until generation tooling exists,
provider assets must identify the canonical source they implement.

The initial Codex adapter is available under `codex/`. Its
[installation guide](codex/install.md) documents supported skills and custom
agents, the deprecated command-prompt compatibility layer, verification, and
current manual-synchronization limits. Claude, Cursor, and generic adapters are
planned for later phases.
