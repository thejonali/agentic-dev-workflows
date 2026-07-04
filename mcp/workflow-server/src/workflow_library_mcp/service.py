"""Read-only operations exposed by the workflow library MCP server."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_CHARS = 20_000
MAX_OUTPUT_CHARS = 50_000
MAX_SCANNED_FILES = 5_000
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class WorkflowServerError(ValueError):
    """An expected tool failure with a stable machine-readable code."""

    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def as_dict(self) -> dict[str, Any]:
        error: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.details:
            error["details"] = self.details
        return error


def repository_root() -> Path:
    configured = os.environ.get("WORKFLOW_LIBRARY_ROOT")
    return (
        Path(configured).expanduser().resolve()
        if configured
        else Path(__file__).resolve().parents[4]
    )


def _load_repository_modules(root: Path) -> tuple[Any, Any]:
    required_scripts = (
        root / "scripts" / "generate_provider_assets.py",
        root / "scripts" / "validate_workflows.py",
    )
    if not all(path.is_file() for path in required_scripts):
        raise WorkflowServerError(
            "invalid-library-root",
            "the configured workflow library root does not contain the required scripts",
            root=root.as_posix(),
        )
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    try:
        from scripts import generate_provider_assets, validate_workflows
    except ImportError as exc:
        raise WorkflowServerError(
            "invalid-library-root",
            "the configured workflow library root does not contain importable scripts",
            root=root.as_posix(),
        ) from exc
    return generate_provider_assets, validate_workflows


def _bounded_limit(max_chars: int) -> int:
    if not isinstance(max_chars, int) or isinstance(max_chars, bool):
        raise WorkflowServerError("invalid-input", "max_chars must be an integer")
    if not 1_000 <= max_chars <= MAX_OUTPUT_CHARS:
        raise WorkflowServerError(
            "invalid-input",
            f"max_chars must be between 1000 and {MAX_OUTPUT_CHARS}",
        )
    return max_chars


def _workflow_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        raise WorkflowServerError(
            "invalid-workflow-name", "workflow must use lowercase kebab-case"
        )
    path = root / "core" / "workflows" / f"{name}.workflow.md"
    if not path.is_file():
        raise WorkflowServerError("workflow-not-found", f"unknown workflow: {name}")
    return path


def _document_metadata(path: Path, validator: Any) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    document = validator.parse_document(text)
    commands = re.findall(
        r"`/([a-z0-9]+(?:-[a-z0-9]+)*)`", document.sections.get("Commands", "")
    )
    agents = re.findall(
        r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", document.sections.get("Required Agents", "")
    )
    purpose = " ".join(document.sections.get("Purpose", "").split())
    return {
        "name": path.name.removesuffix(".workflow.md"),
        "title": document.title,
        "description": purpose,
        "commands": sorted(set(commands)),
        "requiredAgents": sorted(set(agents)),
        "sections": document.sections,
        "markdown": text,
    }


def list_workflows(category: str | None = None, limit: int = 50) -> dict[str, Any]:
    """List canonical workflows, optionally filtering their searchable metadata."""
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise WorkflowServerError("invalid-input", "limit must be between 1 and 100")
    if category is not None and (not isinstance(category, str) or not category.strip()):
        raise WorkflowServerError(
            "invalid-input", "category must be a non-empty string"
        )

    root = repository_root()
    _, validator = _load_repository_modules(root)
    workflows = []
    needle = category.strip().casefold() if category else None
    for path in sorted((root / "core" / "workflows").glob("*.workflow.md")):
        metadata = _document_metadata(path, validator)
        searchable = " ".join(
            [
                metadata["name"],
                metadata["title"],
                metadata["description"],
                *metadata["commands"],
            ]
        ).casefold()
        if needle and needle not in searchable:
            continue
        workflows.append(
            {key: metadata[key] for key in ("name", "title", "description", "commands")}
        )
    return {
        "workflows": workflows[:limit],
        "count": min(len(workflows), limit),
        "total": len(workflows),
    }


def get_workflow(name: str, max_chars: int = DEFAULT_OUTPUT_CHARS) -> dict[str, Any]:
    """Return one canonical workflow and its parsed metadata."""
    limit = _bounded_limit(max_chars)
    root = repository_root()
    _, validator = _load_repository_modules(root)
    metadata = _document_metadata(_workflow_path(root, name), validator)
    markdown = metadata.pop("markdown")
    metadata["markdown"] = markdown[:limit]
    metadata["totalChars"] = len(markdown)
    metadata["truncated"] = len(markdown) > limit
    return metadata


def render_provider_asset(
    workflow: str,
    provider: str = "codex",
    max_chars: int = DEFAULT_OUTPUT_CHARS,
) -> dict[str, Any]:
    """Render one workflow adapter in memory without writing repository files."""
    limit = _bounded_limit(max_chars)
    root = repository_root()
    _workflow_path(root, workflow)
    generator, _ = _load_repository_modules(root)
    if provider not in generator.PROVIDERS:
        raise WorkflowServerError(
            "unsupported-provider",
            "provider must be one of: " + ", ".join(generator.PROVIDERS),
            provider=provider,
        )
    try:
        assets = generator.generate_provider_assets(root, provider)
    except (generator.GenerationError, OSError) as exc:
        raise WorkflowServerError("render-failed", str(exc)) from exc
    asset_path = {
        "claude": f"skills/{workflow}/SKILL.md",
        "codex": f"skills/{workflow}/SKILL.md",
        "cursor": f"rules/{workflow}.mdc",
    }[provider]
    content = assets[asset_path]
    return {
        "workflow": workflow,
        "provider": provider,
        "assetPath": asset_path,
        "content": content[:limit],
        "totalChars": len(content),
        "truncated": len(content) > limit,
    }


def validate_workflow(workflow: str | None = None) -> dict[str, Any]:
    """Validate the canonical library, optionally focusing the result on one workflow."""
    root = repository_root()
    if workflow is not None:
        _workflow_path(root, workflow)
    _, validator = _load_repository_modules(root)
    result = validator.validate_repository(root)
    if workflow is None:
        return result
    workflow_path = f"core/workflows/{workflow}.workflow.md"
    relevant = [
        error
        for error in result["errors"]
        if error["path"] == workflow_path
        or error["path"] == "core/schemas/workflow.schema.json"
    ]
    return {
        "status": "pass" if not relevant else "fail",
        "workflow": workflow,
        "errors": relevant,
        "repositoryStatus": result["status"],
    }


def _inventory(root: Path) -> tuple[set[str], bool]:
    files: set[str] = set()
    truncated = False
    for current, directories, filenames in os.walk(root, followlinks=False):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory
            not in {".git", ".venv", "node_modules", "vendor", "dist", "build"}
        )
        relative_directory = Path(current).relative_to(root)
        for filename in sorted(filenames):
            files.add((relative_directory / filename).as_posix())
            if len(files) >= MAX_SCANNED_FILES:
                truncated = True
                return files, truncated
    return files, truncated


def _has(files: set[str], *candidates: str) -> bool:
    return any(candidate in files for candidate in candidates)


def _has_prefix(files: set[str], prefix: str) -> bool:
    return any(path.startswith(prefix) for path in files)


def score_repo_health(path: str = ".") -> dict[str, Any]:
    """Score repository evidence without executing code or returning file contents."""
    if not isinstance(path, str) or not path.strip():
        raise WorkflowServerError("invalid-input", "path must be a non-empty string")
    root = Path(path).expanduser().resolve()
    if not root.is_dir():
        raise WorkflowServerError(
            "repository-not-found", "path is not a directory", path=str(root)
        )
    files, truncated = _inventory(root)

    build = (
        (8 if _has_prefix(files, ".github/workflows/") else 0)
        + (
            6
            if _has(
                files,
                "uv.lock",
                "poetry.lock",
                "package-lock.json",
                "pnpm-lock.yaml",
                "yarn.lock",
                "Cargo.lock",
                "go.sum",
            )
            else 0
        )
        + (
            6
            if _has(
                files,
                "pyproject.toml",
                "package.json",
                "Cargo.toml",
                "go.mod",
                "pom.xml",
                "Makefile",
            )
            else 0
        )
    )
    docs = (
        (7 if _has(files, "README.md", "README.rst") else 0)
        + (4 if _has_prefix(files, "docs/") else 0)
        + (
            4
            if _has(files, "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE", "LICENSE.md")
            else 0
        )
    )
    tests = (
        (
            10
            if any(path.startswith(("tests/", "test/", "spec/")) for path in files)
            else 0
        )
        + (
            5
            if _has(
                files, "pytest.ini", "tox.ini", "vitest.config.ts", "jest.config.js"
            )
            or _has_prefix(files, ".github/workflows/")
            else 0
        )
        + (5 if any("test" in Path(item).name.casefold() for item in files) else 0)
    )
    security = (
        (6 if _has(files, "SECURITY.md") else 0)
        + (
            5
            if _has(
                files,
                ".github/dependabot.yml",
                "renovate.json",
                ".github/renovate.json",
            )
            else 0
        )
        + (4 if any("codeql" in item.casefold() for item in files) else 0)
    )
    release = (
        (4 if _has(files, "LICENSE", "LICENSE.md") else 0)
        + (4 if _has(files, "CHANGELOG.md", "CHANGES.md") else 0)
        + (
            4
            if any(
                "release" in item.casefold()
                for item in files
                if item.startswith(".github/workflows/")
            )
            else 0
        )
        + (3 if _has(files, "pyproject.toml", "package.json", "Cargo.toml") else 0)
    )
    agent = (
        (6 if _has(files, "AGENTS.md") else 0)
        + (
            5
            if _has(files, "Makefile", "justfile", "Taskfile.yml")
            or _has_prefix(files, "scripts/")
            else 0
        )
        + (4 if _has(files, "CONTRIBUTING.md") or _has_prefix(files, "docs/") else 0)
    )
    dimensions = {
        "buildReliability": {"score": build, "max": 20},
        "documentation": {"score": docs, "max": 15},
        "testing": {"score": tests, "max": 20},
        "security": {"score": security, "max": 15},
        "releaseMaturity": {"score": release, "max": 15},
        "agentReadiness": {"score": agent, "max": 15},
    }
    return {
        "score": sum(item["score"] for item in dimensions.values()),
        "maxScore": 100,
        "dimensions": dimensions,
        "evidenceFilesScanned": len(files),
        "scanTruncated": truncated,
        "method": "file-presence heuristics; no repository code was executed",
    }


def structured_call(operation: Any, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Return expected tool failures as stable structured results."""
    try:
        return {"status": "ok", "result": operation(*args, **kwargs)}
    except WorkflowServerError as exc:
        return {"status": "error", "error": exc.as_dict()}
    except (OSError, UnicodeError) as exc:
        error = WorkflowServerError(
            "repository-read-failed",
            "a required repository file could not be read",
            reason=type(exc).__name__,
        )
        return {"status": "error", "error": error.as_dict()}
