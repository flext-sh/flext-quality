"""Plugin protocol defining standard interface for all flext-quality plugins."""

from __future__ import annotations

from typing import Any, Protocol

from flext_core import FlextResult as r


class FlextQualityPlugin(Protocol):
    """Standard interface that all flext-quality plugins must implement.

    Plugins extend the engine's capabilities by providing:
    - Custom rule loading
    - Specialized validators
    - Language-specific analyzers
    - Integration with external tools
    """

    def initialize(self, config: dict[str, Any]) -> r[None]:
        """Initialize plugin with configuration.

        Args:
            config: Plugin-specific configuration

        Returns:
            Success if initialized, Failure with error message

        """
        ...

    def validate(
        self,
        file_path: str,
        content: str,
        language: str | None = None,
    ) -> r[dict[str, Any]]:
        """Validate file content using plugin's logic.

        Args:
            file_path: Path to file being validated
            content: File content as string
            language: Detected language (optional, plugin may detect itself)

        Returns:
            Success with violation dict, Failure if validation error

        """
        ...

    def detect(
        self,
        file_path: str,
        content: str | None = None,
    ) -> r[str]:
        """Detect programming language (optional method for LanguageDetectorPlugin).

        Args:
            file_path: Path to file (for extension detection)
            content: Optional content (for shebang/syntax detection)

        Returns:
            Success with language string (e.g., "python", "typescript")

        """
        ...
