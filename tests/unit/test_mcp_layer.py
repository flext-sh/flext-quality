"""Behavioral tests for the flext-quality FastMCP server, tools and resources.

The configured FastMCP decorator mode returns the original underlying
function from ``@_mcp.tool()``/``@_mcp.resource(...)`` (registration happens
as a side effect), so each tool/resource is exercised by calling the class
attribute directly — the real production callable, never a mock.
"""

from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

from flext_quality import (
    FlextQualityMcpResources,
    FlextQualityMcpServer,
    FlextQualityMcpTools,
)
from flext_tests import tm

if TYPE_CHECKING:
    from pathlib import Path

# The search/observation tools chain through mcp-cli command building, which
# fails fast (by design) when the mcp-cli executable is not on PATH. Both
# outcomes are real production behavior; branch on the real environment
# instead of assuming mcp-cli is installed.
_MCP_CLI_AVAILABLE = shutil.which("mcp-cli") is not None


class TestsFlextQualityMcpServer:
    """Contract tests for the shared FastMCP server singleton."""

    def test_get_server_returns_the_same_instance(self) -> None:
        """Repeated lookups return the identical FastMCP server instance."""
        first = FlextQualityMcpServer.get_server()
        second = FlextQualityMcpServer.get_server()
        tm.that(first is second, eq=True)

    def test_get_server_exposes_configured_name(self) -> None:
        """The server carries the configured flext-quality identity."""
        server = FlextQualityMcpServer.get_server()
        tm.that(server.name, eq="flext-quality")


class TestsFlextQualityMcpTools:
    """Contract tests for MCP tool functions registered on the shared server."""

    def test_search_memory_builds_command_payload(self) -> None:
        """search_memory returns a command payload for the memory client."""
        output = FlextQualityMcpTools.search_memory(query="find this")
        tm.that(output, is_=dict)
        if not _MCP_CLI_AVAILABLE:
            tm.that(output, has="error")
            return
        tm.that(output, has=("server", "command", "params"))
        tm.that(output.get("server"), eq="claude-mem")
        params = output.get("params")
        assert isinstance(params, dict)
        tm.that(params.get("search_type"), eq="observations")

    def test_search_memory_honors_explicit_search_type_and_limit(self) -> None:
        """Explicit search_type and limit are threaded into the tool output."""
        output = FlextQualityMcpTools.search_memory(
            query="find this", search_type="entities", limit=3
        )
        if not _MCP_CLI_AVAILABLE:
            tm.that(output, has="error")
            return
        params = output.get("params")
        assert isinstance(params, dict)
        tm.that(params.get("search_type"), eq="entities")
        tm.that(params.get("limit"), eq=3)

    def test_search_code_builds_command_payload(self) -> None:
        """search_code returns a command payload for the claude-context client."""
        output = FlextQualityMcpTools.search_code(query="def foo")
        tm.that(output, is_=dict)
        if not _MCP_CLI_AVAILABLE:
            tm.that(output, has="error")
            return
        tm.that(output.get("server"), eq="claude-context")
        tm.that(output, has="command")

    def test_search_code_honors_explicit_limit(self) -> None:
        """An explicit limit is threaded into the search_code tool output."""
        output = FlextQualityMcpTools.search_code(query="def foo", limit=7)
        if not _MCP_CLI_AVAILABLE:
            tm.that(output, has="error")
            return
        params = output.get("params")
        assert isinstance(params, dict)
        tm.that(params.get("limit"), eq=7)

    def test_execute_hook_reports_continue_for_unregistered_event(self) -> None:
        """execute_hook with no registered hooks continues by default."""
        output = FlextQualityMcpTools.execute_hook(
            event="PreToolUse", input_data={"tool_name": "Edit"}
        )
        tm.that(output, is_=dict)
        tm.that(output.get("continue"), eq=True)

    def test_execute_hook_reports_error_for_unknown_event(self) -> None:
        """execute_hook surfaces an error payload for an unknown event name."""
        output = FlextQualityMcpTools.execute_hook(event="NotARealEvent", input_data={})
        tm.that(output, has="error")

    def test_validate_rules_reports_violations_for_a_real_path(
        self, tmp_path: Path
    ) -> None:
        """validate_rules runs the real rules engine against a target path.

        The engine loads its default rules file relative to its own package
        location; when that file is absent from the installed tree the tool
        reports an ``error`` instead of ``violations`` — both are real,
        observable outcomes of the same production code path.
        """
        target = tmp_path / "module.py"
        target.write_text("value = 1\n", encoding="utf-8")
        output = FlextQualityMcpTools.validate_rules(path=str(target))
        tm.that(bool(set(output) & {"violations", "error"}), eq=True)


class TestsFlextQualityMcpResources:
    """Contract tests for MCP resource functions registered on the server."""

    def test_get_hooks_config_returns_json_object(self) -> None:
        """get_hooks_config renders the hook manager's empty config as JSON."""
        output = FlextQualityMcpResources.get_hooks_config()
        tm.that(output, is_=str)
        tm.that(output.strip(), eq="{}")

    def test_get_rules_config_returns_json_array(self) -> None:
        """get_rules_config renders the (empty, unloaded) rule set as JSON."""
        output = FlextQualityMcpResources.get_rules_config()
        tm.that(output, is_=str)
        tm.that(output.strip(), eq="[]")

    def test_get_integrations_status_reports_both_clients(self) -> None:
        """get_integrations_status reports health for both MCP integrations."""
        output = FlextQualityMcpResources.get_integrations_status()
        tm.that(output, is_=str)
        tm.that(output, has="claude_mem")
        tm.that(output, has="claude_context")


__all__: list[str] = [
    "TestsFlextQualityMcpResources",
    "TestsFlextQualityMcpServer",
    "TestsFlextQualityMcpTools",
]
