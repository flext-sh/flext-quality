"""Tests for CLI service.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path

from flext_tests import tm

from flext_quality import FlextQualityCliService
from flext_quality.services.cli import main


class TestFlextQualityCliService:
    """Tests for FlextQualityCliService public interface."""

    def test_init_creates_service(self) -> None:
        """Test service initializes successfully."""
        service = FlextQualityCliService()
        assert service is not None

    def test_display_status_returns_result(self) -> None:
        """Test display_status returns a r with dict."""
        service = FlextQualityCliService()
        result = service.display_status()
        tm.that(result.success, eq=True)
        tm.that(result.value, is_=dict)

    def test_build_check_commands_returns_commands(self, tmp_path: Path) -> None:
        """Test build_check_commands returns list of commands."""
        service = FlextQualityCliService()
        result = service.build_check_commands(tmp_path)
        tm.that(result.success, eq=True)
        commands = result.value
        tm.that(commands, is_=list)
        tm.that(len(commands), eq=2)

    def test_build_check_commands_includes_ruff(self, tmp_path: Path) -> None:
        """Test build_check_commands includes ruff command."""
        service = FlextQualityCliService()
        result = service.build_check_commands(tmp_path)
        tm.that(result.success, eq=True)
        commands = result.value
        ruff_cmd = commands[0]
        tm.that(ruff_cmd, has="ruff")
        tm.that(ruff_cmd, has="check")

    def test_build_check_commands_includes_basedpyright(self, tmp_path: Path) -> None:
        """Test build_check_commands includes basedpyright command."""
        service = FlextQualityCliService()
        result = service.build_check_commands(tmp_path)
        tm.that(result.success, eq=True)
        commands = result.value
        pyright_cmd = commands[1]
        tm.that(pyright_cmd, has="basedpyright")

    def test_build_validate_commands_returns_all_commands(self, tmp_path: Path) -> None:
        """Test build_validate_commands returns all validation commands."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        service = FlextQualityCliService()
        result = service.build_validate_commands(tmp_path)
        tm.that(result.success, eq=True)
        commands = result.value
        tm.that(commands, is_=list)
        tm.that(len(commands), eq=5)

    def test_build_validate_commands_includes_coverage_report(
        self,
        tmp_path: Path,
    ) -> None:
        """Test build_validate_commands includes explicit coverage report command."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        service = FlextQualityCliService()
        result = service.build_validate_commands(tmp_path)
        tm.that(result.success, eq=True)
        commands = result.value
        coverage_report_cmd = commands[4]
        tm.that(coverage_report_cmd, eq=["python", "-m", "coverage", "report"])

    def test_build_validate_commands_includes_bandit(self, tmp_path: Path) -> None:
        """Test build_validate_commands includes bandit command."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        service = FlextQualityCliService()
        result = service.build_validate_commands(tmp_path)
        tm.that(result.success, eq=True)
        commands = result.value
        bandit_cmd = commands[2]
        tm.that(bandit_cmd, has="bandit")


class TestMainFunction:
    """Tests for main CLI entry point."""

    def test_main_with_no_args_exits_zero(self) -> None:
        """Test main with no args returns code 0."""
        sys.argv = ["flext-quality"]
        tm.that(main(), eq=0)

    def test_main_with_status_command_exits_zero(self) -> None:
        """Test main with status command returns code 0."""
        sys.argv = ["flext-quality", "status"]
        tm.that(main(), eq=0)

    def test_main_with_check_command_exits_zero(self, tmp_path: Path) -> None:
        """Test main with check command returns code 0."""
        sys.argv = ["flext-quality", "check", str(tmp_path)]
        tm.that(main(), eq=0)

    def test_main_with_validate_command_exits_zero(self, tmp_path: Path) -> None:
        """Test main with validate command returns code 0."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        sys.argv = ["flext-quality", "validate", str(tmp_path)]
        tm.that(main(), eq=0)

    def test_main_with_unknown_command_exits_one(self) -> None:
        """Test main with unknown command returns code 1."""
        sys.argv = ["flext-quality", "unknown"]
        tm.that(main(), eq=1)
