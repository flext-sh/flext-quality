"""Git tools for quality operations consolidating history rewrite and cleanup.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides git operations for quality tools:
- History rewriting with AI commit cleanup
- Repository cleanup operations
- Submodule management
- Backup operations

ALL operations support:
- dry_run=True (default - MANDATORY)
- temp_path for temporary workspace
- FlextResult error handling (NO try/except)
- FlextLogger structured logging
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes
from pydantic import ConfigDict

from flext_quality.constants import FlextQualityConstants
from flext_quality.models import FlextQualityModels


class FlextQualityGitTools(FlextService[None]):
    """Unified git operations for quality tools with complete flext-core integration.

    Example usage:
    ```python
    from .tools import FlextQualityGitTools

    git = FlextQualityGitTools()

    # ALWAYS test in dry-run first (default)
    result = git.history_rewriter.rewrite_live(
        repo_path="/path/to/repo",
        dry_run=True,  # MANDATORY default
        temp_path="/tmp/test-workspace",
    )

    # Only then run for real if dry-run succeeds
    if result.is_success:
        result = git.history_rewriter.rewrite_live(
            repo_path="/path/to/repo",
            dry_run=False,  # Explicit opt-in to real changes
        )
    ```
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    def execute(self) -> FlextResult[None]:
        """Execute git tools service - FlextService interface."""
        return FlextResult[None].ok(None)

    class HistoryRewriter:
        """Git history rewriting with dry-run support."""

        @staticmethod
        def _create_temp_workspace(
            repo_path: str,
            temp_path: str | None = None,
        ) -> FlextResult[Path]:
            """Create temporary workspace for dry-run testing."""
            if temp_path:
                workspace = Path(temp_path)
                workspace.mkdir(parents=True, exist_ok=True)
            else:
                workspace = Path(
                    tempfile.mkdtemp(
                        prefix=FlextQualityConstants.DryRun.DEFAULT_TEMP_PREFIX
                    )
                )

            # Clone repository to temp workspace for dry-run
            repo = Path(repo_path)
            temp_repo = workspace / repo.name

            result = subprocess.run(
                ["git", "clone", str(repo), str(temp_repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                return FlextResult[Path].fail(
                    f"Failed to clone repo to temp workspace: {result.stderr}"
                )

            return FlextResult[Path].ok(temp_repo)

        @staticmethod
        def _cleanup_temp_workspace(workspace: Path) -> FlextResult[None]:
            """Cleanup temporary workspace."""
            if workspace.exists():
                shutil.rmtree(workspace)
            return FlextResult[None].ok(None)

        @staticmethod
        def _strip_ai_signatures(message: str) -> str:
            """Strip AI signatures from commit messages."""
            patterns = FlextQualityConstants.Git.AI_PATTERNS

            cleaned = message
            for pattern in patterns:
                cleaned = re.sub(pattern, "", cleaned, flags=re.MULTILINE | re.DOTALL)

            # Clean up extra whitespace
            cleaned = re.sub(r"\n\n+", "\n\n", cleaned)
            return cleaned.strip()

        @classmethod
        def rewrite_live(
            cls,
            repo_path: str,
            *,
            dry_run: bool = True,
            temp_path: str | None = None,
        ) -> FlextResult[FlextQualityModels.RewriteResult]:
            """Rewrite git history to remove AI signatures.

            Args:
                repo_path: Path to repository
                dry_run: Test in temporary workspace (MANDATORY default)
                temp_path: Custom temporary workspace path

            Returns:
                FlextResult with RewriteResult containing statistics

            """
            logger = FlextLogger(__name__)

            # In dry-run, create temp workspace
            if dry_run:
                workspace_result = cls._create_temp_workspace(repo_path, temp_path)
                if workspace_result.is_failure:
                    return FlextResult[FlextQualityModels.RewriteResult].fail(
                        workspace_result.error
                    )
                work_repo = workspace_result.value
            else:
                work_repo = Path(repo_path)

            logger.info(
                f"Rewriting git history in {'DRY-RUN' if dry_run else 'LIVE'} mode",
                repo_path=str(work_repo),
            )

            # Get commit list
            result = subprocess.run(
                ["git", "-C", str(work_repo), "rev-list", "--all", "--reverse"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                return FlextResult[FlextQualityModels.RewriteResult].fail(
                    f"Failed to get commit list: {result.stderr}"
                )

            commits = result.stdout.strip().split("\n") if result.stdout.strip() else []
            commits_processed = 0
            commits_changed = 0
            errors: list[str] = []

            for commit_hash in commits:
                # Get commit message
                result = subprocess.run(
                    [
                        "git",
                        "-C",
                        str(work_repo),
                        "log",
                        "-1",
                        "--format=%B",
                        commit_hash,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode != 0:
                    errors.append(f"Failed to get message for {commit_hash}")
                    continue

                original_message = result.stdout.strip()
                cleaned_message = cls._strip_ai_signatures(original_message)

                if cleaned_message != original_message:
                    # Rewrite commit message
                    amend_result = subprocess.run(
                        [
                            "git",
                            "-C",
                            str(work_repo),
                            "commit",
                            "--amend",
                            "-m",
                            cleaned_message,
                        ],
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    if amend_result.returncode != 0:
                        errors.append(f"Failed to amend {commit_hash}")
                        continue

                    commits_changed += 1

                commits_processed += 1

            # Cleanup temp workspace if dry-run
            if dry_run:
                cleanup_result = cls._cleanup_temp_workspace(work_repo.parent)
                if cleanup_result.is_failure:
                    logger.warning(
                        f"Failed to cleanup temp workspace: {cleanup_result.error}"
                    )

            rewrite_result = FlextQualityModels.RewriteResult(
                commits_processed=commits_processed,
                commits_changed=commits_changed,
                success=len(errors) == 0,
                errors=errors,
            )

            return FlextResult[FlextQualityModels.RewriteResult].ok(rewrite_result)

    class CleanupService:
        """Repository cleanup operations."""

        @staticmethod
        def cleanup_cruft(
            repo_path: str,
            *,
            dry_run: bool = True,
        ) -> FlextResult[FlextTypes.Dict]:
            """Cleanup cruft files and directories.

            Args:
                repo_path: Path to repository
                dry_run: Preview changes without applying

            Returns:
                FlextResult with cleanup statistics

            """
            logger = FlextLogger(__name__)
            repo = Path(repo_path)

            logger.info(
                f"Cleaning cruft in {'DRY-RUN' if dry_run else 'LIVE'} mode",
                repo_path=str(repo),
            )

            removed_count = 0
            errors: list[str] = []

            # Run git clean
            cmd = ["git", "-C", str(repo), "clean", "-xfd"]
            if dry_run:
                cmd.insert(4, "-n")  # Dry-run flag

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                errors.append(f"Git clean failed: {result.stderr}")
            else:
                # Count removed items
                removed_count = (
                    len(result.stdout.strip().split("\n"))
                    if result.stdout.strip()
                    else 0
                )

            return FlextResult[FlextTypes.Dict].ok({
                "removed_count": removed_count,
                "errors": errors,
                "success": len(errors) == 0,
            })


__all__ = ["FlextQualityGitTools"]
