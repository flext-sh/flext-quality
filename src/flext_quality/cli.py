"""Canonical flext-quality CLI — inheritance + auto-derived declarative routing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, ClassVar, Self, override

from flext_cli import cli
from flext_quality import FlextQualityCodeExecutionBridge, m, p, quality, r, s, t, u

if TYPE_CHECKING:
    from collections.abc import (
        MutableSequence,
        Sequence,
    )


class FlextQualityCli(s[bool]):
    """FLEXT Quality analysis toolkit."""

    app_name: ClassVar[str] = "flext-quality"

    class Status(s[t.JsonMapping]):
        """Display quality service status."""

        @override
        def execute(self) -> p.Result[t.JsonMapping]:
            """Return the canonical quality service status payload."""
            return quality.fetch_status()

    class Check(s[t.SequenceOf[t.StrSequence]]):
        """Run lint + type check on --target-path."""

        target_path: Annotated[
            Path,
            u.Field(default_factory=Path.cwd, description="Target path"),
        ]

        @override
        def execute(self) -> p.Result[t.SequenceOf[t.StrSequence]]:
            """Build the canonical quality check command sequence."""
            bridge = FlextQualityCodeExecutionBridge()
            cmds: MutableSequence[t.StrSequence] = []
            for build in (bridge.build_ruff_command, bridge.build_basedpyright_command):
                sub = build(self.target_path)
                if sub.failure:
                    return r[t.SequenceOf[t.StrSequence]].fail(sub.error)
                cmds.append(sub.value)
            return self._extend(cmds)

        def _extend(
            self: Self,
            cmds: MutableSequence[t.StrSequence],
        ) -> p.Result[t.SequenceOf[t.StrSequence]]:
            return r[t.SequenceOf[t.StrSequence]].ok(cmds)

    class Validate(Check):
        """Run full validation (lint + type + security + tests) on --target."""

        @override
        def _extend(
            self: Self,
            cmds: MutableSequence[t.StrSequence],
        ) -> p.Result[t.SequenceOf[t.StrSequence]]:
            src = (
                self.target_path / "src"
                if (self.target_path / "src").exists()
                else self.target_path
            )
            cmds.append(["bandit", "-r", str(src), "-c", "pyproject.toml"])
            cmds.append([
                "pytest",
                str(self.target_path / "tests"),
                f"--cov={self.target_path / 'src'}",
                "--cov-report=term-missing",
            ])
            cmds.append(["python", "-m", "coverage", "report"])
            return r[t.SequenceOf[t.StrSequence]].ok(cmds)

    COMMANDS: ClassVar[Sequence[type[m.BaseModel]]] = (Status, Check, Validate)

    @override
    def execute(self) -> p.Result[bool]:
        """Lifecycle entrypoint for parity with FLEXT services."""
        return r[bool].ok(value=True)


def main(args: t.StrSequence | None = None) -> int:
    """flext-quality CLI entry point."""
    app = cli.create_app_with_common_params(
        name=FlextQualityCli.app_name,
        help_text=FlextQualityCli.__doc__ or "",
        settings=cli.settings,
    )
    cli.register_result_routes(
        app,
        [
            m.Cli.ResultCommandRoute(
                name=svc.__name__.lower(),
                help_text=svc.__doc__ or "",
                model_cls=svc,
                handler=lambda params: params.execute(),
            )
            for svc in FlextQualityCli.COMMANDS
        ],
    )
    result = cli.execute_app(
        app,
        prog_name=FlextQualityCli.app_name,
        args=args if args is not None else sys.argv[1:],
    )
    return 0 if result.success else 1


__all__: list[str] = ["FlextQualityCli", "main"]
