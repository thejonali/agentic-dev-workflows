# AGENTS.md

## Repository Purpose

{{repository_purpose}}

## Scope

These instructions apply to {{instruction_scope}}. More specific instruction
files take precedence within their directories.

## Project Structure

{{project_structure}}

## Development Commands

| Task | Command | Notes |
| --- | --- | --- |
| Install | `{{install_command}}` | {{install_notes}} |
| Test | `{{test_command}}` | {{test_notes}} |
| Lint | `{{lint_command}}` | {{lint_notes}} |
| Format | `{{format_command}}` | {{format_notes}} |
| Build | `{{build_command}}` | {{build_notes}} |

## Change Rules

- {{change_rule}}
- Preserve existing behavior unless the task explicitly changes it.
- Keep diffs focused and avoid unrelated cleanup.
- Add or update tests and documentation for changed behavior.
- Never expose secrets, credentials, or private data.

## Verification

{{verification_policy}}

## Delivery

Summarize changed files, commands run, results, assumptions, and remaining risks.
