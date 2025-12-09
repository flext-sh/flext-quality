#!/usr/bin/env python3
"""FLEXT Quality Documentation Audit System.

Comprehensive documentation quality assurance and validation tool.
Performs content freshness analysis, link validation, style checking,
and generates detailed quality reports.

Usage:
    python audit.py --comprehensive
    python audit.py --check-links --check-style
    python audit.py --ci-mode --fail-on-errors
"""

import argparse
import json
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import requests
import yaml


class DocumentationAuditor:
    """Main documentation audit and quality assurance system."""

    def __init__(self, config_path: str = "docs/maintenance/config/") -> None:
        """Initialize documentation audit system.

        Args:
            config_path: Path to configuration directory for audit rules.

        """
        self.config_path = Path(config_path)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.load_config()

        # Audit results storage
        self.results = {
            "timestamp": datetime.now(UTC).isoformat(),
            "files_analyzed": 0,
            "issues": [],
            "metrics": {},
            "recommendations": [],
        }

    def load_config(self) -> None:
        """Load audit configuration files."""
        try:
            with Path(self.config_path / "audit_rules.yaml").open(
                encoding="utf-8",
            ) as f:
                self.audit_rules = yaml.safe_load(f)
        except FileNotFoundError:
            self.audit_rules = self.get_default_audit_rules()

        try:
            with Path(self.config_path / "style_guide.yaml").open(
                encoding="utf-8",
            ) as f:
                self.style_guide = yaml.safe_load(f)
        except FileNotFoundError:
            self.style_guide = self.get_default_style_guide()

        try:
            with Path(self.config_path / "validation_config.yaml").open(
                encoding="utf-8",
            ) as f:
                self.validation_config = yaml.safe_load(f)
        except FileNotFoundError:
            self.validation_config = self.get_default_validation_config()

    def get_default_audit_rules(self) -> dict[str, Any]:
        """Default audit rules if config file not found."""
        return {
            "quality_thresholds": {
                "max_age_days": 90,
                "min_word_count": 100,
                "max_broken_links": 0,
                "min_completeness_score": 0.8,
            },
            "content_checks": {
                "check_freshness": True,
                "check_completeness": True,
                "check_consistency": True,
                "check_links": True,
            },
            "severity_levels": {
                "critical": ["broken_external_link", "missing_section"],
                "high": ["outdated_content", "broken_internal_link"],
                "medium": ["style_inconsistency", "missing_alt_text"],
                "low": ["formatting_issue", "readability_warning"],
            },
        }

    def get_default_style_guide(self) -> dict[str, Any]:
        """Default style guide if config file not found."""
        return {
            "markdown": {
                "heading_style": "atx",
                "list_style": "dash",
                "emphasis_style": "*",
                "code_block_style": "fenced",
            },
            "accessibility": {
                "require_alt_text": True,
                "descriptive_links": True,
                "heading_structure": True,
            },
            "formatting": {
                "max_line_length": 88,
                "consistent_indentation": True,
                "trailing_spaces": False,
            },
        }

    def get_default_validation_config(self) -> dict[str, Any]:
        """Default validation config if config file not found."""
        return {
            "link_validation": {
                "timeout": 10,
                "retry_attempts": 3,
                "user_agent": "FLEXT-Quality-Doc-Auditor/1.0",
                "check_external": True,
                "check_internal": True,
                "check_images": True,
            },
            "content_analysis": {
                "min_section_depth": 2,
                "required_sections": ["Overview", "Installation", "Usage"],
                "check_todos": True,
                "check_fixmes": True,
            },
        }

    def find_documentation_files(self) -> list[Path]:
        """Find all documentation files in the project."""
        doc_files = []

        # Common documentation patterns
        patterns = [
            "**/*.md",
            "**/*.mdx",
            "**/README*",
            "**/CHANGELOG*",
            "**/CONTRIBUTING*",
            "**/docs/**/*.md",
            "**/docs/**/*.mdx",
        ]

        for pattern in patterns:
            doc_files.extend(self.project_root.glob(pattern))

        # Remove duplicates and filter out non-documentation
        doc_files = list(set(doc_files))
        doc_files = [f for f in doc_files if not self._is_ignored_file(f)]

        return sorted(doc_files)

    def _is_ignored_file(self, file_path: Path) -> bool:
        """Check if file should be ignored in audit."""
        ignored_patterns = [
            ".git",
            "__pycache__",
            "node_modules",
            ".pytest_cache",
            "build",
            "dist",
            ".serena/memories",  # Internal tool files
            ".vscode",
            ".idea",
        ]

        return any(pattern in str(file_path) for pattern in ignored_patterns)

    def run_comprehensive_audit(self) -> dict[str, Any]:
        """Run complete documentation audit."""
        doc_files = self.find_documentation_files()
        self.results["files_analyzed"] = len(doc_files)

        # Run all audit checks
        if self.audit_rules["content_checks"]["check_freshness"]:
            self.check_content_freshness(doc_files)

        if self.audit_rules["content_checks"]["check_completeness"]:
            self.check_content_completeness(doc_files)

        if self.audit_rules["content_checks"]["check_consistency"]:
            self.check_content_consistency(doc_files)

        if self.audit_rules["content_checks"]["check_links"]:
            self.check_links_and_references(doc_files)

        # Calculate overall metrics
        self.calculate_quality_metrics()

        # Generate recommendations
        self.generate_recommendations()

        return self.results

    def check_content_freshness(self, doc_files: list[Path]) -> None:
        """Check documentation freshness and identify outdated content."""
        max_age_days = self.audit_rules["quality_thresholds"]["max_age_days"]
        cutoff_date = datetime.now(UTC) - timedelta(days=max_age_days)

        for file_path in doc_files:
            try:
                # Get file modification time
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=UTC)

                if mtime < cutoff_date:
                    age_days = (datetime.now(UTC) - mtime).days

                    # Check for outdated indicators in content
                    content = file_path.read_text(encoding="utf-8")
                    outdated_indicators = self._check_outdated_indicators(content)

                    issue = {
                        "type": "outdated_content",
                        "severity": "high" if age_days > 180 else "medium",
                        "file": str(file_path.relative_to(self.project_root)),
                        "age_days": age_days,
                        "last_modified": mtime.isoformat(),
                        "outdated_indicators": outdated_indicators,
                        "recommendation": f"Review and update content (last modified {age_days} days ago)",
                    }
                    self.results["issues"].append(issue)

            except Exception as e:
                self.results["issues"].append(
                    {
                        "type": "file_access_error",
                        "severity": "medium",
                        "file": str(file_path.relative_to(self.project_root)),
                        "error": str(e),
                    }
                )

    def _check_outdated_indicators(self, content: str) -> list[str]:
        """Check for indicators of outdated content."""
        indicators = []

        # Check for version placeholders
        if re.search(
            r"\b\d+\.\d+\.\d+.*TODO|FIXME|placeholder",
            content,
            re.IGNORECASE,
        ):
            indicators.append("version placeholders")

        # Check for date placeholders
        if re.search(r"\b202\d.*TODO|FIXME|update.*date", content, re.IGNORECASE):
            indicators.append("date placeholders")

        # Check for incomplete sections
        if re.search(
            r"#+\s*(TODO|FIXME|Coming Soon|Work in Progress)",
            content,
            re.IGNORECASE,
        ):
            indicators.append("incomplete sections")

        # Check for outdated status indicators
        if re.search(r"❌.*working|✅.*broken|⚠️.*complete", content, re.IGNORECASE):
            indicators.append("potentially inconsistent status")

        return indicators

    def check_content_completeness(self, doc_files: list[Path]) -> None:
        """Check documentation completeness and identify missing sections."""
        min_word_count = self.audit_rules["quality_thresholds"]["min_word_count"]
        required_sections = self.validation_config["content_analysis"][
            "required_sections"
        ]

        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")

                # Word count check
                word_count = len(content.split())
                if word_count < min_word_count:
                    self.results["issues"].append(
                        {
                            "type": "insufficient_content",
                            "severity": "low",
                            "file": str(file_path.relative_to(self.project_root)),
                            "word_count": word_count,
                            "minimum_required": min_word_count,
                            "recommendation": f"Expand content (currently {word_count} words, minimum {min_word_count})",
                        }
                    )

                # Check for required sections (for main docs)
                if "README.md" in str(file_path) or "docs/" in str(file_path):
                    missing_sections = self._check_required_sections(
                        content,
                        required_sections,
                    )
                    if missing_sections:
                        self.results["issues"].append(
                            {
                                "type": "missing_sections",
                                "severity": "medium",
                                "file": str(file_path.relative_to(self.project_root)),
                                "missing_sections": missing_sections,
                                "recommendation": f"Add missing sections: {', '.join(missing_sections)}",
                            }
                        )

                # Check for TODO/FIXME markers
                if self.validation_config["content_analysis"]["check_todos"]:
                    todos = re.findall(
                        r"(?i)(?:TODO|FIXME|XXX):\s*(.+?)(?:\n|$)",
                        content,
                    )
                    if todos:
                        self.results["issues"].append(
                            {
                                "type": "todo_markers",
                                "severity": "low",
                                "file": str(file_path.relative_to(self.project_root)),
                                "todo_count": len(todos),
                                "todos": todos[:5],  # First 5 for brevity
                                "recommendation": f"Address {len(todos)} TODO/FIXME items",
                            }
                        )

            except Exception as e:
                self.results["issues"].append(
                    {
                        "type": "content_analysis_error",
                        "severity": "medium",
                        "file": str(file_path.relative_to(self.project_root)),
                        "error": str(e),
                    }
                )

    def _check_required_sections(
        self,
        content: str,
        required_sections: list[str],
    ) -> list[str]:
        """Check for required sections in documentation."""
        missing = []

        for section in required_sections:
            # Check for headings containing the section name
            pattern = rf"^#+\s.*{re.escape(section)}.*$"
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                missing.append(section)

        return missing

    def check_content_consistency(self, doc_files: list[Path]) -> None:
        """Check style consistency and formatting issues."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")

                # Check markdown formatting
                formatting_issues = self._check_markdown_formatting(content)
                if formatting_issues:
                    self.results["issues"].append(
                        {
                            "type": "formatting_issues",
                            "severity": "low",
                            "file": str(file_path.relative_to(self.project_root)),
                            "issues": formatting_issues,
                            "recommendation": f"Fix {len(formatting_issues)} formatting issues",
                        }
                    )

                # Check accessibility compliance
                accessibility_issues = self._check_accessibility(content)
                if accessibility_issues:
                    severity = (
                        "high"
                        if any(
                            i["type"] == "missing_alt_text"
                            for i in accessibility_issues
                        )
                        else "medium"
                    )
                    self.results["issues"].append(
                        {
                            "type": "accessibility_issues",
                            "severity": severity,
                            "file": str(file_path.relative_to(self.project_root)),
                            "issues": accessibility_issues,
                            "recommendation": f"Address {len(accessibility_issues)} accessibility issues",
                        }
                    )

                # Check heading hierarchy
                if self.style_guide["accessibility"]["heading_structure"]:
                    heading_issues = self._check_heading_hierarchy(content)
                    if heading_issues:
                        self.results["issues"].append(
                            {
                                "type": "heading_hierarchy",
                                "severity": "medium",
                                "file": str(file_path.relative_to(self.project_root)),
                                "issues": heading_issues,
                                "recommendation": "Fix heading hierarchy structure",
                            }
                        )

            except Exception as e:
                self.results["issues"].append(
                    {
                        "type": "consistency_check_error",
                        "severity": "medium",
                        "file": str(file_path.relative_to(self.project_root)),
                        "error": str(e),
                    }
                )

    def _check_markdown_formatting(self, content: str) -> list[str]:
        """Check for markdown formatting issues."""
        issues = []

        # Check for mixed list styles
        unordered_lists = re.findall(r"^[\s]*[-\*\+]", content, re.MULTILINE)
        if len(set(unordered_lists)) > 1:
            issues.append("mixed unordered list styles")

        # Check for inconsistent emphasis
        emphasis_patterns = [r"\*[^*]+\*", r"_[^_]+_"]
        emphasis_usage = [
            pattern for pattern in emphasis_patterns if re.search(pattern, content)
        ]

        if len(emphasis_usage) > 1:
            issues.append("mixed emphasis styles (* vs _)")

        # Check for trailing spaces
        if self.style_guide["formatting"]["trailing_spaces"]:
            trailing_spaces = re.findall(r"[ \t]+$", content, re.MULTILINE)
            if trailing_spaces:
                issues.append(f"{len(trailing_spaces)} lines with trailing spaces")

        # Check line length
        max_length = self.style_guide["formatting"]["max_line_length"]
        long_lines = [line for line in content.split("\n") if len(line) > max_length]
        if long_lines:
            issues.append(f"{len(long_lines)} lines exceed {max_length} characters")

        return issues

    def _check_accessibility(self, content: str) -> list[dict]:
        """Check accessibility compliance."""
        issues = []

        # Check for images without alt text
        if self.style_guide["accessibility"]["require_alt_text"]:
            images_without_alt = re.findall(r"!\[\]\([^)]+\)", content)
            if images_without_alt:
                issues.extend(
                    [
                        {
                            "type": "missing_alt_text",
                            "description": f"Image without alt text: {img}",
                        }
                        for img in images_without_alt
                    ]
                )

        # Check for non-descriptive links
        if self.style_guide["accessibility"]["descriptive_links"]:
            generic_links = re.findall(
                r"\[here|click here|link|read more\]\([^)]+\)",
                content,
                re.IGNORECASE,
            )
            if generic_links:
                issues.extend(
                    [
                        {
                            "type": "generic_link_text",
                            "description": f"Non-descriptive link text: {link}",
                        }
                        for link in generic_links
                    ]
                )

        return issues

    def _check_heading_hierarchy(self, content: str) -> list[str]:
        """Check heading hierarchy for logical structure."""
        # Extract heading levels
        headings = re.findall(r"^(#+)\s+(.+)$", content, re.MULTILINE)
        heading_levels = [len(level) for level, _ in headings]

        # Check for skipped heading levels
        issues = [
            f"Skipped heading level at line with H{heading_levels[i]}"
            for i in range(1, len(heading_levels))
            if heading_levels[i] > heading_levels[i - 1] + 1
        ]

        # Check for H1 after other content
        if heading_levels and heading_levels[0] != 1:
            issues.append("Document should start with H1")

        return issues

    def check_links_and_references(self, doc_files: list[Path]) -> None:
        """Check links and references for validity."""
        all_links = []
        image_refs = []

        # Collect all links and references
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")

                # Extract external links
                external_links = re.findall(
                    r"\[([^\]]+)\]\((https?://[^)]+)\)",
                    content,
                )
                for text, url in external_links:
                    all_links.append(
                        {
                            "url": url,
                            "text": text,
                            "file": str(file_path.relative_to(self.project_root)),
                            "type": "external",
                        }
                    )

                # Extract internal links
                internal_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
                for text, link in internal_links:
                    if not link.startswith(("http://", "https://", "#", "mailto:")):
                        all_links.append(
                            {
                                "url": link,
                                "text": text,
                                "file": str(file_path.relative_to(self.project_root)),
                                "type": "internal",
                            }
                        )

                # Extract image references
                images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)
                for alt_text, src in images:
                    image_refs.append(
                        {
                            "src": src,
                            "alt": alt_text,
                            "file": str(file_path.relative_to(self.project_root)),
                        }
                    )

            except Exception as e:
                self.results["issues"].append(
                    {
                        "type": "link_extraction_error",
                        "severity": "medium",
                        "file": str(file_path.relative_to(self.project_root)),
                        "error": str(e),
                    }
                )

        # Validate external links
        if self.validation_config["link_validation"]["check_external"]:
            self._validate_external_links(all_links)

        # Validate internal links
        if self.validation_config["link_validation"]["check_internal"]:
            self._validate_internal_links(all_links, doc_files)

        # Validate images
        if self.validation_config["link_validation"]["check_images"]:
            self._validate_images(image_refs)

    def _validate_external_links(self, links: list[dict]) -> None:
        """Validate external links."""
        external_links = [link for link in links if link["type"] == "external"]

        for link in external_links:
            try:
                response = requests.head(
                    link["url"],
                    timeout=self.validation_config["link_validation"]["timeout"],
                    headers={
                        "User-Agent": self.validation_config["link_validation"][
                            "user_agent"
                        ],
                    },
                    allow_redirects=True,
                )

                if response.status_code >= 400:
                    self.results["issues"].append(
                        {
                            "type": "broken_external_link",
                            "severity": "high",
                            "file": link["file"],
                            "url": link["url"],
                            "status_code": response.status_code,
                            "recommendation": f"Fix or remove broken link (HTTP {response.status_code})",
                        }
                    )

            except requests.RequestException as e:
                self.results["issues"].append(
                    {
                        "type": "unreachable_external_link",
                        "severity": "high",
                        "file": link["file"],
                        "url": link["url"],
                        "error": str(e),
                        "recommendation": "Verify link URL and accessibility",
                    }
                )

    def _validate_internal_links(
        self,
        links: list[dict],
        doc_files: list[Path],
    ) -> None:
        """Validate internal links."""
        internal_links = [link for link in links if link["type"] == "internal"]
        doc_file_names = {str(f.relative_to(self.project_root)) for f in doc_files}

        for link in internal_links:
            # Check if link points to existing file
            target_file = link["url"].split("#")[0]  # Remove anchor

            if target_file and target_file not in doc_file_names:
                # Try relative path resolution
                link_file_dir = Path(link["file"]).parent
                potential_target = (link_file_dir / target_file).resolve()

                if not potential_target.exists():
                    self.results["issues"].append(
                        {
                            "type": "broken_internal_link",
                            "severity": "high",
                            "file": link["file"],
                            "target": link["url"],
                            "recommendation": f"Fix broken internal link to '{link['url']}'",
                        }
                    )

    def _validate_images(self, images: list[dict]) -> None:
        """Validate image references."""
        for image in images:
            # Skip external images for now
            if image["src"].startswith(("http://", "https://")):
                continue

            # Check local images
            image_path = Path(image["src"])
            if not image_path.is_absolute():
                # Relative to the file's directory
                file_dir = Path(image["file"]).parent
                full_path = (self.project_root / file_dir / image_path).resolve()
            else:
                full_path = image_path

            if not full_path.exists():
                self.results["issues"].append(
                    {
                        "type": "missing_image",
                        "severity": "medium",
                        "file": image["file"],
                        "image_src": image["src"],
                        "recommendation": f"Add missing image file: {image['src']}",
                    }
                )

    def calculate_quality_metrics(self) -> None:
        """Calculate overall quality metrics."""
        issues = self.results["issues"]
        total_issues = len(issues)

        # Categorize issues by severity
        severity_counts = {
            "critical": len([i for i in issues if i.get("severity") == "critical"]),
            "high": len([i for i in issues if i.get("severity") == "high"]),
            "medium": len([i for i in issues if i.get("severity") == "medium"]),
            "low": len([i for i in issues if i.get("severity") == "low"]),
        }

        # Calculate quality score (0-100)
        # Critical issues have highest weight, low issues have minimal impact
        weights = {"critical": 25, "high": 10, "medium": 5, "low": 1}
        weighted_score = sum(
            severity_counts[level] * weights[level] for level in severity_counts
        )

        # Base score of 100, subtract weighted penalties
        quality_score = max(0, 100 - weighted_score)

        self.results["metrics"] = {
            "total_issues": total_issues,
            "severity_breakdown": severity_counts,
            "quality_score": quality_score,
            "files_analyzed": self.results["files_analyzed"],
            "issues_per_file": total_issues / self.results["files_analyzed"]
            if self.results["files_analyzed"] > 0
            else 0,
        }

    def generate_recommendations(self) -> None:
        """Generate actionable recommendations based on audit results."""
        metrics = self.results["metrics"]
        issues = self.results["issues"]

        recommendations = []

        # Quality score based recommendations
        if metrics["quality_score"] < 50:
            recommendations.append(
                {
                    "priority": "critical",
                    "category": "overall_quality",
                    "recommendation": "Immediate attention required - documentation quality is poor",
                    "actions": [
                        "Address all critical and high-severity issues immediately",
                        "Implement automated quality gates in CI/CD",
                        "Schedule regular maintenance reviews",
                    ],
                }
            )
        elif metrics["quality_score"] < 75:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "quality_improvement",
                    "recommendation": "Documentation quality needs improvement",
                    "actions": [
                        "Focus on fixing high-severity issues",
                        "Implement regular audit schedule",
                        "Consider documentation training for team",
                    ],
                }
            )

        # Issue-specific recommendations
        broken_links = [
            i
            for i in issues
            if "link" in i["type"] and i["severity"] in {"critical", "high"}
        ]
        if broken_links:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "link_maintenance",
                    "recommendation": f"Fix {len(broken_links)} broken links",
                    "actions": [
                        "Update or remove broken external links",
                        "Fix internal reference paths",
                        "Implement automated link checking in CI/CD",
                    ],
                }
            )

        outdated_content = [i for i in issues if i["type"] == "outdated_content"]
        if outdated_content:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "content_freshness",
                    "recommendation": f"Update {len(outdated_content)} outdated documents",
                    "actions": [
                        "Review content for accuracy",
                        "Update version numbers and dates",
                        "Implement content freshness monitoring",
                    ],
                }
            )

        accessibility_issues = [
            i for i in issues if i["type"] == "accessibility_issues"
        ]
        if accessibility_issues:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "accessibility",
                    "recommendation": "Improve documentation accessibility",
                    "actions": [
                        "Add alt text to all images",
                        "Use descriptive link text",
                        "Ensure proper heading hierarchy",
                    ],
                }
            )

        self.results["recommendations"] = recommendations

    def generate_report(
        self,
        output_format: str = "json",
        output_path: str | None = None,
    ) -> str:
        """Generate audit report in specified format.

        Args:
            output_format: Format for the report ('json', 'html', 'summary').
            output_path: Unused parameter for future extensibility.

        """
        # Reserved for future file output implementation
        _ = output_path  # Reserved for future use
        if output_format == "json":
            return json.dumps(self.results, indent=2, default=str)
        if output_format == "html":
            return self._generate_html_report()
        return json.dumps(self.results, default=str)

    def _generate_html_report(self) -> str:
        """Generate HTML audit report."""
        metrics = self.results["metrics"]

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>FLEXT Quality Documentation Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .metrics {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background: #e8f4fd; padding: 15px; border-radius: 5px; flex: 1; }}
        .issues {{ margin: 20px 0; }}
        .issue {{ border: 1px solid #ddd; margin: 10px 0; padding: 10px; border-radius: 5px; }}
        .severity-critical {{ border-left: 5px solid #dc3545; }}
        .severity-high {{ border-left: 5px solid #fd7e14; }}
        .severity-medium {{ border-left: 5px solid #ffc107; }}
        .severity-low {{ border-left: 5px solid #28a745; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>FLEXT Quality Documentation Audit Report</h1>
        <p>Generated: {self.results["timestamp"]}</p>
        <p>Files Analyzed: {metrics["files_analyzed"]}</p>
    </div>

    <div class="metrics">
        <div class="metric">
            <h3>Quality Score</h3>
            <div style="font-size: 2em; font-weight: bold; color: {self._get_score_color(metrics["quality_score"])};">
                {metrics["quality_score"]}%
            </div>
        </div>
        <div class="metric">
            <h3>Total Issues</h3>
            <div style="font-size: 2em; font-weight: bold;">
                {metrics["total_issues"]}
            </div>
        </div>
        <div class="metric">
            <h3>Issues per File</h3>
            <div style="font-size: 2em; font-weight: bold;">
                {metrics["issues_per_file"]:.1f}
            </div>
        </div>
    </div>

    <h2>Issues by Severity</h2>
    <ul>
        <li>Critical: {metrics["severity_breakdown"]["critical"]}</li>
        <li>High: {metrics["severity_breakdown"]["high"]}</li>
        <li>Medium: {metrics["severity_breakdown"]["medium"]}</li>
        <li>Low: {metrics["severity_breakdown"]["low"]}</li>
    </ul>

    <div class="issues">
        <h2>Detailed Issues</h2>
"""

        for issue in self.results["issues"]:
            severity_class = f"severity-{issue['severity']}"
            html += f"""
        <div class="issue {severity_class}">
            <h4>{issue["type"].replace("_", " ").title()} ({issue["severity"].upper()})</h4>
            <p><strong>File:</strong> {issue["file"]}</p>
            <p><strong>Recommendation:</strong> {issue.get("recommendation", "N/A")}</p>
"""

            # Add issue-specific details
            if "age_days" in issue:
                html += f"<p><strong>Age:</strong> {issue['age_days']} days</p>"
            if "word_count" in issue:
                html += f"<p><strong>Word Count:</strong> {issue['word_count']}</p>"
            if "status_code" in issue:
                html += f"<p><strong>Status Code:</strong> {issue['status_code']}</p>"
            if "url" in issue:
                html += f"<p><strong>URL:</strong> <a href='{issue['url']}'>{issue['url']}</a></p>"

            html += "</div>"

        html += """
    </div>
</body>
</html>
"""
        return html

    def _get_score_color(self, score: int) -> str:
        """Get color for quality score."""
        if score >= 80:
            return "#28a745"  # Green
        if score >= 60:
            return "#ffc107"  # Yellow
        return "#dc3545"  # Red

    def save_report(
        self,
        output_format: str = "json",
        output_path: str = "docs/maintenance/reports/",
    ) -> str:
        """Save audit report to file."""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"audit_report_{timestamp}.{output_format}"
        filepath = output_dir / filename

        report_content = self.generate_report(output_format)
        filepath.write_text(report_content, encoding="utf-8")

        # Also save latest report
        latest_file = output_dir / "latest_audit.json"
        json.dump(self.results, latest_file.open("w"), indent=2, default=str)

        return filepath


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="FLEXT Quality Documentation Audit")
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run complete audit with all checks",
    )
    parser.add_argument(
        "--check-freshness",
        action="store_true",
        help="Check content freshness only",
    )
    parser.add_argument(
        "--check-completeness",
        action="store_true",
        help="Check content completeness only",
    )
    parser.add_argument(
        "--check-consistency",
        action="store_true",
        help="Check style consistency only",
    )
    parser.add_argument(
        "--check-links",
        action="store_true",
        help="Check links and references only",
    )
    parser.add_argument(
        "--ci-mode",
        action="store_true",
        help="CI/CD mode - exit with error code on failures",
    )
    parser.add_argument(
        "--fail-on-errors",
        action="store_true",
        help="Exit with error code if critical/high severity issues found",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/maintenance/reports/",
        help="Output directory for reports",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "html"],
        default="json",
        help="Report format",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="docs/maintenance/config/",
        help="Configuration directory path",
    )
    return parser


def _execute_audit_checks(
    auditor: DocumentationAuditor,
    args: argparse.Namespace,
) -> dict[str, Any]:
    """Execute the appropriate audit checks based on arguments."""
    if args.comprehensive:
        return auditor.run_comprehensive_audit()

    doc_files = auditor.find_documentation_files()

    if args.check_freshness:
        auditor.check_content_freshness(doc_files)
    if args.check_completeness:
        auditor.check_content_completeness(doc_files)
    if args.check_consistency:
        auditor.check_content_consistency(doc_files)
    if args.check_links:
        auditor.check_links_and_references(doc_files)

    auditor.calculate_quality_metrics()
    auditor.generate_recommendations()
    return auditor.results


def _should_fail_on_results(args: argparse.Namespace, metrics: dict[str, Any]) -> bool:
    """Determine if the process should fail based on results and arguments."""
    should_fail = False
    if args.fail_on_errors:
        critical_high_issues = (
            metrics["severity_breakdown"]["critical"]
            + metrics["severity_breakdown"]["high"]
        )
        if critical_high_issues > 0:
            should_fail = True

    if args.ci_mode and metrics["quality_score"] < 70:
        should_fail = True

    return should_fail


def main() -> None:
    """Main entry point for documentation audit."""
    parser = _create_argument_parser()
    args = parser.parse_args()

    # Initialize auditor
    auditor = DocumentationAuditor(args.config)

    try:
        # Execute audit checks
        results = _execute_audit_checks(auditor, args)

        # Save report
        auditor.save_report(args.format, args.output)

        # Check for CI/CD failure conditions
        metrics = results["metrics"]
        if _should_fail_on_results(args, metrics):
            sys.exit(1)

    except Exception:
        if args.ci_mode or args.fail_on_errors:
            sys.exit(1)


if __name__ == "__main__":
    main()
