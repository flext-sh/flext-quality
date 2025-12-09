#!/usr/bin/env python3
"""FLEXT Quality Documentation Validation System.

Specialized validation tools for links, references, and content integrity.
Performs external link checking, internal reference validation,
and comprehensive content verification.

Usage:
    python validate.py --external-links
    python validate.py --internal-links --images
    python validate.py --all --verbose
"""

import argparse
import concurrent.futures
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests


class LinkValidator:
    """Advanced link validation and checking system."""

    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        max_workers: int = 5,
    ) -> None:
        """Initialize the link validator with timeout and retry settings."""
        self.timeout = timeout
        self.retries = retries
        self.max_workers = max_workers
        self.user_agent = "FLEXT-Quality-Link-Validator/1.0"

        # Validation results
        self.results = {
            "timestamp": datetime.now(UTC).isoformat(),
            "links_checked": 0,
            "valid_links": 0,
            "broken_links": 0,
            "warnings": 0,
            "errors": [],
            "warnings_list": [],
        }

    def find_all_links(self, doc_files: list[Path]) -> list[dict]:
        """Extract all links from documentation files."""
        all_links = []

        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(
                    file_path.relative_to(file_path.parents[2]),
                )  # Relative to project root

                # Extract markdown links: [text](url)
                link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
                matches = re.findall(link_pattern, content)

                for text, url in matches:
                    link_type = self._classify_link(url)
                    all_links.append({
                        "text": text,
                        "url": url,
                        "type": link_type,
                        "file": file_rel_path,
                        "line_number": self._find_line_number(
                            content,
                            f"[{text}]({url})",
                        ),
                    })

                # Extract HTML links: <a href="url">text</a>
                html_link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
                html_matches = re.findall(html_link_pattern, content, re.IGNORECASE)

                for url, text in html_matches:
                    link_type = self._classify_link(url)
                    all_links.append({
                        "text": text.strip(),
                        "url": url,
                        "type": link_type,
                        "file": file_rel_path,
                        "line_number": self._find_line_number(content, f'href="{url}"'),
                    })

                # Extract image references: ![alt](src)
                image_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
                image_matches = re.findall(image_pattern, content)

                for alt_text, src in image_matches:
                    all_links.append({
                        "text": alt_text,
                        "url": src,
                        "type": "image",
                        "file": file_rel_path,
                        "line_number": self._find_line_number(
                            content,
                            f"![{alt_text}]({src})",
                        ),
                    })

            except Exception as e:
                self.results["errors"].append({
                    "type": "file_read_error",
                    "file": file_rel_path,
                    "error": str(e),
                })

        return all_links

    def _classify_link(self, url: str) -> str:
        """Classify link type based on URL pattern."""
        if url.startswith(("http://", "https://")):
            return "external"
        if url.startswith("mailto:"):
            return "email"
        if url.startswith("#"):
            return "anchor"
        if url.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            return "image"
        if url.startswith(("./", "../")) or url.endswith((".md", ".mdx")):
            return "internal"
        return "reference"

    def _find_line_number(self, content: str, search_text: str) -> int | None:
        """Find line number of specific text in content."""
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if search_text in line:
                return i
        return None

    def validate_external_links(
        self,
        links: list[dict],
        *,
        verbose: bool = False,
    ) -> dict[str, Any]:
        """Validate external links with concurrent checking."""
        external_links = [link for link in links if link["type"] == "external"]

        if not external_links:
            return self.results

        # Use thread pool for concurrent checking
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers,
        ) as executor:
            futures = [
                executor.submit(self._check_single_external_link, link, verbose)
                for link in external_links
            ]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self.results["links_checked"] += 1

                if result["valid"]:
                    self.results["valid_links"] += 1
                else:
                    self.results["broken_links"] += 1
                    self.results["errors"].append(result)

        return self.results

    def _create_link_result(
        self,
        link: dict,
        *,
        valid: bool,
        url: str,
        status_code: int | None = None,
        error: str | None = None,
    ) -> dict[str, Any]:
        """Create a standardized link validation result."""
        result = {
            "valid": valid,
            "url": url,
            "file": link["file"],
            "line": link.get("line_number"),
        }
        if status_code is not None:
            result["status_code"] = status_code
        if error is not None:
            result["error"] = error
        return result

    def _make_http_request(self, url: str, method: str = "head") -> requests.Response:
        """Make an HTTP request with appropriate headers."""
        headers = {"User-Agent": self.user_agent}
        if method == "head":
            headers["Accept"] = "*/*"

        request_func = requests.head if method == "head" else requests.get

        return request_func(
            url,
            timeout=self.timeout,
            headers=headers,
            allow_redirects=True,
        )

    def _should_retry_with_get(self, status_code: int) -> bool:
        """Check if we should retry with GET for certain status codes."""
        return status_code in {405, 406, 409, 410, 500, 502, 503}

    def _handle_request_attempt(
        self,
        url: str,
        attempt: int,
    ) -> tuple[bool, dict[str, Any] | None]:
        """Handle a single request attempt."""
        try:
            response = self._make_http_request(url)

            if response.status_code < 400:
                return True, {"status_code": response.status_code}

            # Try GET for certain error codes
            if self._should_retry_with_get(response.status_code):
                response = self._make_http_request(url, "get")
                if response.status_code < 400:
                    return True, {"status_code": response.status_code}

            return False, {
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
            }

        except requests.exceptions.Timeout:
            if attempt == self.retries - 1:
                return False, {"error": f"Timeout after {self.timeout}s"}
        except requests.exceptions.RequestException as e:
            if attempt == self.retries - 1:
                return False, {"error": str(e)}
        except Exception as e:
            return False, {"error": f"Unexpected error: {e!s}"}

        return False, None

    def _check_single_external_link(
        self,
        link: dict,
        *,
        verbose: bool = False,
    ) -> dict[str, Any]:
        """Check a single external link."""
        # Reserved for future verbose output functionality
        _ = verbose  # Reserved for future use
        url = link["url"]

        for attempt in range(self.retries):
            success, result = self._handle_request_attempt(url, attempt)
            if result is not None:
                return self._create_link_result(link, success, url, **result)

        return self._create_link_result(link, False, url, error="Max retries exceeded")

    def validate_internal_links(
        self,
        links: list[dict],
        doc_files: list[Path],
    ) -> dict[str, Any]:
        """Validate internal links and references."""
        internal_links = [
            link for link in links if link["type"] in {"internal", "reference"}
        ]
        doc_file_names = {
            str(f.relative_to(f.parents[2])) for f in doc_files
        }  # Relative to project root

        for link in internal_links:
            target = link["url"].split("#")[0]  # Remove anchor

            if not target:  # Just an anchor link
                continue

            # Check if target file exists
            if target not in doc_file_names:
                # Try resolving relative paths
                link_file_dir = Path(link["file"]).parent
                potential_targets = [
                    link_file_dir / target,
                    Path(target),
                    self._resolve_relative_path(link_file_dir, target),
                ]

                target_exists = False
                for potential_target in potential_targets:
                    resolved_path = (
                        Path(link["file"]).parent.parent.parent / potential_target
                    )
                    if resolved_path.exists() and resolved_path.suffix in {
                        ".md",
                        ".mdx",
                    }:
                        target_exists = True
                        break

                if not target_exists:
                    self.results["errors"].append({
                        "type": "broken_internal_link",
                        "url": link["url"],
                        "target": target,
                        "file": link["file"],
                        "line": link.get("line_number"),
                        "error": "Target file not found",
                    })
                    self.results["broken_links"] += 1
                else:
                    self.results["valid_links"] += 1
            else:
                self.results["valid_links"] += 1

            self.results["links_checked"] += 1

        return self.results

    def _resolve_relative_path(self, base_dir: Path, target: str) -> Path:
        """Resolve relative path from base directory."""
        if target.startswith("./"):
            return base_dir / target[2:]
        if target.startswith("../"):
            return base_dir.parent / target[3:]
        return Path(target)

    def validate_images(self, links: list[dict], project_root: Path) -> dict[str, Any]:
        """Validate image references."""
        images = [link for link in links if link["type"] == "image"]

        for image in images:
            src = image["url"]

            # Skip external images
            if src.startswith(("http://", "https://")):
                # Could add external image checking here if needed
                self.results["valid_links"] += 1
                continue

            # Check local images
            image_path = Path(src)
            if not image_path.is_absolute():
                # Relative to the file's directory
                file_dir = Path(image["file"]).parent
                full_path = (project_root / file_dir / image_path).resolve()
            else:
                full_path = image_path

            if full_path.exists():
                self.results["valid_links"] += 1
            else:
                self.results["errors"].append({
                    "type": "missing_image",
                    "src": src,
                    "file": image["file"],
                    "line": image.get("line_number"),
                    "error": f"Image file not found: {full_path}",
                })
                self.results["broken_links"] += 1

            self.results["links_checked"] += 1

        return self.results

    def validate_anchors(
        self,
        links: list[dict],
        doc_files: list[Path],
    ) -> dict[str, Any]:
        """Validate anchor links within documents."""
        anchor_links = [link for link in links if link["type"] == "anchor"]

        # Build anchor index for each file
        file_anchors = {}
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(file_path.relative_to(file_path.parents[2]))

                # Extract headings that can be anchors
                headings = re.findall(r"^#{1,6}\s+(.+)$", content, re.MULTILINE)
                anchors = [self._heading_to_anchor(heading) for heading in headings]

                # Extract explicit anchor definitions
                explicit_anchors = re.findall(
                    r'<a[^>]+id=["\']([^"\']+)["\'][^>]*>',
                    content,
                )
                anchors.extend(explicit_anchors)

                file_anchors[file_rel_path] = set(anchors)

            except Exception as e:
                self.results["warnings_list"].append({
                    "type": "anchor_index_error",
                    "file": file_rel_path,
                    "warning": f"Could not build anchor index: {e!s}",
                })

        # Check anchor links
        for link in anchor_links:
            anchor = link["url"][1:]  # Remove leading #
            file_path = link["file"]

            if file_path in file_anchors and anchor in file_anchors[file_path]:
                self.results["valid_links"] += 1
            else:
                self.results["errors"].append({
                    "type": "broken_anchor",
                    "anchor": anchor,
                    "file": file_path,
                    "line": link.get("line_number"),
                    "error": f"Anchor '{anchor}' not found in {file_path}",
                })
                self.results["broken_links"] += 1

            self.results["links_checked"] += 1

        return self.results

    def _heading_to_anchor(self, heading: str) -> str:
        """Convert heading text to anchor format."""
        # GitHub-style anchor generation
        anchor = heading.lower()
        anchor = re.sub(
            r"[^\w\s-]",
            "",
            anchor,
        )  # Remove special chars except spaces and hyphens
        return re.sub(r"\s+", "-", anchor)  # Replace spaces with hyphens

    def check_link_text_quality(self, links: list[dict]) -> dict[str, Any]:
        """Check quality of link text for accessibility and usability."""
        poor_link_texts = [
            "here",
            "click here",
            "link",
            "read more",
            "this",
            "that",
            "page",
            "article",
            "post",
            "click",
            "tap",
            "go",
        ]

        for link in links:
            text = link["text"].lower().strip()

            if text in poor_link_texts or len(text) < 3:
                self.results["warnings_list"].append({
                    "type": "poor_link_text",
                    "text": link["text"],
                    "url": link["url"],
                    "file": link["file"],
                    "line": link.get("line_number"),
                    "warning": "Link text is not descriptive enough for accessibility",
                })
                self.results["warnings"] += 1

        return self.results

    def generate_report(self, report_format: str = "json") -> str:
        """Generate validation report."""
        if report_format == "json":
            return json.dumps(self.results, indent=2, default=str)
        return json.dumps(self.results, default=str)

    def save_report(self, output_path: str = "docs/maintenance/reports/") -> Path:
        """Save validation report."""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"validation_report_{timestamp}.json"
        filepath = output_dir / filename

        report_content = self.generate_report("json")
        filepath.write_text(report_content, encoding="utf-8")

        # Also save latest report
        latest_file = output_dir / "latest_validation.json"
        json.dump(self.results, latest_file.open("w"), indent=2, default=str)

        return filepath


class ContentValidator:
    """Content validation and quality checking system."""

    def __init__(self) -> None:
        """Initialize the content validator."""
        self.results = {
            "timestamp": datetime.now(UTC).isoformat(),
            "files_checked": 0,
            "content_issues": [],
            "quality_metrics": {},
        }

    def validate_markdown_syntax(self, doc_files: list[Path]) -> dict[str, Any]:
        """Validate markdown syntax and formatting."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(file_path.relative_to(file_path.parents[2]))

                issues = self._check_markdown_issues(content)

                if issues:
                    self.results["content_issues"].extend([
                        {**issue, "file": file_rel_path} for issue in issues
                    ])

                self.results["files_checked"] += 1

            except Exception as e:
                self.results["content_issues"].append({
                    "type": "syntax_validation_error",
                    "file": file_rel_path,
                    "error": str(e),
                })

        return self.results

    def _check_markdown_issues(self, content: str) -> list[dict]:
        """Check for markdown syntax issues."""
        issues = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for broken links (unclosed brackets)
            if "[" in line and "]" in line and "(" in line and ")" not in line:
                issues.append({
                    "type": "broken_link_syntax",
                    "line": i,
                    "content": line.strip(),
                    "error": "Unclosed link syntax",
                })

            # Check for broken images (unclosed brackets)
            if "![" in line and "]" in line and "(" in line and ")" not in line:
                issues.append({
                    "type": "broken_image_syntax",
                    "line": i,
                    "content": line.strip(),
                    "error": "Unclosed image syntax",
                })

            # Check for inconsistent list indentation
            if line.strip().startswith(("- ", "* ", "+ ")):
                # This is a basic check - could be enhanced
                pass

            # Check for trailing spaces (configurable)
            if line.rstrip() != line:
                issues.append({
                    "type": "trailing_spaces",
                    "line": i,
                    "content": line,
                    "error": "Line has trailing spaces",
                })

        return issues

    def check_content_quality(self, doc_files: list[Path]) -> dict[str, Any]:
        """Check content quality metrics."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(file_path.relative_to(file_path.parents[2]))

                metrics = self._calculate_content_metrics(content)

                # Check against quality thresholds
                if metrics["word_count"] < 50:
                    self.results["content_issues"].append({
                        "type": "insufficient_content",
                        "file": file_rel_path,
                        "word_count": metrics["word_count"],
                        "warning": "Document appears to be too short",
                    })

                if metrics["readability_score"] < 60:
                    self.results["content_issues"].append({
                        "type": "readability_issue",
                        "file": file_rel_path,
                        "readability_score": metrics["readability_score"],
                        "warning": "Content may be difficult to read",
                    })

                self.results["files_checked"] += 1

            except Exception as e:
                self.results["content_issues"].append({
                    "type": "quality_analysis_error",
                    "file": file_rel_path,
                    "error": str(e),
                })

        return self.results

    def _calculate_content_metrics(self, content: str) -> dict[str, Any]:
        """Calculate basic content quality metrics."""
        words = re.findall(r"\b\w+\b", content)
        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Basic readability calculation (simplified)
        if sentences:
            avg_words_per_sentence = len(words) / len(sentences)
            readability_score = max(
                0,
                min(100, 100 - (avg_words_per_sentence - 15) * 2),
            )
        else:
            readability_score = 0

        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_words_per_sentence": avg_words_per_sentence if sentences else 0,
            "readability_score": readability_score,
            "has_code_blocks": bool(r"```" in content),
            "has_lists": bool(re.search(r"^[\s]*[-\*\+]", content, re.MULTILINE)),
            "has_headers": bool(re.search(r"^#{1,6}\s", content, re.MULTILINE)),
        }


def _create_validation_parser() -> argparse.ArgumentParser:
    """Create and configure the validation argument parser."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality Documentation Validation",
    )
    parser.add_argument(
        "--external-links",
        action="store_true",
        help="Validate external links",
    )
    parser.add_argument(
        "--internal-links",
        action="store_true",
        help="Validate internal links",
    )
    parser.add_argument(
        "--images",
        action="store_true",
        help="Validate image references",
    )
    parser.add_argument("--anchors", action="store_true", help="Validate anchor links")
    parser.add_argument(
        "--link-text",
        action="store_true",
        help="Check link text quality",
    )
    parser.add_argument(
        "--markdown-syntax",
        action="store_true",
        help="Validate markdown syntax",
    )
    parser.add_argument(
        "--content-quality",
        action="store_true",
        help="Analyze content quality",
    )
    parser.add_argument("--all", action="store_true", help="Run all validation checks")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--output",
        type=str,
        default="docs/maintenance/reports/",
        help="Output directory for reports",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout for external link checks",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Retry attempts for external links",
    )
    parser.add_argument("--workers", type=int, default=5, help="Max concurrent workers")
    return parser


def _discover_validation_files() -> list[Path]:
    """Discover documentation files for validation."""
    project_root = Path(__file__).parent.parent.parent.parent
    doc_files = []

    for pattern in [
        "**/*.md",
        "**/*.mdx",
        "**/README*",
        "**/docs/**/*.md",
        "**/docs/**/*.mdx",
    ]:
        doc_files.extend(project_root.glob(pattern))

    # Remove duplicates and ignored files
    doc_files = list(set(doc_files))
    ignored_patterns = [".git", "__pycache__", "node_modules", ".serena/memories"]
    return [
        f
        for f in doc_files
        if not any(pattern in str(f) for pattern in ignored_patterns)
    ]


def _execute_validations(
    link_validator: LinkValidator,
    content_validator: ContentValidator,
    all_links: list[dict],
    doc_files: list[Path],
    args: argparse.Namespace,
) -> bool:
    """Execute the requested validations and return if any were run."""
    run_any_check = False

    if args.external_links or args.all:
        link_validator.validate_external_links(all_links, verbose=args.verbose)
        run_any_check = True

    if args.internal_links or args.all:
        link_validator.validate_internal_links(all_links, doc_files)
        run_any_check = True

    if args.images or args.all:
        project_root = Path(__file__).parent.parent.parent.parent
        link_validator.validate_images(all_links, project_root)
        run_any_check = True

    if args.anchors or args.all:
        link_validator.validate_anchors(all_links, doc_files)
        run_any_check = True

    if args.link_text or args.all:
        link_validator.check_link_text_quality(all_links)
        run_any_check = True

    if args.markdown_syntax or args.all:
        content_validator.validate_markdown_syntax(doc_files)
        run_any_check = True

    if args.content_quality or args.all:
        content_validator.check_content_quality(doc_files)
        run_any_check = True

    return run_any_check


def main() -> None:
    """Main entry point for documentation validation."""
    parser = _create_validation_parser()
    args = parser.parse_args()

    # Discover documentation files
    doc_files = _discover_validation_files()

    # Initialize validators
    link_validator = LinkValidator(
        timeout=args.timeout,
        retries=args.retries,
        max_workers=args.workers,
    )
    content_validator = ContentValidator()

    # Find all links
    all_links = link_validator.find_all_links(doc_files)

    # Execute validations
    run_any_check = _execute_validations(
        link_validator,
        content_validator,
        all_links,
        doc_files,
        args,
    )

    if not run_any_check:
        sys.exit(1)

    # Calculate summary and save reports
    total_errors = len(link_validator.results.get("errors", [])) + len(
        content_validator.results.get("content_issues", []),
    )
    link_validator.save_report(args.output)

    # Exit with error code for CI/CD
    if total_errors > 0:
        sys.exit(1)
