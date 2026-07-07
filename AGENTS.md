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

The repository contains Markdown and template contracts plus a standard-library
validator. Run the focused checks before committing:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_workflows.py
python3 -B scripts/generate_provider_assets.py --check
python3 -B scripts/generate_examples.py --check
git diff --check
```

For a v0.1.0 release candidate, also build and inspect the deterministic
archives without tagging or publishing:

```sh
python3 -B scripts/build_release.py --version 0.1.0
unzip -t dist/agentic-dev-workflows-v0.1.0.zip
(cd dist && shasum -a 256 -c SHA256SUMS-v0.1.0.txt)
```
