#!/usr/bin/env python3
"""Generate deterministic provider assets from canonical core documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

if __package__:
    from .render_templates import TemplateError, render_template
else:
    from render_templates import TemplateError, render_template


PROVIDER = "codex"  # Backward-compatible default for the public helper functions.
PROVIDERS = ("claude", "codex", "cursor")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ASSET_GLOBS = {
    "claude": ("skills/*/SKILL.md", "agents/*.md", "commands/*.md"),
    "codex": ("skills/*/SKILL.md", "agents/*.toml", "commands/*.md"),
    "cursor": ("rules/*.mdc", "commands/*.md"),
}


@dataclass(frozen=True, order=True)
class Drift:
    path: str
    reason: str


class GenerationError(ValueError):
    """Raised when canonical inputs or provider configuration are invalid."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GenerationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GenerationError(f"{path} must contain a JSON object")
    return value


def _read_core_document(path: Path) -> tuple[str, str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GenerationError(f"cannot read {path}: {exc}") from exc
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise GenerationError(f"{path} must start with one H1 title")
    title = lines[0][2:].strip()
    if not title:
        raise GenerationError(f"{path} has an empty title")
    body = "\n".join(lines[1:]).strip()
    if not body:
        raise GenerationError(f"{path} has no body")
    return title, body, text.rstrip()


def _purpose_description(body: str, path: Path) -> str:
    marker = "## Purpose\n"
    if marker not in body:
        raise GenerationError(f"{path} has no Purpose section")
    purpose = body.split(marker, 1)[1].split("\n## ", 1)[0].strip()
    first_paragraph = purpose.split("\n\n", 1)[0]
    description = " ".join(first_paragraph.split())
    if not description:
        raise GenerationError(f"{path} has an empty Purpose section")
    return description


def _template(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GenerationError(f"cannot read template {path}: {exc}") from exc


def _render(template: str, values: dict[str, str], path: Path) -> str:
    try:
        return render_template(template, values)
    except TemplateError as exc:
        raise GenerationError(f"cannot render {path}: {exc}") from exc


def _validate_skill_description(name: str, description: str) -> None:
    if not description or description.strip() != description or "\n" in description:
        raise GenerationError(f"skill description for {name} must be one non-empty line")
    if ": " in description or " #" in description:
        raise GenerationError(
            f"skill description for {name} is unsafe as a plain YAML scalar"
        )


def _core_files(root: Path, directory: str, suffix: str) -> list[Path]:
    files = sorted((root / "core" / directory).glob(f"*{suffix}"))
    if not files:
        raise GenerationError(f"no canonical {directory} found")
    for path in files:
        name = path.name.removesuffix(suffix)
        if not NAME_PATTERN.fullmatch(name):
            raise GenerationError(f"invalid canonical {directory} name: {name}")
    return files


def _validate_frontmatter(
    content: str, expected: dict[str, str], source_path: Path
) -> None:
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise GenerationError(f"generated asset for {source_path} has no frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise GenerationError(
            f"generated asset for {source_path} has unclosed frontmatter"
        ) from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            raise GenerationError(
                f"generated asset for {source_path} has invalid frontmatter: {line}"
            )
        key, value = line.split(":", 1)
        if key in fields:
            raise GenerationError(
                f"generated asset for {source_path} repeats frontmatter key: {key}"
            )
        fields[key] = value.strip()
    if fields != expected:
        raise GenerationError(
            f"generated asset for {source_path} has unexpected frontmatter"
        )


def generate_codex_assets(root: Path) -> dict[str, str]:
    root = root.resolve()
    provider_root = root / "providers" / PROVIDER
    configuration = _read_json(provider_root / "generator.json")
    descriptions = configuration.get("skillDescriptions")
    if not isinstance(descriptions, dict) or not all(
        isinstance(name, str) and isinstance(description, str)
        for name, description in descriptions.items()
    ):
        raise GenerationError("skillDescriptions must be a string-to-string object")

    templates = provider_root / "templates"
    skill_template = _template(templates / "skill.md.template")
    agent_template = _template(templates / "agent.toml.template")
    command_template = _template(templates / "command.md.template")
    assets: dict[str, str] = {}

    workflows = _core_files(root, "workflows", ".workflow.md")
    workflow_names = {path.name.removesuffix(".workflow.md") for path in workflows}
    if set(descriptions) != workflow_names:
        missing = sorted(workflow_names - descriptions.keys())
        extra = sorted(descriptions.keys() - workflow_names)
        details = []
        if missing:
            details.append("missing descriptions: " + ", ".join(missing))
        if extra:
            details.append("unknown descriptions: " + ", ".join(extra))
        raise GenerationError("; ".join(details))
    for source_path in workflows:
        name = source_path.name.removesuffix(".workflow.md")
        _validate_skill_description(name, descriptions[name])
        title, body, _ = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        output = f"skills/{name}/SKILL.md"
        assets[output] = _render(
            skill_template,
            {
                "name": name,
                "description": descriptions[name],
                "title": title,
                "source": source,
                "body": body,
            },
            source_path,
        )

    agents = _core_files(root, "agents", ".agent.md")
    for source_path in agents:
        name = source_path.name.removesuffix(".agent.md")
        _, body, content = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        output = f"agents/{name}.toml"
        rendered = _render(
            agent_template,
            {
                "name_toml": json.dumps(name, ensure_ascii=False),
                "description_toml": json.dumps(
                    _purpose_description(body, source_path), ensure_ascii=False
                ),
                "source": source,
                "content": content,
            },
            source_path,
        )
        try:
            parsed = tomllib.loads(rendered)
        except tomllib.TOMLDecodeError as exc:
            raise GenerationError(f"generated invalid TOML for {source_path}: {exc}") from exc
        encoded_instructions = rendered.split('developer_instructions = """\n', 1)[1].rsplit(
            '"""', 1
        )[0]
        if parsed.get("developer_instructions") != encoded_instructions:
            raise GenerationError(
                f"generated TOML changes instruction text for {source_path}; "
                "check backslashes and multiline delimiters"
            )
        assets[output] = rendered

    commands = _core_files(root, "commands", ".command.md")
    for source_path in commands:
        name = source_path.name.removesuffix(".command.md")
        _, body, _ = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        output = f"commands/{name}.md"
        assets[output] = _render(
            command_template,
            {
                "description_yaml": json.dumps(
                    _purpose_description(body, source_path), ensure_ascii=False
                ),
                "name": name,
                "source": source,
                "body": body,
            },
            source_path,
        )

    return dict(sorted(assets.items()))


def generate_claude_assets(root: Path) -> dict[str, str]:
    """Render Claude Code skills, subagents, and compatibility commands."""
    root = root.resolve()
    provider_root = root / "providers" / "claude"
    templates = provider_root / "templates"
    skill_template = _template(templates / "skill.md.template")
    agent_template = _template(templates / "agent.md.template")
    command_template = _template(templates / "command.md.template")
    assets: dict[str, str] = {}

    for source_path in _core_files(root, "workflows", ".workflow.md"):
        name = source_path.name.removesuffix(".workflow.md")
        title, body, _ = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        description = json.dumps(
            _purpose_description(body, source_path), ensure_ascii=False
        )
        rendered = _render(
            skill_template,
            {
                "name": name,
                "description_yaml": description,
                "title": title,
                "source": source,
                "body": body,
            },
            source_path,
        )
        _validate_frontmatter(
            rendered, {"name": name, "description": description}, source_path
        )
        assets[f"skills/{name}/SKILL.md"] = rendered

    for source_path in _core_files(root, "agents", ".agent.md"):
        name = source_path.name.removesuffix(".agent.md")
        _, body, content = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        description = json.dumps(
            _purpose_description(body, source_path), ensure_ascii=False
        )
        rendered = _render(
            agent_template,
            {
                "name": name,
                "description_yaml": description,
                "source": source,
                "content": content,
            },
            source_path,
        )
        _validate_frontmatter(
            rendered,
            {"name": name, "description": description, "model": "inherit"},
            source_path,
        )
        assets[f"agents/{name}.md"] = rendered

    for source_path in _core_files(root, "commands", ".command.md"):
        name = source_path.name.removesuffix(".command.md")
        _, body, _ = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        assets[f"commands/{name}.md"] = _render(
            command_template,
            {
                "name": name,
                "source": source,
                "body": body,
            },
            source_path,
        )

    return dict(sorted(assets.items()))


def generate_cursor_assets(root: Path) -> dict[str, str]:
    """Render scoped Cursor project rules and beta custom commands."""
    root = root.resolve()
    provider_root = root / "providers" / "cursor"
    templates = provider_root / "templates"
    rule_template = _template(templates / "rule.mdc.template")
    command_template = _template(templates / "command.md.template")
    assets: dict[str, str] = {}

    for source_path in _core_files(root, "workflows", ".workflow.md"):
        name = source_path.name.removesuffix(".workflow.md")
        title, body, _ = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        description = json.dumps(
            _purpose_description(body, source_path), ensure_ascii=False
        )
        rendered = _render(
            rule_template,
            {
                "description_yaml": description,
                "title": title,
                "source": source,
                "body": body,
            },
            source_path,
        )
        _validate_frontmatter(
            rendered,
            {"description": description, "globs": "", "alwaysApply": "false"},
            source_path,
        )
        assets[f"rules/{name}.mdc"] = rendered

    for source_path in _core_files(root, "commands", ".command.md"):
        name = source_path.name.removesuffix(".command.md")
        _, body, _ = _read_core_document(source_path)
        source = source_path.relative_to(root).as_posix()
        assets[f"commands/{name}.md"] = _render(
            command_template,
            {
                "name": name,
                "source": source,
                "body": body,
            },
            source_path,
        )

    return dict(sorted(assets.items()))


def generate_provider_assets(root: Path, provider: str) -> dict[str, str]:
    generators = {
        "claude": generate_claude_assets,
        "codex": generate_codex_assets,
        "cursor": generate_cursor_assets,
    }
    try:
        generator = generators[provider]
    except KeyError as exc:
        raise GenerationError(f"unsupported provider: {provider}") from exc
    return generator(root)


def _existing_asset_paths(
    output_root: Path, provider: str = PROVIDER
) -> Iterable[Path]:
    for pattern in ASSET_GLOBS[provider]:
        yield from output_root.glob(pattern)


def compare_assets(
    assets: dict[str, str], output_root: Path, provider: str = PROVIDER
) -> list[Drift]:
    output_root = output_root.resolve()
    expected = set(assets)
    drift: list[Drift] = []
    for relative_path, content in assets.items():
        path = output_root / relative_path
        if not path.is_file():
            drift.append(Drift(relative_path, "missing"))
        elif path.read_text(encoding="utf-8") != content:
            drift.append(Drift(relative_path, "changed"))
    for path in _existing_asset_paths(output_root, provider):
        relative_path = path.relative_to(output_root).as_posix()
        if relative_path not in expected:
            drift.append(Drift(relative_path, "unexpected"))
    return sorted(drift)


def write_assets(assets: dict[str, str], output_root: Path) -> None:
    for relative_path, content in assets.items():
        path = output_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the script's parent repository)",
    )
    parser.add_argument(
        "--provider",
        choices=[*PROVIDERS, "all"],
        default="all",
        help="provider to generate (defaults to all)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="provider output root (defaults to providers/<provider>)",
    )
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    root = args.root.resolve()
    if args.provider == "all" and args.output:
        message = "--output requires one explicit --provider"
        if args.json:
            print(json.dumps({"status": "fail", "error": message}, sort_keys=True))
        else:
            print(f"generation failed: {message}", file=sys.stderr)
        return 2

    providers = PROVIDERS if args.provider == "all" else (args.provider,)
    results: dict[str, dict[str, Any]] = {}
    try:
        generated = {
            provider: generate_provider_assets(root, provider) for provider in providers
        }
        for provider in providers:
            output_root = (
                args.output if args.output else root / "providers" / provider
            ).resolve()
            assets = generated[provider]
            if not args.check:
                write_assets(assets, output_root)
            drift = compare_assets(assets, output_root, provider)
            results[provider] = {
                "assets": len(assets),
                "drift": [asdict(item) for item in drift],
            }
    except (GenerationError, OSError) as exc:
        if args.json:
            print(json.dumps({"status": "fail", "error": str(exc)}, sort_keys=True))
        else:
            print(f"generation failed: {exc}", file=sys.stderr)
        return 1

    failed = any(result["drift"] for result in results.values())
    asset_count = sum(result["assets"] for result in results.values())
    if len(providers) == 1:
        provider = providers[0]
        result = {
            "status": "fail" if failed else "pass",
            "provider": provider,
            **results[provider],
        }
    else:
        result = {
            "status": "fail" if failed else "pass",
            "provider": "all",
            "assets": asset_count,
            "providers": results,
        }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif failed:
        drift_count = 0
        for provider, provider_result in results.items():
            for item in provider_result["drift"]:
                drift_count += 1
                print(
                    f"providers/{provider}/{item['path']}: {item['reason']}",
                    file=sys.stderr,
                )
        print(
            f"provider generation failed: {drift_count} drifted asset(s)",
            file=sys.stderr,
        )
    else:
        action = "checked" if args.check else "generated"
        if len(providers) == 1:
            print(f"{action}: {asset_count} {providers[0]} assets")
        else:
            print(f"{action}: {asset_count} assets across {len(providers)} providers")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
