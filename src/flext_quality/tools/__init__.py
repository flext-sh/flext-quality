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
from .git import FlextQualityGitTools
from .health import HealthCheckService
from .mypy_checker import MyPyChecker
from .observability import FlextObservabilityService
from .optimizer_operations import FlextQualityOptimizerOperations
from .paths import FlextPathService
from .poetry import PoetryOperations, PoetryValidator
from .quality_operations import FlextQualityOperations
from .script_base import FlextScriptService, ScriptMetadata
from .security import FlextSecurityService, SecretVaultDecryptor
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
    "colorize",
    "get_project_root",
    "get_stdlib_modules",
    "is_stdlib_module",
    "normalize_path",
    "print_colored",
    "should_ignore_path",
]
