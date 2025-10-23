"""FLEXT Quality Tools - Internal utilities package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Internal tools for flext-quality operations. These utilities consume
flext-quality's domain API and provide supporting functionality.
"""

from __future__ import annotations

from .architecture import FlextQualityArchitectureTools
from .backup import BackupManager
from .colors import (
    Colors,
    FlextColorService,
    colorize as colorize_text,
    print_colored as print_colored_text,
)
from .config_manager import ConfigurationManager
from .conflicts import ConflictAnalyzer
from .dependencies import FlextQualityDependencyTools
from .discovery import DependencyDiscovery
from .doc_helper import (
    analyze_api_documentation,
    check_docstring_coverage,
    suggest_docstring_improvements,
    validate_google_style_docstrings,
)
from .example_helper import (
    check_example_structure,
    run_example_safely,
    validate_example_imports,
    validate_examples_directory,
)
from .git import FlextQualityGitTools
from .health import HealthCheckService
from .mypy_checker import MyPyChecker
from .observability import FlextObservabilityService
from .optimizer_operations import FlextQualityOptimizerOperations
from .paths import FlextPathService
from .pattern_helper import (
    audit_flext_patterns,
    check_all_flext_patterns,
    check_exception_patterns,
    check_flext_result_usage,
    check_import_patterns,
    check_module_structure,
)
from .poetry import PoetryOperations, PoetryValidator
from .quality_operations import FlextQualityOperations
from .script_base import FlextScriptService, ScriptMetadata
from .security import FlextSecurityService, SecretVaultDecryptor
from .test_helper import (
    check_test_quality,
    suggest_tests_from_coverage,
    validate_test_execution,
)
from .utilities import (
    FlextQualityToolsUtilities,
    get_project_root,
    get_stdlib_modules,
    is_stdlib_module,
    normalize_path,
    should_ignore_path,
)
from .validation import FlextQualityValidationTools

colorize = colorize_text
print_colored = print_colored_text

__all__ = [
    # Architecture and core tools
    "BackupManager",
    "Colors",
    "ConfigurationManager",
    "ConflictAnalyzer",
    "DependencyDiscovery",
    "FlextColorService",
    "FlextObservabilityService",
    "FlextPathService",
    "FlextQualityArchitectureTools",
    "FlextQualityDependencyTools",
    "FlextQualityGitTools",
    "FlextQualityOperations",
    "FlextQualityOptimizerOperations",
    "FlextQualityToolsUtilities",
    "FlextQualityValidationTools",
    "FlextScriptService",
    "FlextSecurityService",
    "HealthCheckService",
    "MyPyChecker",
    "PoetryOperations",
    "PoetryValidator",
    "ScriptMetadata",
    "SecretVaultDecryptor",
    # Helper functions - Documentation
    "analyze_api_documentation",
    # Helper functions - FLEXT Patterns
    "audit_flext_patterns",
    "check_all_flext_patterns",
    "check_docstring_coverage",
    # Helper functions - Examples
    "check_example_structure",
    "check_exception_patterns",
    "check_flext_result_usage",
    "check_import_patterns",
    "check_module_structure",
    # Helper functions - Tests
    "check_test_quality",
    # Utilities
    "colorize",
    "get_project_root",
    "get_stdlib_modules",
    "is_stdlib_module",
    "normalize_path",
    "print_colored",
    "run_example_safely",
    "should_ignore_path",
    "suggest_docstring_improvements",
    "suggest_tests_from_coverage",
    "validate_example_imports",
    "validate_examples_directory",
    "validate_google_style_docstrings",
    "validate_test_execution",
]

# pragma: no cover
