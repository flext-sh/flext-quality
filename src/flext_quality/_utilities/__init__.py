# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._utilities.quality import FlextQualityUtilitiesQuality


__all__: tuple[str, ...] = ("FlextQualityUtilitiesQuality",)

install_lazy_exports(
    __name__,
    globals(),
    {"FlextQualityUtilitiesQuality": ".quality"},
    public_exports=__all__,
    deferred_members={
        "FlextQualityUtilitiesQuality": (
            "RELAXED_CONTAINER_MAPPING_ADAPTER",
            "RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER",
            "MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER",
            "STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER",
            "REPORT_VALUE_MAPPING_ADAPTER",
            "compile_pattern",
            "escape_pattern",
            "execute_result_command",
            "execute_run_command",
            "execute_run_route",
            "format_hook_output",
            "extract_rules_from_yaml",
            "load_yaml_rules",
            "parse_hook_input",
            "read_stdin",
            "run_shell_command",
        ),
    },
)
