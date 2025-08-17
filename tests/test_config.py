"""Test configuration module."""

from __future__ import annotations

from flext_quality import (
    QualityConfig,
    QualityConfig as InfraQualityConfig,
    config,
    config as config_module,
)


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
        # Use module-level imports
        config_quality_config = config_module.QualityConfig

        # Should be the same class
        assert config_quality_config is InfraQualityConfig

    def test_config_instantiation(self) -> None:
        """Test config can be instantiated through re-export."""
        config_instance = config.QualityConfig()
        assert isinstance(config_instance, QualityConfig)

        # Check basic attributes exist
        assert hasattr(config_instance, "min_coverage")
        assert hasattr(config_instance, "max_complexity")
        assert hasattr(config_instance, "max_duplication")
