# AGENTS.md

## Repository Purpose

An illustrative Python command-line application distributed as an installable package.

## Scope

These instructions apply to the entire repository. More specific instruction
files take precedence within their directories.

## Project Structure

- `src/example_cli/`: application package and command entry point.
- `tests/`: behavior-focused unit and integration tests.
- `pyproject.toml`: package, dependency, tool, and entry-point configuration.

## Development Commands

| Task | Command | Notes |
| --- | --- | --- |
| Install | `python -m pip install -e '.[dev]'` | Install the package and its declared development extras in an active virtual environment. |
| Test | `python -m pytest` | Run the complete test suite. |
| Lint | `ruff check .` | Check Python source and tests. |
| Format | `ruff format --check .` | Verify formatting without rewriting files. |
| Build | `python -m build` | Build source and wheel distributions. |

## Change Rules

- Keep CLI parsing thin and put reusable behavior in importable modules.
- Preserve existing behavior unless the task explicitly changes it.
- Keep diffs focused and avoid unrelated cleanup.
- Add or update tests and documentation for changed behavior.
- Never expose secrets, credentials, or private data.

## Verification

Run the narrowest affected pytest target first, then the complete test, lint, format, and build commands before delivery.

## Delivery

Summarize changed files, commands run, results, assumptions, and remaining risks.
