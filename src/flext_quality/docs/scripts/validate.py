"""FLEXT Quality documentation validation command."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Final, override

import anyio

from flext_cli import cli
from flext_quality import c, m, p, r, s, t, u
from flext_quality.docs.tools.link_checker import FlextQualityLinkChecker

if TYPE_CHECKING:
    from collections.abc import MutableSequence

_MIN_WORD_COUNT: Final[int] = 50
_MIN_READABILITY_SCORE: Final[int] = 60
_VALIDATION_CONFIG = (
    Path(__file__).resolve().parent.parent / "config" / "validation_config.yaml"
)


def _link_defaults() -> FlextQualityLinkChecker.LinkConfig:
    return FlextQualityLinkChecker().settings


def _max_workers_default() -> int:
    loaded = u.Cli.yaml_load_mapping(_VALIDATION_CONFIG)
    validation = t.json_mapping_adapter().validate_python(loaded["validation"])
    return t.TypeAdapter(int).validate_python(validation["max_concurrent_requests"])


class FlextQualityDocumentationValidator:
    """Coordinate public link and content validators through one CLI surface."""

    class ContentValidator:
        """Validate Markdown syntax and content quality."""

        def __init__(self) -> None:
            """Initialize accumulated content-validation results."""
            self.results = m.Quality.ContentValidatorResults(
                timestamp=u.now().isoformat()
            )

        def validate_markdown_syntax(
            self, doc_files: t.SequenceOf[Path]
        ) -> m.Quality.ContentValidatorResults:
            """Validate Markdown syntax for the selected documents."""
            for file_path in doc_files:
                read = u.Cli.files_read_text(file_path)
                if read.failure:
                    self.results.content_issues.append(
                        m.Quality.ContentIssue(
                            type="syntax_validation_error",
                            file=str(file_path),
                            error=read.error,
                        )
                    )
                    continue
                issues = self._check_markdown_issues(read.value)
                self.results.content_issues.extend(
                    issue.model_copy(update={"file": str(file_path)})
                    for issue in issues
                )
                self.results.files_checked += 1
            return self.results

        def _check_markdown_issues(
            self, content: str
        ) -> t.SequenceOf[m.Quality.ContentIssue]:
            issues: MutableSequence[m.Quality.ContentIssue] = []
            for line_number, line in enumerate(content.splitlines(), 1):
                if "[" in line and "]" in line and "(" in line and ")" not in line:
                    issues.append(
                        m.Quality.ContentIssue(
                            type="broken_link_syntax",
                            line=line_number,
                            content=line.strip(),
                            error="Unclosed link syntax",
                        )
                    )
                if line.rstrip() != line:
                    issues.append(
                        m.Quality.ContentIssue(
                            type="trailing_spaces",
                            line=line_number,
                            content=line,
                            error="Line has trailing spaces",
                        )
                    )
            return issues

        def check_content_quality(
            self, doc_files: t.SequenceOf[Path]
        ) -> m.Quality.ContentValidatorResults:
            """Measure content quality for the selected documents."""
            for file_path in doc_files:
                read = u.Cli.files_read_text(file_path)
                if read.failure:
                    self.results.content_issues.append(
                        m.Quality.ContentIssue(
                            type="quality_analysis_error",
                            file=str(file_path),
                            error=read.error,
                        )
                    )
                    continue
                metrics = self._calculate_content_metrics(read.value)
                if metrics.word_count < _MIN_WORD_COUNT:
                    self.results.content_issues.append(
                        m.Quality.ContentIssue(
                            type="insufficient_content",
                            file=str(file_path),
                            word_count=metrics.word_count,
                            warning="Document appears to be too short",
                        )
                    )
                if metrics.readability_score < _MIN_READABILITY_SCORE:
                    self.results.content_issues.append(
                        m.Quality.ContentIssue(
                            type="readability_issue",
                            file=str(file_path),
                            readability_score=metrics.readability_score,
                            warning="Content may be difficult to read",
                        )
                    )
                self.results.files_checked += 1
            return self.results

        def _calculate_content_metrics(self, content: str) -> m.Quality.ContentMetrics:
            words = u.Quality.compile_pattern(r"\b\w+\b").findall(content)
            sentences = [
                sentence.strip()
                for sentence in u.Quality.compile_pattern(r"[.!?]+").split(content)
                if sentence.strip()
            ]
            average = len(words) / len(sentences) if sentences else 0.0
            readability = max(0.0, min(100.0, 100.0 - (average - 15) * 2))
            return m.Quality.ContentMetrics(
                word_count=len(words),
                sentence_count=len(sentences),
                avg_words_per_sentence=average,
                readability_score=readability,
                has_code_blocks="```" in content,
                has_lists=bool(
                    u.Quality.compile_pattern(r"^[\s]*[-*+]", multiline=True).search(
                        content
                    )
                ),
                has_headers=bool(
                    u.Quality.compile_pattern(r"^#{1,6}\s", multiline=True).search(
                        content
                    )
                ),
            )

    @staticmethod
    def discover_validation_files() -> t.SequenceOf[Path]:
        """Discover Markdown files under the package project root."""
        project_root = Path(__file__).parent.parent.parent.parent
        files = [
            path
            for pattern in ("**/*.md", "**/*.mdx", "**/README*")
            for path in project_root.glob(pattern)
        ]
        return sorted({
            path
            for path in files
            if not any(
                ignored in str(path)
                for ignored in (".git", "__pycache__", "node_modules")
            )
        })

    class Run(s[bool]):
        """CLI command for documentation validation."""

        external_links: bool = u.Field(
            False, description="Validate external links", validate_default=True
        )
        internal_links: bool = u.Field(
            False, description="Validate internal links", validate_default=True
        )
        images: bool = u.Field(
            False, description="Validate image references", validate_default=True
        )
        anchors: bool = u.Field(
            False, description="Validate anchor links", validate_default=True
        )
        link_text: bool = u.Field(
            False, description="Check link text quality", validate_default=True
        )
        markdown_syntax: bool = u.Field(
            False, description="Validate Markdown syntax", validate_default=True
        )
        content_quality: bool = u.Field(
            False, description="Check content quality", validate_default=True
        )
        all: bool = u.Field(
            False, description="Run all validation checks", validate_default=True
        )
        verbose: bool = u.Field(
            False, description="Enable verbose output", validate_default=True
        )
        output: str = u.Field(
            c.Quality.PATHS_DOCS_MAINTENANCE_REPORTS_DIR,
            description="Validation report output directory",
            validate_default=True,
        )
        timeout: int = u.Field(
            default_factory=lambda: _link_defaults().external_timeout,
            description="External request timeout",
        )
        retries: int = u.Field(
            default_factory=lambda: _link_defaults().retry_attempts,
            description="External request retries",
        )
        workers: int = u.Field(
            default_factory=_max_workers_default, description="Concurrent link workers"
        )

        @override
        def execute(self) -> p.Result[bool]:
            doc_files = FlextQualityDocumentationValidator.discover_validation_files()
            checker = FlextQualityLinkChecker()
            checker.settings = checker.settings.model_copy(
                update={
                    "external_timeout": self.timeout,
                    "retry_attempts": self.retries,
                }
            )
            links = checker.find_all_links(doc_files)
            selected_links = [
                link
                for link in links
                if self.all
                or (self.external_links and link.type == "external")
                or (self.internal_links and link.type == "internal")
                or (self.images and link.type == "image")
                or (self.anchors and link.type == "anchor")
            ]
            run_any = bool(selected_links) or self.link_text
            if selected_links:
                anyio.run(checker.validate_links, selected_links)
            if self.link_text or self.all:
                checker.check_link_text_quality(links)
                run_any = True
            content_validator = FlextQualityDocumentationValidator.ContentValidator()
            if self.markdown_syntax or self.all:
                content_validator.validate_markdown_syntax(doc_files)
                run_any = True
            if self.content_quality or self.all:
                content_validator.check_content_quality(doc_files)
                run_any = True
            if not run_any:
                return r[bool].fail("No validation selected")
            checker.save_report(self.output)
            total_errors = checker.results.broken_links + len(
                content_validator.results.content_issues
            )
            if total_errors:
                return r[bool].fail(f"Validation found {total_errors} errors")
            return r[bool].ok(value=True)

    @staticmethod
    def main(args: t.StrSequence | None = None) -> int:
        """Run documentation validation through the public CLI facade."""
        return u.Quality.execute_result_command(
            args=args,
            app_name="flext-quality-docs-validate",
            app_help="FLEXT Quality Documentation Validation",
            route=m.Cli.ResultCommandRoute(
                name="run",
                help_text="Run documentation validation checks",
                model_cls=FlextQualityDocumentationValidator.Run,
                handler=lambda params: params.execute(),
            ),
        )


if __name__ == "__main__":
    cli.exit(FlextQualityDocumentationValidator.main())
