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

Generated adapters are available for:

- [Codex](codex/install.md): skills, custom agents, and legacy commands.
- [Claude Code](claude/install.md): skills, custom subagents, and compatibility
  commands.
- [Cursor](cursor/install.md): scoped project rules and beta custom commands.

The generic adapter remains planned for a later phase.

Generation inputs and the safe update procedure are documented in the
[provider adapter guide](../docs/provider-adapters.md).
