"""Pydantic models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_core import FlextModels
from pydantic import BaseModel, Field

from flext_quality import c


class _HookConfig(BaseModel):
    """Configuration for a hook."""

    event: c.Quality.HookEvent
    matcher: list[str] | None = None
    command: str
    timeout_ms: int = Field(default=c.Quality.Defaults.HOOK_TIMEOUT_MS)
    enabled: bool = True


class _HookResult(BaseModel):
    """Result from hook execution."""

    continue_execution: bool = Field(alias="continue")
    system_message: str | None = Field(default=None, alias="systemMessage")
    blocked_reason: str | None = None

    model_config = {"populate_by_name": True}


class _RuleDefinition(BaseModel):
    """A rule definition from YAML."""

    name: str
    type: c.Quality.RuleType
    description: str
    pattern: str | None = None
    action: str
    enabled: bool = True


class _IntegrationConfig(BaseModel):
    """Configuration for an integration."""

    name: str
    enabled: bool = True
    host: str = "localhost"
    port: int
    timeout_ms: int = Field(default=c.Quality.Defaults.INTEGRATION_TIMEOUT_MS)


class _MemoryObservation(BaseModel):
    """An observation from claude-mem."""

    id: str
    type: str
    title: str
    content: str
    concepts: list[str] = Field(default_factory=list)
    files: list[str] = Field(default_factory=list)
    timestamp: str


class _ContextSearchResult(BaseModel):
    """A search result from claude-context."""

    file_path: str
    snippet: str
    score: float
    line_number: int | None = None


class FlextQualityModels(FlextModels):
    """Namespace for flext-quality models.

    Usage:
        from flext_quality import m

        config = m.Quality.HookConfig(event=c.Quality.HookEvent.PRE_TOOL_USE, command="...")
        rule = m.Quality.RuleDefinition(name="rule1", type=c.Quality.RuleType.BLOCKING, ...)
    """

    class Quality:
        """Quality-specific models namespace."""

        HookConfig: Final = _HookConfig
        HookResult: Final = _HookResult
        RuleDefinition: Final = _RuleDefinition
        IntegrationConfig: Final = _IntegrationConfig
        MemoryObservation: Final = _MemoryObservation
        ContextSearchResult: Final = _ContextSearchResult


m = FlextQualityModels

__all__ = ["FlextQualityModels", "m"]
