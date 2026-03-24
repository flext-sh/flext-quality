"""FLEXT Quality Documentation Maintenance - Base Classes.

Common base classes and interfaces for all maintenance system components.
Provides consistent interfaces and shared functionality.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path

from flext_quality import m, p, t


class BaseAuditor(ABC):
    """Base class for all audit operations.

    Provides common functionality and interface for audit components.
    """

    def __init__(self, name: str) -> None:
        """Initialize the audit base class with a name."""
        self.name = name
        self.issues: Sequence[m.Quality.Issue] = []
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None

    def start_audit(self) -> None:
        """Mark the start of an audit operation."""
        self.start_time = datetime.now(UTC)
        self.issues = []

    def end_audit(self) -> None:
        """Mark the end of an audit operation."""
        self.end_time = datetime.now(UTC)

    def add_issue(self, issue: m.Quality.Issue) -> None:
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

    def get_issues_by_severity(self, severity: str) -> Sequence[m.Quality.Issue]:
        """Get issues filtered by severity level."""
        return [issue for issue in self.issues if issue.severity == severity]

    @abstractmethod
    def audit(self, files: Sequence[Path]) -> m.Quality.ValidationResult:
        """Perform the audit operation on given files."""

    def get_summary(self) -> Mapping[str, Mapping[str, int] | float | int | str | None]:
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
        self.results: m.Quality.ValidationResult | None = None

    def validate(
        self, items: Sequence[t.Quality.GenericItem]
    ) -> m.Quality.ValidationResult:
        """Perform validation on given items."""
        self.results = m.Quality.ValidationResult()
        self.results.total_items = len(items)

        self._validate_items(items)

        return self.results

    @abstractmethod
    def _validate_items(self, items: Sequence[t.Quality.GenericItem]) -> None:
        """Implementation-specific validation logic."""

    def get_summary(self) -> Mapping[str, float | int | str] | t.StrMapping:
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
        data: Mapping[
            str,
            str | int | float | bool | Mapping[str, t.Primitives | None] | None,
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
        self.metrics: Mapping[str, t.Primitives | None] = {}

    def analyze(
        self, content: str, filepath: Path | None = None
    ) -> Mapping[str, t.Primitives | None]:
        """Analyze the given content and return metrics."""
        self.metrics = {
            "analyzer": self.name,
            "filepath": str(filepath) if filepath else None,
        }

        try:
            self._analyze_content(content)
        except (
            FileNotFoundError,
            PermissionError,
            UnicodeDecodeError,
            OSError,
            ValueError,
        ) as e:
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


# Re-export canonical protocol from protocols namespace for backward compatibility
Config = p.Quality.DocsConfig
