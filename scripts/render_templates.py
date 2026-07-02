#!/usr/bin/env python3
"""Render strict lower-snake-case placeholders in text templates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Mapping


PLACEHOLDER_PATTERN = re.compile(r"{{([a-z][a-z0-9_]*)}}")
ANY_PLACEHOLDER_PATTERN = re.compile(r"{{([^{}]+)}}")


class TemplateError(ValueError):
    """Raised when a template cannot be rendered safely."""


def render_template(template: str, values: Mapping[str, str]) -> str:
    """Render one pass of strict placeholders without interpreting inserted text."""
    template_without_valid_placeholders = PLACEHOLDER_PATTERN.sub("", template)
    malformed = sorted(
        {
            match.group(1)
            for match in ANY_PLACEHOLDER_PATTERN.finditer(template)
            if not PLACEHOLDER_PATTERN.fullmatch(match.group(0))
        }
    )
    has_unbalanced_braces = (
        "{{" in template_without_valid_placeholders
        or "}}" in template_without_valid_placeholders
    )
    if malformed or has_unbalanced_braces:
        if not malformed:
            malformed.append("unbalanced braces")
        raise TemplateError("invalid placeholders: " + ", ".join(malformed))

    required = set(PLACEHOLDER_PATTERN.findall(template))
    missing = sorted(required - values.keys())
    unused = sorted(values.keys() - required)
    if missing:
        raise TemplateError("missing values: " + ", ".join(missing))
    if unused:
        raise TemplateError("unused values: " + ", ".join(unused))

    return PLACEHOLDER_PATTERN.sub(lambda match: values[match.group(1)], template)


def _load_values(path: Path) -> dict[str, str]:
    try:
        values = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TemplateError(f"cannot read values: {exc}") from exc
    if not isinstance(values, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in values.items()
    ):
        raise TemplateError("values must be a JSON object containing only strings")
    return values


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path, help="template file to render")
    parser.add_argument("--values", type=Path, required=True, help="JSON string-value object")
    parser.add_argument("--output", type=Path, help="write output instead of stdout")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare rendered content with --output without writing",
    )
    args = parser.parse_args(argv)
    if args.check and args.output is None:
        parser.error("--check requires --output")
    return args


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        template = args.template.read_text(encoding="utf-8")
        rendered = render_template(template, _load_values(args.values))
    except (OSError, TemplateError) as exc:
        print(f"render failed: {exc}", file=sys.stderr)
        return 1

    if args.check:
        try:
            current = args.output.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"render check failed: {exc}", file=sys.stderr)
            return 1
        if current != rendered:
            print(f"render check failed: {args.output} is out of date", file=sys.stderr)
            return 1
        print(f"render check passed: {args.output}")
        return 0

    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"rendered: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
