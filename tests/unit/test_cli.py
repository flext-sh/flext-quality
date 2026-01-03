"""Tests for CLI service.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from flext_quality.services.cli import FlextQualityCliService, main


class TestFlextQualityCliService:
    """Tests for FlextQualityCliService public interface."""

    def test_init_creates_service(self) -> None:
        """Test service initializes successfully."""
        service = FlextQualityCliService()
        assert service is not None

    def test_display_status_returns_result(self) -> None:
        """Test display_status returns a FlextResult with dict."""
        service = FlextQualityCliService()
        result = service.display_status()
        assert result.is_success
        assert isinstance(result.value, dict)

    def test_build_check_commands_returns_commands(self, tmp_path: Path) -> None:
        """Test build_check_commands returns list of commands."""
        service = FlextQualityCliService()
        result = service.build_check_commands(tmp_path)
        assert result.is_success
        commands = result.value
        assert isinstance(commands, list)
        assert len(commands) == 2

    def test_build_check_commands_includes_ruff(self, tmp_path: Path) -> None:
        """Test build_check_commands includes ruff command."""
        service = FlextQualityCliService()
        result = service.build_check_commands(tmp_path)
        assert result.is_success
        commands = result.value
        ruff_cmd = commands[0]
        assert "ruff" in ruff_cmd
        assert "check" in ruff_cmd

    def test_build_check_commands_includes_basedpyright(
        self, tmp_path: Path
    ) -> None:
        """Test build_check_commands includes basedpyright command."""
        service = FlextQualityCliService()
        result = service.build_check_commands(tmp_path)
        assert result.is_success
        commands = result.value
        pyright_cmd = commands[1]
        assert "basedpyright" in pyright_cmd

    def test_build_validate_commands_returns_all_commands(
        self, tmp_path: Path
    ) -> None:
        """Test build_validate_commands returns all validation commands."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()

        service = FlextQualityCliService()
        result = service.build_validate_commands(tmp_path)
        assert result.is_success
        commands = result.value
        assert isinstance(commands, list)
        assert len(commands) == 4

    def test_build_validate_commands_includes_coverage(self, tmp_path: Path) -> None:
        """Test build_validate_commands includes coverage setting."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()

        service = FlextQualityCliService()
        result = service.build_validate_commands(tmp_path, min_coverage=90)
        assert result.is_success
        commands = result.value
        pytest_cmd = commands[3]
        assert "--cov-fail-under=90" in pytest_cmd

    def test_build_validate_commands_includes_bandit(self, tmp_path: Path) -> None:
        """Test build_validate_commands includes bandit command."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()

        service = FlextQualityCliService()
        result = service.build_validate_commands(tmp_path)
        assert result.is_success
        commands = result.value
        bandit_cmd = commands[2]
        assert "bandit" in bandit_cmd


class TestMainFunction:
    """Tests for main CLI entry point."""

    def test_main_with_no_args_exits_zero(self) -> None:
        """Test main with no args exits with code 0."""
        sys.argv = ["flext-quality"]
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_main_with_status_command_exits_zero(self) -> None:
        """Test main with status command exits with code 0."""
        sys.argv = ["flext-quality", "status"]
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_main_with_check_command_exits_zero(self, tmp_path: Path) -> None:
        """Test main with check command exits with code 0."""
        sys.argv = ["flext-quality", "check", str(tmp_path)]
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_main_with_validate_command_exits_zero(self, tmp_path: Path) -> None:
        """Test main with validate command exits with code 0."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()

        sys.argv = ["flext-quality", "validate", str(tmp_path)]
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_main_with_unknown_command_exits_one(self) -> None:
        """Test main with unknown command exits with code 1."""
        sys.argv = ["flext-quality", "unknown"]
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
