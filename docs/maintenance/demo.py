#!/usr/bin/env python3
"""FLEXT Quality Documentation Maintenance System Demo.

Complete demonstration of the documentation maintenance framework
showing how to run comprehensive audits, validations, and optimizations.
"""

import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Import maintenance tools
try:
    from scripts.audit import DocumentationAuditor
    from scripts.report import DocumentationReporter
    from tools.content_analyzer import ContentAnalyzer
    from tools.link_checker import LinkChecker
    from tools.style_validator import StyleValidator
except ImportError:
    # Tools may not be available in all environments
    pass


def print_header(title: str) -> None:
    """Print a formatted header."""


def print_step(step_num: int, description: str) -> None:
    """Print a formatted step."""


def run_maintenance_demo() -> None:
    """Run the complete documentation maintenance demonstration."""
    # Constants
    max_files_to_show = 10
    good_score_threshold = 80

    print_header("FLEXT Quality Documentation Maintenance Demo")

    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)

    # Step 1: Discover documentation files
    print_step(1, "Discovering Documentation Files")

    doc_files = []
    patterns = [
        "**/*.md",
        "**/*.mdx",
        "**/README*",
        "**/docs/**/*.md",
        "**/docs/**/*.mdx",
    ]

    for pattern in patterns:
        matches = list(Path().glob(pattern))
        doc_files.extend(matches)

    # Filter out maintenance files and internal docs
    doc_files = [
        f
        for f in doc_files
        if not any(
            exclude in str(f)
            for exclude in [
                "docs/maintenance",
                ".serena/memories",
                "__pycache__",
                ".git",
                "node_modules",
                "build",
                "dist",
            ]
        )
    ]

    doc_files = sorted(set(doc_files))  # Remove duplicates

    for _i, _file in enumerate(
        doc_files[:max_files_to_show], 1
    ):  # Show first max_files_to_show
        pass
    if len(doc_files) > max_files_to_show:
        pass

    # Step 2: Run comprehensive audit
    print_step(2, "Running Comprehensive Documentation Audit")

    try:
        auditor = DocumentationAuditor()

        audit_results = auditor.run_comprehensive_audit()
        auditor.save_report("json", "docs/maintenance/reports/")

        # Show top issues
        if audit_results["issues"]:
            severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            sorted_issues = sorted(
                audit_results["issues"],
                key=lambda x: (
                    severity_order.get(x.get("severity", "low"), 3),
                    x.get("type", ""),
                ),
            )

            for issue in sorted_issues[:5]:
                {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(
                    issue.get("severity"), "⚪"
                )

    except ImportError:
        pass

    # Step 3: Validate links and references
    print_step(3, "Validating Links and References")

    try:
        # Extract links from files
        link_checker = LinkChecker()

        # Simple synchronous validation for demo
        all_links = []
        for file_path in doc_files[:5]:  # Check first 5 files for demo
            try:
                file_path.read_text(encoding="utf-8")
                file_links = link_checker.find_all_links([file_path])
                all_links.extend(file_links)
            except Exception as e:
                logger.warning(f"Failed to extract links from {file_path}: {e}")

        # Categorize links
        link_types = {}
        for link in all_links:
            link_type = link.get("type", "unknown")
            link_types[link_type] = link_types.get(link_type, 0) + 1

        # Save link validation results
        {
            "timestamp": datetime.now(UTC).isoformat(),
            "links_found": len(all_links),
            "link_types": link_types,
            "files_checked": len(doc_files[:5]),
        }

        # Note: Full validation would require async processing and may take time

    except ImportError:
        pass

    # Step 4: Check style consistency
    print_step(4, "Checking Style Consistency")

    try:
        style_validator = StyleValidator()

        # Validate a few key files
        test_files = [
            f for f in doc_files if f.name in {"README.md", "CLAUDE.md", "TODO.md"}
        ][:3]

        total_violations = 0
        total_issues = 0

        for file_path in test_files:
            result = style_validator.validate_file(file_path)
            violations = len(result.get("violations", []))
            issues = len(result.get("issues", []))
            total_violations += violations
            total_issues += issues

        if total_violations + total_issues == 0:
            pass

    except ImportError:
        pass

    # Step 5: Analyze content quality
    print_step(5, "Analyzing Content Quality")

    try:
        content_analyzer = ContentAnalyzer()

        # Analyze key documentation files
        key_files = [f for f in doc_files if f.name in {"README.md", "CLAUDE.md"}][:2]

        total_score = 0
        analyzed_count = 0

        for file_path in key_files:
            analysis = content_analyzer.analyze_file(file_path)
            score = analysis.get("quality_score", 0)
            total_score += score
            analyzed_count += 1

            analysis.get("readability", {})

            if analysis.get("issues"):
                pass

        if analyzed_count > 0:
            avg_score = total_score / analyzed_count
            if avg_score >= good_score_threshold:
                # Good score achieved
                pass

    except ImportError:
        pass

    # Step 6: Generate comprehensive report
    print_step(6, "Generating Maintenance Report")

    try:
        reporter = DocumentationReporter()
        report_content = reporter.generate_quality_report("html")

        # Save report
        reporter.save_report(report_content, "maintenance_demo_report", "html")

    except ImportError:
        pass

    # Step 7: Show automation options
    print_step(7, "Automation and Integration Options")

    # Step 8: Summary and next steps
    print_step(8, "Summary and Recommendations")

    print_header("Demo Complete")


def show_help() -> None:
    """Show help information."""


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in {"--help", "-h"}:
        show_help()
    else:
        try:
            run_maintenance_demo()
        except KeyboardInterrupt:
            logger.info("Demo interrupted by user.")
        except Exception:
            logger.exception("Demo failed with error")
            sys.exit(1)
