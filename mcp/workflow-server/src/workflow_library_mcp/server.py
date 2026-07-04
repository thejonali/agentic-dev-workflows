"""MCP stdio adapter for the workflow library service."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from . import service


mcp = FastMCP(
    "workflow-library-mcp",
    instructions=(
        "Read-only access to canonical workflows, provider rendering, validation, "
        "and evidence-based repository health scoring."
    ),
    json_response=True,
)
READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)


@mcp.tool(annotations=READ_ONLY)
def list_workflows(category: str | None = None, limit: int = 50) -> dict[str, Any]:
    """List workflows. Category is a case-insensitive metadata filter; limit is 1-100."""
    return service.structured_call(service.list_workflows, category, limit)


@mcp.tool(annotations=READ_ONLY)
def get_workflow(
    name: str, max_chars: int = service.DEFAULT_OUTPUT_CHARS
) -> dict[str, Any]:
    """Get a canonical workflow by lowercase kebab-case name with bounded Markdown output."""
    return service.structured_call(service.get_workflow, name, max_chars)


@mcp.tool(annotations=READ_ONLY)
def render_provider_asset(
    workflow: str,
    provider: str = "codex",
    max_chars: int = service.DEFAULT_OUTPUT_CHARS,
) -> dict[str, Any]:
    """Render a provider asset in memory. This tool never writes files."""
    return service.structured_call(
        service.render_provider_asset, workflow, provider, max_chars
    )


@mcp.tool(annotations=READ_ONLY)
def validate_workflow(workflow: str | None = None) -> dict[str, Any]:
    """Validate all canonical contracts or focus the result on one workflow."""
    return service.structured_call(service.validate_workflow, workflow)


@mcp.tool(annotations=READ_ONLY)
def score_repo_health(path: str = ".") -> dict[str, Any]:
    """Score repository file evidence without executing code or returning file contents."""
    return service.structured_call(service.score_repo_health, path)


def main() -> None:
    """Run the local server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
