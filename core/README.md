# Core

This directory is the canonical, provider-neutral source for the project.

Structure:

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

## Available Workflows

- [Repository agentization](workflows/repo-agentization.workflow.md)
- [Safe change](workflows/safe-change.workflow.md)
- [Testing](workflows/testing.workflow.md)
- [Review](workflows/review.workflow.md)
- [Documentation and release](workflows/docs-release.workflow.md)
- [Visual design](workflows/visual-design.workflow.md)

Agent, command, template, and schema definitions remain planned work.
