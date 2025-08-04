"""Test configuration module."""

from __future__ import annotations

from flext_quality import config
from flext_quality.infrastructure.config import QualityConfig


class TestConfigModule:
    """Test configuration module functionality."""

    def test_quality_config_import(self) -> None:
        """Test QualityConfig can be imported from config module."""
        assert hasattr(config, "QualityConfig")
        assert config.QualityConfig is QualityConfig

    def test_config_all_exports(self) -> None:
        """Test __all__ contains expected exports."""
        assert hasattr(config, "__all__")
        assert "QualityConfig" in config.__all__

    def test_backward_compatibility(self) -> None:
        """Test backward compatibility of config re-export."""
        # Import from main config module
        # Import from infrastructure directly
        from flext_quality.config import QualityConfig as ConfigQualityConfig
        from flext_quality.infrastructure.config import (
            QualityConfig as InfraQualityConfig,
        )

        # Should be the same class
        assert ConfigQualityConfig is InfraQualityConfig

    def test_config_instantiation(self) -> None:
        """Test config can be instantiated through re-export."""
        config_instance = config.QualityConfig()
        assert isinstance(config_instance, QualityConfig)

        # Check basic attributes exist
        assert hasattr(config_instance, "min_coverage")
        assert hasattr(config_instance, "max_complexity")
        assert hasattr(config_instance, "max_duplication")
