"""Unit tests for optimizer operations tools.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_quality.tools import FlextQualityOptimizerOperations


class TestOptimizerOperations:
    """Test suite for FlextQualityOptimizerOperations."""

    def test_optimizer_operations_initialization(self) -> None:
        """Test FlextQualityOptimizerOperations initializes correctly."""
        ops = FlextQualityOptimizerOperations()

        assert ops is not None
        assert hasattr(ops, "module")
        assert hasattr(ops, "imports")
        assert hasattr(ops, "syntax")
        assert hasattr(ops, "types")

    def test_module_analyzer_with_invalid_path(self) -> None:
        """Test module analysis with invalid path."""
        ops = FlextQualityOptimizerOperations()

        result = ops.module.analyze_module("nonexistent.py")

        assert result.is_failure
        assert "not found" in result.error.lower()

    def test_module_analyzer_with_valid_syntax(self) -> None:
        """Test module analysis with valid Python file."""
        ops = FlextQualityOptimizerOperations()

        # Create temp file with valid Python code
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".py", delete=False
        ) as f:
            f.write('"""Test module."""\n\ndef test_function():\n    pass\n')
            temp_path = f.name

        try:
            result = ops.module.analyze_module(temp_path)

            assert result.is_success
            analysis = result.value
            assert analysis.complexity_score >= 0
            assert isinstance(analysis.violations, list)
            assert isinstance(analysis.suggestions, list)
        finally:
            Path(temp_path).unlink()

    def test_module_optimizer_dry_run(self) -> None:
        """Test module optimization in dry-run mode."""
        ops = FlextQualityOptimizerOperations()

        # Create temp file
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".py", delete=False
        ) as f:
            f.write('"""Test module."""\n\ndef test_function():\n    pass\n')
            temp_path = f.name

        try:
            result = ops.module.optimize(temp_path, dry_run=True)

            assert result.is_success
            opt_result = result.value
            assert opt_result.success is True
            assert opt_result.changes_made == 0  # Dry run
        finally:
            Path(temp_path).unlink()

    def test_import_refactorer_dry_run(self) -> None:
        """Test import refactoring in dry-run mode."""
        ops = FlextQualityOptimizerOperations()

        result = ops.imports.refactor_imports("module.py", dry_run=True)

        assert result.is_success
        assert result.value["dry_run"] is True

    def test_syntax_modernizer_dry_run(self) -> None:
        """Test syntax modernization in dry-run mode."""
        ops = FlextQualityOptimizerOperations()

        result = ops.syntax.modernize_syntax("module.py", dry_run=True)

        assert result.is_success
        assert result.value["dry_run"] is True

    def test_type_modernizer_dry_run(self) -> None:
        """Test type modernization in dry-run mode."""
        ops = FlextQualityOptimizerOperations()

        result = ops.types.modernize_types("module.py", dry_run=True)

        assert result.is_success
        assert result.value["dry_run"] is True

    def test_execute_interface(self) -> None:
        """Test FlextCore.Service execute interface."""
        ops = FlextQualityOptimizerOperations()

        result = ops.execute()

        assert result.is_success

    def test_domain_library_violation_detection(self) -> None:
        """Test detection of domain library violations."""
        ops = FlextQualityOptimizerOperations()

        # Create temp file with domain library violation
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".py", delete=False
        ) as f:
            f.write("""
import ldap3  # Should use flext_ldap

def connect():
    pass
""")
            temp_path = f.name

        try:
            result = ops.module.analyze_module(temp_path)

            assert result.is_success
            analysis = result.value
            # Check for domain library violation
            violation_found = any("ldap3" in v.lower() for v in analysis.violations)
            assert violation_found
        finally:
            Path(temp_path).unlink()
