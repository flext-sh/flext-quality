"""Additional coverage for ExternalBackend edge cases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_quality import ExternalBackend


def _temp_py(tmp_path: Path) -> Path:
    p = tmp_path / "x.py"
    p.write_text("print('x')\n", encoding="utf-8")
    return p


@patch("shutil.which", return_value=None)
def test_external_tool_missing_returns_error(tmp_path: Path) -> None:
    """When tools are missing, return error messages for each runner."""
    backend = ExternalBackend()
    temp = _temp_py(tmp_path)

    res1 = backend._run_ruff(temp)
    assert res1.is_success
    assert res1.data["status"] == "tool_not_found"
    assert "ruff not installed" in res1.data["message"]

    res2 = backend._run_mypy(temp)
    assert res2.is_success
    assert res2.data["status"] == "tool_not_found"
    assert "mypy not installed" in res2.data["message"]

    # Bandit
    res3 = backend._run_bandit(temp)
    assert res3.is_success
    assert res3.data["status"] == "tool_not_found"
    assert "bandit not installed" in res3.data["message"]

    # Vulture
    res4 = backend._run_vulture(temp)
    assert res4.is_success
    assert res4.data["status"] == "tool_not_found"
    assert "vulture not installed" in res4.data["message"]


@patch("shutil.which", side_effect=lambda name: name)
@patch("flext_core.FlextUtilities.FlextUtilities.CommandExecution.run_external_command")
def test_external_backend_empty_outputs(
    mock_run: MagicMock,
    tmp_path: Path,
) -> None:
    """Empty stdout from tools should produce empty lists in outputs."""
    backend = ExternalBackend()
    temp = _temp_py(tmp_path)

    from flext_core import FlextResult

    mock_run.return_value = FlextResult.ok(
        MagicMock(returncode=0, stdout="[]", stderr="")
    )
    out1 = backend._run_ruff(temp)
    assert out1.is_success
    assert out1.data["issues"] == []

    mock_run.return_value = FlextResult.ok(
        MagicMock(returncode=0, stdout="", stderr="")
    )
    out2 = backend._run_mypy(temp)
    assert out2.is_success
    assert isinstance(out2.data["issues"], list)

    # Bandit with empty stdout -> default path
    mock_run.return_value = FlextResult.ok(
        MagicMock(returncode=0, stdout="", stderr="")
    )
    out3 = backend._run_bandit(temp)
    assert out3.is_success
    assert out3.data["issues"] == []

    # Vulture with empty stdout -> issues []
    mock_run.return_value = FlextResult.ok(
        MagicMock(returncode=0, stdout="[]", stderr="")
    )
    out4 = backend._run_vulture(temp)
    assert out4.is_success
    assert out4.data["issues"] == []


def test_external_backend_invalid_path_handling(tmp_path: Path) -> None:
    """Invalid path returns explicit error message."""
    backend = ExternalBackend()
    # Use non-existent file to trigger invalid path
    missing = tmp_path / "missing.py"
    res = backend._run_ruff(missing)
    assert res.is_failure
    assert "Invalid file path" in str(res.error)


def test_parse_ruff_output_invalid_json() -> None:
    """Invalid JSON from ruff should yield empty list."""
    backend = ExternalBackend()
    assert backend._parse_ruff_output("not json") == []
