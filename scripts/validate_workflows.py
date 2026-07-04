#!/usr/bin/env python3
"""Validate canonical workflow documents and repository-local Markdown links."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

if __package__:
    from . import generate_provider_assets as provider_generator
else:
    try:
        from scripts import generate_provider_assets as provider_generator
    except ModuleNotFoundError:
        import generate_provider_assets as provider_generator


LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SCHEMA_FILES = ("workflow.schema.json", "agent.schema.json", "command.schema.json")
LINK_ROOTS = ("README.md", "AGENTS.md", "core", "docs", "examples", "mcp", "providers")


@dataclass(frozen=True, order=True)
class ValidationError:
    path: str
    line: int
    code: str
    message: str


@dataclass(frozen=True)
class Document:
    title: str
    title_line: int
    headings: tuple[tuple[str, int], ...]
    sections: dict[str, str]


def _active_lines(text: str) -> Iterable[tuple[int, str]]:
    """Yield lines outside fenced code blocks."""
    fence: str | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in {"```", "~~~"}:
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            yield number, line


def parse_document(text: str) -> Document:
    active = list(_active_lines(text))
    titles = [(line[2:].strip(), number) for number, line in active if line.startswith("# ")]
    headings = tuple(
        (line[3:].strip(), number) for number, line in active if line.startswith("## ")
    )
    sections: dict[str, str] = {}
    lines = text.splitlines()
    for index, (heading, line_number) in enumerate(headings):
        end = headings[index + 1][1] - 1 if index + 1 < len(headings) else len(lines)
        sections[heading] = "\n".join(lines[line_number:end]).strip()
    title, title_line = titles[0] if titles else ("", 1)
    return Document(title, title_line, headings, sections)


def _load_schema(path: Path, root: Path) -> tuple[dict[str, Any] | None, list[ValidationError]]:
    relative = path.relative_to(root).as_posix()
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [ValidationError(relative, 1, "invalid-schema", str(exc))]
    if not isinstance(schema, dict):
        return None, [
            ValidationError(relative, 1, "invalid-schema", "schema root must be an object")
        ]

    errors: list[ValidationError] = []
    required_keys = {"$schema", "$id", "type", "properties", "x-markdown"}
    missing = sorted(required_keys - schema.keys())
    if missing:
        errors.append(
            ValidationError(relative, 1, "invalid-schema", f"missing keys: {', '.join(missing)}")
        )
    try:
        section_schema = schema["properties"]["sections"]
        required_sections = section_schema["required"]
        declared_sections = section_schema["properties"]
        metadata = schema["x-markdown"]
        if not isinstance(required_sections, list) or not all(
            isinstance(section, str) for section in required_sections
        ):
            raise TypeError("section requirements must be a list of strings")
        if not isinstance(declared_sections, dict):
            raise TypeError("section properties must be an object")
        if required_sections != list(declared_sections):
            errors.append(
                ValidationError(
                    relative,
                    1,
                    "invalid-schema",
                    "section properties must appear in required order",
                )
            )
        if not metadata["directory"] or not metadata["fileSuffix"]:
            raise KeyError("directory or fileSuffix")
    except (KeyError, TypeError) as exc:
        errors.append(
            ValidationError(relative, 1, "invalid-schema", f"invalid document metadata: {exc}")
        )
    return schema, errors


def _validate_document(path: Path, root: Path, schema: dict[str, Any]) -> list[ValidationError]:
    relative = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    document = parse_document(text)
    errors: list[ValidationError] = []
    suffix = schema["x-markdown"]["fileSuffix"]
    name = path.name[: -len(suffix)]
    name_pattern = schema["properties"]["name"]["pattern"]
    expected_sections = schema["properties"]["sections"]["required"]
    actual_sections = [heading for heading, _ in document.headings]
    first_content_line = next(
        ((number, line) for number, line in _active_lines(text) if line.strip()),
        (1, ""),
    )

    if not re.fullmatch(name_pattern, name):
        errors.append(
            ValidationError(relative, 1, "invalid-filename", "name must use lowercase kebab-case")
        )
    if not document.title:
        errors.append(ValidationError(relative, 1, "missing-title", "expected exactly one H1 title"))
    else:
        title_count = sum(1 for _, line in _active_lines(text) if line.startswith("# "))
        if title_count != 1:
            errors.append(
                ValidationError(
                    relative,
                    document.title_line,
                    "invalid-title",
                    "expected exactly one H1 title",
                )
            )
        if first_content_line[0] != document.title_line:
            errors.append(
                ValidationError(
                    relative,
                    first_content_line[0],
                    "invalid-title-position",
                    "H1 title must be the first non-empty line",
                )
            )
        prefix = schema["x-markdown"].get("titlePrefix", "")
        expected_title = f"{prefix}{name}" if prefix else None
        if expected_title and document.title != expected_title:
            errors.append(
                ValidationError(
                    relative,
                    document.title_line,
                    "title-mismatch",
                    f"expected title '# {expected_title}'",
                )
            )

    if actual_sections != expected_sections:
        errors.append(
            ValidationError(
                relative,
                document.headings[0][1] if document.headings else 1,
                "invalid-sections",
                "expected H2 sections in this order: " + ", ".join(expected_sections),
            )
        )
    for heading, line_number in document.headings:
        if heading in expected_sections and not document.sections.get(heading):
            errors.append(
                ValidationError(
                    relative,
                    line_number,
                    "empty-section",
                    f"section '{heading}' is empty",
                )
            )
    return errors


def _markdown_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for entry in LINK_ROOTS:
        path = root / entry
        if path.is_file():
            files.add(path)
        elif path.is_dir():
            files.update(path.rglob("*.md"))
    return sorted(files)


def _validate_links(path: Path, root: Path) -> tuple[int, list[ValidationError]]:
    relative = path.relative_to(root).as_posix()
    errors: list[ValidationError] = []
    checked = 0
    for line_number, line in _active_lines(path.read_text(encoding="utf-8")):
        for match in LINK_PATTERN.finditer(line):
            raw_target = match.group(1).strip()
            if raw_target.startswith("<") and raw_target.endswith(">"):
                raw_target = raw_target[1:-1]
            target = raw_target.split(maxsplit=1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            checked += 1
            file_target = unquote(target.split("#", 1)[0])
            resolved = (path.parent / file_target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(
                    ValidationError(
                        relative,
                        line_number,
                        "unsafe-link",
                        f"link escapes repository: {target}",
                    )
                )
                continue
            if not resolved.exists():
                errors.append(
                    ValidationError(relative, line_number, "broken-link", f"target does not exist: {target}")
                )
    return checked, errors


def validate_repository(root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors: list[ValidationError] = []
    counts = {
        "workflows": 0,
        "agents": 0,
        "commands": 0,
        "schemas": 0,
        "providerAssets": 0,
        "links": 0,
    }

    schema_dir = root / "core" / "schemas"
    for schema_name in SCHEMA_FILES:
        schema_path = schema_dir / schema_name
        if not schema_path.is_file():
            errors.append(
                ValidationError(schema_path.relative_to(root).as_posix(), 1, "missing-schema", "file not found")
            )
            continue
        schema, schema_errors = _load_schema(schema_path, root)
        errors.extend(schema_errors)
        if schema is None or schema_errors:
            continue
        counts["schemas"] += 1
        metadata = schema["x-markdown"]
        directory = root / metadata["directory"]
        suffix = metadata["fileSuffix"]
        documents = sorted(directory.glob(f"*{suffix}")) if directory.is_dir() else []
        kind = schema_name.removesuffix(".schema.json")
        count_key = f"{kind}s"
        counts[count_key] = len(documents)
        if not documents:
            errors.append(
                ValidationError(
                    metadata["directory"],
                    1,
                    "missing-documents",
                    f"no *{suffix} files found",
                )
            )
        for markdown_file in sorted(directory.glob("*.md")):
            if not markdown_file.name.endswith(suffix):
                errors.append(
                    ValidationError(
                        markdown_file.relative_to(root).as_posix(),
                        1,
                        "invalid-filename",
                        f"canonical files in this directory must end with {suffix}",
                    )
                )
        for document in documents:
            errors.extend(_validate_document(document, root, schema))

    for provider in provider_generator.PROVIDERS:
        try:
            assets = provider_generator.generate_provider_assets(root, provider)
            drift = provider_generator.compare_assets(
                assets, root / "providers" / provider, provider
            )
        except (provider_generator.GenerationError, OSError) as exc:
            errors.append(
                ValidationError(
                    f"providers/{provider}",
                    1,
                    "invalid-provider",
                    str(exc),
                )
            )
            continue
        counts["providerAssets"] += len(assets)
        for item in drift:
            errors.append(
                ValidationError(
                    f"providers/{provider}/{item.path}",
                    1,
                    "provider-drift",
                    item.reason,
                )
            )

    for markdown_file in _markdown_files(root):
        checked, link_errors = _validate_links(markdown_file, root)
        counts["links"] += checked
        errors.extend(link_errors)

    ordered_errors = sorted(set(errors))
    return {
        "status": "pass" if not ordered_errors else "fail",
        "counts": counts,
        "errors": [asdict(error) for error in ordered_errors],
    }


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the script's parent repository)",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    result = validate_repository(args.root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif result["status"] == "pass":
        counts = result["counts"]
        print(
            "validated: "
            f"{counts['workflows']} workflows, {counts['agents']} agents, "
            f"{counts['commands']} commands, {counts['schemas']} schemas, "
            f"{counts['providerAssets']} provider assets, "
            f"{counts['links']} local links"
        )
    else:
        for error in result["errors"]:
            print(
                f"{error['path']}:{error['line']}: {error['code']}: {error['message']}",
                file=sys.stderr,
            )
        print(f"validation failed: {len(result['errors'])} error(s)", file=sys.stderr)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
