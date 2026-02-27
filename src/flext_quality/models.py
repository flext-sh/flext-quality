"""Pydantic models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from flext_quality.constants import c

# =============================================================================
# Module-level model definitions (following flext-core pattern)
# =============================================================================


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


# =============================================================================
# Facade class with namespace (following flext-core pattern)
# =============================================================================


class FlextQualityModels:
    """Namespace for flext-quality models.

    Usage:
        from flext_quality.models import m

        config = m.Quality.HookConfig(event=c.Quality.HookEvent.PRE_TOOL_USE, command="...")
        rule = m.Quality.RuleDefinition(name="rule1", type=c.Quality.RuleType.BLOCKING, ...)
    """

    class Quality:
        """Quality-specific models namespace."""

        HookConfig = _HookConfig
        HookResult = _HookResult
        RuleDefinition = _RuleDefinition
        IntegrationConfig = _IntegrationConfig
        MemoryObservation = _MemoryObservation
        ContextSearchResult = _ContextSearchResult


# Short alias for imports
m = FlextQualityModels
RuleDefinition = _RuleDefinition

__all__ = ["FlextQualityModels", "RuleDefinition", "m"]
