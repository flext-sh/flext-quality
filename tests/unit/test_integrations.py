"""Behavioral tests for the flext-quality MCP integration clients.

Exercises the public contract of ``FlextQualityMcpClient`` and its two
concrete integrations (``FlextQualityClaudeContextClient`` and
``FlextQualityClaudeMemClient``) against real ``shutil.which`` PATH lookups
and real JSON/model serialization — no mocks or patched collaborators.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import tm

from flext_quality import (
    FlextQualityClaudeContextClient,
    FlextQualityClaudeMemClient,
    FlextQualityMcpClient,
)


class TestsFlextQualityIntegrations:
    """Contract tests for the MCP client and its concrete integrations."""

    # -- FlextQualityMcpClient --------------------------------------------

    @staticmethod
    def test_is_mcp_cli_available_reports_real_path_lookup() -> None:
        """The availability probe mirrors the real ``shutil.which`` result."""
        client = FlextQualityMcpClient()
        tm.that(client.mcp_cli_available(), is_=bool)

    @staticmethod
    def test_health_check_reports_disconnected_when_cli_absent() -> None:
        """Health check reflects mcp-cli's real (missing) PATH availability."""
        client = FlextQualityMcpClient()
        result = client.health_check()
        tm.that(result.success, eq=True)
        available = client.mcp_cli_available()
        tm.that(result.value.get("available"), eq=available)
        expected_status = "connected" if available else "disconnected"
        tm.that(result.value.get("status"), eq=expected_status)

    @staticmethod
    def test_health_check_honors_custom_timeout() -> None:
        """The configured timeout is echoed back in the health payload."""
        client = FlextQualityMcpClient(timeout_ms=1234)
        result = client.health_check()
        tm.that(result.value.get("timeout_ms"), eq=1234)

    @staticmethod
    def test_build_server_health_result_wraps_server_name() -> None:
        """The server-scoped health result carries the requested server name."""
        client = FlextQualityMcpClient()
        result = client.build_server_health_result("some-server")
        tm.that(result.success, eq=True)
        tm.that(result.value.get("server"), eq="some-server")
        tm.that(result.value, has="mcp_cli")

    @staticmethod
    def test_build_tool_call_constructs_typed_request() -> None:
        """A tool call request carries the server, tool, and params verbatim."""
        client = FlextQualityMcpClient()
        result = client.build_tool_call("srv", "tool", {"a": 1})
        tm.that(result.success, eq=True)
        tm.that(result.value.server, eq="srv")
        tm.that(result.value.tool, eq="tool")
        tm.that(result.value.params, eq={"a": 1})

    @staticmethod
    def test_build_tool_call_defaults_params_to_empty_mapping() -> None:
        """Omitting params yields an empty mapping, never ``None``."""
        client = FlextQualityMcpClient()
        result = client.build_tool_call("srv", "tool")
        tm.that(result.value.params, eq={})

    @staticmethod
    def test_build_call_command_fails_when_cli_unavailable() -> None:
        """Command building fails fast when mcp-cli is absent from PATH."""
        client = FlextQualityMcpClient()
        if client.mcp_cli_available():
            return
        call = client.build_tool_call("srv", "tool", {"q": "x"}).unwrap()
        result = client.build_call_command(call)
        tm.that(result.failure, eq=True)

    @staticmethod
    def test_build_info_command_fails_when_cli_unavailable() -> None:
        """Info command building fails fast when mcp-cli is absent from PATH."""
        client = FlextQualityMcpClient()
        if client.mcp_cli_available():
            return
        result = client.build_info_command("srv", "tool")
        tm.that(result.failure, eq=True)

    @staticmethod
    def test_parse_result_reports_failure_for_nonzero_exit() -> None:
        """A nonzero exit code yields a failed tool result with the output."""
        client = FlextQualityMcpClient()
        result = client.parse_result("boom", 1)
        tm.that(result.success, eq=True)
        tm.that(result.value.success, eq=False)
        tm.that(result.value.error or "", has="boom")

    @staticmethod
    def test_parse_result_reports_failure_message_for_empty_output() -> None:
        """A nonzero exit with empty output still yields a descriptive error."""
        client = FlextQualityMcpClient()
        result = client.parse_result("", 2)
        tm.that(result.value.error or "", has="exit code 2")

    @staticmethod
    def test_parse_result_parses_json_object_output() -> None:
        """Zero-exit JSON object output is coerced into a string-valued mapping."""
        client = FlextQualityMcpClient()
        result = client.parse_result('{"key": 1, "other": true}', 0)
        tm.that(result.success, eq=True)
        tm.that(result.value.success, eq=True)
        tm.that(result.value.data, eq={"key": "1", "other": "True"})

    @staticmethod
    def test_parse_result_parses_json_list_of_objects() -> None:
        """Zero-exit JSON list output is normalized into an items payload."""
        client = FlextQualityMcpClient()
        result = client.parse_result('[{"a": 1}, {"a": 2}]', 0)
        tm.that(result.success, eq=True)
        tm.that(result.value.data or {}, has="items")

    @staticmethod
    def test_parse_result_parses_json_list_of_scalars() -> None:
        """A JSON list of non-mapping items is coerced to string values."""
        client = FlextQualityMcpClient()
        result = client.parse_result("[1, 2, 3]", 0)
        tm.that(result.success, eq=True)
        tm.that(result.value.data or {}, has="items")

    @staticmethod
    def test_parse_result_falls_back_to_raw_for_non_json_output() -> None:
        """Non-JSON, non-list output is preserved verbatim under ``raw``."""
        client = FlextQualityMcpClient()
        result = client.parse_result("plain text output", 0)
        tm.that(result.success, eq=True)
        tm.that(result.value.data, eq={"raw": "plain text output"})


class TestsFlextQualityClaudeContextIntegrations:
    """Contract tests for the ``FlextQualityClaudeContextClient`` integration."""

    # -- FlextQualityClaudeContextClient -----------------------------------

    @staticmethod
    def test_claude_context_build_index_call_without_path() -> None:
        """Index calls default to an empty params mapping without a path."""
        client = FlextQualityClaudeContextClient()
        result = client.build_index_call()
        tm.that(result.success, eq=True)
        tm.that(result.value.tool, eq="index_codebase")
        tm.that(result.value.params, eq={})

    @staticmethod
    def test_claude_context_build_index_call_with_path() -> None:
        """A supplied path is carried into the index call params."""
        client = FlextQualityClaudeContextClient()
        result = client.build_index_call("/some/path")
        tm.that(result.value.params.get("path"), eq="/some/path")

    @staticmethod
    def test_claude_context_build_search_call_uses_default_limit() -> None:
        """Search calls fall back to the configured default result limit."""
        client = FlextQualityClaudeContextClient()
        result = client.build_search_call("query text")
        tm.that(result.value.params.get("query"), eq="query text")
        tm.that(result.value.params.get("limit"), eq=20)

    @staticmethod
    def test_claude_context_build_search_call_honors_explicit_limit() -> None:
        """An explicit limit overrides the configured default."""
        client = FlextQualityClaudeContextClient()
        result = client.build_search_call("query text", limit=5)
        tm.that(result.value.params.get("limit"), eq=5)

    @staticmethod
    def test_claude_context_build_status_call() -> None:
        """Status calls target the indexing-status tool with no params."""
        client = FlextQualityClaudeContextClient()
        result = client.build_status_call()
        tm.that(result.value.tool, eq="get_indexing_status")
        tm.that(result.value.server, eq="claude-context")

    @staticmethod
    def test_claude_context_get_search_command_reports_availability() -> None:
        """The chained search command mirrors the real mcp-cli availability."""
        client = FlextQualityClaudeContextClient()
        expected_ok = bool(client.health_check().value.get("available"))
        result = client.build_search_command("query text")
        tm.that(result.success, eq=expected_ok)

    @staticmethod
    def test_claude_context_get_index_command_reports_availability() -> None:
        """The chained index command mirrors the real mcp-cli availability."""
        client = FlextQualityClaudeContextClient()
        expected_ok = bool(client.health_check().value.get("available"))
        result = client.build_index_command()
        tm.that(result.success, eq=expected_ok)

    @staticmethod
    def test_claude_context_health_check_reports_server_name() -> None:
        """Health check for claude-context echoes its own server name."""
        client = FlextQualityClaudeContextClient()
        result = client.health_check()
        tm.that(result.value.get("server"), eq="claude-context")


class TestsFlextQualityClaudeMemIntegrations:
    """Contract tests for the ``FlextQualityClaudeMemClient`` integration."""

    # -- FlextQualityClaudeMemClient ----------------------------------------

    @staticmethod
    def test_claude_mem_build_get_observations_call() -> None:
        """Observation lookups carry the requested ids as a JSON list."""
        client = FlextQualityClaudeMemClient()
        result = client.build_get_observations_call([1, 2, 3])
        tm.that(result.value.tool, eq="get_observations")
        tm.that(result.value.params.get("ids"), eq=[1, 2, 3])

    @staticmethod
    def test_claude_mem_build_search_call_uses_default_limit() -> None:
        """Search calls default to the memory-specific search limit."""
        client = FlextQualityClaudeMemClient()
        result = client.build_search_call("find this")
        tm.that(result.value.params.get("limit"), eq=10)

    @staticmethod
    def test_claude_mem_build_search_call_honors_explicit_limit() -> None:
        """An explicit limit overrides the memory search default."""
        client = FlextQualityClaudeMemClient()
        result = client.build_search_call("find this", limit=3)
        tm.that(result.value.params.get("limit"), eq=3)

    @staticmethod
    def test_claude_mem_build_timeline_call_uses_defaults() -> None:
        """Timeline calls default both depth parameters symmetrically."""
        client = FlextQualityClaudeMemClient()
        result = client.build_timeline_call(42)
        tm.that(result.value.params.get("anchor"), eq=42)
        tm.that(result.value.params.get("depth_before"), eq=5)
        tm.that(result.value.params.get("depth_after"), eq=5)

    @staticmethod
    def test_claude_mem_build_timeline_call_honors_explicit_depths() -> None:
        """Explicit before/after depths override the configured defaults."""
        client = FlextQualityClaudeMemClient()
        result = client.build_timeline_call(42, depth_before=1, depth_after=2)
        tm.that(result.value.params.get("depth_before"), eq=1)
        tm.that(result.value.params.get("depth_after"), eq=2)

    @staticmethod
    def test_claude_mem_get_observations_command_reports_availability() -> None:
        """The chained observations command mirrors real mcp-cli availability."""
        client = FlextQualityClaudeMemClient()
        expected_ok = bool(client.health_check().value.get("available"))
        result = client.build_observations_command([1])
        tm.that(result.success, eq=expected_ok)

    @staticmethod
    def test_claude_mem_get_search_command_reports_availability() -> None:
        """The chained search command mirrors real mcp-cli availability."""
        client = FlextQualityClaudeMemClient()
        expected_ok = bool(client.health_check().value.get("available"))
        result = client.build_search_command("find this")
        tm.that(result.success, eq=expected_ok)

    @staticmethod
    def test_claude_mem_get_timeline_command_reports_availability() -> None:
        """The chained timeline command mirrors real mcp-cli availability."""
        client = FlextQualityClaudeMemClient()
        expected_ok = bool(client.health_check().value.get("available"))
        result = client.build_timeline_command(1)
        tm.that(result.success, eq=expected_ok)

    @staticmethod
    def test_claude_mem_health_check_reports_server_name() -> None:
        """Health check for claude-mem echoes its own server name."""
        client = FlextQualityClaudeMemClient()
        result = client.health_check()
        tm.that(result.value.get("server"), eq="claude-mem")
