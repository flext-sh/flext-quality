"""FLEXT Quality Exceptions - Using FlextExceptions from flext-core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions


class FlextQualityExceptions:
    """Quality-specific exception namespace using FlextExceptions from flext-core.

    All exceptions extend FlextExceptions.BaseError with quality-specific context.
    Uses composition pattern - delegates to FlextExceptions for all functionality.
    """

    # Base exception - use FlextExceptions.BaseError directly
    Base = FlextExceptions.BaseError

    # Analysis errors - use OperationError with analysis context
    Analysis = FlextExceptions.OperationError

    # Configuration errors - use ConfigurationError directly
    Config = FlextExceptions.ConfigurationError

    # Model errors - use ValidationError for model validation failures
    Model = FlextExceptions.ValidationError

    # Convenience factory methods for quality-specific exceptions
    @staticmethod
    def analysis_error(
        message: str,
        operation: str | None = None,
        **kwargs: object,
    ) -> FlextExceptions.OperationError:
        """Create analysis error with quality-specific context."""
        return FlextExceptions.OperationError(
            message,
            operation=operation or "quality_analysis",
            **kwargs,
        )

    @staticmethod
    def config_error(
        message: str,
        config_key: str | None = None,
        **kwargs: object,
    ) -> FlextExceptions.ConfigurationError:
        """Create configuration error with quality-specific context."""
        return FlextExceptions.ConfigurationError(
            message,
            config_key=config_key,
            **kwargs,
        )

    @staticmethod
    def model_error(
        message: str,
        field: str | None = None,
        **kwargs: object,
    ) -> FlextExceptions.ValidationError:
        """Create model validation error with quality-specific context."""
        return FlextExceptions.ValidationError(
            message,
            field=field,
            **kwargs,
        )
