# /map-codebase

This Cursor custom command is adapted from `core/commands/map-codebase.command.md`.

Treat task context supplied with the command as additional input. Read applicable
repository instructions, preserve the request's authorization boundaries, and
follow the canonical command contract below. Treat named agent roles as review
perspectives unless the target project defines matching agents.

## Purpose

Produce a concise, evidence-based map of a repository without modifying it.

## Inputs

- Repository root.
- Optional subsystem, entry point, or user flow to trace.
- Optional depth and output-size constraints.

## Preconditions

- The requested repository or subsystem is readable.
- The command remains read-only.

## Procedure

1. Read repository instructions and top-level documentation.
2. Inventory languages, manifests, build systems, and top-level directories.
3. Identify runtime entry points, major modules, data stores, APIs, and integrations.
4. Trace the requested flow through callers and boundaries when supplied.
5. Map test layout and development, build, and release commands.
6. Identify generated code, vendored assets, migrations, and high-risk boundaries.
7. Cite paths for each material claim and separate unknown areas.

## Output Format

```text
Project type:
Main entry points:
Core modules:
Data flow:
Test structure:
Build system:
External dependencies:
Generated or stored data:
Known risks and unknowns:
Recommended first files to read:
```

## Verification

- Confirm every listed path exists.
- Cross-check entry points and commands against configuration.
- Trace at least one concrete caller or execution path for the requested focus.
- Ensure no file was modified.

## Failure Behavior

- If the root is ambiguous, stop and identify candidate roots.
- If parts of the repository are inaccessible, map the readable scope and list omissions.
- If documentation conflicts with code, report both and identify the stronger evidence.
- Do not infer architecture from filenames alone.
