#!/usr/bin/env python3
"""FLEXT Quality Link Validation Tool.

Advanced link checking utility with retry logic, rate limiting,
and comprehensive validation capabilities.
"""

import asyncio
import json
import pathlib
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import aiohttp
import requests
import yaml


class LinkChecker:
    """Advanced link validation and checking system."""

    # Constants for URL validation
    MIN_PATH_PARTS_FOR_REPO = 2
    MIN_PATH_PARTS_FOR_DETAILED_REPO = 3
    MIN_PATH_PARTS_FOR_BRANCH = 3
    MAX_BROKEN_LINKS_TO_SHOW = 10

    def __init__(
        self,
        config_path: str | None = "docs/maintenance/config/validation_config.yaml",
    ) -> None:
        """Initialize the link checker with configuration."""
        self.load_config(config_path)
        self.session = None
        self.cache = {}
        self.results = {
            "total_links": 0,
            "valid_links": 0,
            "broken_links": 0,
            "warnings": 0,
            "errors": [],
            "warnings_list": [],
            "performance": {
                "total_time": 0,
                "average_response_time": 0,
                "slowest_response": 0,
            },
        }

    def load_config(self, config_path: str | None) -> None:
        """Load validation configuration."""
        try:
            with pathlib.Path(config_path).open(encoding="utf-8") as f:
                self.config = yaml.safe_load(f)["link_validation"]
        except (FileNotFoundError, KeyError):
            # Default configuration
            self.config = {
                "external_timeout": 10,
                "retry_attempts": 3,
                "user_agent": "FLEXT-Quality-Link-Validator/1.0",
                "follow_redirects": True,
                "max_redirects": 5,
                "acceptable_status_codes": [
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
            }

    def find_all_links(self, file_paths: list[pathlib.Path]) -> list[dict]:
        """Extract all links from the given files."""
        all_links = []

        for file_path in file_paths:
            try:
                content = file_path.read_text(encoding="utf-8")

                # Find markdown links [text](url)
                md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
                for text, url in md_links:
                    link_type = self._classify_link(url)
                    all_links.append(
                        {
                            "url": url,
                            "text": text,
                            "type": link_type,
                            "file": str(file_path),
                            "line": content.count(
                                "\n", 0, content.find(f"[{text}]({url})")
                            )
                            + 1,
                        }
                    )

                # Find reference-style links [text][ref] and [ref]: url
                ref_links = re.findall(r"\[([^\]]+)\]\[([^\]]+)\]", content)
                ref_defs = re.findall(r"\[([^\]]+)\]:\s*([^\s]+)", content)

                ref_dict = dict[str, Any](ref_defs)
                for text, ref in ref_links:
                    if ref in ref_dict:
                        url = ref_dict[ref]
                        link_type = self._classify_link(url)
                        all_links.append(
                            {
                                "url": url,
                                "text": text,
                                "type": link_type,
                                "file": str(file_path),
                                "reference": ref,
                            }
                        )

            except Exception as e:
                # Log the exception for debugging but continue processing
                print(f"Warning: Failed to extract links from {file_path}: {e}")

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
        context: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Asynchronously check a single link."""
        start_time = time.time()

        try:
            async with self.session.head(
                url,
                timeout=aiohttp.ClientTimeout(total=self.config["external_timeout"]),
                allow_redirects=self.config["follow_redirects"],
                max_redirects=self.config["max_redirects"],
                headers={"User-Agent": self.config["user_agent"]},
            ) as response:
                response_time = time.time() - start_time

                result = {
                    "url": url,
                    "status_code": response.status,
                    "response_time": response_time,
                    "valid": response.status in self.config["acceptable_status_codes"],
                    "redirected": len(response.history) > 0,
                    "final_url": str(response.url),
                    "content_type": response.headers.get("content-type", ""),
                    "context": context or {},
                }

                # Update performance metrics
                self.results["performance"]["slowest_response"] = max(
                    self.results["performance"]["slowest_response"],
                    response_time,
                )

                return result

        except TimeoutError:
            return {
                "url": url,
                "error": "timeout",
                "response_time": self.config["external_timeout"],
                "valid": False,
                "context": context or {},
            }
        except aiohttp.ClientError as e:
            return {
                "url": url,
                "error": str(e),
                "response_time": time.time() - start_time,
                "valid": False,
                "context": context or {},
            }
        except Exception as e:
            return {
                "url": url,
                "error": f"unexpected_error: {e!s}",
                "response_time": time.time() - start_time,
                "valid": False,
                "context": context or {},
            }

    def check_link_sync(
        self,
        url: str,
        context: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Synchronously check a single link (fallback method)."""
        start_time = time.time()

        for attempt in range(self.config["retry_attempts"]):
            try:
                response = requests.head(
                    url,
                    timeout=self.config["external_timeout"],
                    headers={"User-Agent": self.config["user_agent"]},
                    allow_redirects=self.config["follow_redirects"],
                )

                response_time = time.time() - start_time

                result = {
                    "url": url,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "valid": response.status_code
                    in self.config["acceptable_status_codes"],
                    "redirected": len(response.history) > 0,
                    "final_url": response.url,
                    "content_type": response.headers.get("content-type", ""),
                    "context": context or {},
                }

                # Update performance metrics
                self.results["performance"]["slowest_response"] = max(
                    self.results["performance"]["slowest_response"],
                    response_time,
                )

                return result

            except requests.exceptions.Timeout:
                if attempt == self.config["retry_attempts"] - 1:
                    return {
                        "url": url,
                        "error": "timeout",
                        "response_time": self.config["external_timeout"],
                        "valid": False,
                        "context": context or {},
                    }
            except requests.exceptions.RequestException as e:
                if attempt == self.config["retry_attempts"] - 1:
                    return {
                        "url": url,
                        "error": str(e),
                        "response_time": time.time() - start_time,
                        "valid": False,
                        "context": context or {},
                    }
            except Exception as e:
                return {
                    "url": url,
                    "error": f"unexpected_error: {e!s}",
                    "response_time": time.time() - start_time,
                    "valid": False,
                    "context": context or {},
                }

        return {
            "url": url,
            "error": "max_retries_exceeded",
            "valid": False,
            "context": context or {},
        }

    async def check_links_batch_async(self, links: list[dict]) -> list[dict]:
        """Check multiple links asynchronously."""
        start_time = time.time()

        # Create semaphore for rate limiting
        semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests

        async def check_with_semaphore(link_info: dict[str, Any]) -> dict[str, Any]:
            async with semaphore:
                await asyncio.sleep(0.1)  # Rate limiting
                return await self.check_link_async(
                    link_info["url"],
                    link_info.get("context"),
                )

        # Create tasks
        tasks = [check_with_semaphore(link) for link in links]

        # Execute tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append(
                    {
                        "error": f"task_exception: {result!s}",
                        "valid": False,
                    }
                )
            else:
                processed_results.append(result)

        self.results["performance"]["total_time"] = time.time() - start_time

        # Calculate average response time
        valid_times = [
            r["response_time"]
            for r in processed_results
            if "response_time" in r and r.get("valid")
        ]
        if valid_times:
            self.results["performance"]["average_response_time"] = sum(
                valid_times,
            ) / len(valid_times)

        return processed_results

    def check_links_batch_sync(self, links: list[dict]) -> list[dict]:
        """Check multiple links synchronously with thread pool."""
        start_time = time.time()

        def check_single(link_info: dict[str, Any]) -> dict[str, Any]:
            time.sleep(0.1)  # Rate limiting
            return self.check_link_sync(link_info["url"], link_info.get("context"))

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(check_single, links))

        self.results["performance"]["total_time"] = time.time() - start_time

        # Calculate average response time
        valid_times = [
            r["response_time"]
            for r in results
            if "response_time" in r and r.get("valid")
        ]
        if valid_times:
            self.results["performance"]["average_response_time"] = sum(
                valid_times,
            ) / len(valid_times)

        return results

    async def validate_links(
        self,
        links: list[dict],
        *,
        use_async: bool = True,
    ) -> dict[str, Any]:
        """Main link validation method."""
        self.results["total_links"] = len(links)

        if use_async:
            try:
                async with aiohttp.ClientSession() as session:
                    self.session = session
                    results = await self.check_links_batch_async(links)
            except ImportError:
                # Fallback to sync if aiohttp not available
                results = self.check_links_batch_sync(links)
        else:
            results = self.check_links_batch_sync(links)

        # Process results
        for result in results:
            if result.get("valid"):
                self.results["valid_links"] += 1
            else:
                self.results["broken_links"] += 1
                self.results["errors"].append(result)

                # Add warnings for specific cases
                if result.get("error") == "timeout":
                    self.results["warnings"] += 1
                    self.results["warnings_list"].append(
                        {
                            "type": "slow_response",
                            "url": result["url"],
                            "message": f"Link timed out after {self.config['external_timeout']}s",
                        }
                    )

        return self.results

    def check_robots_txt(self, domain: str) -> bool:
        """Check if crawling is allowed by robots.txt."""
        try:
            rp = RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            rp.read()

            return rp.can_fetch(self.config["user_agent"], "/")
        except Exception:
            # If robots.txt can't be read, assume crawling is allowed
            return True

    def validate_github_links(self, links: list[dict]) -> list[dict]:
        """Special validation for GitHub links."""
        github_links = [link for link in links if "github.com" in link["url"]]

        # GitHub API has rate limits, so we use a more conservative approach
        validated_links = []

        for link in github_links:
            url = link["url"]

            # Basic URL structure validation for GitHub
            if self._validate_github_url_structure(url):
                validated_links.append(
                    {
                        **link,
                        "valid": True,
                        "github_validated": True,
                    }
                )
            else:
                validated_links.append(
                    {
                        **link,
                        "valid": False,
                        "error": "invalid_github_url_structure",
                    }
                )

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
        if report_format == "json":
            return json.dumps(self.results, indent=2, default=str)
        if report_format == "summary":
            return self._generate_summary_report()
        return json.dumps(self.results, default=str)

    def _generate_summary_report(self) -> str:
        """Generate a human-readable summary report."""
        r = self.results

        report = f"""
Link Validation Summary Report
==============================

Total Links Checked: {r["total_links"]}
Valid Links: {r["valid_links"]}
Broken Links: {r["broken_links"]}
Warnings: {r["warnings"]}

Performance Metrics:
- Total Time: {r["performance"]["total_time"]:.2f}s
- Average Response Time: {r["performance"]["average_response_time"]:.2f}s
- Slowest Response: {r["performance"]["slowest_response"]:.2f}s

Broken Links:
"""

        for error in r["errors"][:10]:  # Show first 10 broken links
            url = error.get("url", "Unknown")
            status = error.get("status_code", "N/A")
            error_msg = error.get("error", "Unknown error")
            report += f"- {url} (Status: {status}, Error: {error_msg})\n"

        if len(r["errors"]) > self.MAX_BROKEN_LINKS_TO_SHOW:
            report += f"... and {len(r['errors']) - self.MAX_BROKEN_LINKS_TO_SHOW} more broken links\n"

        if r["warnings_list"]:
            report += "\nWarnings:\n"
            for warning in r["warnings_list"][:5]:
                report += f"- {warning['url']}: {warning['message']}\n"

        return report

    def save_report(
        self,
        output_path: str = "docs/maintenance/reports/",
    ) -> pathlib.Path:
        """Save validation report."""
        pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"link_validation_{timestamp}.json"
        filepath = pathlib.Path(output_path) / filename

        with pathlib.Path(filepath).open("w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)

        return filepath


# Synchronous wrapper for easy usage
def validate_links_sync(
    links: list[dict],
    config_path: str | None = None,
) -> dict[str, Any]:
    """Synchronous wrapper for link validation."""
    checker = LinkChecker(config_path)
    # Run async validation in new event loop

    return asyncio.run(checker.validate_links(links, use_async=True))


if __name__ == "__main__":
    # Example usage
    test_links = [
        {
            "url": "https://github.com/microsoft/vscode",
            "context": {"file": "README.md"},
        },
        {"url": "https://httpbin.org/status/200", "context": {"file": "docs/setup.md"}},
        {
            "url": "https://httpbin.org/status/404",
            "context": {"file": "docs/broken.md"},
        },
    ]

    import asyncio

    async def main() -> None:
        """Run example link validation."""
        checker = LinkChecker()
        await checker.validate_links(test_links)
        checker.save_report()

    asyncio.run(main())
