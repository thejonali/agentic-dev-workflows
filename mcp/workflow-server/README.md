# Workflow Library MCP Server

This local, read-only MCP server exposes the canonical workflow library and the
repository's existing validation and Codex rendering logic over stdio.

## Tools

| Tool | Inputs | Behavior |
| --- | --- | --- |
| `list_workflows` | Optional `category`, `limit` (1-100) | Lists canonical workflow metadata. The category filter searches names, titles, purposes, and commands. |
| `get_workflow` | `name`, optional `max_chars` | Returns parsed sections and bounded canonical Markdown. |
| `render_provider_asset` | `workflow`, optional `provider`, `max_chars` | Renders one Codex skill in memory without writing files. |
| `validate_workflow` | Optional `workflow` | Reuses the repository validator for all contracts or one workflow-focused result. |
| `score_repo_health` | Optional repository `path` | Scores file-presence evidence for build, docs, tests, security, releases, and agent readiness without executing repository code. |

Expected failures use a stable envelope:

```json
{
  "status": "error",
  "error": {
    "code": "workflow-not-found",
    "message": "unknown workflow: missing"
  }
}
```

Markdown and rendered output default to 20,000 characters and cannot exceed
50,000 characters per call. Repository scoring scans at most 5,000 files and
reports when that limit truncates the scan.

## Install and Run

The server requires Python 3.11 or newer. From the repository root, create an
isolated environment and install the server package:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e mcp/workflow-server
.venv/bin/workflow-library-mcp
```

The last command starts the stdio transport and waits for an MCP client; it does
not provide an interactive shell. Do not write diagnostics to stdout because
stdout carries protocol messages.

For a client that accepts command and argument configuration, use the installed
entry point:

```json
{
  "command": "/absolute/path/to/agentic-dev-workflows/.venv/bin/workflow-library-mcp",
  "args": [],
  "env": {
    "WORKFLOW_LIBRARY_ROOT": "/absolute/path/to/agentic-dev-workflows"
  }
}
```

`WORKFLOW_LIBRARY_ROOT` is optional when running from this checkout. Set it when
the package location cannot infer the repository root.

## Permissions and Safety

- The server uses stdio and does not listen on a network port.
- Workflow query, rendering, and validation require read access to this checkout.
- `score_repo_health` requires read access to the target path supplied by the
  caller. It reads directory entries only, skips common dependency/build trees,
  does not follow directory symlinks, and never returns file contents.
- No tool writes files, executes target repository code, or starts subprocesses.
  The server code intentionally reads only `WORKFLOW_LIBRARY_ROOT`.
- Provider rendering is limited to the currently supported `codex` adapter.

## Verify

Run the repository checks after installing the package so the stdio integration
test is enabled:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_workflows.py
python3 -B scripts/generate_provider_assets.py --check
git diff --check
```

The unit suite skips only the stdio round-trip test when the MCP SDK is absent;
the service-level tool tests still run.
