#!/usr/bin/env python3
"""FLEXT Quality Link Validation Tool.

Advanced link checking utility with retry logic, rate limiting,
and comprehensive validation capabilities.
"""

from __future__ import annotations

import asyncio
import pathlib
import re
import time
from collections.abc import Mapping, MutableSequence, Sequence
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
import structlog
from aiohttp import ClientError, ClientSession, ClientTimeout
from pydantic import BaseModel, TypeAdapter

from flext_quality import t

_AsyncSession = ClientSession


class FlextQualityLinkChecker:
    """Advanced link validation and checking system."""

    class LinkConfig(BaseModel):
        """Configuration dictionary for link validation."""

        external_timeout: int
        retry_attempts: int
        user_agent: str
        follow_redirects: bool
        max_redirects: int
        acceptable_status_codes: Sequence[int]

    class LinkInfo(BaseModel):
        """Link information dictionary."""

        url: str
        text: str
        type: str
        file: str
        line: int | None = None
        reference: str | None = None
        context: t.ContainerMapping | None = None

    class LinkResult(BaseModel):
        """Link check result dictionary."""

        url: str
        valid: bool
        context: t.ContainerMapping
        status_code: int | None = None
        response_time: float | None = None
        redirected: bool | None = None
        final_url: str | None = None
        content_type: str | None = None
        error: str | None = None

    class PerformanceMetrics(BaseModel):
        """Performance metrics dictionary."""

        total_time: float
        average_response_time: float
        slowest_response: float

    class Results(BaseModel):
        """Results dictionary."""

        total_links: int
        valid_links: int
        broken_links: int
        warnings: int
        errors: MutableSequence[FlextQualityLinkChecker.LinkResult]
        warnings_list: MutableSequence[t.ContainerMapping]
        performance: FlextQualityLinkChecker.PerformanceMetrics

    MIN_PATH_PARTS_FOR_REPO = 2
    MIN_PATH_PARTS_FOR_DETAILED_REPO = 3
    MIN_PATH_PARTS_FOR_BRANCH = 3
    MAX_BROKEN_LINKS_TO_SHOW = 10

    def __init__(
        self,
        config_path: str | None = "docs/maintenance/config/validation_config.yaml",
    ) -> None:
        """Initialize the link checker with configuration."""
        self.config: FlextQualityLinkChecker.LinkConfig = self._get_default_config()
        self.load_config(config_path)
        self.session: _AsyncSession | None = None
        self.cache: t.MutableContainerMapping = {}
        self.results: FlextQualityLinkChecker.Results = FlextQualityLinkChecker.Results(
            total_links=0,
            valid_links=0,
            broken_links=0,
            warnings=0,
            errors=[],
            warnings_list=[],
            performance=FlextQualityLinkChecker.PerformanceMetrics(
                total_time=0.0,
                average_response_time=0.0,
                slowest_response=0.0,
            ),
        )

    @staticmethod
    def _get_default_config() -> FlextQualityLinkChecker.LinkConfig:
        """Get default configuration."""
        return FlextQualityLinkChecker.LinkConfig(
            external_timeout=10,
            retry_attempts=3,
            user_agent="FLEXT-Quality-Link-Validator/1.0",
            follow_redirects=True,
            max_redirects=5,
            acceptable_status_codes=[
                200,
                201,
                202,
                206,
                301,
                302,
                303,
                307,
                308,
            ],
        )

    def load_config(self, _config_path: str | None) -> None:
        """Load validation configuration."""
        self.config = self._get_default_config()

    def find_all_links(
        self,
        file_paths: Sequence[pathlib.Path],
    ) -> Sequence[FlextQualityLinkChecker.LinkInfo]:
        """Extract all links from the given files."""
        all_links: MutableSequence[FlextQualityLinkChecker.LinkInfo] = []

        for file_path in file_paths:
            try:
                content = file_path.read_text(encoding="utf-8")

                md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
                for text, url in md_links:
                    link_type = self._classify_link(url)
                    link_info = FlextQualityLinkChecker.LinkInfo(
                        url=url,
                        text=text,
                        type=link_type,
                        file=str(file_path),
                        line=content.count("\n", 0, content.find(f"[{text}]({url})"))
                        + 1,
                    )
                    all_links.append(link_info)

                ref_links = re.findall(r"\[([^\]]+)\]\[([^\]]+)\]", content)
                ref_defs = re.findall(r"\[([^\]]+)\]:\s*([^\s]+)", content)

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

            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                structlog.get_logger().warning("failed_to_extract_links", file_path=str(file_path), error=str(e))

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
        self,
        url: str,
        context: t.ContainerMapping | None = None,
    ) -> FlextQualityLinkChecker.LinkResult:
        """Asynchronously check a single link."""
        start_time = time.time()

        try:
            if self.session is None:
                return FlextQualityLinkChecker.LinkResult(
                    url=url,
                    error="session_not_initialized",
                    valid=False,
                    context=context or {},
                )
            external_timeout = self.config.external_timeout
            follow_redirects = self.config.follow_redirects
            max_redirects = self.config.max_redirects
            user_agent = self.config.user_agent
            acceptable_codes = self.config.acceptable_status_codes

            async with self.session.head(
                url,
                timeout=ClientTimeout(total=external_timeout),
                allow_redirects=follow_redirects,
                max_redirects=max_redirects,
                headers={"User-Agent": user_agent},
            ) as response:
                response_time = time.time() - start_time

                result = FlextQualityLinkChecker.LinkResult(
                    url=url,
                    status_code=response.status,
                    response_time=response_time,
                    valid=response.status in acceptable_codes,
                    redirected=bool(response.history),
                    final_url=str(response.url),
                    content_type=response.headers.get("content-type", ""),
                    context=context or {},
                )

                self.results.performance.slowest_response = max(
                    self.results.performance.slowest_response,
                    response_time,
                )

                return result

        except TimeoutError:
            return FlextQualityLinkChecker.LinkResult(
                url=url,
                error="timeout",
                response_time=self.config.external_timeout,
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
        except (OSError, ValueError, RuntimeError) as e:
            return FlextQualityLinkChecker.LinkResult(
                url=url,
                error=f"unexpected_error: {e!s}",
                response_time=time.time() - start_time,
                valid=False,
                context=context or {},
            )

    def check_link_sync(
        self,
        url: str,
        context: t.ContainerMapping | None = None,
    ) -> FlextQualityLinkChecker.LinkResult:
        """Synchronously check a single link (fallback method)."""
        start_time = time.time()

        for attempt in range(self.config.retry_attempts):
            try:
                response = requests.head(
                    url,
                    timeout=self.config.external_timeout,
                    headers={"User-Agent": self.config.user_agent},
                    allow_redirects=self.config.follow_redirects,
                )

                response_time = time.time() - start_time

                result = FlextQualityLinkChecker.LinkResult(
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    valid=response.status_code in self.config.acceptable_status_codes,
                    redirected=bool(response.history),
                    final_url=response.url,
                    content_type=response.headers.get("content-type", ""),
                    context=context or {},
                )

                self.results.performance.slowest_response = max(
                    self.results.performance.slowest_response,
                    response_time,
                )

                return result

            except requests.exceptions.Timeout:
                if attempt == self.config.retry_attempts - 1:
                    return FlextQualityLinkChecker.LinkResult(
                        url=url,
                        error="timeout",
                        response_time=self.config.external_timeout,
                        valid=False,
                        context=context or {},
                    )
            except requests.exceptions.RequestException as e:
                if attempt == self.config.retry_attempts - 1:
                    return FlextQualityLinkChecker.LinkResult(
                        url=url,
                        error=str(e),
                        response_time=time.time() - start_time,
                        valid=False,
                        context=context or {},
                    )
            except (OSError, ValueError, RuntimeError) as e:
                return FlextQualityLinkChecker.LinkResult(
                    url=url,
                    error=f"unexpected_error: {e!s}",
                    response_time=time.time() - start_time,
                    valid=False,
                    context=context or {},
                )

        return FlextQualityLinkChecker.LinkResult(
            url=url,
            error="max_retries_exceeded",
            valid=False,
            context={},
        )

    async def check_links_batch_async(
        self,
        links: Sequence[FlextQualityLinkChecker.LinkInfo],
    ) -> Sequence[FlextQualityLinkChecker.LinkResult]:
        """Check multiple links asynchronously."""
        start_time = time.time()

        semaphore = asyncio.Semaphore(10)

        async def check_with_semaphore(
            link_info: FlextQualityLinkChecker.LinkInfo,
        ) -> FlextQualityLinkChecker.LinkResult:
            async with semaphore:
                await asyncio.sleep(0.1)
                url = link_info.url
                context = link_info.context
                return await self.check_link_async(url, context)

        tasks = [check_with_semaphore(link) for link in links]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results: MutableSequence[FlextQualityLinkChecker.LinkResult] = []
        for result in results:
            if isinstance(result, BaseException):
                processed_results.append(
                    FlextQualityLinkChecker.LinkResult(
                        url="",
                        error=f"task_exception: {result!s}",
                        valid=False,
                        context={},
                    ),
                )
            else:
                processed_results.append(result)

        self.results.performance.total_time = time.time() - start_time

        valid_times: MutableSequence[float] = []
        for r in processed_results:
            if r.response_time is not None and r.valid:
                valid_times.append(float(r.response_time))

        if valid_times:
            self.results.performance.average_response_time = sum(
                valid_times,
            ) / len(valid_times)

        return processed_results

    def check_links_batch_sync(
        self,
        links: Sequence[FlextQualityLinkChecker.LinkInfo],
    ) -> Sequence[FlextQualityLinkChecker.LinkResult]:
        """Check multiple links synchronously with thread pool."""
        start_time = time.time()

        def check_single(
            link_info: FlextQualityLinkChecker.LinkInfo,
        ) -> FlextQualityLinkChecker.LinkResult:
            time.sleep(0.1)
            url = link_info.url
            ctx = link_info.context
            return self.check_link_sync(url, ctx)

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(check_single, links))

        self.results.performance.total_time = time.time() - start_time

        valid_times: MutableSequence[float] = []
        for r in results:
            if r.response_time is not None and r.valid:
                valid_times.append(float(r.response_time))

        if valid_times:
            self.results.performance.average_response_time = sum(
                valid_times,
            ) / len(valid_times)

        return results

    async def validate_links(
        self,
        links: Sequence[FlextQualityLinkChecker.LinkInfo],
        *,
        use_async: bool = True,
    ) -> FlextQualityLinkChecker.Results:
        """Main link validation method."""
        self.results.total_links = len(links)

        if use_async:
            try:
                async with ClientSession() as session:
                    self.session = session
                    results = await self.check_links_batch_async(links)
            except (OSError, ClientError, TimeoutError, RuntimeError):
                results = self.check_links_batch_sync(links)
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
                    self.results.warnings_list.append({
                        "type": "slow_response",
                        "url": result.url,
                        "message": f"Link timed out after {self.config.external_timeout}s",
                    })

        return self.results

    def check_robots_txt(self, domain: str) -> bool:
        """Check if crawling is allowed by robots.txt."""
        try:
            rp = RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            rp.read()

            return rp.can_fetch(self.config.user_agent, "/")
        except (OSError, ConnectionError, TimeoutError, UnicodeDecodeError):
            # If robots.txt can't be read, assume crawling is allowed
            return True

    def validate_github_links(
        self,
        links: Sequence[t.ContainerMapping],
    ) -> Sequence[t.ContainerMapping]:
        """Special validation for GitHub links."""
        github_links: MutableSequence[t.ContainerMapping] = []
        for link in links:
            url_raw = link.get("url")
            url_obj: str | None = url_raw if isinstance(url_raw, str) else None
            if isinstance(url_obj, str) and "github.com" in url_obj:
                github_links.append(link)

        validated_links: MutableSequence[Mapping[str, bool | t.NormalizedValue]] = []

        for link in github_links:
            url_candidate = link.get("url")
            if not isinstance(url_candidate, str):
                continue
            url = url_candidate

            if self._validate_github_url_structure(url):
                validated_links.append({
                    **link,
                    "valid": True,
                    "github_validated": True,
                })
            else:
                validated_links.append({
                    **link,
                    "valid": False,
                    "error": "invalid_github_url_structure",
                })

        return validated_links

    def _validate_github_url_structure(self, url: str) -> bool:
        """Validate GitHub URL structure without making requests."""
        parsed = urlparse(url)

        if parsed.netloc != "github.com":
            return False

        path_parts = parsed.path.strip("/").split("/")

        # Basic GitHub URL patterns
        if len(path_parts) >= self.MIN_PATH_PARTS_FOR_REPO:
            # user/repo or user/repo/tree/branch or user/repo/blob/branch/file
            if path_parts[1] in {"tree", "blob", "pull", "issues", "wiki", "releases"}:
                return len(path_parts) >= self.MIN_PATH_PARTS_FOR_DETAILED_REPO
            if path_parts[1] in {"pulls", "issues", "wikis", "releases"}:
                return True
            # Assume it's a valid repo reference
            return True

        return False

    def generate_report(self, report_format: str = "json") -> str:
        """Generate validation report."""
        results_adapter: TypeAdapter[FlextQualityLinkChecker.Results] = TypeAdapter(
            FlextQualityLinkChecker.Results
        )
        if report_format == "json":
            return results_adapter.dump_json(self.results, indent=2).decode()
        if report_format == "summary":
            return self._generate_summary_report()
        return results_adapter.dump_json(self.results).decode()

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

        for error in r.errors[:10]:  # Show first 10 broken links
            url = error.url
            status = error.status_code or "N/A"
            error_msg = error.error or "Unknown error"
            report += f"- {url} (Status: {status}, Error: {error_msg})\n"

        if len(r.errors) > self.MAX_BROKEN_LINKS_TO_SHOW:
            report += f"... and {len(r.errors) - self.MAX_BROKEN_LINKS_TO_SHOW} more broken links\n"

        if r.warnings_list:
            report += "\nWarnings:\n"
            for warning in r.warnings_list[:5]:
                report += f"- {warning['url']}: {warning['message']}\n"

        return report

    def save_report(
        self,
        output_path: str = "docs/maintenance/reports/",
    ) -> pathlib.Path:
        """Save validation report."""
        results_adapter: TypeAdapter[FlextQualityLinkChecker.Results] = TypeAdapter(
            FlextQualityLinkChecker.Results
        )
        pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"link_validation_{timestamp}.json"
        filepath = pathlib.Path(output_path) / filename

        pathlib.Path(filepath).write_bytes(
            results_adapter.dump_json(self.results, indent=2),
        )

        return filepath


def validate_links_sync(
    links: Sequence[FlextQualityLinkChecker.LinkInfo],
    config_path: str | None = None,
) -> FlextQualityLinkChecker.Results:
    """Synchronous wrapper for link validation."""
    checker = FlextQualityLinkChecker(config_path)
    return asyncio.run(checker.validate_links(links, use_async=True))


if __name__ == "__main__":
    test_links: Sequence[FlextQualityLinkChecker.LinkInfo] = [
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

    import asyncio

    async def main() -> None:
        """Run example link validation."""
        checker = FlextQualityLinkChecker()
        await checker.validate_links(test_links)
        checker.save_report()

    asyncio.run(main())
