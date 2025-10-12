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
        assert isinstance(audit_rules, AuditRules)
        assert hasattr(audit_rules, "quality_thresholds")

        # Test loading style guide
        style_guide = config_manager.get_style_guide()
        assert isinstance(style_guide, StyleGuide)
        assert hasattr(style_guide, "markdown")

        # Test loading validation config
        validation_config = config_manager.get_validation_config()
        assert isinstance(validation_config, ValidationConfig)
        assert hasattr(validation_config, "link_validation")

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
        assert isinstance(files, list)
        assert len(files) > 0  # Should find some files

        # Test markdown file filtering
        finder.find_markdown_files()

        # Test file categorization
        categories = finder.categorize_files()
        assert isinstance(categories, dict)
        assert "readme" in categories

        # Test metadata
        if files:
            metadata = finder.get_file_metadata(files[0])
            assert isinstance(metadata, FileMetadata)

        # Test statistics
        stats = finder.get_statistics()
        assert isinstance(stats, dict)
        assert "total_files" in stats

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
        assert issue.type == "test_issue"
        assert issue.severity == "medium"

        # Test ValidationResult class
        result = ValidationResult()
        result.total_items = 10
        result.valid_items = 8
        assert result.success_rate == 80.0

        # Test FileMetadata class
        test_file = Path(__file__)
        metadata = FileMetadata(test_file)
        assert metadata.path == test_file
        assert metadata.size > 0

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
