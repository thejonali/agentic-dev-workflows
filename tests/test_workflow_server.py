from __future__ import annotations

import asyncio
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SERVER_SRC = ROOT / "mcp" / "workflow-server" / "src"
sys.path.insert(0, str(SERVER_SRC))

from workflow_library_mcp import service  # noqa: E402

try:
    SDK_AVAILABLE = importlib.util.find_spec("mcp.client.session") is not None
except ModuleNotFoundError:
    SDK_AVAILABLE = False


class WorkflowServiceTests(unittest.TestCase):
    def test_list_and_get_workflows_return_canonical_metadata(self) -> None:
        listed = service.list_workflows(category="test-gap-analysis")
        workflow = service.get_workflow("testing")

        self.assertEqual([item["name"] for item in listed["workflows"]], ["testing"])
        self.assertIn("test-gap-analysis", workflow["commands"])
        self.assertEqual(
            " ".join(workflow["sections"]["Purpose"].split()), workflow["description"]
        )
        self.assertFalse(workflow["truncated"])

    def test_unknown_workflow_is_a_structured_error(self) -> None:
        result = service.structured_call(service.get_workflow, "does-not-exist")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"]["code"], "workflow-not-found")

    def test_workflow_markdown_is_bounded(self) -> None:
        workflow = service.get_workflow("safe-change", max_chars=1_000)

        self.assertEqual(len(workflow["markdown"]), 1_000)
        self.assertGreater(workflow["totalChars"], 1_000)
        self.assertTrue(workflow["truncated"])

    def test_render_reuses_each_checked_in_provider_output(self) -> None:
        expected_paths = {
            "claude": "skills/safe-change/SKILL.md",
            "codex": "skills/safe-change/SKILL.md",
            "cursor": "rules/safe-change.mdc",
        }

        for provider, asset_path in expected_paths.items():
            rendered = service.render_provider_asset("safe-change", provider)
            expected = (ROOT / "providers" / provider / asset_path).read_text(
                encoding="utf-8"
            )
            self.assertEqual(rendered["content"], expected)
            self.assertEqual(rendered["assetPath"], asset_path)
            self.assertFalse(rendered["truncated"])

    def test_validation_reuses_repository_validator(self) -> None:
        result = service.validate_workflow("review")

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["repositoryStatus"], "pass")
        self.assertEqual(result["errors"], [])

    def test_repo_health_is_bounded_and_does_not_execute_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tests").mkdir()
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                "invalid on purpose\n", encoding="utf-8"
            )
            (root / "tests/test_demo.py").write_text(
                "raise RuntimeError('must not execute')\n", encoding="utf-8"
            )

            result = service.score_repo_health(directory)

        self.assertEqual(result["evidenceFilesScanned"], 3)
        self.assertGreater(result["dimensions"]["testing"]["score"], 0)
        self.assertIn("no repository code was executed", result["method"])

    def test_configured_library_root_must_contain_repository_scripts(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.dict(os.environ, {"WORKFLOW_LIBRARY_ROOT": directory}),
        ):
            sys.modules.pop("scripts.generate_provider_assets", None)
            sys.modules.pop("scripts.validate_workflows", None)
            sys.modules.pop("scripts", None)
            result = service.structured_call(service.list_workflows)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"]["code"], "invalid-library-root")


@unittest.skipUnless(SDK_AVAILABLE, "MCP SDK is not installed")
class McpProtocolTests(unittest.TestCase):
    def test_stdio_server_lists_and_calls_tools(self) -> None:
        async def exercise_server() -> None:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(SERVER_SRC)
            environment["WORKFLOW_LIBRARY_ROOT"] = str(ROOT)
            parameters = StdioServerParameters(
                command=sys.executable,
                args=["-m", "workflow_library_mcp.server"],
                env=environment,
            )
            async with stdio_client(parameters) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    called = await session.call_tool("list_workflows", {"limit": 1})

            self.assertEqual(
                {tool.name for tool in tools.tools},
                {
                    "get_workflow",
                    "list_workflows",
                    "render_provider_asset",
                    "score_repo_health",
                    "validate_workflow",
                },
            )
            self.assertTrue(all(tool.annotations.readOnlyHint for tool in tools.tools))
            self.assertTrue(
                all(not tool.annotations.destructiveHint for tool in tools.tools)
            )
            self.assertFalse(called.isError)
            self.assertEqual(called.structuredContent["status"], "ok")
            self.assertEqual(called.structuredContent["result"]["count"], 1)

        asyncio.run(exercise_server())


if __name__ == "__main__":
    unittest.main()
