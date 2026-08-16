"""FLEXT Quality Link Validation Tool.

Advanced link checking utility with retry logic, rate limiting,
and comprehensive validation capabilities.
"""

from __future__ import annotations

import anyio
import pathlib
import time
from collections.abc import Mapping, MutableSequence
from typing import ClassVar
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

from aiohttp import ClientError, ClientSession, ClientTimeout

from flext_quality import c, m, p, t, u

_VALIDATION_CONFIG_PATH = (
    pathlib.Path(__file__).resolve().parent.parent / "config" / "validation_config.yaml"
)


class FlextQualityLinkChecker:
    """Advanced link validation and checking system."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    class LinkConfig(m.BaseModel):
        """Configuration dictionary for link validation."""

        external_timeout: int
        retry_attempts: int
        user_agent: str
        follow_redirects: bool
        max_redirects: int
        acceptable_status_codes: t.SequenceOf[int]

    class LinkInfo(m.BaseModel):
        """Link information dictionary."""

        url: str
        text: str
        type: str
        file: str
        line: int | None = None
        reference: str | None = None
        context: t.JsonMapping | None = None

    class LinkResult(m.BaseModel):
        """Link check result dictionary."""

        url: str
        valid: bool
        context: t.JsonMapping
        status_code: int | None = None
        response_time: float | None = None
        redirected: bool | None = None
        final_url: str | None = None
        content_type: str | None = None
        error: str | None = None

    class PerformanceMetrics(m.BaseModel):
        """Performance metrics dictionary."""

        total_time: float
        average_response_time: float
        slowest_response: float

    class Results(m.BaseModel):
        """Results dictionary."""

        total_links: int
        valid_links: int
        broken_links: int
        warnings: int
        errors: MutableSequence[FlextQualityLinkChecker.LinkResult]
        warnings_list: MutableSequence[t.JsonMapping]
        performance: FlextQualityLinkChecker.PerformanceMetrics

    def __init__(self, config_path: str | None = str(_VALIDATION_CONFIG_PATH)) -> None:
        """Initialize the link checker with configuration."""
        self.settings: FlextQualityLinkChecker.LinkConfig
        self.load_config(config_path)
        self.session: ClientSession | None = None
        self.cache: t.MutableJsonMapping = {}
        self.results: FlextQualityLinkChecker.Results = FlextQualityLinkChecker.Results(
            total_links=0,
            valid_links=0,
            broken_links=0,
            warnings=0,
            errors=[],
            warnings_list=[],
            performance=FlextQualityLinkChecker.PerformanceMetrics(
                total_time=0.0, average_response_time=0.0, slowest_response=0.0
            ),
        )

    def load_config(self, config_path: str | None) -> None:
        """Load validation configuration."""
        resolved_path = (
            pathlib.Path(config_path) if config_path else _VALIDATION_CONFIG_PATH
        )
        loaded = u.Cli.yaml_load_mapping(resolved_path)
        validation = t.json_mapping_adapter().validate_python(loaded["validation"])
        link_validation = t.json_mapping_adapter().validate_python(
            loaded["link_validation"]
        )
        self.settings = FlextQualityLinkChecker.LinkConfig.model_validate({
            "external_timeout": link_validation["timeout"],
            "retry_attempts": validation["retry_attempts"],
            "user_agent": link_validation["user_agent"],
            "follow_redirects": link_validation["follow_redirects"],
            "max_redirects": link_validation["max_redirects"],
            "acceptable_status_codes": link_validation["acceptable_status_codes"],
        })

    def find_all_links(
        self, file_paths: t.SequenceOf[pathlib.Path]
    ) -> t.SequenceOf[FlextQualityLinkChecker.LinkInfo]:
        """Extract all links from the given files."""
        all_links: MutableSequence[FlextQualityLinkChecker.LinkInfo] = []

        for file_path in file_paths:
            read = u.Cli.files_read_text(file_path)
            if read.failure:
                self.logger.warning(
                    "failed_to_extract_links",
                    file_path=str(file_path),
                    error=read.error,
                )
                continue
            content = read.value
            md_links = u.Quality.compile_pattern(r"\[([^\]]+)\]\(([^)]+)\)").findall(
                content
            )
            for text, url in md_links:
                link_type = self._classify_link(url)
                link_info = FlextQualityLinkChecker.LinkInfo(
                    url=url,
                    text=text,
                    type=link_type,
                    file=str(file_path),
                    line=content.count("\n", 0, content.find(f"[{text}]({url})")) + 1,
                )
                all_links.append(link_info)

            ref_links = u.Quality.compile_pattern(r"\[([^\]]+)\]\[([^\]]+)\]").findall(
                content
            )
            ref_defs = u.Quality.compile_pattern(r"\[([^\]]+)\]:\s*([^\s]+)").findall(
                content
            )

            ref_dict: t.StrMapping = dict(ref_defs)
            for text, ref in ref_links:
                if ref in ref_dict:
                    url = ref_dict[ref]
                    link_type = self._classify_link(url)
                    link_info = FlextQualityLinkChecker.LinkInfo(
                        url=url,
                        text=text,
                        type=link_type,
                        file=str(file_path),
                        reference=ref,
                    )
                    all_links.append(link_info)

        return all_links

    def check_link_text_quality(
        self, links: t.SequenceOf[FlextQualityLinkChecker.LinkInfo]
    ) -> FlextQualityLinkChecker.Results:
        """Record accessibility warnings for generic link labels."""
        generic_text = {"here", "click here", "link", "read more"}
        for link in links:
            if link.text.strip().lower() in generic_text:
                self.results.warnings += 1
                self.results.warnings_list.append({
                    "type": "poor_link_text",
                    "url": link.url,
                    "message": link.text,
                })
        return self.results

    def _classify_link(self, url: str) -> str:
        """Classify link type based on URL."""
        if url.startswith(("http://", "https://")):
            return "external"
        if url.startswith("#"):
            return "anchor"
        if url.startswith(("mailto:", "tel:")):
            return "contact"
        if url.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            return "image"
        return "internal"

    async def check_link_async(
        self, url: str, context: t.JsonMapping | None = None
    ) -> FlextQualityLinkChecker.LinkResult:
        """Asynchronously check a single link."""
        start_time = time.time()

        try:
            return await self._check_link_async_unchecked(url, start_time, context)

        except TimeoutError:
            return FlextQualityLinkChecker.LinkResult(
                url=url,
                error="timeout",
                response_time=self.settings.external_timeout,
                valid=False,
                context=context or {},
            )
        except ClientError as e:
            return FlextQualityLinkChecker.LinkResult(
                url=url,
                error=str(e),
                response_time=time.time() - start_time,
                valid=False,
                context=context or {},
            )
        except OSError as e:
            return FlextQualityLinkChecker.LinkResult(
                url=url,
                error=f"unexpected_error: {e!s}",
                response_time=time.time() - start_time,
                valid=False,
                context=context or {},
            )

    async def _check_link_async_unchecked(
        self, url: str, start_time: float, context: t.JsonMapping | None
    ) -> FlextQualityLinkChecker.LinkResult:
        """Check an async link while allowing transport exceptions to propagate."""
        if self.session is None:
            return FlextQualityLinkChecker.LinkResult(
                url=url,
                error="session_not_initialized",
                valid=False,
                context=context or {},
            )

        async with self.session.head(
            url,
            timeout=ClientTimeout(total=self.settings.external_timeout),
            allow_redirects=self.settings.follow_redirects,
            max_redirects=self.settings.max_redirects,
            headers={"User-Agent": self.settings.user_agent},
        ) as response:
            response_time = time.time() - start_time
            result = FlextQualityLinkChecker.LinkResult(
                url=url,
                status_code=response.status,
                response_time=response_time,
                valid=response.status in self.settings.acceptable_status_codes,
                redirected=bool(response.history),
                final_url=str(response.url),
                content_type=response.headers.get("content-type", ""),
                context=context or {},
            )
            self.results.performance.slowest_response = max(
                self.results.performance.slowest_response, response_time
            )
            return result

    async def check_links_batch_async(
        self, links: t.SequenceOf[FlextQualityLinkChecker.LinkInfo]
    ) -> t.SequenceOf[FlextQualityLinkChecker.LinkResult]:
        """Check multiple links asynchronously."""
        start_time = time.time()

        processed_results = [
            await self.check_link_async(link.url, link.context) for link in links
        ]

        self.results.performance.total_time = time.time() - start_time

        valid_times: t.SequenceOf[float] = [
            r.response_time
            for r in processed_results
            if r.response_time is not None and r.valid
        ]

        if valid_times:
            self.results.performance.average_response_time = sum(valid_times) / len(
                valid_times
            )

        return processed_results

    async def validate_links(
        self, links: t.SequenceOf[FlextQualityLinkChecker.LinkInfo]
    ) -> FlextQualityLinkChecker.Results:
        """Validate all provided links."""
        self.results.total_links = len(links)

        async with ClientSession() as session:
            self.session = session
            results = await self.check_links_batch_async(links)

        # Process results
        for result in results:
            if result.valid:
                self.results.valid_links += 1
            else:
                self.results.broken_links += 1
                self.results.errors.append(result)

                # Add warnings for specific cases
                if result.error == "timeout":
                    self.results.warnings += 1
                    self.results.warnings_list.append({
                        "type": "slow_response",
                        "url": result.url,
                        "message": f"Link timed out after {self.settings.external_timeout}s",
                    })

        return self.results

    def check_robots_txt(self, domain: str) -> bool:
        """Check if crawling is allowed by robots.txt."""
        try:
            rp = RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            rp.read()

            return rp.can_fetch(self.settings.user_agent, "/")
        except (OSError, ConnectionError, TimeoutError, UnicodeDecodeError):
            # If robots.txt can't be read, assume crawling is allowed
            return True

    def validate_github_links(
        self, links: t.SequenceOf[t.JsonMapping]
    ) -> t.SequenceOf[t.JsonMapping]:
        """Perform special validation for GitHub links."""
        github_links: t.SequenceOf[t.JsonMapping] = [
            link
            for link in links
            if isinstance(link.get("url"), str) and "github.com" in str(link.get("url"))
        ]

        validated_links: t.SequenceOf[Mapping[str, bool | t.JsonValue]] = [
            {**link, "valid": True, "github_validated": True}
            if self._validate_github_url_structure(str(link.get("url")))
            else {**link, "valid": False, "error": "invalid_github_url_structure"}
            for link in github_links
            if isinstance(link.get("url"), str)
        ]

        return validated_links

    def _validate_github_url_structure(self, url: str) -> bool:
        """Validate GitHub URL structure without making requests."""
        parsed = urlparse(url)

        if parsed.netloc != "github.com":
            return False

        path_parts = parsed.path.strip("/").split("/")

        # Basic GitHub URL patterns
        if len(path_parts) >= c.Quality.LINK_CHECKER_MIN_PATH_PARTS_FOR_REPO:
            # user/repo or user/repo/tree/branch or user/repo/blob/branch/file
            if path_parts[1] in {"tree", "blob", "pull", "issues", "wiki", "releases"}:
                min_detailed_parts: int = (
                    c.Quality.LINK_CHECKER_MIN_PATH_PARTS_FOR_DETAILED_REPO
                )
                return len(path_parts) >= min_detailed_parts
            if path_parts[1] in {"pulls", "issues", "wikis", "releases"}:
                return True
            # Assume it's a valid repo reference
            return True

        return False

    def generate_report(self, report_format: str = "json") -> str:
        """Generate validation report."""
        if report_format == "summary":
            return self._generate_summary_report()
        adapter = m.TypeAdapter(FlextQualityLinkChecker.Results)
        report_text: str = (
            adapter.dump_json(self.results, indent=2).decode()
            if report_format == "json"
            else adapter.dump_json(self.results).decode()
        )
        return report_text

    def _generate_summary_report(self) -> str:
        """Generate a human-readable summary report."""
        r = self.results

        report = f"""
Link Validation Summary Report
==============================

Total Links Checked: {r.total_links}
Valid Links: {r.valid_links}
Broken Links: {r.broken_links}
Warnings: {r.warnings}

Performance Metrics:
- Total Time: {r.performance.total_time:.2f}s
- Average Response Time: {r.performance.average_response_time:.2f}s
- Slowest Response: {r.performance.slowest_response:.2f}s

Broken Links:
"""

        for error in r.errors[: c.Quality.THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW]:
            url = error.url
            status = error.status_code or "N/A"
            error_msg = error.error or "Unknown error"
            report += f"- {url} (Status: {status}, Error: {error_msg})\n"

        if len(r.errors) > c.Quality.THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW:
            remaining_links = (
                len(r.errors) - c.Quality.THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW
            )
            report += f"... and {remaining_links} more broken links\n"

        if r.warnings_list:
            report += "\nWarnings:\n"
            for warning in r.warnings_list[:5]:
                report += f"- {warning['url']}: {warning['message']}\n"

        return report

    def save_report(
        self, output_path: str = c.Quality.PATHS_DOCS_MAINTENANCE_REPORTS_DIR
    ) -> pathlib.Path:
        """Save validation report."""
        timestamp = u.now().strftime("%Y%m%d_%H%M%S")
        filename = f"link_validation_{timestamp}.json"
        filepath = pathlib.Path(output_path) / filename
        _ = u.Cli.json_write(
            filepath, self.results, options=m.Cli.JsonWriteOptions(indent=2)
        ).unwrap()
        return filepath

    @staticmethod
    async def run_demo() -> None:
        """Run the example validation without leaking module-level test data."""
        test_links: t.SequenceOf[FlextQualityLinkChecker.LinkInfo] = [
            FlextQualityLinkChecker.LinkInfo(
                url="https://github.com/microsoft/vscode",
                text="VSCode",
                type="external",
                file="README.md",
                context={"file": "README.md"},
            ),
            FlextQualityLinkChecker.LinkInfo(
                url="https://httpbin.org/status/200",
                text="httpbin",
                type="external",
                file="docs/setup.md",
                context={"file": "docs/setup.md"},
            ),
            FlextQualityLinkChecker.LinkInfo(
                url="https://httpbin.org/status/404",
                text="broken",
                type="external",
                file="docs/broken.md",
                context={"file": "docs/broken.md"},
            ),
        ]
        checker = FlextQualityLinkChecker()
        await checker.validate_links(test_links)
        checker.save_report()

    @staticmethod
    def main() -> int:
        """Run the example CLI entrypoint."""
        anyio.run(FlextQualityLinkChecker.run_demo)
        return 0


if __name__ == "__main__":
    raise SystemExit(FlextQualityLinkChecker.main())
