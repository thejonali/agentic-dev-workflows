from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import unittest
import zipfile

from scripts import build_release


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"


class BuildReleaseTests(unittest.TestCase):
    def test_release_archives_have_expected_installation_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            artifacts = build_release.build_release(ROOT, VERSION, output)
            names = {path.name for path in artifacts}
            archive_entries = {}
            for path in artifacts:
                if path.suffix == ".zip":
                    with zipfile.ZipFile(path) as archive:
                        archive_entries[path.name] = set(archive.namelist())

        self.assertEqual(
            names,
            {
                "SHA256SUMS-v0.1.0.txt",
                "agentic-dev-workflows-v0.1.0.zip",
                "agentic-dev-workflows-claude-v0.1.0.zip",
                "agentic-dev-workflows-codex-v0.1.0.zip",
                "agentic-dev-workflows-cursor-v0.1.0.zip",
            },
        )
        self.assertIn(
            "agentic-dev-workflows-v0.1.0/core/workflows/safe-change.workflow.md",
            archive_entries["agentic-dev-workflows-v0.1.0.zip"],
        )
        self.assertIn(
            "agentic-dev-workflows-v0.1.0/mcp/workflow-server/pyproject.toml",
            archive_entries["agentic-dev-workflows-v0.1.0.zip"],
        )
        self.assertIn(
            "agentic-dev-workflows-codex-v0.1.0/.agents/skills/safe-change/SKILL.md",
            archive_entries["agentic-dev-workflows-codex-v0.1.0.zip"],
        )
        self.assertIn(
            "agentic-dev-workflows-claude-v0.1.0/.claude/agents/reviewer.md",
            archive_entries["agentic-dev-workflows-claude-v0.1.0.zip"],
        )
        self.assertIn(
            "agentic-dev-workflows-cursor-v0.1.0/.cursor/rules/testing.mdc",
            archive_entries["agentic-dev-workflows-cursor-v0.1.0.zip"],
        )
        for entries in archive_entries.values():
            self.assertFalse(any("__pycache__" in name for name in entries))
            self.assertFalse(
                any(name.startswith("/") or "../" in name for name in entries)
            )

    def test_release_archives_are_byte_for_byte_reproducible(self) -> None:
        with (
            tempfile.TemporaryDirectory() as first,
            tempfile.TemporaryDirectory() as second,
        ):
            first_paths = build_release.build_release(ROOT, VERSION, Path(first))
            second_paths = build_release.build_release(ROOT, VERSION, Path(second))
            first_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in first_paths
            }
            second_hashes = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in second_paths
            }

        self.assertEqual(first_hashes, second_hashes)

    def test_release_version_must_match_package_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(
                build_release.ReleaseBuildError, "does not match MCP package"
            ):
                build_release.build_release(ROOT, "0.2.0", Path(directory))


if __name__ == "__main__":
    unittest.main()
