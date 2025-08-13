"""Additional coverage for ExternalBackend edge cases."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

from flext_quality.backends.external_backend import ExternalBackend

if TYPE_CHECKING:
    from pathlib import Path


def _temp_py(tmp_path: Path) -> Path:
    p = tmp_path / "x.py"
    p.write_text("print('x')\n", encoding="utf-8")
    return p


@patch("shutil.which", return_value=None)
def test_external_tool_missing_returns_error(tmp_path: Path) -> None:
    """When tools are missing, return error messages for each runner."""
    backend = ExternalBackend()
    temp = _temp_py(tmp_path)
    # Ruff
    res1 = backend._run_ruff("code", temp)
    assert "error" in res1  # type: ignore[operator]
    assert "Ruff not found" in str(res1["error"])  # type: ignore[index]
    # MyPy
    res2 = backend._run_mypy("code", temp)
    assert "error" in res2  # type: ignore[operator]
    assert "MyPy not found" in str(res2["error"])  # type: ignore[index]
    # Bandit
    res3 = backend._run_bandit("code", temp)
    assert "error" in res3  # type: ignore[operator]
    assert "Bandit not found" in str(res3["error"])  # type: ignore[index]
    # Vulture
    res4 = backend._run_vulture("code", temp)
    assert "error" in res4  # type: ignore[operator]
    assert "Vulture not found" in str(res4["error"])  # type: ignore[index]


@patch("shutil.which", side_effect=lambda name: name)
@patch("subprocess.run")
def test_external_backend_empty_outputs(
    mock_run: MagicMock,
    tmp_path: Path,
) -> None:
    """Empty stdout from tools should produce empty lists in outputs."""
    backend = ExternalBackend()
    temp = _temp_py(tmp_path)

    # Ruff with empty stdout -> issues []
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    out1 = backend._run_ruff("code", temp)
    assert out1["issues"] == []  # type: ignore[index]

    # MyPy with empty stdout -> issues []
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    out2 = backend._run_mypy("code", temp)
    assert isinstance(out2["issues"], list)  # type: ignore[index]

    # Bandit with empty stdout -> default path
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    out3 = backend._run_bandit("code", temp)
    assert out3["issues"] == []  # type: ignore[index]

    # Vulture with empty stdout -> dead_code []
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    out4 = backend._run_vulture("code", temp)
    assert out4["dead_code"] == []  # type: ignore[index]


def test_external_backend_invalid_path_handling(tmp_path: Path) -> None:
    """Invalid path returns explicit error message."""
    backend = ExternalBackend()
    # Use non-existent file to trigger invalid path
    missing = tmp_path / "missing.py"
    res = backend._run_ruff("code", missing)
    assert "error" in res  # type: ignore[operator]
    assert res["error"] == "Invalid file path"  # type: ignore[index]


def test_parse_ruff_output_invalid_json() -> None:
    """Invalid JSON from ruff should yield empty list."""
    backend = ExternalBackend()
    assert backend._parse_ruff_output("not json") == []
