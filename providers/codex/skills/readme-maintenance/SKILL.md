---
name: readme-maintenance
description: Create, rewrite, audit, and synchronize professional project README files from repository evidence. Use for new projects, README work, major feature or architecture updates, releases, installation and testing changes, licenses, diagrams, use cases, or badges.
---

# README Maintenance Workflow

Canonical source in this repository: `core/workflows/readme-maintenance.workflow.md`

## Codex Execution Notes

- Read the applicable repository instructions before acting.
- Treat the required-agent names below as review perspectives. Spawn subagents only when the user explicitly requests subagents or parallel agent work.
- Preserve analysis-only, read-only, and write-authorization boundaries from the request.
- Prefer targeted verification before broader checks and report only checks actually run.
- End with changed files or findings, verification results, assumptions, and remaining risks.

## Canonical Workflow

## Purpose

Create and maintain professional project README files that accurately explain
the product, architecture, use cases, installation, usage, testing, licensing,
and project status without overstating unverified capabilities.

## When to Use

- Creating a README for a new or newly public project.
- Rewriting or auditing a README for clarity, completeness, or accuracy.
- Completing a major feature, architecture, API, CLI, configuration, packaging,
  installation, testing, compatibility, or licensing change.
- Preparing a release, portfolio review, open-source launch, or handoff.
- Adding or correcting badges, diagrams, examples, or documentation links.

Do not invoke this workflow for changes that cannot affect user-facing claims,
setup, supported behavior, architecture, verification, or project status.

## Inputs

- Repository purpose, intended audience, maturity, and supported use cases.
- Current README and linked documentation, when present.
- Source layout, public interfaces, configuration, examples, and screenshots.
- Package manifests, lockfiles, CI configuration, test configuration, and
  release metadata.
- License file, contribution policy, security policy, and support channels.
- The completed change or release range when synchronizing after major work.

## Required Agents

- `readme-specialist`: owns repository discovery, README structure, writing, and
  claim-to-evidence verification.
- `architect`: validates architecture boundaries and diagrams for structural
  changes.
- `test-runner`: verifies installation, usage, and testing commands where the
  environment supports them.

Use `docs-maintainer` for cross-document consistency, `release-manager` for
release status and artifact claims, and `security-reviewer` for security,
credential, or trust-boundary guidance.

## Commands

- `/readme-refresh`: create, rewrite, or synchronize the project README from
  repository evidence.
- `/readme-truth-audit`: report stale claims, commands, links, and badges without
  changing files.
- `/docs-sync`: update related documentation when README changes expose broader
  documentation drift.

## Procedure

1. Establish the target audience, requested write scope, project maturity, and
   whether the task is creation, rewrite, or post-change synchronization.
2. Read repository instructions and the existing README before editing. Map the
   package metadata, entry points, configuration, CI, tests, license, and
   canonical documentation.
3. For post-change work, inspect the exact diff or release range and identify
   affected claims, commands, paths, architecture descriptions, examples,
   compatibility notes, screenshots, and badges.
4. Build an evidence table for the project description, supported use cases,
   prerequisites, installation, usage, architecture, testing, license, support,
   and project status. Mark missing evidence instead of guessing.
5. Choose sections for the audience and project maturity. Prefer a concise
   landing page with links to deeper canonical documentation over duplicating
   long specifications in the README.
6. Write a direct title and value proposition, then add verified use cases,
   installation and quick-start steps, architecture, testing, and license
   information. Add configuration, troubleshooting, contributing, security,
   roadmap, or screenshots only when they are useful and supported.
7. Add badges only when their targets, labels, and live status endpoints are
   known. Prefer a small set covering build, release or package version,
   coverage when meaningful, and license. Never use decorative, duplicate, or
   misleading badges.
8. Keep architecture diagrams readable in source form and consistent with the
   actual component boundaries. Link to an ADR or architecture document when
   the explanation no longer fits a concise overview.
9. Run supported installation, quick-start, and test commands in a representative
   environment. Validate local links, anchors, referenced files, image paths,
   badge URLs where network access is available, and Markdown rendering.
10. Review the README against the completed change and final repository state,
    remove stale or speculative claims, and report edits, verification, unknowns,
    and remaining documentation risks.

## Rules

- Derive commands and claims from repository evidence; never invent setup steps,
  support guarantees, metrics, compatibility, or roadmap commitments.
- Put the reader's first successful outcome before internal implementation detail.
- Distinguish production-ready, experimental, planned, deprecated, and unsupported
  behavior explicitly.
- Use relative links for repository files and stable public links for external
  resources.
- Keep secrets, private URLs, local absolute paths, and environment values out of
  examples and badge targets.
- Do not add a license badge or license statement unless an actual license file or
  explicit licensing decision supports it.
- Do not use test, coverage, release, or quality badges that report a workflow or
  service unrelated to the current repository and default branch.
- Do not copy implementation-heavy architecture, exhaustive API references, or
  contributor procedures into the README when canonical documents already exist.
- Preserve established project terminology and avoid marketing language that
  cannot be verified.

## Outputs

- Created or updated `README.md`, when writes are authorized.
- Audience-appropriate overview, use cases, installation, quick start,
  architecture, testing, license, and optional project-specific sections.
- Badge inventory with each badge's meaning, image endpoint, and destination.
- Documentation drift report for claims or linked files outside the approved
  write scope.
- Verification record listing passed, failed, blocked, and unknown checks.
- Remaining risks such as unverified platforms, missing license, unavailable
  services, or absent canonical architecture documentation.

## Verification

- Confirm every documented command exists in configuration, CI, or source and
  run the commands supported by the current environment.
- Verify use cases and feature claims against implementation or current tests.
- Compare architecture text and diagrams with actual modules, entry points,
  dependencies, and deployment boundaries.
- Validate internal links, anchors, images, referenced files, and documented
  environment variables.
- Confirm each badge points to the correct repository, branch, package, workflow,
  license, or service and has meaningful alt text.
- Confirm license wording matches the repository license file.
- Review the final diff for unrelated prose churn, duplicated canonical content,
  unsupported claims, secrets, and machine-specific values.

## Failure Modes

- If product purpose or audience is unclear, preserve verified facts and return a
  focused draft plus the decisions required to complete positioning.
- If installation or usage commands fail, keep the exact failure, mark the step
  unverified, and do not rewrite it speculatively.
- If a license is absent or ambiguous, state that licensing must be decided and
  do not choose one automatically.
- If badge endpoints or repository metadata cannot be confirmed, omit the badges
  or return them as proposed rather than presenting them as live.
- If architecture evidence conflicts with existing documentation, surface the
  discrepancy and do not silently establish a new contract in the README.
- If the requested change affects broader canonical documentation, complete the
  authorized README scope and report the additional files requiring sync.

## Provider Notes

Provider adapters should expose this workflow as both an automatically selected
README skill and an explicit refresh command. Major-change and release workflows
should route README-impacting changes to the README specialist. Provider tooling
may validate rendering or external badge endpoints, but unavailable network or
browser access must remain `unknown`, not `pass`.
