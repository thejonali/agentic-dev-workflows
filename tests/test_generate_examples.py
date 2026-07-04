from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest

from scripts import generate_examples as examples


ROOT = Path(__file__).resolve().parents[1]


class GenerateExamplesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assets = examples.generate_examples(ROOT)

    def test_checked_in_examples_are_reviewed_snapshots(self) -> None:
        drift = examples.compare_examples(self.assets, ROOT / "examples")

        self.assertEqual(drift, [])
        self.assertEqual(len(self.assets), 6)

    def test_provider_installations_match_generated_provider_assets(self) -> None:
        expected_sources = {
            "provider-installations/codex/.agents/skills/safe-change/SKILL.md": (
                "providers/codex/skills/safe-change/SKILL.md"
            ),
            "provider-installations/claude/.claude/skills/safe-change/SKILL.md": (
                "providers/claude/skills/safe-change/SKILL.md"
            ),
            "provider-installations/cursor/.cursor/rules/safe-change.mdc": (
                "providers/cursor/rules/safe-change.mdc"
            ),
            "provider-installations/cursor/.cursor/rules/testing.mdc": (
                "providers/cursor/rules/testing.mdc"
            ),
        }

        for output, source in expected_sources.items():
            self.assertEqual(
                self.assets[output], (ROOT / source).read_text(encoding="utf-8")
            )

    def test_agent_guides_render_without_template_placeholders(self) -> None:
        python_guide = self.assets["repository-guides/python-cli/AGENTS.md"]
        react_guide = self.assets["repository-guides/react-app/AGENTS.md"]

        self.assertNotIn("{{", python_guide + react_guide)
        self.assertIn("python -m pytest", python_guide)
        self.assertIn("npm run build", react_guide)
        self.assertIn("illustrative", python_guide)
        self.assertIn("illustrative", react_guide)

    def test_write_and_drift_detection_cover_changed_and_unexpected_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            examples.write_examples(self.assets, output)
            changed = output / "repository-guides/python-cli/AGENTS.md"
            changed.write_text("changed\n", encoding="utf-8")
            unexpected = output / "provider-installations/obsolete.md"
            unexpected.write_text("obsolete\n", encoding="utf-8")

            drift = examples.compare_examples(self.assets, output)

        self.assertEqual(
            [(item.path, item.reason) for item in drift],
            [
                ("provider-installations/obsolete.md", "unexpected"),
                ("repository-guides/python-cli/AGENTS.md", "changed"),
            ],
        )

    def test_cli_reports_clean_examples_as_json(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            status = examples.main(["--root", str(ROOT), "--check", "--json"])

        result = json.loads(output.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(result, {"assets": 6, "drift": [], "status": "pass"})


if __name__ == "__main__":
    unittest.main()
