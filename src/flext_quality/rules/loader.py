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

from pathlib import Path
from typing import Any

import yaml

from .models import RuleCategory, RuleSeverity, ValidationRule


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

        Returns:
            List of ValidationRule objects from all global YAML files.

        Raises:
            ValueError: If any YAML file has parsing or validation errors.

        """
        rules: list[ValidationRule] = []

        if not cls.DATA_DIR.exists():
            return rules

        for yaml_file in sorted(cls.DATA_DIR.glob("*.yaml")):
            rules.extend(cls.load_file(yaml_file))

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


__all__ = ["RuleLoader"]
