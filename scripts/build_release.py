#!/usr/bin/env python3
"""Build deterministic GitHub release archives for one repository version."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tomllib
import zipfile
from pathlib import Path, PurePosixPath
from typing import Iterable


VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ROOT_FILES = ("AGENTS.md", "CHANGELOG.md", "LICENSE", "README.md", "ROADMAP.md")
ROOT_DIRECTORIES = (
    "core",
    "docs",
    "examples",
    "mcp",
    "providers",
    "scripts",
    "tests",
)
EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}
PROVIDERS = ("claude", "codex", "cursor")
PROVIDER_DESTINATIONS = {
    "claude": {
        "skills": ".claude/skills",
        "agents": ".claude/agents",
        "commands": ".claude/commands",
    },
    "codex": {
        "skills": ".agents/skills",
        "agents": ".codex/agents",
        "commands": "legacy-prompts",
    },
    "cursor": {
        "rules": ".cursor/rules",
        "commands": ".cursor/commands",
    },
}
PROVIDER_INSTALL_NOTES = {
    "claude": """Copy `.claude/` into the target repository. Skills are the primary workflow interface; commands are compatibility assets. Do not install a skill and command with the same name.""",
    "codex": """Copy `.agents/` and any required `.codex/agents/` files into the target repository. `legacy-prompts/` is optional and belongs under the user's Codex home, not the project.""",
    "cursor": """Copy `.cursor/` into the target repository. Rules are agent-requested rather than always-on. Custom commands are a provider beta surface.""",
}


class ReleaseBuildError(ValueError):
    """Raised when release inputs do not satisfy the archive contract."""


def _validate_version(root: Path, version: str) -> None:
    if not VERSION_PATTERN.fullmatch(version):
        raise ReleaseBuildError("version must use semantic version form X.Y.Z")
    metadata_path = root / "mcp" / "workflow-server" / "pyproject.toml"
    try:
        metadata = tomllib.loads(metadata_path.read_text(encoding="utf-8"))
        package_version = metadata["project"]["version"]
    except (OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        raise ReleaseBuildError(f"cannot read MCP package version: {exc}") from exc
    if package_version != version:
        raise ReleaseBuildError(
            f"release version {version} does not match MCP package {package_version}"
        )
    required = (
        root / "CHANGELOG.md",
        root / "docs" / "releases" / f"v{version}.md",
    )
    for path in required:
        if not path.is_file():
            raise ReleaseBuildError(f"missing release input: {path.relative_to(root)}")


def _included_file(path: Path) -> bool:
    return (
        path.is_file()
        and not path.is_symlink()
        and not any(part in EXCLUDED_PARTS for part in path.parts)
        and path.suffix not in {".pyc", ".pyo"}
    )


def _repository_files(root: Path) -> Iterable[Path]:
    for name in ROOT_FILES:
        path = root / name
        if not path.is_file():
            raise ReleaseBuildError(f"missing release input: {name}")
        yield path
    for directory in ROOT_DIRECTORIES:
        path = root / directory
        if not path.is_dir():
            raise ReleaseBuildError(f"missing release directory: {directory}")
        yield from sorted(
            candidate for candidate in path.rglob("*") if _included_file(candidate)
        )


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def _write_archive(path: Path, entries: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for name, content in sorted(entries.items()):
            archive.writestr(_zip_info(name), content)


def _full_archive(root: Path, version: str, output: Path) -> Path:
    prefix = f"agentic-dev-workflows-v{version}"
    entries = {
        f"{prefix}/{path.relative_to(root).as_posix()}": path.read_bytes()
        for path in _repository_files(root)
    }
    target = output / f"{prefix}.zip"
    _write_archive(target, entries)
    return target


def _provider_install(provider: str, version: str) -> bytes:
    provider_name = {"claude": "Claude Code", "codex": "Codex", "cursor": "Cursor"}[
        provider
    ]
    text = f"""# Agentic Developer Workflows for {provider_name}

Version: {version}

{PROVIDER_INSTALL_NOTES[provider]}

Review destination files before copying. Installing these assets does not grant
permission to write, publish, deploy, access secrets, or delegate unrelated work.

Verify this archive against `SHA256SUMS-v{version}.txt` from the GitHub release.
See https://github.com/thejonali/agentic-dev-workflows for complete documentation.
"""
    return text.encode("utf-8")


def _provider_archive(root: Path, provider: str, version: str, output: Path) -> Path:
    prefix = f"agentic-dev-workflows-{provider}-v{version}"
    entries = {
        f"{prefix}/INSTALL.md": _provider_install(provider, version),
        f"{prefix}/CHANGELOG.md": (root / "CHANGELOG.md").read_bytes(),
        f"{prefix}/LICENSE": (root / "LICENSE").read_bytes(),
    }
    provider_root = root / "providers" / provider
    for source_directory, destination_directory in PROVIDER_DESTINATIONS[
        provider
    ].items():
        source_root = provider_root / source_directory
        if not source_root.is_dir():
            raise ReleaseBuildError(
                f"missing generated provider directory: {source_root.relative_to(root)}"
            )
        for path in sorted(
            candidate
            for candidate in source_root.rglob("*")
            if _included_file(candidate)
        ):
            relative = path.relative_to(source_root).as_posix()
            destination = PurePosixPath(prefix, destination_directory, relative)
            entries[destination.as_posix()] = path.read_bytes()
    target = output / f"{prefix}.zip"
    _write_archive(target, entries)
    return target


def build_release(root: Path, version: str, output: Path) -> list[Path]:
    """Build all versioned archives and their checksum manifest."""
    root = root.resolve()
    output = output.resolve()
    _validate_version(root, version)
    artifacts = [_full_archive(root, version, output)]
    artifacts.extend(
        _provider_archive(root, provider, version, output) for provider in PROVIDERS
    )
    checksum_path = output / f"SHA256SUMS-v{version}.txt"
    checksum_lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
        for path in sorted(artifacts)
    ]
    checksum_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    return [*artifacts, checksum_path]


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version", required=True, help="release version without a v prefix"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    parser.add_argument(
        "--output", type=Path, help="artifact directory (defaults to <root>/dist)"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    root = args.root.resolve()
    output = (args.output or root / "dist").resolve()
    try:
        artifacts = build_release(root, args.version, output)
    except (OSError, ReleaseBuildError, zipfile.BadZipFile) as exc:
        print(f"release build failed: {exc}", file=sys.stderr)
        return 1
    for path in artifacts:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
