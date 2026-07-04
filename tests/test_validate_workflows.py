from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_workflows.py"
SPEC = importlib.util.spec_from_file_location("validate_workflows", SCRIPT_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ValidateWorkflowsTests(unittest.TestCase):
    def test_repository_validation_covers_all_generated_providers(self) -> None:
        result = VALIDATOR.validate_repository(SCRIPT_PATH.parents[1])

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["counts"]["providerAssets"], 93)

    def test_mcp_documentation_is_checked_for_local_links(self) -> None:
        root = SCRIPT_PATH.parents[1]
        files = {
            path.relative_to(root).as_posix()
            for path in VALIDATOR._markdown_files(root)
        }

        self.assertIn("mcp/workflow-server/README.md", files)

    def test_parser_ignores_headings_inside_fenced_code(self) -> None:
        document = VALIDATOR.parse_document(
            "# Demo\n\n## Purpose\n\nText.\n\n```md\n## Not A Section\n```\n"
        )

        self.assertEqual(document.title, "Demo")
        self.assertEqual(document.headings, (("Purpose", 3),))

    def test_document_rejects_wrong_section_order(self) -> None:
        schema = {
            "properties": {
                "name": {"pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"},
                "sections": {"required": ["Purpose", "Inputs"]},
            },
            "x-markdown": {"fileSuffix": ".workflow.md"},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "demo.workflow.md"
            path.write_text("# Demo\n\n## Inputs\n\nInput.\n\n## Purpose\n\nPurpose.\n")

            errors = VALIDATOR._validate_document(path, root, schema)

        self.assertIn("invalid-sections", {error.code for error in errors})

    def test_command_title_must_match_filename(self) -> None:
        schema = {
            "properties": {
                "name": {"pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"},
                "sections": {"required": ["Purpose"]},
            },
            "x-markdown": {"fileSuffix": ".command.md", "titlePrefix": "/"},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "expected.command.md"
            path.write_text("# /different\n\n## Purpose\n\nPurpose.\n")

            errors = VALIDATOR._validate_document(path, root, schema)

        self.assertIn("title-mismatch", {error.code for error in errors})

    def test_title_must_be_first_content(self) -> None:
        schema = {
            "properties": {
                "name": {"pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"},
                "sections": {"required": ["Purpose"]},
            },
            "x-markdown": {"fileSuffix": ".workflow.md"},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "demo.workflow.md"
            path.write_text("Intro.\n\n# Demo\n\n## Purpose\n\nPurpose.\n")

            errors = VALIDATOR._validate_document(path, root, schema)

        self.assertIn("invalid-title-position", {error.code for error in errors})

    def test_broken_local_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("[missing](docs/missing.md)\n")

            checked, errors = VALIDATOR._validate_links(path, root)

        self.assertEqual(checked, 1)
        self.assertEqual([error.code for error in errors], ["broken-link"])


if __name__ == "__main__":
    unittest.main()
