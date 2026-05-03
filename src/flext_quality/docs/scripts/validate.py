"""FLEXT Quality Documentation Validation System.

Specialized validation tools for links, references, and content integrity.
Performs external link checking, internal reference validation,
and comprehensive content verification.

Usage:
    python validate.py --external-links
    python validate.py --internal-links --images
    python validate.py --all --verbose
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
from collections.abc import (
    MutableMapping,
    MutableSequence,
)
from datetime import UTC, datetime
from pathlib import Path

import requests
from flext_api import FlextApiConstants

from flext_quality import c, m, t, u


class FlextQualityLinkValidator:
    """Advanced link validation and checking system."""

    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        max_workers: int = 5,
    ) -> None:
        """Initialize the link validator with timeout and retry settings."""
        super().__init__()
        self.timeout = timeout
        self.retries = retries
        self.max_workers = max_workers
        self.user_agent = "FLEXT-Quality-Link-Validator/1.0"
        self.results: m.Quality.LinkValidatorResults = m.Quality.LinkValidatorResults(
            timestamp=datetime.now(UTC).isoformat(),
        )

    def find_all_links(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> t.SequenceOf[m.Quality.LinkRecord]:
        """Extract all links from documentation files."""
        all_links: MutableSequence[m.Quality.LinkRecord] = []
        for file_path in doc_files:
            file_rel_path = str(file_path)
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(file_path.relative_to(file_path.parents[2]))
                link_pattern = "\\[([^\\]]+)\\]\\(([^)]+)\\)"
                matches = re.findall(link_pattern, content)
                for text, url in matches:
                    link_type = self._classify_link(url)
                    all_links.append(
                        m.Quality.LinkRecord(
                            text=text,
                            url=url,
                            type=link_type,
                            file=file_rel_path,
                            line_number=self._find_line_number(
                                content,
                                f"[{text}]({url})",
                            ),
                        ),
                    )
                html_link_pattern = (
                    "<a[^>]+href=[\"\\']([^\"\\']+)[\"\\'][^>]*>([^<]+)</a>"
                )
                html_matches = re.findall(html_link_pattern, content, re.IGNORECASE)
                for url, text in html_matches:
                    link_type = self._classify_link(url)
                    all_links.append(
                        m.Quality.LinkRecord(
                            text=text.strip(),
                            url=url,
                            type=link_type,
                            file=file_rel_path,
                            line_number=self._find_line_number(
                                content,
                                f'href="{url}"',
                            ),
                        ),
                    )
                image_pattern = "!\\[([^\\]]*)\\]\\(([^)]+)\\)"
                image_matches = re.findall(image_pattern, content)
                for alt_text, src in image_matches:
                    all_links.append(
                        m.Quality.LinkRecord(
                            text=alt_text,
                            url=src,
                            type="image",
                            file=file_rel_path,
                            line_number=self._find_line_number(
                                content,
                                f"![{alt_text}]({src})",
                            ),
                        ),
                    )
            except c.EXC_FS_DECODING as e:
                self.results.errors.append(
                    m.Quality.LinkCheckResult(
                        type="file_read_error",
                        file=file_rel_path,
                        error=str(e),
                    ),
                )
        return all_links

    def _classify_link(self, url: str) -> str:
        """Classify link type based on URL pattern."""
        match url:
            case _ if url.startswith(("http://", "https://")):
                return "external"
            case _ if url.startswith("mailto:"):
                return "email"
            case _ if url.startswith("#"):
                return "anchor"
            case _ if url.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
                return "image"
            case _ if url.startswith(("./", "../")) or url.endswith((".md", ".mdx")):
                return "internal"
            case _:
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
        links: t.SequenceOf[m.Quality.LinkRecord],
        *,
        verbose: bool = False,
    ) -> m.Quality.LinkValidatorResults:
        """Validate external links with concurrent checking."""
        external_links = [link for link in links if link.type == "external"]
        if not external_links:
            return self.results
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers,
        ) as executor:
            futures = [
                executor.submit(self._check_single_external_link, link, verbose=verbose)
                for link in external_links
            ]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self.results.links_checked += 1
                if result.valid:
                    self.results.valid_links += 1
                else:
                    self.results.broken_links += 1
                    self.results.errors.append(result)
        return self.results

    def _create_link_result(
        self,
        link: m.Quality.LinkRecord,
        *,
        valid: bool,
        url: str,
        status_code: int | None = None,
        error: str | None = None,
    ) -> m.Quality.LinkCheckResult:
        """Create a standardized link validation result."""
        return m.Quality.LinkCheckResult(
            valid=valid,
            url=url,
            file=link.file,
            line=link.line_number,
            status_code=status_code,
            error=error,
        )

    def _make_http_request(
        self, url: str, method: str = FlextApiConstants.Api.METHOD_LITERALS_HEAD_LOWER
    ) -> requests.Response:
        """Make an HTTP request with appropriate headers."""
        headers = {"User-Agent": self.user_agent}
        if method == FlextApiConstants.Api.METHOD_LITERALS_HEAD_LOWER:
            headers["Accept"] = "*/*"
        request_func = (
            requests.head
            if method == FlextApiConstants.Api.METHOD_LITERALS_HEAD_LOWER
            else requests.get
        )
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
    ) -> tuple[bool, t.HeaderMapping | None]:
        """Handle a single request attempt."""
        result: tuple[bool, t.HeaderMapping | None] = (False, None)
        try:
            response = self._make_http_request(url)
            if response.status_code < 400:
                result = (True, {"status_code": response.status_code})
            elif self._should_retry_with_get(response.status_code):
                response = self._make_http_request(url, "get")
                if response.status_code < 400:
                    result = (True, {"status_code": response.status_code})
                else:
                    result = (
                        False,
                        {
                            "status_code": response.status_code,
                            "error": f"HTTP {response.status_code}",
                        },
                    )
            else:
                result = (
                    False,
                    {
                        "status_code": response.status_code,
                        "error": f"HTTP {response.status_code}",
                    },
                )
        except requests.exceptions.Timeout:
            if attempt == self.retries - 1:
                result = (False, {"error": f"Timeout after {self.timeout}s"})
        except requests.exceptions.RequestException as e:
            if attempt == self.retries - 1:
                result = (False, {"error": str(e)})
        except c.EXC_OS_RUNTIME_VALUE as e:
            result = (False, {"error": f"Unexpected error: {e!s}"})
        return result

    def _check_single_external_link(
        self,
        link: m.Quality.LinkRecord,
        *,
        verbose: bool = False,
    ) -> m.Quality.LinkCheckResult:
        """Check a single external link."""
        _ = verbose
        url = link.url
        for attempt in range(self.retries):
            success, result = self._handle_request_attempt(url, attempt)
            if result is not None:
                raw_status = result.get("status_code")
                raw_error = result.get("error")
                return self._create_link_result(
                    link,
                    valid=success,
                    url=url,
                    status_code=raw_status if isinstance(raw_status, int) else None,
                    error=raw_error if isinstance(raw_error, str) else None,
                )
        return self._create_link_result(
            link,
            valid=False,
            url=url,
            error="Max retries exceeded",
        )

    def validate_internal_links(
        self,
        links: t.SequenceOf[m.Quality.LinkRecord],
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.LinkValidatorResults:
        """Validate internal links and references."""
        internal_links = [
            link for link in links if link.type in {"internal", "reference"}
        ]
        doc_file_names = {str(f.relative_to(f.parents[2])) for f in doc_files}
        for link in internal_links:
            target = link.url.split("#")[0]
            if not target:
                continue
            if target not in doc_file_names:
                link_file_dir = Path(link.file).parent
                potential_targets = [
                    link_file_dir / target,
                    Path(target),
                    self._resolve_relative_path(link_file_dir, target),
                ]
                target_exists = False
                for potential_target in potential_targets:
                    resolved_path = (
                        Path(link.file).parent.parent.parent / potential_target
                    )
                    if resolved_path.exists() and resolved_path.suffix in {
                        ".md",
                        ".mdx",
                    }:
                        target_exists = True
                        break
                if not target_exists:
                    self.results.errors.append(
                        m.Quality.LinkCheckResult(
                            type="broken_internal_link",
                            url=link.url,
                            target=target,
                            file=link.file,
                            line=link.line_number,
                            error="Target file not found",
                        ),
                    )
                    self.results.broken_links += 1
                else:
                    self.results.valid_links += 1
            else:
                self.results.valid_links += 1
            self.results.links_checked += 1
        return self.results

    def _resolve_relative_path(self, base_dir: Path, target: str) -> Path:
        """Resolve relative path from base directory."""
        if target.startswith("./"):
            return base_dir / target[2:]
        if target.startswith("../"):
            return base_dir.parent / target[3:]
        return Path(target)

    def validate_images(
        self,
        links: t.SequenceOf[m.Quality.LinkRecord],
        project_root: Path,
    ) -> m.Quality.LinkValidatorResults:
        """Validate image references."""
        images = [link for link in links if link.type == "image"]
        for image in images:
            src = image.url
            if src.startswith(("http://", "https://")):
                self.results.valid_links += 1
                continue
            image_path = Path(src)
            if not image_path.is_absolute():
                file_dir = Path(image.file).parent
                full_path = (project_root / file_dir / image_path).resolve()
            else:
                full_path = image_path
            if full_path.exists():
                self.results.valid_links += 1
            else:
                self.results.errors.append(
                    m.Quality.LinkCheckResult(
                        type="missing_image",
                        src=src,
                        file=image.file,
                        line=image.line_number,
                        error=f"Image file not found: {full_path}",
                    ),
                )
                self.results.broken_links += 1
            self.results.links_checked += 1
        return self.results

    def validate_anchors(
        self,
        links: t.SequenceOf[m.Quality.LinkRecord],
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.LinkValidatorResults:
        """Validate anchor links within documents."""
        anchor_links = [link for link in links if link.type == "anchor"]
        file_anchors: MutableMapping[str, set[str]] = {}
        for file_path in doc_files:
            file_rel_path = str(file_path)
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(file_path.relative_to(file_path.parents[2]))
                headings = re.findall(r"^#{1,6}\\s+(.+)$", content, re.MULTILINE)
                anchors = [self._heading_to_anchor(heading) for heading in headings]
                explicit_anchors = re.findall(
                    r"<a[^>]+id=[\"\\']([^\"\\']+)[\"\\'][^>]*>",
                    content,
                )
                anchors.extend(explicit_anchors)
                file_anchors[file_rel_path] = set(anchors)
            except c.EXC_FS_DECODING as e:
                self.results.warnings_list.append(
                    m.Quality.LinkCheckResult(
                        type="anchor_index_error",
                        file=file_rel_path,
                        warning=f"Could not build anchor index: {e!s}",
                    ),
                )
        for link in anchor_links:
            anchor = link.url[1:]
            link_file = link.file
            if link_file in file_anchors and anchor in file_anchors[link_file]:
                self.results.valid_links += 1
            else:
                self.results.errors.append(
                    m.Quality.LinkCheckResult(
                        type="broken_anchor",
                        anchor=anchor,
                        file=link_file,
                        line=link.line_number,
                        error=f"Anchor '{anchor}' not found in {link_file}",
                    ),
                )
                self.results.broken_links += 1
            self.results.links_checked += 1
        return self.results

    def _heading_to_anchor(self, heading: str) -> str:
        """Convert heading text to anchor format."""
        anchor = heading.lower()
        anchor = re.sub(r"[^\\w\\s-]", "", anchor)
        return re.sub(r"\\s+", "-", anchor)

    def check_link_text_quality(
        self,
        links: t.SequenceOf[m.Quality.LinkRecord],
    ) -> m.Quality.LinkValidatorResults:
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
            text = link.text.lower().strip()
            if text in poor_link_texts or len(text) < 3:
                self.results.warnings_list.append(
                    m.Quality.LinkCheckResult(
                        type="poor_link_text",
                        text=link.text,
                        url=link.url,
                        file=link.file,
                        line=link.line_number,
                        warning="Link text is not descriptive enough for accessibility",
                    ),
                )
                self.results.warnings += 1
        return self.results

    def generate_report(self, report_format: str = "json") -> str:
        """Generate validation report."""
        report_text: str = (
            self.results.model_dump_json(indent=2)
            if report_format == "json"
            else self.results.model_dump_json()
        )
        return report_text

    def save_report(self, output_path: str = "docs/maintenance/reports/") -> Path:
        """Save validation report."""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"validation_report_{timestamp}.json"
        filepath = output_dir / filename
        report_content = self.generate_report("json")
        _ = filepath.write_text(report_content, encoding="utf-8")
        latest_file = output_dir / "latest_validation.json"
        latest_file.write_text(self.results.model_dump_json(indent=2), encoding="utf-8")
        return filepath


class FlextQualityContentValidator:
    """Content validation and quality checking system."""

    def __init__(self) -> None:
        """Initialize the content validator."""
        super().__init__()
        self.results: m.Quality.ContentValidatorResults = (
            m.Quality.ContentValidatorResults(
                timestamp=datetime.now(UTC).isoformat(),
            )
        )

    def validate_markdown_syntax(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.ContentValidatorResults:
        """Validate markdown syntax and formatting."""
        for file_path in doc_files:
            file_rel_path = str(file_path)
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(file_path.relative_to(file_path.parents[2]))
                issues = self._check_markdown_issues(content)
                if issues:
                    self.results.content_issues.extend([
                        issue.model_copy(update={"file": file_rel_path})
                        for issue in issues
                    ])
                self.results.files_checked += 1
            except c.EXC_FS_DECODING as e:
                self.results.content_issues.append(
                    m.Quality.ContentIssue(
                        type="syntax_validation_error",
                        file=file_rel_path,
                        error=str(e),
                    ),
                )
        return self.results

    def _check_markdown_issues(
        self, content: str
    ) -> t.SequenceOf[m.Quality.ContentIssue]:
        """Check for markdown syntax issues."""
        issues: MutableSequence[m.Quality.ContentIssue] = []
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if "[" in line and "]" in line and ("(" in line) and (")" not in line):
                issues.append(
                    m.Quality.ContentIssue(
                        type="broken_link_syntax",
                        line=i,
                        content=line.strip(),
                        error="Unclosed link syntax",
                    ),
                )
            if "![" in line and "]" in line and ("(" in line) and (")" not in line):
                issues.append(
                    m.Quality.ContentIssue(
                        type="broken_image_syntax",
                        line=i,
                        content=line.strip(),
                        error="Unclosed image syntax",
                    ),
                )
            line.strip().startswith(("- ", "* ", "+ "))
            if line.rstrip() != line:
                issues.append(
                    m.Quality.ContentIssue(
                        type="trailing_spaces",
                        line=i,
                        content=line,
                        error="Line has trailing spaces",
                    ),
                )
        return issues

    def check_content_quality(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.ContentValidatorResults:
        """Check content quality metrics."""
        for file_path in doc_files:
            file_rel_path = str(file_path)
            try:
                content = file_path.read_text(encoding="utf-8")
                file_rel_path = str(file_path.relative_to(file_path.parents[2]))
                metrics = self._calculate_content_metrics(content)
                if metrics.word_count < 50:
                    self.results.content_issues.append(
                        m.Quality.ContentIssue(
                            type="insufficient_content",
                            file=file_rel_path,
                            word_count=metrics.word_count,
                            warning="Document appears to be too short",
                        ),
                    )
                if metrics.readability_score < 60:
                    self.results.content_issues.append(
                        m.Quality.ContentIssue(
                            type="readability_issue",
                            file=file_rel_path,
                            readability_score=metrics.readability_score,
                            warning="Content may be difficult to read",
                        ),
                    )
                self.results.files_checked += 1
            except c.EXC_FS_DECODING as e:
                self.results.content_issues.append(
                    m.Quality.ContentIssue(
                        type="quality_analysis_error",
                        file=file_rel_path,
                        error=str(e),
                    ),
                )
        return self.results

    def _calculate_content_metrics(self, content: str) -> m.Quality.ContentMetrics:
        """Calculate basic content quality metrics."""
        words = re.findall(r"\\b\\w+\\b", content)
        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]
        avg_words_per_sentence: float = 0.0
        if sentences:
            avg_words_per_sentence = len(words) / len(sentences)
            readability_score = max(
                0.0,
                min(100.0, 100.0 - (avg_words_per_sentence - 15) * 2),
            )
        else:
            readability_score = 0.0
        return m.Quality.ContentMetrics(
            word_count=len(words),
            sentence_count=len(sentences),
            avg_words_per_sentence=avg_words_per_sentence,
            readability_score=readability_score,
            has_code_blocks="```" in content,
            has_lists=bool(re.search(r"^[\\s]*[-\\*\\+]", content, re.MULTILINE)),
            has_headers=bool(re.search(r"^#{1,6}\\s", content, re.MULTILINE)),
        )


def _discover_validation_files() -> t.SequenceOf[Path]:
    """Discover documentation files for validation."""
    project_root = Path(__file__).parent.parent.parent.parent
    doc_files: MutableSequence[Path] = []
    for pattern in [
        "**/*.md",
        "**/*.mdx",
        "**/README*",
        "**/docs/**/*.md",
        "**/docs/**/*.mdx",
    ]:
        doc_files.extend(project_root.glob(pattern))
    seen: set[Path] = set()
    unique: MutableSequence[Path] = []
    for f in doc_files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    ignored_patterns = [".git", "__pycache__", "node_modules", ".serena/memories"]
    return [
        f for f in unique if not any(pattern in str(f) for pattern in ignored_patterns)
    ]


def _execute_validations(
    link_validator: FlextQualityLinkValidator,
    content_validator: FlextQualityContentValidator,
    all_links: t.SequenceOf[m.Quality.LinkRecord],
    doc_files: t.SequenceOf[Path],
    args: argparse.Namespace,
) -> bool:
    """Execute the requested validations and return if any were run."""
    run_any_check = False
    if args.external_links or args.all:
        _ = link_validator.validate_external_links(all_links, verbose=args.verbose)
        run_any_check = True
    if args.internal_links or args.all:
        _ = link_validator.validate_internal_links(all_links, doc_files)
        run_any_check = True
    if args.images or args.all:
        project_root = Path(__file__).parent.parent.parent.parent
        _ = link_validator.validate_images(all_links, project_root)
        run_any_check = True
    if args.anchors or args.all:
        _ = link_validator.validate_anchors(all_links, doc_files)
        run_any_check = True
    if args.link_text or args.all:
        _ = link_validator.check_link_text_quality(all_links)
        run_any_check = True
    if args.markdown_syntax or args.all:
        _ = content_validator.validate_markdown_syntax(doc_files)
        run_any_check = True
    if args.content_quality or args.all:
        _ = content_validator.check_content_quality(doc_files)
        run_any_check = True
    return run_any_check


def main() -> None:
    """Main entry point for documentation validation."""
    parser = u.Quality.build_argument_parser(
        m.Quality.ArgumentParserSpec(
            description="FLEXT Quality Documentation Validation",
            options=[
                m.Quality.ArgumentOptionSpec(
                    flags=("--external-links",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Validate external links",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--internal-links",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Validate internal links",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--images",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Validate image references",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--anchors",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Validate anchor links",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--link-text",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Check link text quality",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--markdown-syntax",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Validate markdown syntax",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--content-quality",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Analyze content quality",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--all",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Run all validation checks",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--verbose",),
                    action=c.Quality.ArgumentAction.STORE_TRUE,
                    help="Verbose output",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--output",),
                    default=c.Quality.PATHS_DOCS_MAINTENANCE_REPORTS_DIR,
                    value_type=c.Quality.ArgumentValueType.STRING,
                    help="Output directory for reports",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--timeout",),
                    default=10,
                    value_type=c.Quality.ArgumentValueType.INTEGER,
                    help="Timeout for external link checks",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--retries",),
                    default=3,
                    value_type=c.Quality.ArgumentValueType.INTEGER,
                    help="Retry attempts for external links",
                ),
                m.Quality.ArgumentOptionSpec(
                    flags=("--workers",),
                    default=5,
                    value_type=c.Quality.ArgumentValueType.INTEGER,
                    help="Max concurrent workers",
                ),
            ],
        )
    )
    args = parser.parse_args()
    doc_files = _discover_validation_files()
    link_validator = FlextQualityLinkValidator(
        timeout=args.timeout,
        retries=args.retries,
        max_workers=args.workers,
    )
    content_validator = FlextQualityContentValidator()
    all_links = link_validator.find_all_links(doc_files)
    run_any_check = _execute_validations(
        link_validator,
        content_validator,
        all_links,
        doc_files,
        args,
    )
    if not run_any_check:
        raise SystemExit(1)
    link_errors = link_validator.results.errors
    content_issues = content_validator.results.content_issues
    total_errors = len(link_errors) + len(content_issues)
    _ = link_validator.save_report(args.output)
    if total_errors > 0:
        raise SystemExit(1)
