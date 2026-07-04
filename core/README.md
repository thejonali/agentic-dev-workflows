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
- [README maintenance](workflows/readme-maintenance.workflow.md)
- [Visual design](workflows/visual-design.workflow.md)

## Available Agents

- [Architect](agents/architect.agent.md)
- [Implementer](agents/implementer.agent.md)
- [Test runner](agents/test-runner.agent.md)
- [Reviewer](agents/reviewer.agent.md)
- [Security reviewer](agents/security-reviewer.agent.md)
- [Documentation maintainer](agents/docs-maintainer.agent.md)
- [README specialist](agents/readme-specialist.agent.md)
- [CI debugger](agents/ci-debugger.agent.md)
- [CLI designer](agents/cli-designer.agent.md)
- [Data contract reviewer](agents/data-contract-reviewer.agent.md)
- [Release manager](agents/release-manager.agent.md)
- [UI architect](agents/ui-architect.agent.md)
- [Visual QA reviewer](agents/visual-qa-reviewer.agent.md)
- [Accessibility reviewer](agents/accessibility-reviewer.agent.md)
- [Asset director](agents/asset-director.agent.md)

## Available Commands

- [`/agentize-repo`](commands/agentize-repo.command.md)
- [`/map-codebase`](commands/map-codebase.command.md)
- [`/new-feature-plan`](commands/new-feature-plan.command.md)
- [`/implement-plan`](commands/implement-plan.command.md)
- [`/bug-repro`](commands/bug-repro.command.md)
- [`/fix-bug`](commands/fix-bug.command.md)
- [`/safe-refactor`](commands/safe-refactor.command.md)
- [`/test-gap-analysis`](commands/test-gap-analysis.command.md)
- [`/review-council`](commands/review-council.command.md)
- [`/release-check`](commands/release-check.command.md)
- [`/readme-refresh`](commands/readme-refresh.command.md)
- [`/make-agent-friendly-cli`](commands/make-agent-friendly-cli.command.md)
- [`/ui-polish-pass`](commands/ui-polish-pass.command.md)
- [`/image-brief`](commands/image-brief.command.md)

## Templates

`templates/` contains canonical starting points for repository instructions,
plans, ADRs, issues, pull requests, release notes, UI/component briefs, and image
briefs/prompts, plus a professional README structure. These are renderer inputs,
not installed provider assets.

Machine-readable contracts for workflows, agents, and commands live in
`schemas/`. Run `python3 -B scripts/validate_workflows.py` from the repository
root to validate those contracts, canonical documents, and local Markdown
links. See the [workflow authoring guide](../docs/workflow-authoring-guide.md)
for authoring and compatibility rules.
