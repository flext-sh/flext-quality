"""Language Detection System for FLEXT Rules - FASE 6.

Detects programming language from file path and content.
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar


class LanguageDetector:
    """Detect programming language from file path and content."""

    EXT_TO_LANG: ClassVar[dict[str, str]] = {
        ".py": "python",
        ".pyw": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".go": "go",
        ".rs": "rust",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
        ".fish": "bash",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".jsonc": "json",
        ".xml": "xml",
        ".html": "html",
        ".htm": "html",
        ".css": "css",
        ".scss": "scss",
        ".less": "less",
        ".sql": "sql",
        ".proto": "protobuf",
        ".graphql": "graphql",
        ".gql": "graphql",
    }

    @classmethod
    def detect_from_path(cls, file_path: str) -> str:
        """Detect language from file extension.

        Args:
            file_path: Path to file

        Returns:
            Language name (e.g., "python", "typescript", "unknown")

        """
        suffix = Path(file_path).suffix.lower()
        return cls.EXT_TO_LANG.get(suffix, "unknown")

    @classmethod
    def detect_from_content(cls, content: str) -> str:
        """Detect language from shebang or syntax.

        Args:
            content: File content

        Returns:
            Language name

        """
        lines = content.split("\n", 5)  # Check first 5 lines

        # Check shebang
        if lines and lines[0].startswith("#!"):
            shebang = lines[0].lower()
            if "python" in shebang:
                return "python"
            if "bash" in shebang or "sh" in shebang:
                return "bash"
            if "node" in shebang or "javascript" in shebang:
                return "javascript"

        # Check for TypeScript/JavaScript specific syntax
        content_lower = content.lower()
        if (
            "interface " in content_lower
            and ":" in content
            and ("extends" in content_lower or "implements" in content_lower)
        ):
            return "typescript"

        # Check for Python specific syntax
        if ("from __future__" in content or "import " in content) and (
            "from " in content and " import " in content
        ):
            return "python"

        # Check for bash syntax
        if "#!/" in lines[0] if lines else False:
            return "bash"
        if "${" in content or "$((" in content:
            return "bash"

        # Check for JSON
        if content.strip().startswith("{") or content.strip().startswith("["):
            return "json"

        return "unknown"

    @classmethod
    def detect(cls, file_path: str, content: str | None = None) -> str:
        """Auto-detect language (path first, then content).

        Args:
            file_path: Path to file
            content: Optional file content for context

        Returns:
            Language name

        """
        # Try path-based detection first (fastest)
        lang = cls.detect_from_path(file_path)

        # If path detection fails and content available, try content-based
        if lang == "unknown" and content:
            lang = cls.detect_from_content(content)

        return lang
