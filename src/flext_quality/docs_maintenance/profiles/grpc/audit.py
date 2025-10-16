#!/usr/bin/env python3
"""FLEXT-gRPC Documentation Audit System.

Comprehensive content quality audit system for documentation maintenance.
Performs automated analysis of documentation files for quality, completeness,
freshness, and structural integrity.

Author: FLEXT-gRPC Documentation Maintenance System
Version: 1.0.0
"""

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from flext_core import (
    FlextTypes,
)

try:
    import frontmatter

    FRONTMATTER_AVAILABLE = True
except ImportError:
    frontmatter = None
    FRONTMATTER_AVAILABLE = False
import requests


@dataclass
class AuditResult:
    """Represents the result of auditing a single documentation file."""

    file_path: str
    file_size: int
    last_modified: float
    word_count: int
    quality_score: float
    structure_score: float
    completeness_score: float
    freshness_score: float
    issues: list[dict[str, object]]
    warnings: list[dict[str, object]]
    suggestions: list[dict[str, object]]
    metadata: dict[str, object]


@dataclass
class AuditReport:
    """Comprehensive audit report for all documentation."""

    timestamp: str
    total_files: int
    total_size: int
    average_quality: float
    quality_distribution: dict[str, int]
    critical_issues: list[dict[str, object]]
    recommendations: list[dict[str, object]]
    file_results: list[AuditResult]
    summary: dict[str, object]


class DocumentationAuditor:
    """Main class for performing documentation audits."""

    # Audit thresholds and constants
    THRESHOLD_DAYS = 30
    MAX_FILE_LENGTH = 1000

    # HTTP status codes
    HTTP_CLIENT_ERROR_START = 400

    def __init__(self, root_path: str = ".") -> None:
        """Initialize the documentation auditor.

        Args:
            root_path: Root path for documentation audit.

        """
        self.root_path = Path(root_path)
        self.config = self._load_config()
        self.results: list[AuditResult] = []

    def _load_config(self) -> dict[str, object]:
        """Load audit configuration."""
        config_path = self.root_path / "docs" / "maintenance" / "config.json"
        if config_path.exists():
            with Path(config_path).open("r", encoding="utf-8") as f:
                return json.load(f)

        # Default configuration
        return {
            "audit": {
                "file_patterns": ["*.md", "*.mdx"],
                "exclude_dirs": [".git", "node_modules", "__pycache__", ".venv"],
                "quality_thresholds": {"excellent": 90, "good": 80, "needs_work": 70},
                "freshness_threshold_days": 30,
                "min_word_count": 50,
                "max_word_count": 5000,
            },
            "structure": {
                "required_sections": ["Overview", "Installation", "Usage"],
                "heading_hierarchy": True,
                "max_line_length": 88,
            },
            "content": {
                "check_external_links": True,
                "check_images": True,
                "spell_check": False,
                "readability_check": True,
            },
        }

    def discover_files(self) -> list[Path]:
        """Discover all documentation files to audit."""
        files = []

        for pattern in self.config["audit"]["file_patterns"]:
            for file_path in self.root_path.rglob(pattern):
                # Skip excluded directories
                if any(
                    excl in str(file_path)
                    for excl in self.config["audit"]["exclude_dirs"]
                ):
                    continue

                # Skip if file is too large or too small
                if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
                    continue

                files.append(file_path)

        return sorted(files)

    def audit_file(self, file_path: Path) -> AuditResult:
        """Perform comprehensive audit of a single documentation file."""
        # Read file content
        content = file_path.read_text(encoding="utf-8")

        # Parse frontmatter if present
        if FRONTMATTER_AVAILABLE and frontmatter is not None:
            try:
                post = frontmatter.loads(content)
                metadata = dict[str, object](post.metadata)
                content_body = post.content
            except Exception:
                metadata = {}
                content_body = content
        else:
            metadata = {}
            content_body = content

        # Basic file statistics
        stat = file_path.stat()
        file_size = stat.st_size
        last_modified = stat.st_mtime

        # Content analysis
        word_count = len(content_body.split())
        lines = content_body.split("\n")

        # Quality analysis
        structure_score = self._analyze_structure(content_body, lines)
        completeness_score = self._analyze_completeness(content_body, metadata)
        freshness_score = self._analyze_freshness(last_modified, metadata)
        accuracy_score = self._analyze_accuracy(content_body)

        # Calculate overall quality score
        quality_score = (
            structure_score * 0.3
            + completeness_score * 0.25
            + freshness_score * 0.25
            + accuracy_score * 0.2
        )

        # Issue detection
        issues, warnings, suggestions = self._detect_issues(
            content_body, lines, metadata, file_path
        )

        return AuditResult(
            file_path=str(file_path.relative_to(self.root_path)),
            file_size=file_size,
            last_modified=last_modified,
            word_count=word_count,
            quality_score=round(quality_score, 1),
            structure_score=round(structure_score, 1),
            completeness_score=round(completeness_score, 1),
            freshness_score=round(freshness_score, 1),
            issues=issues,
            warnings=warnings,
            suggestions=suggestions,
            metadata=metadata,
        )

    def _analyze_structure(self, content: str, lines: FlextTypes.StringList) -> float:
        """Analyze document structure quality."""
        score = 100.0

        # Check heading hierarchy
        headings = re.findall(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)
        if self.config["structure"]["heading_hierarchy"]:
            heading_levels = [len(h[0]) for h in headings]
            if heading_levels:
                # Check for proper hierarchy (no skipping levels)
                for i in range(1, len(heading_levels)):
                    if heading_levels[i] > heading_levels[i - 1] + 1:
                        score -= 10

        # Check line length
        max_length = self.config["structure"]["max_line_length"]
        long_lines = [line for line in lines if len(line) > max_length]
        if long_lines:
            score -= min(20, len(long_lines) * 2)

        # Check for proper markdown formatting
        if not re.search(r"^#{1,6}\s+", content, re.MULTILINE):
            score -= 15  # No headings

        # Check for code blocks
        if "```" not in content:
            score -= 5  # No code examples

        # Check for lists
        if not re.search(r"^[-*+]\s", content, re.MULTILINE):
            score -= 5  # No lists

        return max(0, score)

    def _analyze_completeness(self, content: str, metadata: dict[str, object]) -> float:
        """Analyze documentation completeness."""
        score = 100.0

        # Check word count
        word_count = len(content.split())
        min_words = self.config["audit"]["min_word_count"]
        max_words = self.config["audit"]["max_word_count"]

        if word_count < min_words:
            score -= 30
        elif word_count > max_words:
            score -= 10  # Too long, may need splitting

        # Check for required sections
        required_sections = self.config["structure"]["required_sections"]
        missing_sections = 0
        for section in required_sections:
            if not re.search(
                rf"^#{1, 3}\s+{re.escape(section)}",
                content,
                re.MULTILINE | re.IGNORECASE,
            ):
                missing_sections += 1

        if missing_sections > 0:
            score -= missing_sections * 15

        # Check metadata completeness
        if not metadata.get("title"):
            score -= 5
        if not metadata.get("last_updated") and not metadata.get("updated"):
            score -= 5

        # Check for TODO/FIXME markers (reduce completeness)
        todos = len(re.findall(r"\b(TODO|FIXME|XXX)\b", content, re.IGNORECASE))
        if todos > 0:
            score -= min(20, todos * 5)

        return max(0, score)

    def _analyze_freshness(
        self, last_modified: float, metadata: dict[str, object]
    ) -> float:
        """Analyze documentation freshness."""
        score = 100.0

        # Check file modification time
        threshold_days = self.config["audit"]["freshness_threshold_days"]
        days_since_modified = (time.time() - last_modified) / (24 * 3600)

        if days_since_modified > threshold_days:
            # Gradual score reduction based on age
            age_penalty = min(50, (days_since_modified - threshold_days) / 10 * 5)
            score -= age_penalty

        # Check metadata dates
        last_updated = metadata.get("last_updated") or metadata.get("updated")
        if last_updated:
            try:
                if isinstance(last_updated, str):
                    updated_date = datetime.fromisoformat(last_updated)
                else:
                    updated_date = datetime.fromtimestamp(last_updated, tz=UTC)

                days_since_updated = (datetime.now(UTC) - updated_date).days
                if days_since_updated > DocumentationAuditor.THRESHOLD_DAYS:
                    score -= min(30, (days_since_updated - threshold_days) / 5 * 5)
            except Exception:
                score -= 10  # Invalid date format

        return max(0, score)

    def _analyze_accuracy(self, content: str) -> float:
        """Analyze content accuracy (basic checks)."""
        score = 100.0

        # Check for obvious placeholders
        placeholders = re.findall(
            r"\b(PLACEHOLDER|TODO|FIXME|TBD)\b", content, re.IGNORECASE
        )
        if placeholders:
            score -= min(30, len(placeholders) * 10)

        # Check for broken internal links (basic)
        internal_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        broken_links = 0
        for text, link in internal_links:
            if link.startswith("#") and not re.search(
                rf"^#{1, 6}\s+{re.escape(text)}", content, re.MULTILINE | re.IGNORECASE
            ):
                broken_links += 1

        if broken_links > 0:
            score -= min(20, broken_links * 5)

        # Check for consistent terminology
        if "grpc" in content.lower() and "gRPC" not in content:
            score -= 5  # Inconsistent capitalization

        return max(0, score)

    def _detect_issues(
        self,
        content: str,
        lines: FlextTypes.StringList,
        metadata: dict[str, object],
        file_path: Path,
    ) -> tuple[
        list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]
    ]:
        """Detect specific issues, warnings, and suggestions."""
        issues = []
        warnings = []
        suggestions = []

        # Critical issues
        if len(content.strip()) == 0:
            issues.append({
                "type": "empty_file",
                "severity": "critical",
                "message": f"File {file_path} appears to be empty",
                "line": 0,
            })

        if not re.search(r"^#{1,6}\s+", content, re.MULTILINE):
            issues.append({
                "type": "no_headings",
                "severity": "high",
                "message": "No headings found - document lacks structure",
                "line": 0,
            })

        # Warnings
        if len(lines) > DocumentationAuditor.MAX_FILE_LENGTH:
            warnings.append({
                "type": "long_file",
                "severity": "medium",
                "message": f"File {file_path} is very long ({len(lines)} lines) - consider splitting",
                "line": 0,
            })

        todos = re.findall(r"\b(TODO|FIXME|XXX)\b", content, re.IGNORECASE)
        if todos:
            warnings.append({
                "type": "todo_markers",
                "severity": "low",
                "message": f"Found {len(todos)} TODO/FIXME markers",
                "line": 0,
            })

        # Check for broken external links (basic check)
        if self.config["content"]["check_external_links"]:
            external_links = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", content)
            for _text, url in external_links:
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code >= self.HTTP_CLIENT_ERROR_START:
                        warnings.append({
                            "type": "broken_link",
                            "severity": "medium",
                            "message": f"Link may be broken: {url}",
                            "line": 0,
                        })
                except Exception:
                    warnings.append({
                        "type": "link_check_failed",
                        "severity": "low",
                        "message": f"Could not verify link: {url}",
                        "line": 0,
                    })

        # Suggestions
        if not metadata.get("title"):
            suggestions.append({
                "type": "add_title",
                "message": "Consider adding a title in frontmatter",
                "action": "Add 'title: \"Document Title\"' to frontmatter",
            })

        if r"```" not in content:
            suggestions.append({
                "type": "add_code_examples",
                "message": "Consider adding code examples",
                "action": "Add code blocks with ```language syntax",
            })

        if not re.search(r"!\[", content):
            suggestions.append({
                "type": "add_visuals",
                "message": "Consider adding diagrams or images",
                "action": "Add relevant images with ![alt text](path)",
            })

        return issues, warnings, suggestions

    def run_audit(self, files: list[Path] | None = None) -> AuditReport:
        """Run complete audit on all or specified documentation files."""
        if files is None:
            files = self.discover_files()

        self.results = []
        for file_path in files:
            try:
                result = self.audit_file(file_path)
                self.results.append(result)
                self._get_quality_level(result.quality_score)
            except Exception:
                pass

        return self._generate_report()

    def _get_quality_level(self, score: float) -> str:
        """Get quality level indicator based on score."""
        if score >= self.config["audit"]["quality_thresholds"]["excellent"]:
            return "✅"
        if score >= self.config["audit"]["quality_thresholds"]["good"]:
            return "⚠️"
        if score >= self.config["audit"]["quality_thresholds"]["needs_work"]:
            return "🟡"
        return "❌"

    def _generate_report(self) -> AuditReport:
        """Generate comprehensive audit report."""
        total_files = len(self.results)
        total_size = sum(r.file_size for r in self.results)
        average_quality = (
            sum(r.quality_score for r in self.results) / total_files
            if total_files > 0
            else 0
        )

        # Quality distribution
        quality_distribution = {
            "excellent": 0,
            "good": 0,
            "needs_work": 0,
            "critical": 0,
        }

        for result in self.results:
            if (
                result.quality_score
                >= self.config["audit"]["quality_thresholds"]["excellent"]
            ):
                quality_distribution["excellent"] += 1
            elif (
                result.quality_score
                >= self.config["audit"]["quality_thresholds"]["good"]
            ):
                quality_distribution["good"] += 1
            elif (
                result.quality_score
                >= self.config["audit"]["quality_thresholds"]["needs_work"]
            ):
                quality_distribution["needs_work"] += 1
            else:
                quality_distribution["critical"] += 1

        # Critical issues
        critical_issues = []
        for result in self.results:
            critical_issues.extend(
                {"file": result.file_path, **issue}
                for issue in result.issues
                if issue["severity"] in {"critical", "high"}
            )

        # Recommendations
        recommendations = []
        for result in self.results:
            recommendations.extend(
                {"file": result.file_path, **suggestion}
                for suggestion in result.suggestions
            )

        # Summary statistics
        summary = {
            "total_words": sum(r.word_count for r in self.results),
            "oldest_file_days": 0,
            "newest_file_days": 0,
            "quality_trends": {
                "excellent": quality_distribution["excellent"] / total_files * 100,
                "good": quality_distribution["good"] / total_files * 100,
                "needs_work": quality_distribution["needs_work"] / total_files * 100,
                "critical": quality_distribution["critical"] / total_files * 100,
            },
        }

        if self.results:
            now = time.time()
            ages = [(now - r.last_modified) / (24 * 3600) for r in self.results]
            summary["oldest_file_days"] = int(max(ages))
            summary["newest_file_days"] = int(min(ages))

        return AuditReport(
            timestamp=datetime.now(UTC).isoformat(),
            total_files=total_files,
            total_size=total_size,
            average_quality=round(average_quality, 1),
            quality_distribution=quality_distribution,
            critical_issues=critical_issues,
            recommendations=recommendations,
            file_results=self.results,
            summary=summary,
        )

    def save_report(self, report: AuditReport, output_path: Path | None = None) -> None:
        """Save audit report to file."""
        if output_path is None:
            output_path = (
                self.root_path
                / "docs"
                / "maintenance"
                / "reports"
                / f"audit_{int(time.time())}.json"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with Path(output_path).open("w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2, default=str)

    def print_summary(self, report: AuditReport) -> None:
        """Print audit summary to console."""
        for count in report.quality_distribution.values():
            count / report.total_files * 100 if report.total_files > 0 else 0

        if report.critical_issues:
            for _issue in report.critical_issues[:5]:  # Show first 5
                pass

        if report.recommendations:
            for _rec in report.recommendations[:5]:  # Show first 5
                pass


def main() -> int:
    """Main entry point for documentation audit."""
    parser = argparse.ArgumentParser(
        description="FLEXT-gRPC Documentation Audit System"
    )
    parser.add_argument("--path", default=".", help="Root path to audit")
    parser.add_argument("--output", help="Output path for report")
    parser.add_argument(
        "--comprehensive", action="store_true", help="Run comprehensive audit"
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")

    args = parser.parse_args()

    # Create auditor
    auditor = DocumentationAuditor(args.path)

    # Discover files
    files = auditor.discover_files()

    if not files:
        return 1

    # Run audit
    report = auditor.run_audit(files)

    # Save report
    output_path = Path(args.output) if args.output else None

    auditor.save_report(report, output_path)

    # Print summary
    if not args.quiet:
        auditor.print_summary(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
