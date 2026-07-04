# AGENTS.md

## Repository Purpose

An illustrative React application built as a client-side web interface.

## Scope

These instructions apply to the entire repository. More specific instruction
files take precedence within their directories.

## Project Structure

- `src/`: React components, hooks, styles, and application logic.
- `src/**/*.test.*`: behavior-focused component and hook tests.
- `public/`: static assets copied without transformation.
- `package.json`: scripts and dependency contract.
- `package-lock.json`: reproducible dependency versions used by `npm ci`.

## Development Commands

| Task | Command | Notes |
| --- | --- | --- |
| Install | `npm ci` | Install exactly the dependency versions recorded in the lockfile. |
| Test | `npm run test -- --run` | Run the test suite once without watch mode. |
| Lint | `npm run lint` | Check JavaScript, JSX, and configuration files. |
| Format | `npm run format:check` | Verify formatting without rewriting files. |
| Build | `npm run build` | Create the production bundle. |

## Change Rules

- Keep components focused, preserve accessibility semantics, and test user-visible behavior.
- Preserve existing behavior unless the task explicitly changes it.
- Keep diffs focused and avoid unrelated cleanup.
- Add or update tests and documentation for changed behavior.
- Never expose secrets, credentials, or private data.

## Verification

Run the nearest affected test first, then the complete test, lint, format, and production-build commands before delivery.

## Delivery

Summarize changed files, commands run, results, assumptions, and remaining risks.
