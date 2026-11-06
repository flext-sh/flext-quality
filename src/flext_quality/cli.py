"""Canonical flext-quality CLI — inheritance + auto-derived declarative routing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import MutableSequence, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, ClassVar, override

from flext_cli import cli

from flext_quality import c, m, p, quality, r, s, t
from flext_quality.integrations import FlextQualityCodeExecutionBridge

if TYPE_CHECKING:
    from flext_quality import FlextQualityServiceBase


class FlextQualityCli(s[bool]):
    """FLEXT Quality analysis toolkit."""

    app_name: ClassVar[str] = "flext-quality"

    class Status(s[t.JsonMapping]):
        """Display quality service status."""

        @override
        def execute(self) -> p.Result[t.JsonMapping]:
            """Return the canonical quality service status payload."""
            return quality.fetch_status()

    class Check(s[Sequence[Sequence[str]]]):
        """Run lint + type check on --target-path."""

        target_path: Annotated[
            Path,
            m.Field(default_factory=Path.cwd, description="Target path"),
        ]

        @override
        def execute(self) -> p.Result[Sequence[Sequence[str]]]:
            """Build the canonical quality check command sequence.

            Returns:
                The resulting ``p.Result[Sequence[Sequence[str]]]``.

            """
            built = self._analysis_commands()
            if built.failure:
                return r[Sequence[Sequence[str]]].fail(built.error)
            return r[Sequence[Sequence[str]]].ok(built.value)

        def _analysis_commands(self) -> p.Result[MutableSequence[Sequence[str]]]:
            """Build the static-analysis command sequence for the target path.

            Returns:
                The resulting ``p.Result[MutableSequence[Sequence[str]]]``.

            """
            bridge = FlextQualityCodeExecutionBridge()
            cmds: MutableSequence[Sequence[str]] = []
            for build in (bridge.build_ruff_command, bridge.build_basedpyright_command):
                sub = build(self.target_path)
                if sub.failure:
                    return r[MutableSequence[Sequence[str]]].fail(sub.error)
                cmds.append(sub.value)
            return r[MutableSequence[Sequence[str]]].ok(cmds)

    class Validate(Check):
        """Run full validation (lint + type + security + tests) on --target."""

        @override
        def _analysis_commands(self) -> p.Result[MutableSequence[Sequence[str]]]:
            built = super()._analysis_commands()
            if built.failure:
                return built
            cmds = built.value
            src = (
                self.target_path / "src"
                if (self.target_path / "src").exists()
                else self.target_path
            )
            cmds.append(["bandit", "-r", str(src), "-c", c.PYPROJECT_FILENAME])
            cmds.append([
                "pytest",
                str(self.target_path / "tests"),
                f"--cov={self.target_path / 'src'}",
                "--cov-report=term-missing",
            ])
            cmds.append(["python", "-m", "coverage", "report"])
            return r[MutableSequence[Sequence[str]]].ok(cmds)

    COMMANDS: ClassVar[
        tuple[
            type[Status | Check | Validate],
            ...,
        ]
    ] = (Status, Check, Validate)

    @override
    def execute(self) -> p.Result[bool]:
        """Lifecycle entrypoint for parity with FLEXT services.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        return r[bool].ok(value=True)

    @staticmethod
    def invoke(
        params: FlextQualityServiceBase[t.JsonMapping]
        | FlextQualityServiceBase[Sequence[Sequence[str]]],
    ) -> p.Result[t.JsonMapping] | p.Result[Sequence[Sequence[str]]]:
        """Execute a registered service instance for its declarative CLI route.

        Args:
            params: Service instance whose declarative route is invoked.

        Returns:
            The resulting ``p.Result[t.JsonMapping] |
                p.Result[Sequence[Sequence[str]]]``.

        """
        return params.execute()


def main(args: Sequence[str] | None = None) -> int:
    """Run the flext-quality CLI entry point.

    Args:
        args: Command-line arguments; defaults to ``sys.argv[1:]`` when ``None``.

    Returns:
        The process exit code.

    """
    app = cli.create_app_with_common_params(
        name=FlextQualityCli.app_name,
        help_text=FlextQualityCli.__doc__ or "",
    )
    cli.register_result_routes(
        app,
        [
            m.Cli.ResultCommandRoute(
                name=svc.__name__.lower(),
                help_text=svc.__doc__ or "",
                model_cls=svc,
                handler=FlextQualityCli.invoke,
            )
            for svc in FlextQualityCli.COMMANDS
        ],
    )
    result = cli.execute_app(
        app,
        prog_name=FlextQualityCli.app_name,
        args=args if args is not None else sys.argv[1:],
    )
    return cli.finalize_result(result)


__all__: list[str] = ["FlextQualityCli", "main"]
