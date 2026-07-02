from __future__ import annotations

from contextlib import redirect_stdout
import io
import tempfile
import unittest
from pathlib import Path

from scripts import generate_provider_assets as generator
from scripts import render_templates as renderer
from scripts.render_templates import TemplateError, render_template


ROOT = Path(__file__).resolve().parents[1]
class RenderTemplateTests(unittest.TestCase):
    def test_render_is_strict_and_non_recursive(self) -> None:
        rendered = render_template("Hello {{name}}", {"name": "{{later}}"})

        self.assertEqual(rendered, "Hello {{later}}")

    def test_missing_and_unused_values_fail(self) -> None:
        with self.assertRaisesRegex(TemplateError, "missing values: name"):
            render_template("Hello {{name}}", {})
        with self.assertRaisesRegex(TemplateError, "unused values: extra"):
            render_template("Hello", {"extra": "value"})

    def test_malformed_placeholder_fails(self) -> None:
        with self.assertRaisesRegex(TemplateError, "invalid placeholders"):
            render_template("Hello {{Display Name}}", {})
        with self.assertRaisesRegex(TemplateError, "unbalanced braces"):
            render_template("Hello {{name", {})

    def test_renderer_cli_writes_and_checks_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template = root / "input.template"
            values = root / "values.json"
            output = root / "output.txt"
            template.write_text("Hello {{name}}\n", encoding="utf-8")
            values.write_text('{"name": "Codex"}\n', encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                write_status = renderer.main(
                    [str(template), "--values", str(values), "--output", str(output)]
                )
                check_status = renderer.main(
                    [
                        str(template),
                        "--values",
                        str(values),
                        "--output",
                        str(output),
                        "--check",
                    ]
                )

            rendered = output.read_text(encoding="utf-8")

        self.assertEqual((write_status, check_status), (0, 0))
        self.assertEqual(rendered, "Hello Codex\n")


class GenerateProviderAssetsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assets = generator.generate_codex_assets(ROOT)

    def test_checked_in_codex_assets_are_reviewed_snapshots(self) -> None:
        drift = generator.compare_assets(self.assets, ROOT / "providers" / "codex")

        self.assertEqual(drift, [])

    def test_write_and_drift_detection_cover_changed_and_unexpected_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            generator.write_assets(self.assets, output)
            changed = output / "agents" / "architect.toml"
            changed.write_text("changed\n", encoding="utf-8")
            unexpected = output / "commands" / "obsolete.md"
            unexpected.write_text("obsolete\n", encoding="utf-8")

            drift = generator.compare_assets(self.assets, output)

        self.assertEqual(
            [(item.path, item.reason) for item in drift],
            [
                ("agents/architect.toml", "changed"),
                ("commands/obsolete.md", "unexpected"),
            ],
        )

    def test_drift_detection_reports_missing_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            drift = generator.compare_assets(
                {"commands/missing.md": "expected\n"}, Path(directory)
            )

        self.assertEqual(
            [(item.path, item.reason) for item in drift],
            [("commands/missing.md", "missing")],
        )


if __name__ == "__main__":
    unittest.main()
