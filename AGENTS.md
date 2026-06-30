# Repository Agent Guide

## Purpose

This repository defines provider-neutral software-development workflows and
renders them into thin provider-specific adapters.

## Source of Truth

- Treat `core/` as canonical.
- Keep provider-specific behavior in `providers/` as small as possible.
- Do not add behavior only to a provider adapter when it belongs in the core.
- Keep generated files reproducible from their canonical inputs once generators
  are introduced.

## Change Rules

1. Identify the goal, scope, and verification path before broad edits.
2. Prefer small, reviewable changes and preserve behavior unless requested.
3. Avoid unrelated refactors and new dependencies.
4. Update tests and documentation when behavior changes.
5. Run the narrowest relevant validation first, then broader checks.
6. Never place secrets, tokens, credentials, or private data in repository files
   or logs.
7. Summarize changed files, verification results, and remaining risks.

## Content Conventions

- Use lowercase kebab-case filenames for workflows, commands, and agents.
- Give workflow documents explicit inputs, procedures, outputs, verification,
  and failure modes.
- Make commands deterministic and suitable for both human and machine use.
- Keep provider notes separate from provider-neutral procedure.
- Use relative links for files within this repository.

## Current Verification

Phase 0 contains documentation and scaffolding only. Until validation tooling is
added, check Markdown links and inspect `git diff --check` before committing.
