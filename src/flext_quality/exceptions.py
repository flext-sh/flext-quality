"""FLEXT Quality Exceptions - Using FlextExceptions from flext-core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions


class FlextQualityExceptions:
    """Quality-specific exception namespace using FlextExceptions from flext-core.

    All exceptions extend FlextExceptions.BaseError with quality-specific context.
    Uses real inheritance to expose the full hierarchy.
    """

    # Base exception - real inheritance from FlextExceptions.BaseError
    class Base(FlextExceptions.BaseError):
        """Base exception for quality operations - real inheritance from BaseError."""

    # Analysis errors - real inheritance from OperationError with analysis context
    class Analysis(FlextExceptions.OperationError):
        """Analysis error for quality operations - inherits from OperationError."""

    # Configuration errors - real inheritance from ConfigurationError
    class Config(FlextExceptions.ConfigurationError):
        """Configuration error - real inheritance from ConfigurationError."""

    # Model errors - real inheritance from ValidationError for model validation failures
    class Model(FlextExceptions.ValidationError):
        """Model validation error - real inheritance from ValidationError."""

    # Convenience factory methods for quality-specific exceptions
    @staticmethod
    def analysis_error(
        message: str,
        operation: str | None = None,
        **kwargs: object,
    ) -> FlextQualityExceptions.Analysis:
        """Create analysis error with quality-specific context."""
        return FlextQualityExceptions.Analysis(
            message,
            operation=operation or "quality_analysis",
            **kwargs,
        )

    @staticmethod
    def config_error(
        message: str,
        config_key: str | None = None,
        **kwargs: object,
    ) -> FlextQualityExceptions.Config:
        """Create configuration error with quality-specific context."""
        return FlextQualityExceptions.Config(
            message,
            config_key=config_key,
            **kwargs,
        )

    @staticmethod
    def model_error(
        message: str,
        field: str | None = None,
        **kwargs: object,
    ) -> FlextQualityExceptions.Model:
        """Create model validation error with quality-specific context."""
        return FlextQualityExceptions.Model(
            message,
            field=field,
            **kwargs,
        )
