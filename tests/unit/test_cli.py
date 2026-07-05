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

    def test_status_execute_succeeds_with_mapping_payload(self) -> None:
        result = FlextQualityCli.Status().execute()
        tm.that(result.success, eq=True)
        tm.that(result.value, is_=dict)

    def test_status_payload_exposes_service_contract_keys(self) -> None:
        payload = FlextQualityCli.Status().execute().unwrap()
        for key in ("name", "version", "settings", "hooks_registered"):
            tm.that(payload, has=key)

    # ---- Check ----------------------------------------------------------

    def test_check_builds_exactly_lint_then_typecheck(self, tmp_path: Path) -> None:
        result = FlextQualityCli.Check(target_path=tmp_path).execute()
        tm.that(result.success, eq=True)
        commands = result.unwrap()
        tm.that(len(commands), eq=2)
        tm.that(commands[0], has="ruff")
        tm.that(commands[1], has="basedpyright")

    def test_check_commands_reference_target_path(self, tmp_path: Path) -> None:
        commands = FlextQualityCli.Check(target_path=tmp_path).execute().unwrap()
        for command in commands:
            tm.that(command, has=str(tmp_path))

    # ---- Validate -------------------------------------------------------

    def test_validate_extends_check_with_security_and_tests(
        self, tmp_path: Path
    ) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        result = FlextQualityCli.Validate(target_path=tmp_path).execute()
        tm.that(result.success, eq=True)
        commands = result.unwrap()
        tm.that(len(commands), eq=5)
        tm.that(commands[2], has="bandit")
        tm.that(commands[4], eq=["python", "-m", "coverage", "report"])

    def test_validate_is_superset_of_check(self, tmp_path: Path) -> None:
        """LSP invariant: Validate keeps Check's lint+typecheck prefix intact."""
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        check = FlextQualityCli.Check(target_path=tmp_path).execute().unwrap()
        validate = FlextQualityCli.Validate(target_path=tmp_path).execute().unwrap()
        tm.that(len(validate), eq=len(check) + 3)
        tm.that(list(validate[:2]), eq=list(check))

    def test_validate_bandit_scans_src_dir_when_present(self, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        commands = FlextQualityCli.Validate(target_path=tmp_path).execute().unwrap()
        tm.that(commands[2], has=str(tmp_path / "src"))

    def test_validate_bandit_falls_back_to_target_without_src(
        self, tmp_path: Path
    ) -> None:
        (tmp_path / "tests").mkdir()
        commands = FlextQualityCli.Validate(target_path=tmp_path).execute().unwrap()
        tm.that(commands[2], has=str(tmp_path))

    # ---- Lifecycle ------------------------------------------------------

    def test_facade_execute_reports_ready(self) -> None:
        result = FlextQualityCli().execute()
        tm.that(result.success, eq=True)
        tm.that(result.unwrap(), eq=True)

    # ---- main() exit codes ---------------------------------------------

    def test_main_status_exits_zero(self) -> None:
        tm.that(main(["status"]), eq=0)

    def test_main_check_exits_zero(self, tmp_path: Path) -> None:
        tm.that(main(["check", "--target-path", str(tmp_path)]), eq=0)

    def test_main_validate_exits_zero(self, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        tm.that(main(["validate", "--target-path", str(tmp_path)]), eq=0)

    @pytest.mark.parametrize("bad_args", [["unknown"], ["not-a-command"], ["xyz"]])
    def test_main_unknown_command_exits_nonzero(
        self, bad_args: list[str]
    ) -> None:
        tm.that(main(bad_args), eq=1)


__all__: list[str] = ["TestsFlextQualityCli"]
