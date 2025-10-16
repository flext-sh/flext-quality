"""Unit tests for quality operations tools.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_quality.tools import FlextQualityOperations


class TestQualityOperations:
    """Test suite for FlextQualityOperations."""

    def test_quality_operations_initialization(self) -> None:
        """Test FlextQualityOperations initializes correctly."""
        ops = FlextQualityOperations()

        assert ops is not None
        assert hasattr(ops, "gateway")
        assert hasattr(ops, "linting")
        assert hasattr(ops, "types")
        assert hasattr(ops, "duplicates")
        assert hasattr(ops, "exports")
        assert hasattr(ops, "docstrings")
        assert hasattr(ops, "patterns")
        assert hasattr(ops, "audit")

    def test_linting_service_fix_issues_dry_run(self) -> None:
        """Test lint fixing in dry-run mode."""
        ops = FlextQualityOperations()

        # Dry-run should not fail even with invalid path
        result = ops.linting.fix_issues("nonexistent.py", dry_run=True)

        assert result.is_success
        assert result.value["dry_run"] is True

    def test_type_checker_run_with_invalid_path(self) -> None:
        """Test type checker with invalid path."""
        ops = FlextQualityOperations()

        # Type checker with invalid path should fail gracefully
        result = ops.types.run_type_check("nonexistent.py")

        assert result.is_failure

    def test_duplicate_detector(self) -> None:
        """Test duplicate detection placeholder."""
        ops = FlextQualityOperations()

        result = ops.duplicates.detect_duplicates(".", threshold=10)

        assert result.is_success
        assert "duplicates_found" in result.value
        assert "threshold" in result.value

    def test_export_repairer_dry_run(self) -> None:
        """Test export repair in dry-run mode."""
        ops = FlextQualityOperations()

        result = ops.exports.repair_exports(".", dry_run=True)

        assert result.is_success
        assert result.value["dry_run"] is True

    def test_docstring_normalizer_dry_run(self) -> None:
        """Test docstring normalization in dry-run mode."""
        ops = FlextQualityOperations()

        result = ops.docstrings.normalize_docstrings("module.py", dry_run=True)

        assert result.is_success
        assert result.value["dry_run"] is True

    def test_pattern_auditor(self) -> None:
        """Test pattern auditing placeholder."""
        ops = FlextQualityOperations()

        result = ops.patterns.audit_patterns(".")

        assert result.is_success
        assert "patterns_checked" in result.value

    def test_false_positive_auditor(self) -> None:
        """Test false positive filtering."""
        ops = FlextQualityOperations()

        results = [
            {"issue": "error1", "false_positive": False},
            {"issue": "error2", "false_positive": True},
            {"issue": "error3", "false_positive": False},
        ]

        result = ops.audit.audit_false_positives(results)

        assert result.is_success
        assert len(result.value) == 2  # Only non-false positives
        assert all(not r.get("false_positive", False) for r in result.value)

    def test_execute_interface(self) -> None:
        """Test FlextService execute interface."""
        ops = FlextQualityOperations()

        result = ops.execute()

        assert result.is_success
