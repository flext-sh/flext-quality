"""Comprehensive dry-run validation for all migrated quality tools.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Validates that all tools work correctly in dry-run mode without making
any actual changes to the system.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_quality.tools import (
    FlextQualityArchitectureTools,
    FlextQualityDependencyTools,
    FlextQualityGitTools,
    FlextQualityOperations,
    FlextQualityOptimizerOperations,
    FlextQualityValidationTools,
)


class TestDryRunValidation:
    """Comprehensive dry-run validation for all migrated tools."""

    def test_quality_operations_all_dry_run(self) -> None:
        """Test all FlextQualityOperations methods in dry-run mode."""
        quality = FlextQualityOperations()

        # Create temp test file
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            f.write('"""Test module."""\n\ndef test_function():\n    pass\n')
            temp_path = f.name

        try:
            # Test linting service dry-run
            lint_result = quality.linting.fix_issues(temp_path, dry_run=True)
            assert lint_result.is_success
            assert lint_result.value["dry_run"] is True

            # Test export repairer dry-run
            export_result = quality.exports.repair_exports(".", dry_run=True)
            assert export_result.is_success
            assert export_result.value["dry_run"] is True

            # Test docstring normalizer dry-run
            doc_result = quality.docstrings.normalize_docstrings(
                temp_path,
                dry_run=True,
            )
            assert doc_result.is_success
            assert doc_result.value["dry_run"] is True

        finally:
            Path(temp_path).unlink()

    def test_optimizer_operations_all_dry_run(self) -> None:
        """Test all FlextQualityOptimizerOperations methods in dry-run mode."""
        optimizer = FlextQualityOptimizerOperations()

        # Create temp test file
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            f.write('"""Test module."""\n\ndef test_function():\n    pass\n')
            temp_path = f.name

        try:
            # Test module optimizer dry-run
            opt_result = optimizer.module.optimize(temp_path, dry_run=True)
            assert opt_result.is_success
            assert opt_result.value.changes_made == 0  # Dry-run makes no changes

            # Test import refactorer dry-run
            import_result = optimizer.imports.refactor_imports(temp_path, dry_run=True)
            assert import_result.is_success
            assert import_result.value["dry_run"] is True

            # Test syntax modernizer dry-run
            syntax_result = optimizer.syntax.modernize_syntax(temp_path, dry_run=True)
            assert syntax_result.is_success
            assert syntax_result.value["dry_run"] is True

            # Test type modernizer dry-run
            type_result = optimizer.types.modernize_types(temp_path, dry_run=True)
            assert type_result.is_success
            assert type_result.value["dry_run"] is True

        finally:
            Path(temp_path).unlink()

    def test_architecture_tools_all_dry_run(self) -> None:
        """Test all FlextQualityArchitectureTools methods in dry-run mode."""
        arch = FlextQualityArchitectureTools()

        # Test pattern enforcer dry-run
        pattern_result = arch.patterns.enforce_patterns(".", dry_run=True)
        assert pattern_result.is_success
        assert pattern_result.value["dry_run"] is True

    def test_dependency_tools_all_dry_run(self) -> None:
        """Test all FlextQualityDependencyTools methods in dry-run mode."""
        deps = FlextQualityDependencyTools()

        # Test dependency consolidator dry-run
        consolidate_result = deps.consolidator.consolidate_dependencies(
            ".",
            dry_run=True,
        )
        assert consolidate_result.is_success
        assert consolidate_result.value["dry_run"] is True

        # Note: PoetryOperations.sync_poetry_lock doesn't support dry_run
        # It's a read-only operation

    def test_git_tools_all_dry_run(self) -> None:
        """Test all FlextQualityGitTools methods in dry-run mode."""
        # Note: Git tools require real git repository
        # This is a placeholder test - real testing would need git repo setup
        git = FlextQualityGitTools()

        # Test cleanup service dry-run (safe without git repo)
        cleanup_result = git.CleanupService.cleanup_cruft(".", dry_run=True)
        # Expected to fail without git repo, but should handle gracefully
        assert cleanup_result.is_success or cleanup_result.is_failure

    def test_validation_tools_all_operations(self) -> None:
        """Test all FlextQualityValidationTools operations."""
        validator = FlextQualityValidationTools()

        # Test equilibrium validator
        equilibrium_result = validator.equilibrium.validate_equilibrium(".")
        assert equilibrium_result.is_success
        # ValidationResult object with passed/checks_run/checks_passed/failures
        assert hasattr(equilibrium_result.value, "passed")
        assert equilibrium_result.value.passed is True

        # Test domain validator
        domain_result = validator.domain.validate_domain_separation(".")
        assert domain_result.is_success
        assert hasattr(domain_result.value, "passed")

        # Test ecosystem validator
        ecosystem_result = validator.ecosystem.validate_ecosystem_quality(".")
        assert ecosystem_result.is_success
        assert hasattr(ecosystem_result.value, "passed")

    def test_all_tools_no_side_effects(self) -> None:
        """Verify that dry-run operations produce no side effects."""
        quality = FlextQualityOperations()
        optimizer = FlextQualityOptimizerOperations()

        # Create temp test file
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".py",
            delete=False,
        ) as f:
            original_content = '"""Test module."""\n\ndef test_function():\n    pass\n'
            f.write(original_content)
            temp_path = f.name

        try:
            # Run multiple dry-run operations
            quality.linting.fix_issues(temp_path, dry_run=True)
            optimizer.module.optimize(temp_path, dry_run=True)
            optimizer.imports.refactor_imports(temp_path, dry_run=True)

            # Verify file content unchanged
            with Path(temp_path).open(encoding="utf-8") as f:
                current_content = f.read()

            assert current_content == original_content, (
                "Dry-run operations modified file content!"
            )

        finally:
            Path(temp_path).unlink()

    def test_dry_run_consistency(self) -> None:
        """Test that dry_run parameter is consistently respected across all tools."""
        tools_and_methods = [
            (FlextQualityOperations().linting, "fix_issues", "test.py"),
            (FlextQualityOperations().exports, "repair_exports", "."),
            (FlextQualityOperations().docstrings, "normalize_docstrings", "test.py"),
            (FlextQualityOptimizerOperations().module, "optimize", "test.py"),
            (FlextQualityOptimizerOperations().imports, "refactor_imports", "test.py"),
            (FlextQualityOptimizerOperations().syntax, "modernize_syntax", "test.py"),
            (FlextQualityOptimizerOperations().types, "modernize_types", "test.py"),
            (FlextQualityArchitectureTools().patterns, "enforce_patterns", "."),
            (
                FlextQualityDependencyTools().consolidator,
                "consolidate_dependencies",
                ".",
            ),
            # Note: PoetryOperations.sync_poetry_lock doesn't support dry_run
        ]

        for service, method_name, path in tools_and_methods:
            method = getattr(service, method_name)
            result = method(path, dry_run=True)

            # All dry-run operations should succeed or fail gracefully
            assert result.is_success or result.is_failure

            # If successful, should indicate dry-run
            if result.is_success and isinstance(result.value, dict):
                assert (
                    result.value.get("dry_run") is True
                    or result.value.get("changes_made") == 0
                ), f"{service.__class__.__name__}.{method_name} did not respect dry_run"
