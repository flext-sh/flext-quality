r"""Universal YAML rule loader for any programming project.

This module provides the RuleLoader class that loads validation rules
from YAML files and converts them to ValidationRule Pydantic models.
Works with any project type (Python, TypeScript, Go, Rust, etc.).

YAML File Format:
    metadata:
      category: python_code
      version: "1.0.0"
      description: "Description of rule category"

    rules:
      - code: DC001
        name: rm -rf
        pattern: 'rm\s+-rf?\s+'
        severity: critical
        guidance: |
          Educational message here
        blocking: true
        tags: [tag1, tag2]

Supports:
  - Global rules: data/*.yaml
  - Project-specific rules: data/projects/{project_name}/*.yaml
  - Framework-specific rules: data/frameworks/{framework_name}.yaml
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from .models import RuleCategory, RuleSeverity, ValidationRule

logger = logging.getLogger(__name__)

# Import PyprojectParser for dependency resolution
try:
    from flext_quality.tools.workspace_discovery import FlextWorkspaceDiscovery
except ImportError:
    FlextWorkspaceDiscovery = None


class RuleLoader:
    """Universal loader for validation rules from YAML files.

    Loads rules from YAML files and converts them to ValidationRule
    objects with Pydantic validation. Works with any project type.

    Supports global rules, project-specific rules, and framework-specific rules.

    Attributes:
        DATA_DIR: Path to directory containing YAML rule files

    Example:
        >>> loader = RuleLoader()
        >>> rules = loader.load_all()  # Load all global rules
        >>> project_rules = loader.load_project("my-project")  # Project-specific

    """

    DATA_DIR: Path = Path(__file__).parent / "data"
    PROJECTS_DIR: Path = DATA_DIR / "projects"
    FRAMEWORKS_DIR: Path = DATA_DIR / "frameworks"

    @classmethod
    def load_all(cls) -> list[ValidationRule]:
        """Load all global rules from data/*.yaml files.

        Loads as many rules as possible, reporting errors for files that fail.

        Returns:
            List of ValidationRule objects from all successfully loaded YAML files.

        """
        rules: list[ValidationRule] = []
        errors: list[tuple[str, str]] = []

        if not cls.DATA_DIR.exists():
            return rules

        for yaml_file in sorted(cls.DATA_DIR.glob("*.yaml")):
            try:
                rules.extend(cls.load_file(yaml_file))
            except (ValueError, OSError) as e:
                errors.append((yaml_file.name, str(e)))

        # Report errors after loading all files
        if errors:
            error_lines = [f"  ❌ {fname}: {err.split(chr(10))[0]}" for fname, err in errors]
            logger.warning(f"Errors loading {len(errors)} YAML files")
            for line in error_lines:
                logger.warning(line)
            logger.info(f"Loaded {len(rules)} rules from {len(list(cls.DATA_DIR.glob('*.yaml'))) - len(errors)} valid files")

        return rules

    @classmethod
    def load_file(cls, path: Path) -> list[ValidationRule]:
        """Load rules from a single YAML file.

        Args:
            path: Path to the YAML file

        Returns:
            List of ValidationRule objects from the file.

        Raises:
            ValueError: If YAML parsing or validation fails.

        """
        try:
            with path.open(encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data:
                return []

            metadata = data.get("metadata", {})
            category_str = metadata.get("category")

            if not category_str:
                msg = f"Missing 'metadata.category' in {path.name}"
                raise ValueError(msg)

            try:
                category = RuleCategory(category_str)
            except ValueError as e:
                valid = ", ".join(c.value for c in RuleCategory)
                msg = f"Invalid category '{category_str}' in {path.name}. Valid: {valid}"
                raise ValueError(msg) from e

            rules: list[ValidationRule] = []
            for idx, rule_data in enumerate(data.get("rules", [])):
                rule = cls._parse_rule(rule_data, category, path.name, idx)
                rules.append(rule)

            return rules

        except yaml.YAMLError as e:
            msg = f"YAML parse error in {path.name}: {e}"
            raise ValueError(msg) from e
        except OSError as e:
            msg = f"Cannot read {path.name}: {e}"
            raise OSError(msg) from e

    @classmethod
    def _parse_rule(
        cls,
        rule_data: dict[str, Any],
        category: RuleCategory,
        filename: str,
        index: int,
    ) -> ValidationRule:
        """Parse a single rule from YAML data.

        Args:
            rule_data: Dictionary from YAML with rule fields
            category: Category from file metadata
            filename: Name of the YAML file (for error messages)
            index: Index of the rule in the file (for error messages)

        Returns:
            ValidationRule object.

        Raises:
            ValueError: If required fields are missing or invalid.

        """
        try:
            # Convert severity string to enum
            severity_str = rule_data.get("severity", "high")
            try:
                severity = RuleSeverity(severity_str)
            except ValueError as e:
                valid = ", ".join(s.value for s in RuleSeverity)
                msg = (
                    f"Invalid severity '{severity_str}' in {filename} rule #{index}. "
                    f"Valid: {valid}"
                )
                raise ValueError(msg) from e

            # Build rule with explicit field mapping
            return ValidationRule(
                code=rule_data["code"],
                name=rule_data["name"],
                pattern=rule_data["pattern"],
                category=category,
                severity=severity,
                guidance=rule_data.get("guidance", rule_data["name"]),
                applies_to=tuple(rule_data.get("applies_to", [])),
                exceptions=tuple(rule_data.get("exceptions", [])),
                blocking=rule_data.get("blocking", True),
                context_required=tuple(rule_data.get("context_required", [])),
                tags=frozenset(rule_data.get("tags", [])),
                language=rule_data.get("language"),
                file_types=tuple(rule_data.get("file_types", [])),
                patterns=rule_data.get("patterns", {}),
            )

        except KeyError as e:
            msg = f"Missing required field {e} in {filename} rule #{index}"
            raise ValueError(msg) from e

    @classmethod
    def load_project(cls, project_name: str) -> list[ValidationRule]:
        """Load project-specific rules.

        Args:
            project_name: Name of the project (e.g., "my-project")

        Returns:
            List of project-specific ValidationRule objects.

        Raises:
            ValueError: If any YAML file in the project directory has errors.

        """
        project_dir = cls.PROJECTS_DIR / project_name

        if not project_dir.exists():
            return []

        rules: list[ValidationRule] = []
        for yaml_file in sorted(project_dir.glob("*.yaml")):
            rules.extend(cls.load_file(yaml_file))

        return rules

    @classmethod
    def load_framework(cls, framework_name: str) -> list[ValidationRule]:
        """Load framework-specific rules.

        Args:
            framework_name: Name of the framework (e.g., "fastapi")

        Returns:
            List of framework-specific ValidationRule objects.

        Raises:
            ValueError: If the YAML file has parsing or validation errors.

        """
        framework_file = cls.FRAMEWORKS_DIR / f"{framework_name}.yaml"

        if not framework_file.exists():
            return []

        return cls.load_file(framework_file)

    @classmethod
    def load_combined(
        cls,
        project: str | None = None,
        frameworks: list[str] | None = None,
    ) -> list[ValidationRule]:
        """Load rules from all sources: global, project-specific, framework-specific.

        Args:
            project: Optional project name for project-specific rules
            frameworks: Optional list of framework names for framework-specific rules

        Returns:
            Combined list of all applicable ValidationRule objects.

        Raises:
            ValueError: If any YAML file has parsing or validation errors.

        """
        rules: list[ValidationRule] = []

        # Load global rules
        rules.extend(cls.load_all())

        # Load project-specific rules if project provided
        if project:
            rules.extend(cls.load_project(project))

        # Load framework-specific rules if frameworks provided
        if frameworks:
            for framework in frameworks:
                rules.extend(cls.load_framework(framework))

        return rules

    @classmethod
    def list_projects(cls) -> list[str]:
        """List all available project-specific rule directories.

        Returns:
            List of project names that have specific rules.

        """
        if not cls.PROJECTS_DIR.exists():
            return []

        return sorted([d.name for d in cls.PROJECTS_DIR.iterdir() if d.is_dir()])

    @classmethod
    def list_frameworks(cls) -> list[str]:
        """List all available framework-specific rule files.

        Returns:
            List of framework names that have specific rules.

        """
        if not cls.FRAMEWORKS_DIR.exists():
            return []

        return sorted([
            f.stem
            for f in cls.FRAMEWORKS_DIR.glob("*.yaml")
            if f.is_file()
        ])

    @classmethod
    def get_project_dependencies(cls, project_path: Path) -> list[str]:
        """Get flext-* dependencies from project's pyproject.toml.

        Uses existing FlextWorkspaceDiscovery.PyprojectParser to read dependencies.

        Args:
            project_path: Path to project root (e.g., /home/user/flext/flext-core)

        Returns:
            List of flext-* dependency names (e.g., ["flext-core", "flext-cli"])
            Empty list if no dependencies found or pyproject.toml missing

        """
        if FlextWorkspaceDiscovery is None:
            return []

        pyproject = project_path / "pyproject.toml"

        if not pyproject.exists():
            return []

        # Use existing PyprojectParser from workspace_discovery
        result = FlextWorkspaceDiscovery.PyprojectParser.parse_dependencies(pyproject)

        # PyprojectParser returns FlextResult[list[str]]
        if hasattr(result, "is_failure") and result.is_failure:
            return []

        if hasattr(result, "unwrap"):
            return result.unwrap()

        # Fallback: if not FlextResult, assume it's a list
        return result if isinstance(result, list) else []

    @classmethod
    def load_project_with_dependencies(
        cls, project_path: Path, workspace_root: Path | None = None
    ) -> list[ValidationRule]:
        """Load rules for project and all its dependencies recursively.

        Reads project dependencies from pyproject.toml and loads rules from all
        dependent projects, ensuring proper ordering (foundation libs first).

        Args:
            project_path: Path to project root
            workspace_root: Path to workspace root (parent of all projects).
                           Auto-detected from project_path if None.

        Returns:
            Combined list of rules from project and all dependencies

        """
        # Auto-detect workspace root if not provided
        if workspace_root is None:
            workspace_root = project_path.parent

        # Get this project's dependencies
        dependencies = cls.get_project_dependencies(project_path)

        rules: list[ValidationRule] = []
        seen: set[str] = set()

        # Load dependencies first (in order - foundation first)
        for dep_name in dependencies:
            if dep_name in seen:
                continue  # Skip already processed

            dep_path = workspace_root / dep_name

            if dep_path.exists() and dep_path.is_dir():
                # Recursively load this dependency's rules and its dependencies
                dep_rules = cls.load_project_with_dependencies(dep_path, workspace_root)
                rules.extend(dep_rules)
                seen.add(dep_name)

        # Load this project's rules last (higher precedence)
        project_rules = cls.load_all()  # Global rules always included
        rules.extend(project_rules)

        return rules


__all__ = ["RuleLoader"]
