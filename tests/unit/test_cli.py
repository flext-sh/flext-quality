"""Tests for canonical flext-quality CLI.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import tm

from flext_quality import FlextQualityCli, main


class TestCommandServices:
    """Direct unit tests against the nested Pydantic service classes."""

    def test_status(self) -> None:
        result = FlextQualityCli.Status().execute()
        tm.that(result.success, eq=True)
        tm.that(result.value, is_=dict)

    def test_check(self, tmp_path: Path) -> None:
        result = FlextQualityCli.Check(target_path=tmp_path).execute()
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=2)
        tm.that(result.value[0], has="ruff")
        tm.that(result.value[1], has="basedpyright")

    def test_validate(self, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        result = FlextQualityCli.Validate(target_path=tmp_path).execute()
        tm.that(result.success, eq=True)
        tm.that(len(result.value), eq=5)
        tm.that(result.value[2], has="bandit")
        tm.that(result.value[4], eq=["python", "-m", "coverage", "report"])


class TestMain:
    """Tests for the `main` entry point exercising full CLI dispatch."""

    def test_status_ok(self) -> None:
        tm.that(main(["status"]), eq=0)

    def test_check_ok(self, tmp_path: Path) -> None:
        tm.that(main(["check", "--target-path", str(tmp_path)]), eq=0)

    def test_validate_ok(self, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        tm.that(main(["validate", "--target-path", str(tmp_path)]), eq=0)

    def test_unknown_fails(self) -> None:
        tm.that(main(["unknown"]), eq=1)
