"""Module optimization operations - SOLID pattern with delegated responsibilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Operations:
- ModuleOptimizer: AST analysis and pattern detection (via ASTAnalyzer)
- ImportRefactorer: Import standardization (via ImportOptimizer)
- SyntaxModernizer: Python 3.13+ syntax updates (via SyntaxUpdater)
- TypeModernizer: Type checker migration (via ConfigUpdater)

All operations delegate to utility services for SINGLE RESPONSIBILITY.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes as t
from pydantic import BaseModel, ConfigDict, Field

from flext_quality.models import FlextQualityModels

# =========================================================================
# PYDANTIC CONFIGURATION MODELS - Replace hardcoded patterns with data
# =========================================================================


class DomainLibraryPattern(BaseModel):
    """Forbidden import pattern and required replacement."""

    import_pattern: str = Field(..., description="Forbidden import pattern")
    required_library: str = Field(..., description="Required domain library")

    model_config = ConfigDict(frozen=True)


class OptimizerConfig(BaseModel):
    """Optimizer configuration with all patterns as data."""

    domain_violations: list[DomainLibraryPattern] = Field(
        default_factory=lambda: [
            DomainLibraryPattern(
                import_pattern="import ldap3",
                required_library="flext-ldap",
            ),
            DomainLibraryPattern(
                import_pattern="from ldap3",
                required_library="flext-ldap",
            ),
            DomainLibraryPattern(
                import_pattern="import click",
                required_library="flext-cli",
            ),
            DomainLibraryPattern(
                import_pattern="from click",
                required_library="flext-cli",
            ),
            DomainLibraryPattern(
                import_pattern="import httpx",
                required_library="flext-api",
            ),
            DomainLibraryPattern(
                import_pattern="from httpx",
                required_library="flext-api",
            ),
            DomainLibraryPattern(
                import_pattern="import oracledb",
                required_library="flext-db-oracle",
            ),
            DomainLibraryPattern(
                import_pattern="from oracledb",
                required_library="flext-db-oracle",
            ),
        ],
    )
    temp_prefix: str = Field(default="flext-optim-")
    complexity_threshold: float = Field(default=0.7)
    max_functions: int = Field(default=15)
    max_ast_depth: int = Field(default=8)
    max_line_count: int = Field(default=500)


# =========================================================================
# UTILITY SERVICES - Focused, single-responsibility operations
# =========================================================================


class ASTAnalyzer:
    """AST analysis utility - calculates metrics, finds violations."""

    @staticmethod
    def calculate_depth(node: ast.AST, depth: int = 0) -> int:
        """Calculate maximum AST depth recursively."""
        if not hasattr(node, "body"):
            return depth

        return max(
            (
                ASTAnalyzer.calculate_depth(child, depth + 1)
                for child in ast.iter_child_nodes(node)
            ),
            default=depth,
        )

    @staticmethod
    def calculate_complexity(
        tree: ast.Module,
        content: str,
        config: OptimizerConfig,
    ) -> float:
        """Calculate complexity score based on AST analysis."""
        score = 0.0

        class_count = sum(
            1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )
        if class_count > 1:
            score += 0.3
        elif class_count == 0:
            score += 0.2

        func_count = sum(
            1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        )
        if func_count > config.max_functions:
            score += 0.3

        depth = ASTAnalyzer.calculate_depth(tree)
        if depth > config.max_ast_depth:
            score += 0.2

        lines = len(content.split("\n"))
        if lines > config.max_line_count:
            score += 0.2

        return min(score, 1.0)

    @staticmethod
    def find_violations(content: str, config: OptimizerConfig) -> list[str]:
        """Find domain library violations in content."""
        return [
            f"Domain violation: {pattern.import_pattern} should use {pattern.required_library}"
            for pattern in config.domain_violations
            if pattern.import_pattern in content
        ]


class ImportOptimizer:
    """Import optimization - sys.path removal, submodule rewrites."""

    @staticmethod
    def remove_sys_path_hacks(content: str) -> tuple[str, bool]:
        """Remove sys.path manipulation hacks."""
        pattern = re.compile(r"^\s*sys\.path\.(insert|append)\(.*\)\s*$", re.MULTILINE)
        if pattern.search(content):
            return pattern.sub("", content), True
        return content, False

    @staticmethod
    def rewrite_submodule_imports(content: str, package: str) -> tuple[str, bool]:
        """Rewrite from pkg.sub import X → from pkg import X."""
        pattern = re.compile(
            rf"^\s*from\s+{re.escape(package)}\.(?P<sub>[A-Za-z0-9_\.]+)\s+import\s+(?P<names>[^\n]+)$",
            re.MULTILINE,
        )
        if not pattern.search(content):
            return content, False

        def replace_sub(m: re.Match[str]) -> str:
            return f"from {package} import {m.group('names')}"

        return pattern.sub(replace_sub, content), True

    @staticmethod
    def promote_type_checking_imports(content: str) -> tuple[str, bool]:
        """Promote non-typing imports from TYPE_CHECKING blocks."""
        allowed = ("typing", "collections.abc")

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return content, False

        lines = content.splitlines(keepends=True)
        promoted, changed = [], False

        for node in tree.body:
            if not ImportOptimizer._is_type_checking_node(node):
                continue

            start, end = (
                getattr(node, "lineno", None),
                getattr(node, "end_lineno", None),
            )
            if not (start and end):
                continue

            block = "".join(lines[start - 1 : end])
            block_promoted = ImportOptimizer._extract_imports_from_block(block, allowed)
            if block_promoted:
                promoted.extend(block_promoted)
                changed = True

        if promoted and changed:
            content = (
                re.sub(r"if TYPE_CHECKING:.*?(?=\n\n|\Z)", "", content, flags=re.DOTALL)
                + "\n"
                + "\n".join(promoted)
            )
            return content, True

        return content, False

    @staticmethod
    def _is_type_checking_node(node: ast.AST) -> bool:
        """Check if node is a TYPE_CHECKING if statement.

        Args:
            node: AST node to check

        Returns:
            True if node is TYPE_CHECKING if statement

        """
        return (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "TYPE_CHECKING"
        )

    @staticmethod
    def _extract_imports_from_block(
        block: str,
        allowed: tuple[str, ...],
    ) -> list[str]:
        """Extract imports from TYPE_CHECKING block.

        Args:
            block: Code block string
            allowed: Allowed module prefixes

        Returns:
            List of import statements to promote

        """
        try:
            promoted = [
                f"from {sub_node.module} import {', '.join(a.name for a in sub_node.names)}"
                for sub_node in ast.parse(block).body
                if (
                    isinstance(sub_node, ast.ImportFrom)
                    and sub_node.module
                    and not sub_node.module.startswith(allowed)
                )
            ]
        except SyntaxError:
            promoted = []
        return promoted


class SyntaxUpdater:
    """Python 3.13+ syntax modernization."""

    @staticmethod
    def modernize_unions(content: str) -> tuple[str, list[str]]:
        """Convert Union[A, B] → A | B and Optional[T] → T | None."""
        changes = []

        for union_match in re.finditer(r"Union\[([^\]]+)\]", content):
            types = [t.strip() for t in union_match.group(1).split(",")]
            new = " | ".join(types)
            content = content.replace(union_match.group(0), new)
            changes.append(f"Union → {new}")

        for opt_match in re.finditer(r"Optional\[([^\]]+)\]", content):
            new = f"{opt_match.group(1)} | None"
            content = content.replace(opt_match.group(0), new)
            changes.append(f"Optional → {new}")

        return content, changes

    @staticmethod
    def modernize_collections(content: str) -> tuple[str, list[str]]:
        """Convert Dict/List/Set/Tuple → dict/list/set/tuple."""
        changes = []
        replacements = {"Dict": "dict", "List": "list", "Set": "set", "Tuple": "tuple"}

        for old, new in replacements.items():
            pattern = rf"\b{old}\["
            if re.search(pattern, content):
                content = re.sub(pattern, f"{new}[", content)
                changes.append(f"{old} → {new}")

        return content, changes


class ConfigUpdater:
    """Configuration file modernization - pyproject.toml, Makefile."""

    @staticmethod
    def update_pyproject(content: str) -> tuple[str, list[str]]:
        """Update pyproject.toml for Pyrefly instead of MyPy."""
        changes = []
        lines = content.splitlines()
        modified_lines = []
        in_tool_section = False
        in_pyrefly_section = False

        for line in lines:
            # Check if we're entering a tool section
            if line.strip().startswith("[tool"):
                in_tool_section = True
                if ".mypy]" in line or ".pyright]" in line:
                    changes.append(f"Removed {line.strip()}")
                    continue
                if ".pyrefly]" in line:
                    in_pyrefly_section = True
            elif line.strip().startswith("[") and not line.strip().startswith("[tool"):
                in_tool_section = False
                in_pyrefly_section = False

            # Skip mypy/pyright tool sections
            if in_tool_section and (".mypy]" in line or ".pyright]" in line):
                continue
            if in_pyrefly_section:
                # Keep existing pyrefly config
                modified_lines.append(line)
                continue

            # Remove mypy from dev dependencies
            if 'mypy = "' in line or "mypy = '" in line:
                changes.append("Removed MyPy")
                continue

            modified_lines.append(line)

        # Add pyrefly if not present
        pyrefly_config = """
[tool.pyrefly]
python_version = "3.13"
show_error_codes = true
"""
        if "[tool.pyrefly]" not in content:
            modified_lines.append(pyrefly_config.strip())
            changes.append("Added Pyrefly config")

        # Add pyrefly to dev dependencies if poetry section exists
        if (
            "[tool.poetry.group.dev.dependencies]" in content
            and 'pyrefly = "' not in content
        ):
            # Find the dev dependencies section and add pyrefly
            for i, line in enumerate(modified_lines):
                if line.strip() == "[tool.poetry.group.dev.dependencies]":
                    modified_lines.insert(i + 1, 'pyrefly = "^0.34.0"')
                    changes.append("Added Pyrefly")
                    break

        result = "\n".join(modified_lines)
        return (result if changes else content), changes

    @staticmethod
    def update_makefile(content: str) -> tuple[str, list[str]]:
        """Update Makefile to use Pyrefly."""
        changes = []
        replacements = [
            (r"mypy\s+\$\(SRC_DIR\)\s+--strict", "pyrefly check $(SRC_DIR)"),
            (r"mypy\s+src/\s+--strict", "pyrefly check src/"),
        ]

        for pattern, replacement in replacements:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes.append("Updated type-check command")

        return content, changes


# =========================================================================
# MAIN SERVICE - Unified API delegating to utilities
# =========================================================================


class FlextQualityOptimizerOperations(FlextService[bool]):
    """Unified optimizer service delegating to focused utilities.

    ONE CLASS PER MODULE - All utilities composed here.
    """

    _optimizer_config: OptimizerConfig

    def __init__(self, config: OptimizerConfig | None = None) -> None:
        """Initialize with optional custom config.

        Args:
            config: Optional optimizer configuration. If None, creates default config.

        """
        super().__init__()
        # Must provide config explicitly - no fallback patterns allowed
        # Use object.__setattr__ to bypass Pydantic's custom __setattr__ for private attributes
        if config is None:
            object.__setattr__(self, "_optimizer_config", OptimizerConfig())
        else:
            object.__setattr__(self, "_optimizer_config", config)
        self._logger = FlextLogger(__name__)

    def execute(self) -> FlextResult[bool]:
        """FlextService interface."""
        return FlextResult[bool].ok(True)

    def analyze_module(
        self,
        module_path: str,
    ) -> FlextResult[FlextQualityModels.Quality.AnalysisResult]:
        """Analyze module for optimization opportunities."""
        path = Path(module_path)
        if not path.exists():
            return FlextResult[FlextQualityModels.Quality.AnalysisResult].fail(
                f"Module not found: {module_path}",
            )

        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(path))
        except Exception as e:
            return FlextResult[FlextQualityModels.Quality.AnalysisResult].fail(str(e))

        ASTAnalyzer.find_violations(content, self._optimizer_config)
        ASTAnalyzer.calculate_complexity(tree, content, self._optimizer_config)

        result = FlextQualityModels.Quality.AnalysisResult(
            analysis_id="",
            project_path=module_path,
            status="completed",
        )

        return FlextResult[FlextQualityModels.Quality.AnalysisResult].ok(result)

    def optimize_module(
        self,
        module_path: str,
        *,
        dry_run: bool = True,
    ) -> FlextResult[FlextQualityModels.Quality.OptimizationResult]:
        """Optimize module - fix violations."""
        path = Path(module_path)
        if not path.exists():
            return FlextResult[FlextQualityModels.Quality.OptimizationResult].fail(
                f"Module not found: {module_path}",
            )

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            return FlextResult[FlextQualityModels.Quality.OptimizationResult].fail(str(e))

        # Fix violations
        for pattern in self._optimizer_config.domain_violations:
            if pattern.import_pattern in content:
                lib_class = f"Flext{pattern.required_library.split('-')[1].title()}"
                content = content.replace(
                    pattern.import_pattern,
                    f"from {pattern.required_library.replace('-', '_')} import {lib_class}",
                )

        if not dry_run and content != path.read_text(encoding="utf-8"):
            path.write_text(content, encoding="utf-8")

        result = FlextQualityModels.Quality.OptimizationResult(
            target=FlextQualityModels.Quality.OptimizationTarget(
                project_path=".",
                module_name=path.stem,
                file_path=module_path,
                optimization_type="pattern_violation",
            ),
            changes_made=1 if content != path.read_text(encoding="utf-8") else 0,
            success=True,
            errors=[],
            warnings=[],
        )

        return FlextResult[FlextQualityModels.Quality.OptimizationResult].ok(result)

    def refactor_imports(
        self,
        module_path: str,
        *,
        dry_run: bool = True,
        package_name: str | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Refactor imports using ImportOptimizer."""
        path = Path(module_path)
        if not path.exists():
            return FlextResult[dict[str, t.GeneralValueType]].fail(
                f"Module not found: {module_path}",
            )

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            return FlextResult[dict[str, t.GeneralValueType]].fail(str(e))

        changes = []

        content, sys_changed = ImportOptimizer.remove_sys_path_hacks(content)
        if sys_changed:
            changes.append("Removed sys.path hacks")

        if package_name:
            content, sub_changed = ImportOptimizer.rewrite_submodule_imports(
                content,
                package_name,
            )
            if sub_changed:
                changes.append("Rewrote submodule imports")

        content, tc_changed = ImportOptimizer.promote_type_checking_imports(content)
        if tc_changed:
            changes.append("Promoted TYPE_CHECKING imports")

        if not dry_run and changes:
            path.write_text(content, encoding="utf-8")

        return FlextResult[dict[str, t.GeneralValueType]].ok({
            "changes": changes,
            "file": str(module_path),
        })

    def modernize_syntax(
        self,
        module_path: str,
        *,
        dry_run: bool = True,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Modernize Python 3.13+ syntax."""
        path = Path(module_path)
        if not path.exists():
            return FlextResult[dict[str, t.GeneralValueType]].fail(
                f"Module not found: {module_path}",
            )

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            return FlextResult[dict[str, t.GeneralValueType]].fail(str(e))

        all_changes = []

        content, union_changes = SyntaxUpdater.modernize_unions(content)
        all_changes.extend(union_changes)

        content, coll_changes = SyntaxUpdater.modernize_collections(content)
        all_changes.extend(coll_changes)

        if not dry_run and all_changes:
            path.write_text(content, encoding="utf-8")

        return FlextResult[dict[str, t.GeneralValueType]].ok({
            "changes": all_changes,
            "file": str(module_path),
        })

    def modernize_types(
        self,
        module_path: str,
        *,
        dry_run: bool = True,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Modernize type checking configuration."""
        path = Path(module_path)

        if path.is_dir():
            pyproject_path = path / "pyproject.toml"
            makefile_path = path / "Makefile"
        elif path.name == "pyproject.toml":
            pyproject_path = path
            makefile_path = path.parent / "Makefile"
        else:
            return FlextResult[dict[str, t.GeneralValueType]].fail(
                f"Invalid path: {module_path}"
            )

        all_changes = []
        files_modified = []

        if pyproject_path.exists():
            try:
                content = pyproject_path.read_text(encoding="utf-8")
                updated, changes = ConfigUpdater.update_pyproject(content)
                all_changes.extend([f"pyproject.toml: {c}" for c in changes])

                if not dry_run and updated != content:
                    pyproject_path.write_text(updated, encoding="utf-8")
                    files_modified.append(str(pyproject_path))
            except Exception as e:
                return FlextResult[dict[str, t.GeneralValueType]].fail(str(e))

        if makefile_path.exists():
            try:
                content = makefile_path.read_text(encoding="utf-8")
                updated, changes = ConfigUpdater.update_makefile(content)
                all_changes.extend([f"Makefile: {c}" for c in changes])

                if not dry_run and updated != content:
                    makefile_path.write_text(updated, encoding="utf-8")
                    files_modified.append(str(makefile_path))
            except Exception as e:
                return FlextResult[dict[str, t.GeneralValueType]].fail(str(e))

        return FlextResult[dict[str, t.GeneralValueType]].ok({
            "changes": all_changes,
            "files_modified": files_modified,
        })


__all__ = ["FlextQualityOptimizerOperations", "OptimizerConfig"]
