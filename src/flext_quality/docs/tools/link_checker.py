"""FLEXT Quality Link Validation Tool.

Advanced link checking utility with retry logic, rate limiting,
and comprehensive validation capabilities.
"""

from __future__ import annotations

import asyncio
import pathlib
import time
from collections.abc import Mapping, MutableSequence
from concurrent.futures import ThreadPoolExecutor
from typing import ClassVar
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from aiohttp import ClientError, ClientSession, ClientTimeout

from flext_quality import FlextQualityConfigManager, c, m, p, t, u


class FlextQualityLinkChecker:
    """Advanced link validation and checking system."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    def __init__(self, config_dir: str | pathlib.Path | None = None) -> None:
        """Initialize the link checker from the validated link configuration.

        Args:
            config_dir: Configuration directory; ``None`` selects the package's
                declared configuration directory.

        """
        self.settings: m.Quality.LinkValidationConfig = (
            FlextQualityConfigManager(config_dir)
            .resolve_validation_config()
            .link_validation
        )
        self.session: ClientSession | None = None
        self.results: m.Quality.LinkValidatorResults = m.Quality.LinkValidatorResults(
            timestamp=u.now().isoformat(),
            performance=m.Quality.LinkPerformanceMetrics(),
        )

    def find_all_links(
        self, file_paths: t.SequenceOf[pathlib.Path]
    ) -> t.SequenceOf[m.Quality.LinkRecord]:
        """Extract all links from the given files."""
        all_links: MutableSequence[m.Quality.LinkRecord] = []

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
                link_info = m.Quality.LinkRecord(
                    url=url,
                    text=text,
                    type=link_type,
                    file=str(file_path),
                    line_number=content.count("\n", 0, content.find(f"[{text}]({url})"))
                    + 1,
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
                    link_info = m.Quality.LinkRecord(
                        url=url,
                        text=text,
                        type=link_type,
                        file=str(file_path),
                        reference=ref,
                    )
                    all_links.append(link_info)

        return all_links

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
    ) -> m.Quality.LinkCheckResult:
        """Asynchronously check a single link."""
        start_time = time.time()

        try:
            return await self._check_link_async_unchecked(url, start_time, context)

        except TimeoutError:
            return m.Quality.LinkCheckResult(
                url=url,
                error="timeout",
                response_time=self.settings.timeout,
                valid=False,
                context=context or {},
            )
        except ClientError as e:
            return m.Quality.LinkCheckResult(
                url=url,
                error=str(e),
                response_time=time.time() - start_time,
                valid=False,
                context=context or {},
            )
        except c.EXC_OS_RUNTIME_VALUE as e:
            return m.Quality.LinkCheckResult(
                url=url,
                error=f"unexpected_error: {e!s}",
                response_time=time.time() - start_time,
                valid=False,
                context=context or {},
            )

    async def _check_link_async_unchecked(
        self, url: str, start_time: float, context: t.JsonMapping | None
    ) -> m.Quality.LinkCheckResult:
        """Check an async link while allowing transport exceptions to propagate."""
        if self.session is None:
            return m.Quality.LinkCheckResult(
                url=url,
                error="session_not_initialized",
                valid=False,
                context=context or {},
            )

        async with self.session.head(
            url,
            timeout=ClientTimeout(total=self.settings.timeout),
            allow_redirects=self.settings.follow_redirects,
            max_redirects=self.settings.max_redirects,
            headers={"User-Agent": self.settings.user_agent},
        ) as response:
            response_time = time.time() - start_time
            result = m.Quality.LinkCheckResult(
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

    def check_link_sync(
        self, url: str, context: t.JsonMapping | None = None
    ) -> m.Quality.LinkCheckResult:
        """Check a single link synchronously with one request."""
        start_time = time.time()
        try:
            response = requests.head(
                url,
                timeout=self.settings.timeout,
                headers={"User-Agent": self.settings.user_agent},
                allow_redirects=self.settings.follow_redirects,
            )
        except requests.exceptions.Timeout:
            return m.Quality.LinkCheckResult(
                url=url,
                error="timeout",
                response_time=self.settings.timeout,
                valid=False,
                context=context or {},
            )
        except requests.exceptions.RequestException as e:
            return m.Quality.LinkCheckResult(
                url=url,
                error=str(e),
                response_time=time.time() - start_time,
                valid=False,
                context=context or {},
            )
        response_time = time.time() - start_time
        self.results.performance.slowest_response = max(
            self.results.performance.slowest_response, response_time
        )
        return m.Quality.LinkCheckResult(
            url=url,
            status_code=response.status_code,
            response_time=response_time,
            valid=response.status_code in self.settings.acceptable_status_codes,
            redirected=bool(response.history),
            final_url=response.url,
            content_type=response.headers.get("content-type", ""),
            context=context or {},
        )

    async def check_links_batch_async(
        self, links: t.SequenceOf[m.Quality.LinkRecord]
    ) -> t.SequenceOf[m.Quality.LinkCheckResult]:
        """Check multiple links asynchronously."""
        start_time = time.time()

        semaphore = asyncio.Semaphore(10)

        async def check_with_semaphore(
            link_info: m.Quality.LinkRecord,
        ) -> m.Quality.LinkCheckResult:
            async with semaphore:
                await asyncio.sleep(0.1)
                url = link_info.url
                context = link_info.context
                return await self.check_link_async(url, context)

        tasks = [check_with_semaphore(link) for link in links]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results: t.SequenceOf[m.Quality.LinkCheckResult] = [
            m.Quality.LinkCheckResult(
                url="", error=f"task_exception: {result!s}", valid=False, context={}
            )
            if isinstance(result, BaseException)
            else result
            for result in results
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

    def check_links_batch_sync(
        self, links: t.SequenceOf[m.Quality.LinkRecord]
    ) -> t.SequenceOf[m.Quality.LinkCheckResult]:
        """Check multiple links synchronously with thread pool."""
        start_time = time.time()

        def check_single(link_info: m.Quality.LinkRecord) -> m.Quality.LinkCheckResult:
            time.sleep(0.1)
            url = link_info.url
            ctx = link_info.context
            return self.check_link_sync(url, ctx)

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(check_single, links))

        self.results.performance.total_time = time.time() - start_time

        valid_times: t.SequenceOf[float] = [
            r.response_time for r in results if r.response_time is not None and r.valid
        ]

        if valid_times:
            self.results.performance.average_response_time = sum(valid_times) / len(
                valid_times
            )

        return results

    async def validate_links(
        self, links: t.SequenceOf[m.Quality.LinkRecord], *, use_async: bool = True
    ) -> m.Quality.LinkValidatorResults:
        """Validate all provided links."""
        self.results.links_checked = len(links)

        if use_async:
            async with ClientSession() as session:
                self.session = session
                results = await self.check_links_batch_async(links)
        else:
            results = self.check_links_batch_sync(links)

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
                    self.results.warnings_list.append(
                        m.Quality.LinkCheckResult(
                            type="slow_response",
                            url=result.url,
                            warning=f"Link timed out after {self.settings.timeout}s",
                        )
                    )

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
        adapter = m.TypeAdapter(m.Quality.LinkValidatorResults)
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

Total Links Checked: {r.links_checked}
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
                report += f"- {warning.url}: {warning.warning}\n"

        return report

    def save_report(
        self, output_path: str = "docs/maintenance/reports/"
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
    def validate_links_sync(
        links: t.SequenceOf[m.Quality.LinkRecord], config_dir: str | None = None
    ) -> m.Quality.LinkValidatorResults:
        """Validate links synchronously."""
        checker = FlextQualityLinkChecker(config_dir)
        return asyncio.run(checker.validate_links(links, use_async=True))

    @staticmethod
    async def run_demo() -> None:
        """Run the example validation without leaking module-level test data."""
        test_links: t.SequenceOf[m.Quality.LinkRecord] = [
            m.Quality.LinkRecord(
                url=c.Quality.LinkCheckerDemo.VSCODE_URL,
                text="VSCode",
                type="external",
                file="README.md",
                context={"file": "README.md"},
            ),
            m.Quality.LinkRecord(
                url=c.Quality.LinkCheckerDemo.HTTPBIN_OK_URL,
                text="httpbin",
                type="external",
                file="docs/setup.md",
                context={"file": "docs/setup.md"},
            ),
            m.Quality.LinkRecord(
                url=c.Quality.LinkCheckerDemo.HTTPBIN_BROKEN_URL,
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
        asyncio.run(FlextQualityLinkChecker.run_demo())
        return 0


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityLinkChecker"]


if __name__ == "__main__":
    raise SystemExit(FlextQualityLinkChecker.main())
