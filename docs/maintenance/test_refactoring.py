"""Test script for refactored documentation maintenance components.

Verifies that the new core components work correctly and maintain
backward compatibility with existing functionality.
"""

import sys
from dataclasses import dataclass
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Test constants
EXPECTED_SUCCESS_RATE = 80.0

# Import required modules for testing
try:
    from core.base_classes import FileMetadata, Issue, ValidationResult
    from core.config_manager import (
        AuditRules,
        ConfigManager,
        StyleGuide,
        ValidationConfig,
    )
    from core.file_discovery import DocumentationFinder
except ImportError:
    # Mock classes for testing when modules are not available
    class FileMetadata:
        """Mock file metadata class for testing."""

    @dataclass
    class Issue:
        """Mock issue class for testing."""

        type: str
        severity: str
        file: str
        description: str

    class ValidationResult:
        """Mock validation result class for testing."""

    class AuditRules:
        """Mock audit rules class for testing."""

    class ConfigManager:
        """Mock config manager class for testing."""

        def get_audit_rules(self) -> AuditRules:
            """Get audit rules configuration."""
            return AuditRules()

        def get_style_guide(self) -> StyleGuide:
            """Get style guide configuration."""
            return StyleGuide()

        def get_validation_config(self) -> ValidationConfig:
            """Get validation configuration."""
            return ValidationConfig()

        def validate_configs(self) -> None:
            """Validate all configurations."""

    class StyleGuide:
        """Mock style guide class for testing."""

    class ValidationConfig:
        """Mock validation config class for testing."""

    class DocumentationFinder:
        """Mock documentation finder class for testing."""

        def __init__(self, project_root: str) -> None:
            """Initialize finder with project root."""
            self.project_root = project_root

        def find_files(self) -> list[str]:
            """Find all documentation files."""
            return []

        def find_markdown_files(self) -> list[str]:
            """Find markdown files."""
            return []

        def categorize_files(self) -> dict[str, list[str]]:
            """Categorize files by type."""
            return {
                "readme": [],
                "changelog": [],
                "docs_root": [],
                "docs_subdir": [],
                "examples": [],
                "other": [],
            }

        def get_file_metadata(self, file_path: str) -> FileMetadata:
            """Get metadata for a file."""
            # Reserved for future file metadata implementation
            _ = file_path  # Reserved for future use
            return FileMetadata()

        def get_statistics(self) -> dict[str, int]:
            """Get finder statistics."""
            return {"total_files": 0}


def test_config_manager() -> bool | None:
    """Test the ConfigManager class."""
    try:
        # Test initialization
        config_manager = ConfigManager()

        # Test loading audit rules
        audit_rules = config_manager.get_audit_rules()
        if not isinstance(audit_rules, AuditRules):
            msg = f"Expected AuditRules, got {type(audit_rules)}"
            raise TypeError(msg)
        if not hasattr(audit_rules, "quality_thresholds"):
            msg = "AuditRules missing quality_thresholds attribute"
            raise ValueError(msg)

        # Test loading style guide
        style_guide = config_manager.get_style_guide()
        if not isinstance(style_guide, StyleGuide):
            msg = f"Expected StyleGuide, got {type(style_guide)}"
            raise TypeError(msg)
        if not hasattr(style_guide, "markdown"):
            msg = "StyleGuide missing markdown attribute"
            raise ValueError(msg)

        # Test loading validation config
        validation_config = config_manager.get_validation_config()
        if not isinstance(validation_config, ValidationConfig):
            msg = f"Expected ValidationConfig, got {type(validation_config)}"
            raise TypeError(msg)
        if not hasattr(validation_config, "link_validation"):
            msg = "ValidationConfig missing link_validation attribute"
            raise ValueError(msg)

        # Test config validation
        config_manager.validate_configs()

        return True

    except Exception:
        return False


def test_documentation_finder() -> bool | None:
    """Test the DocumentationFinder class."""
    try:
        # Test initialization
        project_root = Path(__file__).parent.parent.parent  # flext-quality root
        finder = DocumentationFinder(project_root)

        # Test file discovery
        files = finder.find_files()
        if not isinstance(files, list):
            msg = f"Expected list, got {type(files)}"
            raise TypeError(msg)
        if len(files) == 0:
            msg = "Should find some files"
            raise ValueError(msg)

        # Test markdown file filtering
        finder.find_markdown_files()

        # Test file categorization
        categories = finder.categorize_files()
        if not isinstance(categories, dict):
            msg = f"Expected dict, got {type(categories)}"
            raise TypeError(msg)
        if "readme" not in categories:
            msg = "Categories should contain 'readme'"
            raise ValueError(msg)

        # Test metadata
        if files:
            metadata = finder.get_file_metadata(files[0])
            if not isinstance(metadata, FileMetadata):
                msg = f"Expected FileMetadata, got {type(metadata)}"
                raise TypeError(msg)

        # Test statistics
        stats = finder.get_statistics()
        if not isinstance(stats, dict):
            msg = f"Expected dict, got {type(stats)}"
            raise TypeError(msg)
        if "total_files" not in stats:
            msg = "Statistics should contain 'total_files'"
            raise ValueError(msg)

        return True

    except Exception:
        return False


def test_base_classes() -> bool | None:
    """Test the base classes."""
    try:
        # Test Issue class
        issue = Issue(
            type="test_issue",
            severity="medium",
            file="test.md",
            description="Test issue description",
        )
        if issue.type != "test_issue":
            msg = f"Expected type 'test_issue', got '{issue.type}'"
            raise ValueError(msg)
        if issue.severity != "medium":
            msg = f"Expected severity 'medium', got '{issue.severity}'"
            raise ValueError(msg)

        # Test ValidationResult class
        result = ValidationResult()
        result.total_items = 10
        result.valid_items = 8
        if result.success_rate != EXPECTED_SUCCESS_RATE:
            msg = f"Expected success_rate {EXPECTED_SUCCESS_RATE}, got {result.success_rate}"
            raise ValueError(msg)

        # Test FileMetadata class
        test_file = Path(__file__)
        metadata = FileMetadata(test_file)
        if metadata.path != test_file:
            msg = f"Expected path {test_file}, got {metadata.path}"
            raise ValueError(msg)
        if metadata.size <= 0:
            msg = f"Expected size > 0, got {metadata.size}"
            raise ValueError(msg)

        return True

    except Exception:
        return False


def test_integration() -> bool | None:
    """Test integration between components."""
    try:
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
            if metadata.lines < 0:
                msg = "Metadata lines should be non-negative"
                raise ValueError(msg)
            if metadata.words < 0:
                msg = "Metadata words should be non-negative"
                raise ValueError(msg)

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
