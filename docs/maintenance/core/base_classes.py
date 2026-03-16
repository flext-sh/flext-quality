"""FLEXT Quality Documentation Maintenance - Base Classes.

Common base classes and interfaces for all maintenance system components.
Provides consistent interfaces and shared functionality.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, Field

type GenericItem = (
    str | int | float | bool | Path | dict[str, str | int | float | bool | None]
)


class Issue(BaseModel):
    """Represents a documentation quality issue."""

    type: str = Field(description="Issue type identifier")
    severity: str = Field(
        description="Severity level: critical, high, medium, low, info"
    )
    file: str = Field(description="File path where issue was found")
    line: int | None = Field(default=None, description="Line number of the issue")
    description: str = Field(default="", description="Detailed issue description")
    recommendation: str = Field(default="", description="Recommended fix for the issue")
    context: dict[str, str | int | float | bool | None] | None = Field(
        default=None,
        description="Additional context data",
    )

    def to_dict(
        self,
    ) -> dict[str, str | int | dict[str, str | int | float | bool | None] | None]:
        """Convert issue to dictionary representation."""
        return {
            "type": self.type,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "description": self.description,
            "recommendation": self.recommendation,
            "context": self.context if self.context is not None else {},
        }


class ValidationResult(BaseModel):
    """Result of a validation operation."""

    total_items: int = Field(default=0, description="Total items validated")
    valid_items: int = Field(default=0, description="Number of valid items")
    invalid_items: int = Field(default=0, description="Number of invalid items")
    issues: list[Issue] = []
    warnings: list[str] = Field(default_factory=list, description="Warning messages")
    errors: list[str] = Field(default_factory=list, description="Error messages")
    metadata: dict[str, str | int | float | bool] = Field(
        default_factory=dict,
        description="Additional metadata",
    )

    @property
    def success_rate(self) -> float:
        """Calculate success rate as a percentage."""
        if self.total_items == 0:
            return 100.0
        return (self.valid_items / self.total_items) * 100.0

    def add_issue(self, issue: Issue) -> None:
        """Add an issue to the result."""
        self.issues.append(issue)
        if issue.severity == "critical":
            self.invalid_items += 1
        else:
            self.valid_items += 1

    def to_dict(
        self,
    ) -> dict[
        str,
        float
        | int
        | list[str]
        | list[dict[str, str | int | dict[str, str | int | float | bool | None] | None]]
        | dict[str, str | int | float | bool],
    ]:
        """Convert result to dictionary representation."""
        return {
            "total_items": self.total_items,
            "valid_items": self.valid_items,
            "invalid_items": self.invalid_items,
            "success_rate": self.success_rate,
            "issues": [issue.to_dict() for issue in self.issues],
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata,
        }


class BaseAuditor(ABC):
    """Base class for all audit operations.

    Provides common functionality and interface for audit components.
    """

    def __init__(self, name: str) -> None:
        """Initialize the audit base class with a name."""
        self.name = name
        self.issues: list[Issue] = []
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None

    def start_audit(self) -> None:
        """Mark the start of an audit operation."""
        self.start_time = datetime.now(UTC)
        self.issues = []

    def end_audit(self) -> None:
        """Mark the end of an audit operation."""
        self.end_time = datetime.now(UTC)

    def add_issue(self, issue: Issue) -> None:
        """Add an issue found during audit."""
        self.issues.append(issue)

    @property
    def duration(self) -> float | None:
        """Get the duration of the audit in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @property
    def issue_count(self) -> int:
        """Get the total number of issues found."""
        return len(self.issues)

    def get_issues_by_severity(self, severity: str) -> list[Issue]:
        """Get issues filtered by severity level."""
        return [issue for issue in self.issues if issue.severity == severity]

    @abstractmethod
    def audit(self, files: list[Path]) -> ValidationResult:
        """Perform the audit operation on given files."""

    def get_summary(self) -> dict[str, dict[str, int] | float | int | str | None]:
        """Get a summary of the audit results."""
        return {
            "auditor": self.name,
            "duration": self.duration,
            "total_issues": self.issue_count,
            "issues_by_severity": {
                "critical": len(self.get_issues_by_severity("critical")),
                "high": len(self.get_issues_by_severity("high")),
                "medium": len(self.get_issues_by_severity("medium")),
                "low": len(self.get_issues_by_severity("low")),
                "info": len(self.get_issues_by_severity("info")),
            },
        }


class BaseValidator(ABC):
    """Base class for all validation operations.

    Provides common functionality and interface for validation components.
    """

    def __init__(self, name: str) -> None:
        """Initialize the validator base class with a name."""
        self.name = name
        self.results: ValidationResult | None = None

    def validate(self, items: list[GenericItem]) -> ValidationResult:
        """Perform validation on given items."""
        self.results = ValidationResult()
        self.results.total_items = len(items)

        self._validate_items(items)

        return self.results

    @abstractmethod
    def _validate_items(self, items: list[GenericItem]) -> None:
        """Implementation-specific validation logic."""

    def get_summary(self) -> dict[str, float | int | str] | dict[str, str]:
        """Get a summary of validation results."""
        if not self.results:
            return {"validator": self.name, "status": "not_run"}

        return {
            "validator": self.name,
            "success_rate": self.results.success_rate,
            "total_items": self.results.total_items,
            "valid_items": self.results.valid_items,
            "invalid_items": self.results.invalid_items,
            "issues": len(self.results.issues),
            "warnings": len(self.results.warnings),
            "errors": len(self.results.errors),
        }


class BaseReporter(ABC):
    """Base class for all reporting operations.

    Provides common functionality and interface for report generation.
    """

    def __init__(self, name: str, template_dir: Path | None = None) -> None:
        """Initialize the reporter base class with name and template directory."""
        self.name = name
        self.template_dir = template_dir or Path(__file__).parent.parent / "templates"

    @abstractmethod
    def generate_report(
        self,
        data: dict[
            str,
            str
            | int
            | float
            | bool
            | dict[str, str | int | float | bool | None]
            | None,
        ],
        output_format: str = "html",
    ) -> str:
        """Generate a report from the given data."""

    def save_report(self, content: str, filename: str, output_dir: Path) -> Path:
        """Save report content to a file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / f"{filename}.html"
        _ = filepath.write_text(content, encoding="utf-8")
        return filepath


class BaseAnalyzer(ABC):
    """Base class for all analysis operations.

    Provides common functionality and interface for content analysis.
    """

    def __init__(self, name: str) -> None:
        """Initialize the analyzer base class with a name."""
        self.name = name
        self.metrics: dict[str, str | int | float | bool | None] = {}

    def analyze(
        self, content: str, filepath: Path | None = None
    ) -> dict[str, str | int | float | bool | None]:
        """Analyze the given content and return metrics."""
        self.metrics = {
            "analyzer": self.name,
            "filepath": str(filepath) if filepath else None,
        }

        try:
            self._analyze_content(content)
        except Exception as e:
            self.metrics["error"] = str(e)
            self.metrics["success"] = False
        else:
            self.metrics["success"] = True

        return self.metrics

    @abstractmethod
    def _analyze_content(self, content: str) -> None:
        """Implementation-specific analysis logic."""

    def get_score(self) -> float | None:
        """Get a quality score from the analysis (0-100)."""
        val = self.metrics.get("quality_score")
        return float(val) if isinstance(val, (int, float)) else None

    def get_readability_score(self) -> float | None:
        """Get a readability score from the analysis."""
        val = self.metrics.get("readability_score")
        return float(val) if isinstance(val, (int, float)) else None


class Config(Protocol):
    """Protocol for configuration objects."""

    def get(self, key: str, default: str | float | bool | None = None) -> None:
        """Get a configuration value."""
        ...

    def __getitem__(self, key: str) -> None:
        """Get a configuration value with bracket notation."""
        ...


class FileMetadata:
    """Metadata about a documentation file."""

    def __init__(self, path: Path) -> None:
        """Initialize file metadata from a file path."""
        self.path = path
        self.size = path.stat().st_size if path.exists() else 0
        self.modified_time = path.stat().st_mtime if path.exists() else 0
        self.extension = path.suffix.lower()
        self.is_markdown = self.extension in {".md", ".mdx"}
        self.lines = 0
        self.words = 0

        if path.exists():
            self._analyze_content()

    def _analyze_content(self) -> None:
        """Analyze file content for basic metrics."""
        try:
            content = self.path.read_text(encoding="utf-8")
            self.lines = content.count("\n") + 1
            self.words = len(content.split())
        except (OSError, UnicodeDecodeError):
            # If we can't read the file, keep defaults (file not accessible or not text)
            pass

    def to_dict(self) -> dict[str, bool | float | int | str]:
        """Convert metadata to dictionary."""
        return {
            "path": str(self.path),
            "size": self.size,
            "modified_time": self.modified_time,
            "extension": self.extension,
            "is_markdown": self.is_markdown,
            "lines": self.lines,
            "words": self.words,
        }
