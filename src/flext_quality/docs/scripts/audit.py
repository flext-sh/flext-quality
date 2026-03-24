"""FLEXT Quality Documentation Audit System.

Comprehensive documentation quality assurance and validation tool.
Performs content freshness analysis, link validation, style checking,
and generates detailed quality reports.

Usage:
    python audit.py --comprehensive
    python audit.py --check-links --check-style
    python audit.py --ci-mode --fail-on-errors
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path

import requests
import yaml
from pydantic import ValidationError

from flext_quality import m, t


class FlextQualityDocumentationAuditor:
    """Main documentation audit and quality assurance system."""

    def __init__(self, config_path: str = "docs/maintenance/config/") -> None:
        """Initialize documentation audit system.

        Args:
            config_path: Path to configuration directory for audit rules.

        """
        self.config_path = Path(config_path)
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.audit_rules: m.Quality.AuditRulesConfig = self.get_default_audit_rules()
        self.style_guide: m.Quality.StyleGuideConfig = self.get_default_style_guide()
        self.validation_config: m.Quality.ValidationConfig = (
            self.get_default_validation_config()
        )
        self.load_config()
        self.results: m.Quality.AuditorResults = m.Quality.AuditorResults(
            timestamp=datetime.now(UTC).isoformat(),
        )

    def load_config(self) -> None:
        """Load audit configuration files."""
        try:
            with Path(self.config_path / "audit_rules.yaml").open(
                encoding="utf-8",
            ) as f:
                self.audit_rules = m.Quality.AuditRulesConfig.model_validate(
                    yaml.safe_load(f),
                )
        except (FileNotFoundError, ValidationError, yaml.YAMLError, TypeError):
            self.audit_rules = self.get_default_audit_rules()

        try:
            with Path(self.config_path / "style_guide.yaml").open(
                encoding="utf-8",
            ) as f:
                self.style_guide = m.Quality.StyleGuideConfig.model_validate(
                    yaml.safe_load(f),
                )
        except (FileNotFoundError, ValidationError, yaml.YAMLError, TypeError):
            self.style_guide = self.get_default_style_guide()

        try:
            with Path(self.config_path / "validation_config.yaml").open(
                encoding="utf-8",
            ) as f:
                self.validation_config = m.Quality.ValidationConfig.model_validate(
                    yaml.safe_load(f),
                )
        except (FileNotFoundError, ValidationError, yaml.YAMLError, TypeError):
            self.validation_config = self.get_default_validation_config()

    def get_default_audit_rules(self) -> m.Quality.AuditRulesConfig:
        """Default audit rules if config file not found."""
        return m.Quality.AuditRulesConfig.model_validate({
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
        })

    def get_default_style_guide(self) -> m.Quality.StyleGuideConfig:
        """Default style guide if config file not found."""
        return m.Quality.StyleGuideConfig.model_validate({
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
        })

    def get_default_validation_config(self) -> m.Quality.ValidationConfig:
        """Default validation config if config file not found."""
        return m.Quality.ValidationConfig.model_validate({
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
        })

    def find_documentation_files(self) -> Sequence[Path]:
        """Find all documentation files in the project."""
        doc_files: MutableSequence[Path] = []
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
            ".serena/memories",
            ".vscode",
            ".idea",
        ]
        return any(pattern in str(file_path) for pattern in ignored_patterns)

    def run_comprehensive_audit(self) -> m.Quality.AuditorResults:
        """Run complete documentation audit."""
        doc_files = self.find_documentation_files()
        self.results.files_analyzed = len(doc_files)
        content_checks = self.audit_rules.content_checks
        if content_checks.check_freshness:
            self.check_content_freshness(doc_files)
        if content_checks.check_completeness:
            self.check_content_completeness(doc_files)
        if content_checks.check_consistency:
            self.check_content_consistency(doc_files)
        if content_checks.check_links:
            self.check_links_and_references(doc_files)
        self.calculate_quality_metrics()
        self.generate_recommendations()
        return self.results

    def check_content_freshness(self, doc_files: Sequence[Path]) -> None:
        """Check documentation freshness and identify outdated content."""
        max_age_days = self.audit_rules.quality_thresholds.max_age_days
        cutoff_date = datetime.now(UTC) - timedelta(days=max_age_days)
        for file_path in doc_files:
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=UTC)
                if mtime < cutoff_date:
                    age_days = (datetime.now(UTC) - mtime).days
                    content = file_path.read_text(encoding="utf-8")
                    outdated_indicators = self._check_outdated_indicators(content)
                    issue: MutableMapping[
                        str,
                        str
                        | int
                        | float
                        | bool
                        | t.StrSequence
                        | Sequence[t.StrMapping]
                        | None,
                    ] = {
                        "type": "outdated_content",
                        "severity": "high" if age_days > 180 else "medium",
                        "file": str(file_path.relative_to(self.project_root)),
                        "age_days": age_days,
                        "last_modified": mtime.isoformat(),
                        "outdated_indicators": outdated_indicators,
                        "recommendation": f"Review and update content (last modified {age_days} days ago)",
                    }
                    _ = self.results.issues.append(issue)
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                _ = self.results.issues.append({
                    "type": "file_access_error",
                    "severity": "medium",
                    "file": str(file_path.relative_to(self.project_root)),
                    "error": str(e),
                })

    def _check_outdated_indicators(self, content: str) -> MutableSequence[str]:
        """Check for indicators of outdated content."""
        indicators: MutableSequence[str] = []
        if re.search(
            r"\\b\\d+\\.\\d+\\.\\d+.*TODO|FIXME|placeholder",
            content,
            re.IGNORECASE,
        ):
            indicators.append("version placeholders")
        if re.search(r"\\b202\\d.*TODO|FIXME|update.*date", content, re.IGNORECASE):
            indicators.append("date placeholders")
        if re.search(
            r"#+\\s*(TODO|FIXME|Coming Soon|Work in Progress)",
            content,
            re.IGNORECASE,
        ):
            indicators.append("incomplete sections")
        if re.search(r"❌.*working|✅.*broken|⚠️.*complete", content, re.IGNORECASE):
            indicators.append("potentially inconsistent status")
        return indicators

    def check_content_completeness(self, doc_files: Sequence[Path]) -> None:
        """Check documentation completeness and identify missing sections."""
        min_word_count = self.audit_rules.quality_thresholds.min_word_count
        required_sections = self.validation_config.content_analysis.required_sections
        check_todos = self.validation_config.content_analysis.check_todos
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                word_count = len(content.split())
                if word_count < min_word_count:
                    _ = self.results.issues.append({
                        "type": "insufficient_content",
                        "severity": "low",
                        "file": str(file_path.relative_to(self.project_root)),
                        "word_count": word_count,
                        "minimum_required": min_word_count,
                        "recommendation": f"Expand content (currently {word_count} words, minimum {min_word_count})",
                    })
                if "README.md" in str(file_path) or "docs/" in str(file_path):
                    missing_sections = self._check_required_sections(
                        content,
                        required_sections,
                    )
                    if missing_sections:
                        _ = self.results.issues.append({
                            "type": "missing_sections",
                            "severity": "medium",
                            "file": str(file_path.relative_to(self.project_root)),
                            "missing_sections": missing_sections,
                            "recommendation": f"Add missing sections: {', '.join(missing_sections)}",
                        })
                if check_todos:
                    todos = re.findall(
                        r"(?i)(?:TODO|FIXME|XXX):\\s*(.+?)(?:\\n|$)",
                        content,
                    )
                    if todos:
                        _ = self.results.issues.append({
                            "type": "todo_markers",
                            "severity": "low",
                            "file": str(file_path.relative_to(self.project_root)),
                            "todo_count": len(todos),
                            "todos": todos[:5],
                            "recommendation": f"Address {len(todos)} TODO/FIXME items",
                        })
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                _ = self.results.issues.append({
                    "type": "content_analysis_error",
                    "severity": "medium",
                    "file": str(file_path.relative_to(self.project_root)),
                    "error": str(e),
                })

    def _check_required_sections(
        self,
        content: str,
        required_sections: t.StrSequence,
    ) -> MutableSequence[str]:
        """Check for required sections in documentation."""
        missing: MutableSequence[str] = []
        for section in required_sections:
            pattern = f"^#+\\s.*{re.escape(section)}.*$"
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                missing.append(section)
        return missing

    def check_content_consistency(self, doc_files: Sequence[Path]) -> None:
        """Check style consistency and formatting issues."""
        accessibility_cfg = self.style_guide.accessibility
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                formatting_issues = self._check_markdown_formatting(content)
                if formatting_issues:
                    _ = self.results.issues.append({
                        "type": "formatting_issues",
                        "severity": "low",
                        "file": str(file_path.relative_to(self.project_root)),
                        "issues": formatting_issues,
                        "recommendation": f"Fix {len(formatting_issues)} formatting issues",
                    })
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
                    _ = self.results.issues.append({
                        "type": "accessibility_issues",
                        "severity": severity,
                        "file": str(file_path.relative_to(self.project_root)),
                        "issues": accessibility_issues,
                        "recommendation": f"Address {len(accessibility_issues)} accessibility issues",
                    })
                if accessibility_cfg.heading_structure:
                    heading_issues = self._check_heading_hierarchy(content)
                    if heading_issues:
                        _ = self.results.issues.append({
                            "type": "heading_hierarchy",
                            "severity": "medium",
                            "file": str(file_path.relative_to(self.project_root)),
                            "issues": heading_issues,
                            "recommendation": "Fix heading hierarchy structure",
                        })
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                _ = self.results.issues.append({
                    "type": "consistency_check_error",
                    "severity": "medium",
                    "file": str(file_path.relative_to(self.project_root)),
                    "error": str(e),
                })

    def _check_markdown_formatting(self, content: str) -> MutableSequence[str]:
        """Check for markdown formatting issues."""
        issues: MutableSequence[str] = []
        formatting_cfg = self.style_guide.formatting
        unordered_lists = re.findall(r"^[\\s]*[-\\*\\+]", content, re.MULTILINE)
        if len(set(unordered_lists)) > 1:
            issues.append("mixed unordered list styles")
        emphasis_patterns = ["\\*[^*]+\\*", "_[^_]+_"]
        emphasis_usage = [
            pattern for pattern in emphasis_patterns if re.search(pattern, content)
        ]
        if len(emphasis_usage) > 1:
            issues.append("mixed emphasis styles (* vs _)")
        if formatting_cfg.trailing_spaces:
            trailing_spaces = re.findall(r"[ \\t]+$", content, re.MULTILINE)
            if trailing_spaces:
                issues.append(f"{len(trailing_spaces)} lines with trailing spaces")
        max_length = formatting_cfg.max_line_length
        long_lines = [line for line in content.split("\n") if len(line) > max_length]
        if long_lines:
            issues.append(f"{len(long_lines)} lines exceed {max_length} characters")
        return issues

    def _check_accessibility(self, content: str) -> MutableSequence[t.StrMapping]:
        """Check accessibility compliance."""
        issues: MutableSequence[t.StrMapping] = []
        accessibility_cfg = self.style_guide.accessibility
        if accessibility_cfg.require_alt_text:
            images_without_alt = re.findall(r"!\\[\\]\\([^)]+\\)", content)
            if images_without_alt:
                issues.extend([
                    {
                        "type": "missing_alt_text",
                        "description": f"Image without alt text: {img}",
                    }
                    for img in images_without_alt
                ])
        if accessibility_cfg.descriptive_links:
            generic_links = re.findall(
                r"\\[here|click here|link|read more\\]\\([^)]+\\)",
                content,
                re.IGNORECASE,
            )
            if generic_links:
                issues.extend([
                    {
                        "type": "generic_link_text",
                        "description": f"Non-descriptive link text: {link}",
                    }
                    for link in generic_links
                ])
        return issues

    def _check_heading_hierarchy(self, content: str) -> t.StrSequence:
        """Check heading hierarchy for logical structure."""
        headings = re.findall(r"^(#+)\\s+(.+)$", content, re.MULTILINE)
        heading_levels = [len(level) for level, _ in headings]
        issues = [
            f"Skipped heading level at line with H{heading_levels[i]}"
            for i in range(1, len(heading_levels))
            if heading_levels[i] > heading_levels[i - 1] + 1
        ]
        if heading_levels and heading_levels[0] != 1:
            issues.append("Document should start with H1")
        return issues

    def check_links_and_references(self, doc_files: Sequence[Path]) -> None:
        """Check links and references for validity."""
        link_validation = self.validation_config.link_validation
        all_links: MutableSequence[Mapping[str, str | int]] = []
        image_refs: MutableSequence[t.StrMapping] = []
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                external_links = re.findall(
                    r"\\[([^\\]]+)\\]\\((https?://[^)]+)\\)",
                    content,
                )
                for text, url in external_links:
                    all_links.append({
                        "url": url,
                        "text": text,
                        "file": str(file_path.relative_to(self.project_root)),
                        "type": "external",
                    })
                internal_links = re.findall(r"\\[([^\\]]+)\\]\\(([^)]+)\\)", content)
                for text, link in internal_links:
                    if not link.startswith(("http://", "https://", "#", "mailto:")):
                        all_links.append({
                            "url": link,
                            "text": text,
                            "file": str(file_path.relative_to(self.project_root)),
                            "type": "internal",
                        })
                images = re.findall(r"!\\[([^\\]]*)\\]\\(([^)]+)\\)", content)
                for alt_text, src in images:
                    image_refs.append({
                        "src": src,
                        "alt": alt_text,
                        "file": str(file_path.relative_to(self.project_root)),
                    })
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                _ = self.results.issues.append({
                    "type": "link_extraction_error",
                    "severity": "medium",
                    "file": str(file_path.relative_to(self.project_root)),
                    "error": str(e),
                })
        if link_validation.check_external:
            self._validate_external_links(all_links)
        if link_validation.check_internal:
            self._validate_internal_links(all_links, doc_files)
        if link_validation.check_images:
            self._validate_images(image_refs)

    def _validate_external_links(
        self,
        links: Sequence[Mapping[str, str | int]],
    ) -> None:
        """Validate external links."""
        link_validation = self.validation_config.link_validation
        timeout = link_validation.timeout
        user_agent = link_validation.user_agent
        external_links = [link for link in links if link["type"] == "external"]
        for link in external_links:
            try:
                response = requests.head(
                    str(link["url"]),
                    timeout=timeout,
                    headers={"User-Agent": user_agent},
                    allow_redirects=True,
                )
                if response.status_code >= 400:
                    _ = self.results.issues.append({
                        "type": "broken_external_link",
                        "severity": "high",
                        "file": link["file"],
                        "url": link["url"],
                        "status_code": response.status_code,
                        "recommendation": f"Fix or remove broken link (HTTP {response.status_code})",
                    })
            except requests.RequestException as e:
                _ = self.results.issues.append({
                    "type": "unreachable_external_link",
                    "severity": "high",
                    "file": link["file"],
                    "url": link["url"],
                    "error": str(e),
                    "recommendation": "Verify link URL and accessibility",
                })

    def _validate_internal_links(
        self,
        links: Sequence[Mapping[str, str | int]],
        doc_files: Sequence[Path],
    ) -> None:
        """Validate internal links."""
        internal_links = [link for link in links if link["type"] == "internal"]
        doc_file_names = {str(f.relative_to(self.project_root)) for f in doc_files}
        for link in internal_links:
            url_val = link["url"]
            target_file = (
                (str(url_val).split("#")[0]) if isinstance(url_val, str) else ""
            )
            if target_file and target_file not in doc_file_names:
                file_val = link["file"]
                link_file_dir = (
                    Path(str(file_val)).parent if isinstance(file_val, str) else Path()
                )
                potential_target = (link_file_dir / target_file).resolve()
                if not potential_target.exists():
                    _ = self.results.issues.append({
                        "type": "broken_internal_link",
                        "severity": "high",
                        "file": link["file"],
                        "target": link["url"],
                        "recommendation": f"Fix broken internal link to '{link['url']}'",
                    })

    def _validate_images(self, images: Sequence[t.StrMapping]) -> None:
        """Validate image references."""
        for image in images:
            if image["src"].startswith(("http://", "https://")):
                continue
            image_path = Path(image["src"])
            if not image_path.is_absolute():
                file_dir = Path(image["file"]).parent
                full_path = (self.project_root / file_dir / image_path).resolve()
            else:
                full_path = image_path
            if not full_path.exists():
                _ = self.results.issues.append({
                    "type": "missing_image",
                    "severity": "medium",
                    "file": image["file"],
                    "image_src": image["src"],
                    "recommendation": f"Add missing image file: {image['src']}",
                })

    def calculate_quality_metrics(self) -> None:
        """Calculate overall quality metrics."""
        issues = self.results.issues
        total_issues = len(issues)
        severity_counts = {
            "critical": len([i for i in issues if i.get("severity") == "critical"]),
            "high": len([i for i in issues if i.get("severity") == "high"]),
            "medium": len([i for i in issues if i.get("severity") == "medium"]),
            "low": len([i for i in issues if i.get("severity") == "low"]),
        }
        weights = {"critical": 25, "high": 10, "medium": 5, "low": 1}
        weighted_score = sum(
            severity_counts[level] * weights[level] for level in severity_counts
        )
        quality_score = max(0, 100 - weighted_score)
        self.results.metrics = m.Quality.AuditMetrics.model_validate({
            "total_issues": total_issues,
            "severity_breakdown": severity_counts,
            "quality_score": quality_score,
            "files_analyzed": self.results.files_analyzed,
            "issues_per_file": total_issues / self.results.files_analyzed
            if self.results.files_analyzed > 0
            else 0,
        })

    def generate_recommendations(self) -> None:
        """Generate actionable recommendations based on audit results."""
        metrics = self.results.metrics
        issues = self.results.issues
        recommendations: MutableSequence[m.Quality.AuditRecommendation] = []
        quality_score = metrics.quality_score
        if quality_score < 50:
            recommendations.append(
                m.Quality.AuditRecommendation(
                    priority="critical",
                    category="overall_quality",
                    recommendation="Immediate attention required - documentation quality is poor",
                    actions=[
                        "Address all critical and high-severity issues immediately",
                        "Implement automated quality gates in CI/CD",
                        "Schedule regular maintenance reviews",
                    ],
                ),
            )
        elif quality_score < 75:
            recommendations.append(
                m.Quality.AuditRecommendation(
                    priority="high",
                    category="quality_improvement",
                    recommendation="Documentation quality needs improvement",
                    actions=[
                        "Focus on fixing high-severity issues",
                        "Implement regular audit schedule",
                        "Consider documentation training for team",
                    ],
                ),
            )
        broken_links = [
            i
            for i in issues
            if "link" in str(i.get("type", ""))
            and i.get("severity") in {"critical", "high"}
        ]
        if broken_links:
            recommendations.append(
                m.Quality.AuditRecommendation(
                    priority="high",
                    category="link_maintenance",
                    recommendation=f"Fix {len(broken_links)} broken links",
                    actions=[
                        "Update or remove broken external links",
                        "Fix internal reference paths",
                        "Implement automated link checking in CI/CD",
                    ],
                ),
            )
        outdated_content = [i for i in issues if i["type"] == "outdated_content"]
        if outdated_content:
            recommendations.append(
                m.Quality.AuditRecommendation(
                    priority="medium",
                    category="content_freshness",
                    recommendation=f"Update {len(outdated_content)} outdated documents",
                    actions=[
                        "Review content for accuracy",
                        "Update version numbers and dates",
                        "Implement content freshness monitoring",
                    ],
                ),
            )
        accessibility_issues = [
            i for i in issues if i["type"] == "accessibility_issues"
        ]
        if accessibility_issues:
            recommendations.append(
                m.Quality.AuditRecommendation(
                    priority="medium",
                    category="accessibility",
                    recommendation="Improve documentation accessibility",
                    actions=[
                        "Add alt text to all images",
                        "Use descriptive link text",
                        "Ensure proper heading hierarchy",
                    ],
                ),
            )
        self.results.recommendations = recommendations

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
        _ = output_path
        if output_format == "json":
            return self.results.model_dump_json(indent=2)
        if output_format == "html":
            return self._generate_html_report()
        return self.results.model_dump_json()

    def _generate_html_report(self) -> str:
        """Generate HTML audit report."""
        metrics = self.results.metrics
        severity_breakdown = metrics.severity_breakdown
        critical_count = severity_breakdown["critical"]
        high_count = severity_breakdown["high"]
        medium_count = severity_breakdown["medium"]
        low_count = severity_breakdown["low"]
        quality_score = metrics.quality_score
        total_issues = metrics.total_issues
        issues_per_file = metrics.issues_per_file
        files_analyzed = metrics.files_analyzed
        html = f"""\n<!DOCTYPE html>\n<html>\n<head>\n    <title>FLEXT Quality Documentation Audit Report</title>\n    <style>\n        body {{ font-family: Arial, sans-serif; margin: 40px; }}\n        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}\n        .metrics {{ display: flex; gap: 20px; margin: 20px 0; }}\n        .metric {{ background: #e8f4fd; padding: 15px; border-radius: 5px; flex: 1; }}\n        .issues {{ margin: 20px 0; }}\n        .issue {{ border: 1px solid #ddd; margin: 10px 0; padding: 10px; border-radius: 5px; }}\n        .severity-critical {{ border-left: 5px solid #dc3545; }}\n        .severity-high {{ border-left: 5px solid #fd7e14; }}\n        .severity-medium {{ border-left: 5px solid #ffc107; }}\n        .severity-low {{ border-left: 5px solid #28a745; }}\n    </style>\n</head>\n<body>\n    <div class="header">\n        <h1>FLEXT Quality Documentation Audit Report</h1>\n        <p>Generated: {self.results.timestamp}</p>\n        <p>Files Analyzed: {files_analyzed}</p>\n    </div>\n\n    <div class="metrics">\n        <div class="metric">\n            <h3>Quality Score</h3>\n            <div style="font-size: 2em; font-weight: bold; color: {self._get_score_color(quality_score)};">\n                {quality_score}%\n            </div>\n        </div>\n        <div class="metric">\n            <h3>Total Issues</h3>\n            <div style="font-size: 2em; font-weight: bold;">\n                {total_issues}\n            </div>\n        </div>\n        <div class="metric">\n            <h3>Issues per File</h3>\n            <div style="font-size: 2em; font-weight: bold;">\n                {issues_per_file:.1f}\n            </div>\n        </div>\n    </div>\n\n    <h2>Issues by Severity</h2>\n    <ul>\n        <li>Critical: {critical_count}</li>\n        <li>High: {high_count}</li>\n        <li>Medium: {medium_count}</li>\n        <li>Low: {low_count}</li>\n    </ul>\n\n    <div class="issues">\n        <h2>Detailed Issues</h2>\n"""
        for issue in self.results.issues:
            severity_class = f"severity-{issue.get('severity', 'info')}"
            type_str = str(issue.get("type", ""))
            sev_str = str(issue.get("severity", ""))
            html += f"""\n        <div class="issue {severity_class}">\n            <h4>{type_str.replace("_", " ").title()} ({sev_str.upper()})</h4>\n            <p><strong>File:</strong> {issue.get("file", "N/A")}</p>\n            <p><strong>Recommendation:</strong> {issue.get("recommendation", "N/A")}</p>\n"""
            if "age_days" in issue:
                html += f"<p><strong>Age:</strong> {issue['age_days']} days</p>"
            if "word_count" in issue:
                html += f"<p><strong>Word Count:</strong> {issue['word_count']}</p>"
            if "status_code" in issue:
                html += f"<p><strong>Status Code:</strong> {issue['status_code']}</p>"
            if "url" in issue:
                html += f"<p><strong>URL:</strong> <a href='{issue['url']}'>{issue['url']}</a></p>"
            html += "</div>"
        html += "\n    </div>\n</body>\n</html>\n"
        return html

    def _get_score_color(self, score: int) -> str:
        """Get color for quality score."""
        if score >= 80:
            return "#28a745"
        if score >= 60:
            return "#ffc107"
        return "#dc3545"

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
        _ = filepath.write_text(report_content, encoding="utf-8")
        latest_file = output_dir / "latest_audit.json"
        latest_file.write_text(self.results.model_dump_json(indent=2), encoding="utf-8")
        return str(filepath)


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="FLEXT Quality Documentation Audit")
    _ = parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run complete audit with all checks",
    )
    _ = parser.add_argument(
        "--check-freshness",
        action="store_true",
        help="Check content freshness only",
    )
    _ = parser.add_argument(
        "--check-completeness",
        action="store_true",
        help="Check content completeness only",
    )
    _ = parser.add_argument(
        "--check-consistency",
        action="store_true",
        help="Check style consistency only",
    )
    _ = parser.add_argument(
        "--check-links",
        action="store_true",
        help="Check links and references only",
    )
    _ = parser.add_argument(
        "--ci-mode",
        action="store_true",
        help="CI/CD mode - exit with error code on failures",
    )
    _ = parser.add_argument(
        "--fail-on-errors",
        action="store_true",
        help="Exit with error code if critical/high severity issues found",
    )
    _ = parser.add_argument(
        "--output",
        type=str,
        default="docs/maintenance/reports/",
        help="Output directory for reports",
    )
    _ = parser.add_argument(
        "--format",
        type=str,
        choices=["json", "html"],
        default="json",
        help="Report format",
    )
    _ = parser.add_argument(
        "--config",
        type=str,
        default="docs/maintenance/config/",
        help="Configuration directory path",
    )
    return parser


def _execute_audit_checks(
    auditor: FlextQualityDocumentationAuditor,
    args: argparse.Namespace,
) -> m.Quality.AuditorResults:
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


def _should_fail_on_results(
    args: argparse.Namespace, metrics: m.Quality.AuditMetrics,
) -> bool:
    """Determine if the process should fail based on results and arguments."""
    should_fail = False
    if args.fail_on_errors:
        severity_breakdown = metrics.severity_breakdown
        critical = severity_breakdown["critical"]
        high = severity_breakdown["high"]
        critical_high_issues = critical + high
        if critical_high_issues > 0:
            should_fail = True
    quality_score = metrics.quality_score
    if args.ci_mode and quality_score < 70:
        should_fail = True
    return should_fail


def main() -> None:
    """Main entry point for documentation audit."""
    parser = _create_argument_parser()
    args = parser.parse_args()
    auditor = FlextQualityDocumentationAuditor(args.config)
    try:
        results = _execute_audit_checks(auditor, args)
        auditor.save_report(args.format, args.output)
        metrics = results.metrics
        if _should_fail_on_results(args, metrics):
            raise SystemExit(1)
    except (
        FileNotFoundError,
        PermissionError,
        OSError,
        yaml.YAMLError,
        KeyError,
        ValueError,
    ):
        if args.ci_mode or args.fail_on_errors:
            raise SystemExit(1) from None


if __name__ == "__main__":
    main()
