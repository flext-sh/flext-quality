"""FLEXT Quality Tools - Internal utilities package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Internal tools for flext-quality operations. These utilities consume
flext-quality's domain API and provide supporting functionality.
"""

from __future__ import annotations

from .architecture import FlextQualityArchitectureTools
from .backup import BackupManager
from .config_manager import ConfigurationManager
from .conflicts import ConflictAnalyzer
from .dependencies import FlextQualityDependencyTools
from .discovery import DependencyDiscovery
from .git import FlextQualityGitTools
from .mypy_checker import MyPyChecker
from .optimizer_operations import FlextQualityOptimizerOperations
from .paths import FlextPathService
from .poetry import PoetryOperations, PoetryValidator
from .quality_operations import FlextQualityOperations
from .script_base import FlextScriptService, ScriptMetadata
from .security import FlextSecurityService, SecretVaultDecryptor
from .utilities import (
    Colors,
    FlextQualityToolsUtilities,
    colorize,
    get_project_root,
    get_stdlib_modules,
    is_stdlib_module,
    normalize_path,
    print_colored,
    should_ignore_path,
)
from .validation import FlextQualityValidationTools

__all__ = [
    "BackupManager",
    "Colors",
    "ConfigurationManager",
    "ConflictAnalyzer",
    "DependencyDiscovery",
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
    "SecretVaultDecryptor",
    "MyPyChecker",
    "PoetryOperations",
    "PoetryValidator",
    "ScriptMetadata",
    "colorize",
    "get_project_root",
    "get_stdlib_modules",
    "is_stdlib_module",
    "normalize_path",
    "print_colored",
    "should_ignore_path",
]
