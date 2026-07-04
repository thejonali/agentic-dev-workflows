#!/usr/bin/env python3
"""Generate deterministic Phase 8 installation and repository-guide examples."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

if __package__:
    from . import generate_provider_assets as provider_generator
    from .render_templates import TemplateError, render_template
else:
    import generate_provider_assets as provider_generator
    from render_templates import TemplateError, render_template


GENERATED_DIRECTORIES = ("provider-installations", "repository-guides")


class ExampleGenerationError(ValueError):
    """Raised when example inputs or output paths are invalid."""


def _read_configuration(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ExampleGenerationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ExampleGenerationError(f"{path} must contain a JSON object")
    return value


def _relative_path(value: Any, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ExampleGenerationError(f"{label} must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ExampleGenerationError(f"{label} must stay within the repository")
    return path


def generate_examples(root: Path) -> dict[str, str]:
    root = root.resolve()
    configuration = _read_configuration(root / "examples" / "generator.json")
    installations = configuration.get("providerInstallations")
    guides = configuration.get("agentGuides")
    if not isinstance(installations, list) or not all(
        isinstance(item, dict) for item in installations
    ):
        raise ExampleGenerationError("providerInstallations must be a list of objects")
    if not isinstance(guides, dict) or not all(
        isinstance(name, str) and isinstance(values, dict)
        for name, values in guides.items()
    ):
        raise ExampleGenerationError("agentGuides must be an object of value objects")

    assets: dict[str, str] = {}
    for index, installation in enumerate(installations):
        source = _relative_path(
            installation.get("source"), f"providerInstallations[{index}].source"
        )
        output = _relative_path(
            installation.get("output"), f"providerInstallations[{index}].output"
        )
        if source.parts[:1] != ("providers",):
            raise ExampleGenerationError(
                "provider installation sources must be under providers/"
            )
        if output.parts[:1] != ("provider-installations",):
            raise ExampleGenerationError(
                "provider installation outputs must be under provider-installations/"
            )
        source_path = root / Path(*source.parts)
        try:
            content = source_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ExampleGenerationError(f"cannot read {source_path}: {exc}") from exc
        output_text = output.as_posix()
        if output_text in assets:
            raise ExampleGenerationError(f"duplicate example output: {output_text}")
        assets[output_text] = content

    try:
        template = (root / "core" / "templates" / "AGENTS.template.md").read_text(
            encoding="utf-8"
        )
    except OSError as exc:
        raise ExampleGenerationError(f"cannot read AGENTS template: {exc}") from exc
    for name, values in sorted(guides.items()):
        if not provider_generator.NAME_PATTERN.fullmatch(name):
            raise ExampleGenerationError(f"invalid agent guide name: {name}")
        if not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in values.items()
        ):
            raise ExampleGenerationError(
                f"agent guide values for {name} must be strings"
            )
        try:
            content = render_template(template, values)
        except TemplateError as exc:
            raise ExampleGenerationError(
                f"cannot render agent guide {name}: {exc}"
            ) from exc
        assets[f"repository-guides/{name}/AGENTS.md"] = content

    return dict(sorted(assets.items()))


def _existing_example_paths(output_root: Path) -> Iterable[Path]:
    for directory in GENERATED_DIRECTORIES:
        path = output_root / directory
        if path.is_dir():
            yield from path.rglob("*")


def compare_examples(
    assets: dict[str, str], output_root: Path
) -> list[provider_generator.Drift]:
    output_root = output_root.resolve()
    expected = set(assets)
    drift: list[provider_generator.Drift] = []
    for relative_path, content in assets.items():
        path = output_root / relative_path
        if not path.is_file():
            drift.append(provider_generator.Drift(relative_path, "missing"))
        elif path.read_text(encoding="utf-8") != content:
            drift.append(provider_generator.Drift(relative_path, "changed"))
    for path in _existing_example_paths(output_root):
        if not path.is_file():
            continue
        relative_path = path.relative_to(output_root).as_posix()
        if relative_path not in expected:
            drift.append(provider_generator.Drift(relative_path, "unexpected"))
    return sorted(drift)


def write_examples(assets: dict[str, str], output_root: Path) -> None:
    provider_generator.write_assets(assets, output_root)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the script's parent repository)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="example output root (defaults to <root>/examples)",
    )
    parser.add_argument(
        "--check", action="store_true", help="report drift without writing"
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    root = args.root.resolve()
    output_root = (args.output or root / "examples").resolve()
    try:
        assets = generate_examples(root)
        if not args.check:
            write_examples(assets, output_root)
        drift = compare_examples(assets, output_root)
    except (ExampleGenerationError, OSError) as exc:
        if args.json:
            print(json.dumps({"status": "fail", "error": str(exc)}, sort_keys=True))
        else:
            print(f"example generation failed: {exc}", file=sys.stderr)
        return 1

    result = {
        "status": "pass" if not drift else "fail",
        "assets": len(assets),
        "drift": [asdict(item) for item in drift],
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif drift:
        for item in drift:
            print(f"{item.path}: {item.reason}", file=sys.stderr)
        print(
            f"example generation failed: {len(drift)} drifted asset(s)", file=sys.stderr
        )
    else:
        action = "checked" if args.check else "generated"
        print(f"{action}: {len(assets)} example assets")
    return 0 if not drift else 1


if __name__ == "__main__":
    raise SystemExit(main())
