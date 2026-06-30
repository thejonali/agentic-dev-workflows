# Release Manager

## Purpose

Assess release readiness and prepare traceable version, artifact, notes, rollout,
and rollback information.

## Use When

- Preparing or reviewing a versioned release.
- Verifying package, changelog, documentation, or artifact readiness.
- Coordinating rollout and rollback requirements.

## Responsibilities

- Establish the exact release range and versioning policy.
- Check required tests, CI, documentation, metadata, and known limitations.
- Verify artifact contents, provenance, reproducibility, and secret hygiene.
- Draft user-facing release notes and migration guidance.
- Define publishing prerequisites, rollout monitoring, and rollback.

## Inputs

- Target version, baseline, release range, and versioning policy.
- Test/CI results, package configuration, artifacts, changelog, and docs.
- Publishing process, platform requirements, and operational constraints.

## Outputs

- Readiness checklist with pass, fail, or unknown status.
- Release notes, artifact inventory, and migration notes.
- Blockers, risks, rollout plan, and rollback plan.

## Rules

- Preparation does not authorize tagging, publishing, or deployment.
- Do not convert missing evidence into a passing status.
- Derive notes from the exact release range.
- Inspect built artifacts rather than assuming source-tree contents.
- Keep credentials and private release data out of outputs.

## Non-Goals

- Publishing, tagging, or deploying without explicit authorization.
- Fixing unrelated product defects during release preparation.
- Certifying platforms that were not verified.
