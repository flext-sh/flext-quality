#!/usr/bin/env python3
"""Test script for refactored documentation maintenance components.

Verifies that the new core components work correctly and maintain
backward compatibility with existing functionality.
"""

import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))


def test_config_manager() -> bool | None:
    """Test the ConfigManager class."""
    try:
        from core.config_manager import (
            AuditRules,
            ConfigManager,
            StyleGuide,
            ValidationConfig,
        )

        # Test initialization
        config_manager = ConfigManager()

        # Test loading audit rules
        audit_rules = config_manager.get_audit_rules()
        if not isinstance(audit_rules, AuditRules):
            raise ValueError(f"Expected AuditRules, got {type(audit_rules)}")
        if not hasattr(audit_rules, "quality_thresholds"):
            raise ValueError("AuditRules missing quality_thresholds attribute")

        # Test loading style guide
        style_guide = config_manager.get_style_guide()
        if not isinstance(style_guide, StyleGuide):
            raise ValueError(f"Expected StyleGuide, got {type(style_guide)}")
        if not hasattr(style_guide, "markdown"):
            raise ValueError("StyleGuide missing markdown attribute")

        # Test loading validation config
        validation_config = config_manager.get_validation_config()
        if not isinstance(validation_config, ValidationConfig):
            raise ValueError(f"Expected ValidationConfig, got {type(validation_config)}")
        if not hasattr(validation_config, "link_validation"):
            raise ValueError("ValidationConfig missing link_validation attribute")

        # Test config validation
        config_manager.validate_configs()

        return True

    except Exception:
        return False


def test_documentation_finder() -> bool | None:
    """Test the DocumentationFinder class."""
    try:
        from core.base_classes import FileMetadata
        from core.file_discovery import DocumentationFinder

        # Test initialization
        project_root = Path(__file__).parent.parent.parent  # flext-quality root
        finder = DocumentationFinder(project_root)

        # Test file discovery
        files = finder.find_files()
        if not isinstance(files, list):
            raise ValueError(f"Expected list, got {type(files)}")
        if len(files) == 0:
            raise ValueError("Should find some files")

        # Test markdown file filtering
        finder.find_markdown_files()

        # Test file categorization
        categories = finder.categorize_files()
        if not isinstance(categories, dict):
            raise ValueError(f"Expected dict, got {type(categories)}")
        if "readme" not in categories:
            raise ValueError("Categories should contain 'readme'")

        # Test metadata
        if files:
            metadata = finder.get_file_metadata(files[0])
            if not isinstance(metadata, FileMetadata):
                raise ValueError(f"Expected FileMetadata, got {type(metadata)}")

        # Test statistics
        stats = finder.get_statistics()
        if not isinstance(stats, dict):
            raise ValueError(f"Expected dict, got {type(stats)}")
        if "total_files" not in stats:
            raise ValueError("Statistics should contain 'total_files'")

        return True

    except Exception:
        return False


def test_base_classes() -> bool | None:
    """Test the base classes."""
    try:
        from core.base_classes import FileMetadata, Issue, ValidationResult

        # Test Issue class
        issue = Issue(
            type="test_issue",
            severity="medium",
            file="test.md",
            description="Test issue description",
        )
        if issue.type != "test_issue":
            raise ValueError(f"Expected type 'test_issue', got '{issue.type}'")
        if issue.severity != "medium":
            raise ValueError(f"Expected severity 'medium', got '{issue.severity}'")

        # Test ValidationResult class
        result = ValidationResult()
        result.total_items = 10
        result.valid_items = 8
        if result.success_rate != 80.0:
            raise ValueError(f"Expected success_rate 80.0, got {result.success_rate}")

        # Test FileMetadata class
        test_file = Path(__file__)
        metadata = FileMetadata(test_file)
        if metadata.path != test_file:
            raise ValueError(f"Expected path {test_file}, got {metadata.path}")
        if metadata.size <= 0:
            raise ValueError(f"Expected size > 0, got {metadata.size}")

        return True

    except Exception:
        return False


def test_integration() -> bool | None:
    """Test integration between components."""
    try:
        from core.config_manager import ConfigManager
        from core.file_discovery import DocumentationFinder

        # Test that components work together
        config_manager = ConfigManager()
        config_manager.get_audit_rules()

        project_root = Path(__file__).parent.parent.parent
        finder = DocumentationFinder(project_root)

        # Test that finder can use config settings
        files = finder.find_files()
        if files:
            # Test metadata extraction
            metadata = finder.get_file_metadata(files[0])
            assert metadata.lines >= 0
            assert metadata.words >= 0

        return True

    except Exception:
        return False


def main() -> int:
    """Run all tests."""
    tests = [
        test_base_classes,
        test_config_manager,
        test_documentation_finder,
        test_integration,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    if failed == 0:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
