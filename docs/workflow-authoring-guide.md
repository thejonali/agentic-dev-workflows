# Workflow Authoring Guide

## Purpose

This guide defines how to create canonical workflows, agent roles, commands, and
templates in `core/`. Canonical content describes provider-neutral behavior;
provider adapters translate that behavior without redefining it.

## Authoring Principles

1. Start from a recurring development outcome, not a provider feature.
2. Keep workflows composable and give each command one clear entry point.
3. Separate analysis, approved repository writes, and external side effects.
4. Make inputs, verification, outputs, and failure behavior explicit.
5. Prefer repository evidence over assumptions or generic best practices.
6. Keep specialist roles distinct enough to avoid duplicate work.
7. Preserve accurate `pass`, `fail`, `blocked`, and `unknown` states.

## File Naming

Use lowercase kebab-case names:

```text
core/workflows/<name>.workflow.md
core/agents/<name>.agent.md
core/commands/<name>.command.md
core/templates/<NAME>.template.<extension>
```

Names are stable identifiers. Renaming a canonical file is a compatibility change
for schemas, generators, provider assets, and downstream links.

## Workflow Files

Every workflow must contain these second-level headings exactly once and in this
order:

```md
# Workflow Name

## Purpose
## When to Use
## Inputs
## Required Agents
## Commands
## Procedure
## Rules
## Outputs
## Verification
## Failure Modes
## Provider Notes
```

### Workflow Content Requirements

- `Purpose` states one outcome and the value it provides.
- `When to Use` defines positive triggers and important exclusions.
- `Inputs` lists required context, scope, evidence, and constraints.
- `Required Agents` assigns responsibilities; optional roles have explicit triggers.
- `Commands` lists user-facing entry points and their distinct outcomes.
- `Procedure` is ordered, testable, and clear about authorization boundaries.
- `Rules` contains invariants and safety constraints, not procedural duplication.
- `Outputs` defines artifacts and report fields a consumer can rely on.
- `Verification` states how behavior and claims are checked.
- `Failure Modes` defines safe partial results, stopping conditions, and unknowns.
- `Provider Notes` permits packaging differences without changing core behavior.

Do not embed provider-specific frontmatter or assume a specific agent runtime in a
workflow file.

## Agent Files

Every agent must contain these headings exactly once and in this order:

```md
# Agent Name

## Purpose
## Use When
## Responsibilities
## Inputs
## Outputs
## Rules
## Non-Goals
```

An agent owns a narrow review or delivery responsibility. `Responsibilities` must
describe work the role performs; `Non-Goals` prevents overlap and unapproved
scope expansion. Agents should exchange evidence and artifacts, not rely on hidden
conversation state.

## Command Files

Every command must contain these headings exactly once and in this order:

```md
# /command-name

## Purpose
## Inputs
## Preconditions
## Procedure
## Output Format
## Verification
## Failure Behavior
```

### Command Content Requirements

- A command name is an interface; keep its purpose narrow and predictable.
- `Preconditions` states required context and whether writes are authorized.
- `Procedure` distinguishes read-only discovery, local writes, and external writes.
- `Output Format` provides stable field names. It may use a text block or schema.
- `Verification` includes both behavioral checks and scope/diff checks.
- `Failure Behavior` defines when to stop, return partial output, or mark unknown.
- Commands that write should support a preview or dry-run in provider/tool layers
  where the result can be modeled accurately.

Do not make publication, deployment, messaging, tagging, or other external side
effects implicit in a preparation or review command.

## Templates

Templates use `{{lower_snake_case}}` placeholders. A renderer must either resolve
every placeholder or fail with a list of unresolved names; it must not silently
delete unresolved content.

Template rules:

- Keep headings and fixed labels stable where tools may consume them.
- Use singular placeholders in repeatable example rows or bullets.
- Replace unused optional sections deliberately with `None` or remove the complete
  section during rendering according to provider policy.
- Never place secret values or machine-specific private paths in rendered output.
- Preserve Markdown validity before and after substitution.

Provider-oriented templates in `core/templates/` are canonical inputs for later
adapters, not installed provider assets.

## Procedure Design

A reliable procedure normally follows this sequence:

1. Establish goal, scope, non-goals, and authorization.
2. Read applicable instructions and inspect current behavior.
3. Establish a baseline or reproduction.
4. Plan the smallest viable change or analysis.
5. Perform authorized work.
6. Verify targeted behavior, then broader relevant checks.
7. Review outputs and diffs for scope, safety, and unsupported claims.
8. Report results, failures, unknowns, and remaining risk.

Omit steps that do not apply, but do not omit scope, authorization, verification,
or accurate failure reporting.

## Output and Severity Conventions

Use these evidence states consistently:

- `pass`: the stated check ran successfully against the current target.
- `fail`: the check ran and did not satisfy its expected result.
- `blocked`: a known prerequisite prevented the check from running.
- `unknown`: evidence is missing or the relevant state could not be established.

For review findings, prioritize by user or operational impact and likelihood:

- `blocker`: unsafe to merge or release under expected use.
- `high`: material defect likely to affect supported use.
- `medium`: real defect with narrower impact or likelihood.
- `optional`: maintainability or polish without a current correctness failure.

Every finding must identify a location, triggering condition, impact, evidence,
and actionable remediation direction.

## Provider Adapter Requirements

Adapters may:

- Add required frontmatter, metadata, or directory structure.
- Split a workflow into skills, commands, rules, or specialist agents.
- Bind canonical actions to provider tools.
- Add provider-specific installation and invocation guidance.

Adapters must not:

- Weaken safety, verification, authorization, or failure-reporting requirements.
- Make provider output the new source of truth.
- Convert unknown checks into passing checks.
- Add external side effects to a read-only or preparation command.
- Change command meaning without a canonical core change.

Every manually maintained provider asset should identify its canonical source.
Generated assets should also record the generator or source version when the
provider format permits it.

## Authoring Checklist

- [ ] The outcome is recurring and provider-neutral.
- [ ] Filename and title use the canonical naming convention.
- [ ] All required headings appear once and in order.
- [ ] Inputs, scope, and authorization boundaries are explicit.
- [ ] Procedures are ordered and verifiable.
- [ ] Outputs have stable, useful fields.
- [ ] Failure behavior preserves evidence and unknown states.
- [ ] Referenced agents, commands, templates, and paths exist or are clearly planned.
- [ ] Provider notes preserve the core contract.
- [ ] Internal links and Markdown formatting validate.
- [ ] The diff contains no unrelated or generated churn.

## Review and Evolution

Canonical changes should be reviewed for downstream impact on schemas, provider
assets, generators, examples, and MCP tools. Additive clarification is usually
safe; renamed identifiers, removed output fields, changed command meaning, and
weakened invariants require an explicit compatibility decision.
