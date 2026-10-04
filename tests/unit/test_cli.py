"""Behavioral tests for the canonical flext-quality CLI.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_quality import FlextQualityCli, main

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextQualityCli:
    """Contract tests for the observable CLI behavior.

    These exercise the public surface only: the ``r[T]`` outcome of each
    service ``execute()``, the built command sequences the CLI promises, and
    the process exit code returned by ``main``. No private attributes,
    collaborators, or internal call spying are touched.
    """

    # ---- Status ---------------------------------------------------------

    @staticmethod
    def test_status_execute_succeeds_with_mapping_payload() -> None:
        """Test status execute succeeds with mapping payload."""
        result = FlextQualityCli.Status().execute()
        tm.that(result.success, eq=True)
        tm.that(result.value, is_=dict)

    @staticmethod
    def test_status_payload_exposes_service_contract_keys() -> None:
        """Test status payload exposes service contract keys."""
        payload = FlextQualityCli.Status().execute().unwrap()
        for key in ("name", "version", "settings", "hooks_registered"):
            tm.that(payload, has=key)

    # ---- Check ----------------------------------------------------------

    @staticmethod
    def test_check_builds_exactly_lint_then_typecheck(tmp_path: Path) -> None:
        """Test check builds exactly lint then typecheck."""
        result = FlextQualityCli.Check(target_path=tmp_path).execute()
        tm.that(result.success, eq=True)
        commands = result.unwrap()
        tm.that(len(commands), eq=2)
        tm.that(commands[0], has="ruff")
        tm.that(commands[1], has="basedpyright")

    @staticmethod
    def test_check_commands_reference_target_path(tmp_path: Path) -> None:
        """Test check commands reference target path."""
        commands = FlextQualityCli.Check(target_path=tmp_path).execute().unwrap()
        for command in commands:
            tm.that(command, has=str(tmp_path))

    # ---- Validate -------------------------------------------------------

    @staticmethod
    def test_validate_extends_check_with_security_and_tests(
        tmp_path: Path,
    ) -> None:
        """Test validate extends check with security and tests."""
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        result = FlextQualityCli.Validate(target_path=tmp_path).execute()
        tm.that(result.success, eq=True)
        commands = result.unwrap()
        tm.that(len(commands), eq=5)
        tm.that(commands[2], has="bandit")
        tm.that(commands[4], eq=["python", "-m", "coverage", "report"])

    @staticmethod
    def test_validate_is_superset_of_check(tmp_path: Path) -> None:
        """LSP invariant: Validate keeps Check's lint+typecheck prefix intact."""
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        check = FlextQualityCli.Check(target_path=tmp_path).execute().unwrap()
        validate = FlextQualityCli.Validate(target_path=tmp_path).execute().unwrap()
        tm.that(len(validate), eq=len(check) + 3)
        tm.that(list(validate[:2]), eq=list(check))

    @staticmethod
    def test_validate_bandit_scans_src_dir_when_present(tmp_path: Path) -> None:
        """Test validate bandit scans src dir when present."""
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        commands = FlextQualityCli.Validate(target_path=tmp_path).execute().unwrap()
        tm.that(commands[2], has=str(tmp_path / "src"))

    @staticmethod
    def test_validate_bandit_falls_back_to_target_without_src(
        tmp_path: Path,
    ) -> None:
        """Test validate bandit falls back to target without src."""
        (tmp_path / "tests").mkdir()
        commands = FlextQualityCli.Validate(target_path=tmp_path).execute().unwrap()
        tm.that(commands[2], has=str(tmp_path))

    # ---- Lifecycle ------------------------------------------------------

    @staticmethod
    def test_facade_execute_reports_ready() -> None:
        """Test facade execute reports ready."""
        result = FlextQualityCli().execute()
        tm.that(result.success, eq=True)
        tm.that(result.unwrap(), eq=True)

    # ---- main() exit codes ---------------------------------------------

    @staticmethod
    def test_main_status_exits_zero() -> None:
        """Test main status exits zero."""
        tm.that(main(["status"]), eq=0)

    @staticmethod
    def test_main_check_exits_zero(tmp_path: Path) -> None:
        """Test main check exits zero."""
        tm.that(main(["check", "--target-path", str(tmp_path)]), eq=0)

    @staticmethod
    def test_main_validate_exits_zero(tmp_path: Path) -> None:
        """Test main validate exits zero."""
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        tm.that(main(["validate", "--target-path", str(tmp_path)]), eq=0)

    @staticmethod
    @pytest.mark.parametrize("bad_args", [["unknown"], ["not-a-command"], ["xyz"]])
    def test_main_unknown_command_exits_nonzero(bad_args: list[str]) -> None:
        """Test main unknown command exits nonzero."""
        tm.that(main(bad_args), eq=1)
