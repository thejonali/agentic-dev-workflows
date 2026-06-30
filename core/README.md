# Core

This directory is the canonical, provider-neutral source for the project.

Planned content:

```text
core/
  workflows/  Reusable development procedures
  agents/     Narrow role definitions
  commands/   User-invoked workflow entry points
  templates/  Shared repository and delivery templates
  schemas/    Machine-readable content contracts
```

Core content must not depend on a provider-specific file format or runtime.
Provider-specific rendering guidance belongs in `providers/`.
