# VERIFIED_NEW_MODULE
"""Fixture consolidation detection using libcst.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides AST-based detection of duplicate fixtures across projects:
- Finds fixtures in conftest.py files
- Detects semantically identical fixtures by comparing AST body hashes
- Reports consolidation opportunities
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import libcst as cst
from flext_core import FlextLogger, FlextResult as r, FlextService, FlextTypes as t


class FlextQualityFixtureConsolidateOperation(
    FlextService[dict[str, t.GeneralValueType]]
):
    """Detects duplicate fixtures across projects using libcst AST analysis.

    This operation analyzes conftest.py files to find fixtures that could be
    consolidated. Uses libcst for safe AST traversal and hash comparison.

    All nested classes and helpers are inside this facade class.
    """

    # Minimum count to consider fixtures as duplicates
    MIN_DUPLICATE_COUNT: int = 2

    @dataclass
    class FixtureInfo:
        """Represents information about a pytest fixture."""

        name: str
        file_path: Path
        line: int
        body_hash: str
        scope: str = "function"
        has_params: bool = False

    @dataclass
    class DuplicateGroup:
        """Represents a group of duplicate fixtures."""

        name: str
        fixtures: list[FlextQualityFixtureConsolidateOperation.FixtureInfo] = field(
            default_factory=list
        )

        @property
        def count(self: Self) -> int:
            """Get count of fixtures in this group."""
            return len(self.fixtures)

        @property
        def files(self: Self) -> list[str]:
            """Get list of files containing this fixture."""
            return [str(f.file_path) for f in self.fixtures]

    @dataclass
    class AnalysisResult:
        """Result of analyzing fixtures across projects."""

        workspace_path: Path
        total_fixtures: int = 0
        duplicate_groups: list[
            FlextQualityFixtureConsolidateOperation.DuplicateGroup
        ] = field(default_factory=list)

        @property
        def duplicate_count(self: Self) -> int:
            """Get total count of duplicate fixtures."""
            return sum(g.count for g in self.duplicate_groups)

        @property
        def consolidation_opportunities(self: Self) -> int:
            """Get number of fixtures that could be consolidated."""
            # Each group could be consolidated into 1, so savings = count - 1
            return sum(g.count - 1 for g in self.duplicate_groups)

    class FixtureVisitor(cst.CSTVisitor):
        """Visitor to extract fixture information from conftest.py files."""

        def __init__(self: Self, file_path: Path) -> None:
            """Initialize visitor with file path."""
            self.file_path = file_path
            self.fixtures: list[
                FlextQualityFixtureConsolidateOperation.FixtureInfo
            ] = []
            self._current_line = 0

        def visit_FunctionDef(
            self: Self, node: cst.FunctionDef
        ) -> bool | None:
            """Visit function definitions to find fixtures."""
            # Check if function has @pytest.fixture decorator
            is_fixture = False
            scope = "function"
            has_params = False

            for decorator in node.decorators:
                decorator_name = self._get_decorator_name(decorator)
                if "fixture" in decorator_name:
                    is_fixture = True
                    # Try to extract scope from decorator arguments
                    if isinstance(decorator.decorator, cst.Call):
                        for arg in decorator.decorator.args:
                            if isinstance(arg.keyword, cst.Name):
                                if arg.keyword.value == "scope":
                                    scope = self._extract_string_value(arg.value)
                                elif arg.keyword.value == "params":
                                    has_params = True
                    break

            if is_fixture:
                # Generate hash of function body
                body_hash = self._hash_function_body(node)

                self.fixtures.append(
                    FlextQualityFixtureConsolidateOperation.FixtureInfo(
                        name=node.name.value,
                        file_path=self.file_path,
                        line=self._current_line,
                        body_hash=body_hash,
                        scope=scope,
                        has_params=has_params,
                    )
                )

            return None

        def _get_decorator_name(self: Self, decorator: cst.Decorator) -> str:
            """Extract name from decorator."""
            dec = decorator.decorator
            if isinstance(dec, cst.Name):
                return dec.value
            if isinstance(dec, cst.Attribute):
                return f"{self._get_node_name(dec.value)}.{dec.attr.value}"
            if isinstance(dec, cst.Call):
                return self._get_node_name(dec.func)
            return ""

        def _get_node_name(self: Self, node: cst.BaseExpression) -> str:
            """Extract name from expression node."""
            if isinstance(node, cst.Name):
                return node.value
            if isinstance(node, cst.Attribute):
                return f"{self._get_node_name(node.value)}.{node.attr.value}"
            return ""

        def _extract_string_value(self: Self, node: cst.BaseExpression) -> str:
            """Extract string value from node."""
            if isinstance(node, cst.SimpleString):
                # Remove quotes
                return node.value.strip("\"'")
            return "function"

        def _hash_function_body(self: Self, node: cst.FunctionDef) -> str:
            """Generate hash of function body for comparison."""
            # Serialize the body to string and hash it
            body_code = node.body.deep_clone()
            body_str = repr(body_code)
            return hashlib.sha256(body_str.encode()).hexdigest()[:16]

    def __init__(self: Self) -> None:
        """Initialize fixture consolidation operation."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def find_fixtures(self: Self, conftest_path: Path) -> r[list[FixtureInfo]]:
        """Extract fixtures from a conftest.py file.

        Args:
            conftest_path: Path to conftest.py file

        Returns:
            FlextResult containing list of FixtureInfo

        """
        if not conftest_path.exists():
            return r[list[FlextQualityFixtureConsolidateOperation.FixtureInfo]].fail(
                f"File not found: {conftest_path}"
            )

        if conftest_path.name != "conftest.py":
            return r[list[FlextQualityFixtureConsolidateOperation.FixtureInfo]].fail(
                f"Not a conftest.py file: {conftest_path}"
            )

        source = conftest_path.read_text(encoding="utf-8")
        parsed_module = cst.parse_module(source)

        visitor = FlextQualityFixtureConsolidateOperation.FixtureVisitor(conftest_path)
        parsed_module.walk(visitor)

        return r[list[FlextQualityFixtureConsolidateOperation.FixtureInfo]].ok(
            visitor.fixtures
        )

    def find_duplicates(
        self: Self, workspace_path: Path
    ) -> r[AnalysisResult]:
        """Find duplicate fixtures across a workspace.

        Args:
            workspace_path: Root path of workspace

        Returns:
            FlextResult containing AnalysisResult with duplicates

        """
        if not workspace_path.exists():
            return r[FlextQualityFixtureConsolidateOperation.AnalysisResult].fail(
                f"Workspace not found: {workspace_path}"
            )

        # Collect all fixtures by name and hash
        fixtures_by_name: dict[
            str, list[FlextQualityFixtureConsolidateOperation.FixtureInfo]
        ] = {}
        total_fixtures = 0

        for conftest in workspace_path.rglob("conftest.py"):
            result = self.find_fixtures(conftest)
            if result.is_success:
                for fixture in result.value:
                    total_fixtures += 1
                    fixtures_by_name.setdefault(fixture.name, []).append(fixture)

        # Find groups with duplicates (same name AND same body hash)
        duplicate_groups: list[
            FlextQualityFixtureConsolidateOperation.DuplicateGroup
        ] = []

        for name, fixtures in fixtures_by_name.items():
            if len(fixtures) < self.MIN_DUPLICATE_COUNT:
                continue

            # Group by body hash to find truly identical fixtures
            by_hash: dict[
                str, list[FlextQualityFixtureConsolidateOperation.FixtureInfo]
            ] = {}
            for fixture in fixtures:
                by_hash.setdefault(fixture.body_hash, []).append(fixture)

            # Only report groups where multiple fixtures have same hash
            duplicate_groups.extend(
                FlextQualityFixtureConsolidateOperation.DuplicateGroup(
                    name=name, fixtures=hash_fixtures
                )
                for hash_fixtures in by_hash.values()
                if len(hash_fixtures) > 1
            )

        return r[FlextQualityFixtureConsolidateOperation.AnalysisResult].ok(
            FlextQualityFixtureConsolidateOperation.AnalysisResult(
                workspace_path=workspace_path,
                total_fixtures=total_fixtures,
                duplicate_groups=duplicate_groups,
            )
        )

    def dry_run(
        self: Self, targets: list[Path]
    ) -> r[dict[str, t.GeneralValueType]]:
        """Preview fixture consolidation opportunities.

        Args:
            targets: List of workspace directories to analyze

        Returns:
            FlextResult with summary of duplicates found

        """
        all_duplicates: list[dict[str, t.GeneralValueType]] = []
        total_fixtures = 0
        total_duplicates = 0
        total_opportunities = 0

        for target in targets:
            if not target.is_dir():
                continue

            result = self.find_duplicates(target)
            if result.is_success:
                analysis = result.value
                total_fixtures += analysis.total_fixtures
                total_duplicates += analysis.duplicate_count
                total_opportunities += analysis.consolidation_opportunities

                all_duplicates.extend(
                    {
                        "name": group.name,
                        "count": group.count,
                        "files": group.files,
                        "body_hash": group.fixtures[0].body_hash if group.fixtures else "",
                    }
                    for group in analysis.duplicate_groups
                )

        summary: dict[str, t.GeneralValueType] = {
            "workspaces_analyzed": len(targets),
            "total_fixtures": total_fixtures,
            "duplicate_groups": len(all_duplicates),
            "total_duplicates": total_duplicates,
            "consolidation_opportunities": total_opportunities,
            "duplicates": all_duplicates,
        }

        return r[dict[str, t.GeneralValueType]].ok(summary)

    def execute(
        self: Self,
        targets: list[Path],
        _backup_path: Path | None = None,
    ) -> r[dict[str, t.GeneralValueType]]:
        """Execute fixture consolidation detection (same as dry_run).

        Args:
            targets: List of workspace directories to analyze
            _backup_path: Not used for detection-only operation

        Returns:
            FlextResult with summary of duplicates found

        """
        # Detection-only operation - same as dry_run
        return self.dry_run(targets)

    def rollback(
        self: Self, _backup_path: Path
    ) -> r[dict[str, t.GeneralValueType]]:
        """Rollback not applicable for detection-only operation.

        Args:
            _backup_path: Backup path (not used)

        Returns:
            FlextResult indicating rollback not applicable

        """
        return r[dict[str, t.GeneralValueType]].ok({
            "status": "not_applicable",
            "message": "Detection-only operation has no changes to rollback",
        })


# Short alias for convenience
FixtureConsolidateOperation = FlextQualityFixtureConsolidateOperation
