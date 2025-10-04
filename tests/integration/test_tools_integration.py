"""Integration tests for all migrated quality tools.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Tests integration between:
- Quality operations (lint, type check, duplicates, etc.)
- Optimizer operations (module analysis, refactoring)
- Architecture tools (violation analysis, pattern enforcement)
- Dependency tools (analysis, consolidation)
- Validation tools (equilibrium, domain, ecosystem)
- Git tools (history rewriting, cleanup)
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


class TestToolsIntegration:
    """Integration tests for all migrated quality tools."""

    def test_all_tools_initialize_successfully(self) -> None:
        """Test that all migrated tools can be initialized."""
        quality_ops = FlextQualityOperations()
        optimizer_ops = FlextQualityOptimizerOperations()
        arch_tools = FlextQualityArchitectureTools()
        dep_tools = FlextQualityDependencyTools()
        val_tools = FlextQualityValidationTools()
        git_tools = FlextQualityGitTools()

        assert quality_ops is not None
        assert optimizer_ops is not None
        assert arch_tools is not None
        assert dep_tools is not None
        assert val_tools is not None
        assert git_tools is not None

    def test_quality_operations_integration(self) -> None:
        """Test quality operations tool integration."""
        ops = FlextQualityOperations()

        # Test that all nested services are accessible
        assert hasattr(ops, "gateway")
        assert hasattr(ops, "linting")
        assert hasattr(ops, "types")
        assert hasattr(ops, "duplicates")
        assert hasattr(ops, "exports")
        assert hasattr(ops, "docstrings")
        assert hasattr(ops, "patterns")
        assert hasattr(ops, "audit")

    def test_optimizer_operations_integration(self) -> None:
        """Test optimizer operations tool integration."""
        ops = FlextQualityOptimizerOperations()

        # Test that all nested services are accessible
        assert hasattr(ops, "module")
        assert hasattr(ops, "imports")
        assert hasattr(ops, "syntax")
        assert hasattr(ops, "types")

    def test_architecture_tools_integration(self) -> None:
        """Test architecture tools integration."""
        tools = FlextQualityArchitectureTools()

        # Test that all nested services are accessible
        assert hasattr(tools, "violations")
        assert hasattr(tools, "patterns")
        assert hasattr(tools, "imports")

    def test_dependency_tools_integration(self) -> None:
        """Test dependency tools integration."""
        tools = FlextQualityDependencyTools()

        # Test that all nested services are accessible
        assert hasattr(tools, "analyzer")
        assert hasattr(tools, "consolidator")
        assert hasattr(tools, "poetry")

    def test_validation_tools_integration(self) -> None:
        """Test validation tools integration."""
        tools = FlextQualityValidationTools()

        # Test that all nested services are accessible
        assert hasattr(tools, "equilibrium")
        assert hasattr(tools, "domain")
        assert hasattr(tools, "ecosystem")

    def test_git_tools_integration(self) -> None:
        """Test git tools integration."""
        FlextQualityGitTools()

        # Test that all nested services are accessible
        # Note: HistoryRewriter and CleanupService are class attributes (capitalized)
        assert hasattr(FlextQualityGitTools, "HistoryRewriter")
        assert hasattr(FlextQualityGitTools, "CleanupService")

    def test_quality_workflow_integration(self) -> None:
        """Test complete quality workflow integration."""
        # Create temp Python file for testing
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".py", delete=False
        ) as f:
            f.write("""
'''Test module for quality workflow.'''

from __future__ import annotations


def example_function() -> str:
    '''Example function with proper docstring.'''
    return "example"


class ExampleClass:
    '''Example class with proper docstring.'''

    def method(self) -> None:
        '''Example method.'''
        pass
""")
            temp_path = f.name

        try:
            # Step 1: Analyze module with optimizer
            optimizer = FlextQualityOptimizerOperations()
            analysis_result = optimizer.module.analyze_module(temp_path)
            assert analysis_result.is_success
            analysis = analysis_result.value
            assert analysis.complexity_score >= 0

            # Step 2: Run quality checks
            quality = FlextQualityOperations()

            # Linting (dry-run)
            lint_result = quality.linting.fix_issues(temp_path, dry_run=True)
            assert lint_result.is_success

            # Duplicate detection
            dup_result = quality.duplicates.detect_duplicates(
                str(Path(temp_path).parent)
            )
            assert dup_result.is_success

            # Step 3: Validate with architecture tools
            arch = FlextQualityArchitectureTools()
            violation_result = arch.violations.analyze_violations(
                str(Path(temp_path).parent)
            )
            assert violation_result.is_success

        finally:
            Path(temp_path).unlink()

    def test_all_tools_execute_interface(self) -> None:
        """Test FlextService execute interface for all tools."""
        tools = [
            FlextQualityOperations(),
            FlextQualityOptimizerOperations(),
            FlextQualityArchitectureTools(),
            FlextQualityDependencyTools(),
            FlextQualityValidationTools(),
            FlextQualityGitTools(),
        ]

        for tool in tools:
            result = tool.execute()
            assert result.is_success

    def test_cross_tool_data_flow(self) -> None:
        """Test data flowing between different tools."""
        # Create temp module
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".py", delete=False
        ) as f:
            f.write("""
import ldap3  # Domain library violation for testing

def test_function():
    pass
""")
            temp_path = f.name

        try:
            # Step 1: Optimizer analyzes and detects domain library violation
            optimizer = FlextQualityOptimizerOperations()
            analysis_result = optimizer.module.analyze_module(temp_path)

            assert analysis_result.is_success
            analysis = analysis_result.value

            # Should detect ldap3 domain library violation
            has_violation = any("ldap3" in v.lower() for v in analysis.violations)
            assert has_violation, "Should detect ldap3 domain library violation"

            # Step 2: Quality operations can work with same module
            quality = FlextQualityOperations()
            lint_result = quality.linting.fix_issues(temp_path, dry_run=True)
            assert lint_result.is_success

            # Step 3: Architecture tools can validate
            arch = FlextQualityArchitectureTools()
            arch_result = arch.violations.analyze_violations(
                str(Path(temp_path).parent)
            )
            assert arch_result.is_success

        finally:
            Path(temp_path).unlink()

    def test_dry_run_consistency_across_tools(self) -> None:
        """Test that dry_run behavior is consistent across all tools."""
        # All tools should support dry_run and return success for dry-run operations
        quality = FlextQualityOperations()
        optimizer = FlextQualityOptimizerOperations()
        deps = FlextQualityDependencyTools()

        # Quality operations dry-run
        lint_dry = quality.linting.fix_issues("test.py", dry_run=True)
        assert lint_dry.is_success
        assert lint_dry.value.get("dry_run") is True

        # Optimizer operations dry-run
        import_dry = optimizer.imports.refactor_imports("test.py", dry_run=True)
        assert import_dry.is_success
        assert import_dry.value.get("dry_run") is True

        # Dependency operations dry-run
        consolidate_dry = deps.consolidator.consolidate_dependencies(".", dry_run=True)
        assert consolidate_dry.is_success
        assert consolidate_dry.value.get("dry_run") is True
