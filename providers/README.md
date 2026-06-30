# Providers

This directory contains thin adapters that expose canonical `core/` behavior in
provider-specific formats.

Planned adapters:

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
