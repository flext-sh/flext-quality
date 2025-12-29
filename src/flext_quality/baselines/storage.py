"""Persistent storage for quality baselines.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult

from flext_quality.constants import FlextQualityConstants as c


class FlextQualityBaselinesStorage:
    """File-based baseline storage for dead code tracking."""

    class Storage:
        """Baseline storage operations."""

        def __init__(self, baseline_path: Path) -> None:
            """Initialize baseline storage.

            Args:
                baseline_path: Path to the baseline file.

            """
            self._path = baseline_path

        def read(self) -> FlextResult[dict[str, int]]:
            """Read baseline counts from file.

            Returns:
                FlextResult containing dict mapping project names to dead code counts.

            """
            if not self._path.exists():
                return FlextResult[dict[str, int]].ok({})

            try:
                baselines: dict[str, int] = {}
                for line in self._path.read_text().splitlines():
                    if line.strip() and not line.startswith("#"):
                        parts = line.split(":")
                        if len(parts) == c.Quality.Baseline.PARTS_COUNT:
                            name, count = parts
                            baselines[name.strip()] = int(count.strip())
                return FlextResult[dict[str, int]].ok(baselines)
            except Exception as e:
                return FlextResult[dict[str, int]].fail(f"Failed to read baseline: {e}")

        def write(self, baselines: dict[str, int]) -> FlextResult[bool]:
            """Write baseline counts to file.

            Args:
                baselines: Dict mapping project names to dead code counts.

            Returns:
                FlextResult indicating success or failure.

            """
            try:
                lines = ["# Dead code baseline - auto-generated"]
                for name, count in sorted(baselines.items()):
                    lines.append(f"{name}:{count}")
                self._path.write_text("\n".join(lines) + "\n")
                return FlextResult[bool].ok(True)
            except Exception as e:
                return FlextResult[bool].fail(f"Failed to write baseline: {e}")

        def update(self, project: str, count: int) -> FlextResult[bool]:
            """Update baseline for a single project.

            Args:
                project: Project name.
                count: New dead code count.

            Returns:
                FlextResult indicating success or failure.

            """
            result = self.read()
            if result.is_failure:
                return FlextResult[bool].fail(result.error or "Read failed")

            baselines = result.value
            baselines[project] = count
            return self.write(baselines)


__all__ = ["FlextQualityBaselinesStorage"]
