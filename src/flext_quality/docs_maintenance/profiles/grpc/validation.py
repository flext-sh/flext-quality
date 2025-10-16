#!/usr/bin/env python3
"""FLEXT-gRPC Link and Reference Validation System.

Comprehensive validation system for documentation links, references,
and style consistency checking.

Author: FLEXT-gRPC Documentation Maintenance System
Version: 1.0.0
"""

import json
import operator
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path

import requests
from flext_core import (
    FlextTypes,
)


@dataclass
class LinkValidationResult:
    """Result of validating a single link."""

    url: str
    status: str
    status_code: int | None
    response_time: float
    error_message: str | None
    redirect_url: str | None


@dataclass
class ReferenceValidationResult:
    """Result of validating internal references."""

    reference: str
    type: str  # 'heading', 'file', 'anchor'
    found: bool
    target_file: str | None
    line_number: int | None


@dataclass
class StyleCheckResult:
    """Result of style consistency checking."""

    file_path: str
    issues: list[dict[str, object]]
    score: float


@dataclass
class ValidationReport:
    """Comprehensive validation report."""

    timestamp: str
    link_results: list[LinkValidationResult]
    reference_results: list[ReferenceValidationResult]
    style_results: list[StyleCheckResult]
    summary: dict[str, object]


class LinkValidator:
    """Validate external and internal links in documentation."""

    def __init__(
        self, timeout: int = 10, max_retries: int = 3, user_agent: str | None = None
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent or "FLEXT-gRPC-Doc-Validator/1.0"

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def validate_external_link(self, url: str) -> LinkValidationResult:
        """Validate an external link."""
        start_time = time.time()

        for attempt in range(self.max_retries):
            try:
                response = self.session.head(
                    url, timeout=self.timeout, allow_redirects=True
                )

                response_time = time.time() - start_time
                redirect_url = response.url if response.url != url else None

                if response.status_code < 400:
                    return LinkValidationResult(
                        url=url,
                        status="valid",
                        status_code=response.status_code,
                        response_time=round(response_time, 2),
                        error_message=None,
                        redirect_url=redirect_url,
                    )
                return LinkValidationResult(
                    url=url,
                    status="broken",
                    status_code=response.status_code,
                    response_time=round(response_time, 2),
                    error_message=f"HTTP {response.status_code}",
                    redirect_url=redirect_url,
                )

            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    return LinkValidationResult(
                        url=url,
                        status="timeout",
                        status_code=None,
                        response_time=round(time.time() - start_time, 2),
                        error_message="Request timed out",
                        redirect_url=None,
                    )
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    return LinkValidationResult(
                        url=url,
                        status="error",
                        status_code=None,
                        response_time=round(time.time() - start_time, 2),
                        error_message=str(e),
                        redirect_url=None,
                    )

        # Should not reach here, but just in case
        return LinkValidationResult(
            url=url,
            status="unknown",
            status_code=None,
            response_time=0,
            error_message="Validation failed",
            redirect_url=None,
        )

    def validate_internal_links(
        self, content: str, file_path: Path, all_files: list[Path]
    ) -> list[ReferenceValidationResult]:
        """Validate internal links within documentation."""
        results = []

        # Find all internal links (not starting with http/https)
        internal_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

        for _text, link in internal_links:
            if link.startswith(("http://", "https://", "mailto:")):
                continue  # Skip external links

            if link.startswith("#"):
                # Anchor link - check if heading exists in same file
                results.append(self._validate_anchor_link(link[1:], content, file_path))
            elif link.startswith(("./", "../")) or not link.startswith("/"):
                # Relative file link
                results.append(self._validate_file_link(link, file_path, all_files))
            else:
                # Absolute path link
                results.append(self._validate_file_link(link, file_path, all_files))

        return results

    def _validate_anchor_link(
        self, anchor: str, content: str, file_path: Path
    ) -> ReferenceValidationResult:
        """Validate anchor link within the same file."""
        # Convert anchor to heading text (remove special chars, normalize)
        heading_text = re.sub(r"[^\w\s-]", "", anchor.replace("-", " ")).strip()

        # Look for heading in content
        heading_pattern = rf"^#{1, 6}\s+{re.escape(heading_text)}"
        if re.search(heading_pattern, content, re.MULTILINE | re.IGNORECASE):
            return ReferenceValidationResult(
                reference=f"#{anchor}",
                type="anchor",
                found=True,
                target_file=str(file_path),
                line_number=None,
            )
        return ReferenceValidationResult(
            reference=f"#{anchor}",
            type="anchor",
            found=False,
            target_file=str(file_path),
            line_number=None,
        )

    def _validate_file_link(
        self, link: str, source_file: Path, all_files: list[Path]
    ) -> ReferenceValidationResult:
        """Validate file link."""
        try:
            # Resolve the link relative to source file
            if link.startswith("/"):
                # Absolute path from project root
                target_path = Path(link[1:])
            else:
                # Relative path
                target_path = (source_file.parent / link).resolve()

            # Check if file exists
            if target_path.exists():
                return ReferenceValidationResult(
                    reference=link,
                    type="file",
                    found=True,
                    target_file=str(target_path),
                    line_number=None,
                )
            return ReferenceValidationResult(
                reference=link,
                type="file",
                found=False,
                target_file=None,
                line_number=None,
            )

        except Exception:
            return ReferenceValidationResult(
                reference=link,
                type="file",
                found=False,
                target_file=None,
                line_number=None,
            )


class StyleValidator:
    """Validate documentation style consistency."""

    def __init__(self, config: dict[str, object] | None = None) -> None:
        self.config = config or {
            "max_line_length": 88,
            "heading_hierarchy": True,
            "list_consistency": True,
            "code_block_languages": True,
            "emphasis_consistency": True,
        }

    def check_file_style(self, file_path: Path) -> StyleCheckResult:
        """Check style consistency for a single file."""
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        issues = []

        # Check line length
        max_length = self.config["max_line_length"]
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                issues.append({
                    "type": "line_too_long",
                    "severity": "low",
                    "line": i,
                    "message": f"Line too long ({len(line)} > {max_length} characters)",
                    "content": line[:50] + "..." if len(line) > 50 else line,
                })

        # Check heading hierarchy
        if self.config["heading_hierarchy"]:
            issues.extend(self._check_heading_hierarchy(content))

        # Check list consistency
        if self.config["list_consistency"]:
            issues.extend(self._check_list_consistency(content))

        # Check code block languages
        if self.config["code_block_languages"]:
            issues.extend(self._check_code_blocks(content))

        # Check emphasis consistency
        if self.config["emphasis_consistency"]:
            issues.extend(self._check_emphasis_consistency(content))

        # Calculate style score
        score = max(0, 100 - (len(issues) * 2))

        return StyleCheckResult(file_path=str(file_path), issues=issues, score=score)

    def _check_heading_hierarchy(self, content: str) -> list[dict[str, object]]:
        """Check heading hierarchy consistency."""
        issues = []
        headings = re.findall(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)

        if not headings:
            return issues

        levels = [len(h[0]) for h in headings]

        # Check for proper hierarchy (no level skipping)
        for i in range(1, len(levels)):
            if levels[i] > levels[i - 1] + 1:
                line_num = content[: content.find(headings[i][1])].count("\n") + 1
                issues.append({
                    "type": "heading_hierarchy",
                    "severity": "medium",
                    "line": line_num,
                    "message": f"Heading level skips from {levels[i - 1]} to {levels[i]}",
                    "content": f"{'#' * levels[i]} {headings[i][1]}",
                })

        return issues

    def _check_list_consistency(self, content: str) -> list[dict[str, object]]:
        """Check list marker consistency."""
        issues = []

        # Find unordered lists
        unordered_lists = re.findall(r"^[-*+]\s+.+$", content, re.MULTILINE)

        if len(unordered_lists) > 5:  # Only check if there are multiple lists
            markers = [line[0] for line in unordered_lists]
            primary_marker = max(set(markers), key=markers.count)

            for i, marker in enumerate(markers):
                if marker != primary_marker:
                    # Find line number (approximate)
                    list_start = content.find(unordered_lists[i])
                    line_num = content[:list_start].count("\n") + 1

                    issues.append({
                        "type": "list_consistency",
                        "severity": "low",
                        "line": line_num,
                        "message": f"Inconsistent list marker '{marker}', expected '{primary_marker}'",
                        "content": unordered_lists[i][:30] + "...",
                    })

        return issues

    def _check_code_blocks(self, content: str) -> list[dict[str, object]]:
        """Check code block formatting and languages."""
        issues = []

        # Find code blocks
        code_blocks = re.findall(r"```(\w+)?\n(.*?)\n```", content, re.DOTALL)

        for lang, code in code_blocks:
            if not lang:
                # Code block without language
                block_start = content.find(f"```\n{code[:50]}")
                line_num = content[:block_start].count("\n") + 1

                issues.append({
                    "type": "code_block_language",
                    "severity": "low",
                    "line": line_num,
                    "message": "Code block missing language specification",
                    "content": f"```{lang or ''}\n{code[:30]}...",
                })

        return issues

    def _check_emphasis_consistency(self, content: str) -> list[dict[str, object]]:
        """Check emphasis style consistency."""
        issues = []

        # Count different emphasis styles
        italic_asterisk = len(re.findall(r"\*[^*]+\*", content))
        italic_underscore = len(re.findall(r"_[^_]+_", content))
        bold_asterisk = len(re.findall(r"\*\*[^*]+\*\*", content))
        bold_underscore = len(re.findall(r"__[^_]+__", content))

        # Check for mixed emphasis styles
        if italic_asterisk > 0 and italic_underscore > 0:
            issues.append({
                "type": "emphasis_consistency",
                "severity": "low",
                "line": 0,
                "message": f"Mixed italic styles: * ({italic_asterisk}) vs _ ({italic_underscore})",
                "content": "Mixed emphasis styles detected",
            })

        if bold_asterisk > 0 and bold_underscore > 0:
            issues.append({
                "type": "emphasis_consistency",
                "severity": "low",
                "line": 0,
                "message": f"Mixed bold styles: ** ({bold_asterisk}) vs __ ({bold_underscore})",
                "content": "Mixed emphasis styles detected",
            })

        return issues


class DocumentationValidator:
    """Main class for comprehensive documentation validation."""

    def __init__(self, root_path: str = ".") -> None:
        self.root_path = Path(root_path)
        self.link_validator = LinkValidator()
        self.style_validator = StyleValidator()

    def validate_all_files(self, files: list[Path] | None = None) -> ValidationReport:
        """Run comprehensive validation on all documentation files."""
        if files is None:
            files = self._discover_files()

        link_results = []
        reference_results = []
        style_results = []

        # Validate links in parallel
        external_links = self._extract_external_links(files)
        link_results = self._validate_external_links_parallel(external_links)

        # Validate internal references
        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
                refs = self.link_validator.validate_internal_links(
                    content, file_path, files
                )
                reference_results.extend(refs)
            except Exception:
                pass

        # Check style consistency
        for file_path in files:
            try:
                style_result = self.style_validator.check_file_style(file_path)
                style_results.append(style_result)

            except Exception:
                pass

        # Generate summary
        summary = self._generate_summary(link_results, reference_results, style_results)

        return ValidationReport(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            link_results=link_results,
            reference_results=reference_results,
            style_results=style_results,
            summary=summary,
        )

    def _discover_files(self) -> list[Path]:
        """Discover documentation files."""
        files = []
        patterns = ["*.md", "*.mdx"]

        for pattern in patterns:
            files.extend(
                file_path
                for file_path in self.root_path.rglob(pattern)
                if not any(
                    excl in str(file_path)
                    for excl in [".git", "node_modules", "__pycache__", ".venv"]
                )
            )

        return sorted(files)

    def _extract_external_links(self, files: list[Path]) -> FlextTypes.StringList:
        """Extract all external links from documentation files."""
        links = set()

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
                # Find all markdown links
                link_matches = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", content)
                links.update(url for _, url in link_matches)
            except Exception:
                pass

        return sorted(links)

    def _validate_external_links_parallel(
        self, links: FlextTypes.StringList
    ) -> list[LinkValidationResult]:
        """Validate external links in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {
                executor.submit(self.link_validator.validate_external_link, url): url
                for url in links
            }

            for future in as_completed(future_to_url):
                future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)

                except Exception:
                    pass

        return results

    def _generate_summary(
        self,
        link_results: list[LinkValidationResult],
        reference_results: list[ReferenceValidationResult],
        style_results: list[StyleCheckResult],
    ) -> dict[str, object]:
        """Generate validation summary."""
        summary = {
            "total_external_links": len(link_results),
            "valid_links": len([r for r in link_results if r.status == "valid"]),
            "broken_links": len([r for r in link_results if r.status == "broken"]),
            "timeout_links": len([r for r in link_results if r.status == "timeout"]),
            "total_internal_references": len(reference_results),
            "valid_references": len([r for r in reference_results if r.found]),
            "broken_references": len([r for r in reference_results if not r.found]),
            "total_style_checks": len(style_results),
            "average_style_score": 0,
            "total_style_issues": sum(len(r.issues) for r in style_results),
        }

        if style_results:
            summary["average_style_score"] = int(
                sum(r.score for r in style_results) / len(style_results)
            )

        # Calculate percentages
        if summary["total_external_links"] > 0:
            summary["link_health_percentage"] = int(
                (summary["valid_links"] / summary["total_external_links"]) * 100
            )
        else:
            summary["link_health_percentage"] = 100

        if summary["total_internal_references"] > 0:
            summary["reference_health_percentage"] = int(
                (summary["valid_references"] / summary["total_internal_references"])
                * 100
            )
        else:
            summary["reference_health_percentage"] = 100

        return summary

    def save_report(
        self, report: ValidationReport, output_path: Path | None = None
    ) -> None:
        """Save validation report to file."""
        if output_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = (
                self.root_path
                / "docs"
                / "maintenance"
                / "reports"
                / f"validation_{timestamp}.json"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert dataclasses to dictionaries
        report_dict = {
            "timestamp": report.timestamp,
            "link_results": [asdict(r) for r in report.link_results],
            "reference_results": [asdict(r) for r in report.reference_results],
            "style_results": [asdict(r) for r in report.style_results],
            "summary": report.summary,
        }

        with Path(output_path).open("w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=2)

    def print_summary(self, report: ValidationReport) -> None:
        """Print validation summary to console."""
        # Show top issues
        if report.summary["broken_links"] > 0:
            broken_links: list[LinkValidationResult] = [
                r for r in report.link_results if r.status == "broken"
            ]
            for _link in broken_links[:5]:  # Show first 5
                pass

        if report.summary["broken_references"] > 0:
            broken_refs: list[ReferenceValidationResult] = [
                r for r in report.reference_results if not r.found
            ]
            for _ref in broken_refs[:5]:  # Show first 5
                pass

        # Show style issues
        style_issues: list[StyleCheckResult] = []
        for result in report.style_results:
            style_issues.extend(result.issues)

        if style_issues:
            # Group by type
            issue_types: dict[str, int] = {}
            for issue in style_issues:
                issue_type = issue["type"]
                if issue_type not in issue_types:
                    issue_types[issue_type] = 0
                issue_types[issue_type] += 1

            for issue_type, _count in sorted(
                issue_types.items(), key=operator.itemgetter(1), reverse=True
            ):
                pass


def main() -> int:
    """Main entry point for documentation validation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="FLEXT-gRPC Documentation Validation System"
    )
    parser.add_argument("--path", default=".", help="Root path to validate")
    parser.add_argument("--output", help="Output path for report")
    parser.add_argument(
        "--links-only", action="store_true", help="Validate only external links"
    )
    parser.add_argument(
        "--style-only", action="store_true", help="Check only style consistency"
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")

    args = parser.parse_args()

    # Create validator
    validator = DocumentationValidator(args.path)

    # Run validation
    if args.links_only:
        # Quick link validation
        files = validator._discover_files()
        external_links = validator._extract_external_links(files)
        link_results = validator._validate_external_links_parallel(external_links)

        report = ValidationReport(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            link_results=link_results,
            reference_results=[],
            style_results=[],
            summary={
                "total_external_links": len(link_results),
                "valid_links": len([r for r in link_results if r.status == "valid"]),
                "broken_links": len([r for r in link_results if r.status == "broken"]),
                "timeout_links": len([
                    r for r in link_results if r.status == "timeout"
                ]),
            },
        )
    elif args.style_only:
        # Style check only
        files = validator._discover_files()
        style_results = []

        for file_path in files:
            try:
                result = validator.style_validator.check_file_style(file_path)
                style_results.append(result)
            except Exception:
                if not args.quiet:
                    pass

        report = ValidationReport(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            link_results=[],
            reference_results=[],
            style_results=style_results,
            summary={
                "total_style_checks": len(style_results),
                "average_style_score": sum(r.score for r in style_results)
                / len(style_results)
                if style_results
                else 0,
                "total_style_issues": sum(len(r.issues) for r in style_results),
            },
        )
    else:
        # Full validation
        report = validator.validate_all_files()

    # Save report
    output_path = Path(args.output) if args.output else None

    validator.save_report(report, output_path)

    # Print summary
    if not args.quiet:
        validator.print_summary(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
