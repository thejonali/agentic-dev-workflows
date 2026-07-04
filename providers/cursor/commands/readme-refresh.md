# /readme-refresh

This Cursor custom command is adapted from `core/commands/readme-refresh.command.md`.

Treat task context supplied with the command as additional input. Read applicable
repository instructions, preserve the request's authorization boundaries, and
follow the canonical command contract below. Treat named agent roles as review
perspectives unless the target project defines matching agents.

## Purpose

Create, rewrite, or synchronize a professional project README from current
repository evidence.

## Inputs

- Target repository and intended README audience.
- Requested mode: create, rewrite, or synchronize after a defined change.
- Current README and approved write scope.
- Completed diff or release range when applicable.
- Any required positioning, branding, screenshots, or externally managed links.

## Preconditions

- The repository root and applicable instructions are known.
- README writes are explicitly authorized; otherwise return a read-only audit or
  proposed structure.
- Major claims, commands, badges, and license details can be checked against
  repository or public evidence.

## Procedure

1. Read repository instructions, the current README, manifests, CI, tests,
   license, entry points, configuration, and canonical documentation.
2. If synchronizing, inspect the exact completed diff or release range and list
   every README surface it can affect.
3. Identify the audience, value proposition, supported use cases, prerequisites,
   installation path, quick start, architecture, testing, license, and status.
4. Build a claim-to-evidence checklist and separate confirmed facts from missing
   decisions or unavailable verification.
5. Create or update the smallest coherent README using the repository's style.
   Use a repository-provided README template when available; otherwise select
   only the sections supported by the project evidence and audience.
6. Add only meaningful badges with confirmed image endpoints and destinations.
7. Run supported documented commands and validate links, anchors, images,
   diagrams, environment-variable names, license wording, and Markdown structure.
8. Review the final diff for stale claims, duplication, speculation, secrets,
   machine-specific data, and unrelated prose churn.

## Output Format

```text
Mode and audience:
README sections created or updated:
Claims and commands verified:
Badges and links verified:
Checks passed:
Checks failed or blocked:
Unknowns and assumptions:
Related documentation drift:
Remaining risks:
```

## Verification

- Run installation, quick-start, and testing commands supported by the current
  environment.
- Confirm use cases, architecture, project status, and compatibility statements
  against current source and configuration.
- Validate internal references and every included badge target.
- Match license wording to the actual license file.
- Run repository documentation checks and inspect the final diff.

## Failure Behavior

- Stop unsupported claims from entering the README and report missing evidence.
- Preserve exact command failures and mark unavailable checks blocked or unknown.
- Omit unconfirmed badges and licenses rather than guessing.
- If the README depends on an unresolved product-positioning decision, return the
  verified structure and identify the minimum decision needed.
- Do not expand into unrelated docs without authorization; report their drift.
