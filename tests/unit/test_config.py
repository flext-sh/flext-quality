"""Test configuration module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_quality.settings import FlextQualitySettings


class TestFlextQualitySettings:
    """Test FlextQualitySettings functionality."""

    def test_config_creation(self) -> None:
        """Test FlextQualitySettings can be created."""
        config = FlextQualitySettings()
        assert isinstance(config, FlextQualitySettings)

    def test_enhanced_singleton_pattern(self) -> None:
        """Test enhanced singleton pattern implementation."""
        # Test global instance
        instance1 = FlextQualitySettings.get_global_instance()
        instance2 = FlextQualitySettings.get_global_instance()
        assert instance1 is instance2

    def test_environment_configs_development(self) -> None:
        """Test development-specific configuration creation."""
        dev_config = FlextQualitySettings.create_for_development()
        assert dev_config.min_coverage == 80.0
        assert dev_config.max_complexity == 15
        assert dev_config.parallel_workers == 2

    def test_environment_configs_production(self) -> None:
        """Test production-specific configuration creation."""
        prod_config = FlextQualitySettings.create_for_production()
        assert prod_config.min_coverage == 95.0
        assert prod_config.max_complexity == 8
        assert prod_config.parallel_workers == 8

    def test_config_attributes(self) -> None:
        """Test config has required quality analysis attributes."""
        config = FlextQualitySettings()

        # Quality Analysis Configuration
        assert hasattr(config, "min_coverage")
        assert hasattr(config, "max_complexity")
        assert hasattr(config, "max_duplication")
        assert hasattr(config, "min_security_score")
        assert hasattr(config, "min_maintainability")

        # Service Configuration
        assert hasattr(config, "analysis_timeout")
        assert hasattr(config, "parallel_workers")
        assert hasattr(config, "memory_limit_mb")

        # Backend Configuration
        assert hasattr(config, "enable_ast_analysis")
        assert hasattr(config, "enable_external_tools")
        assert hasattr(config, "enable_ruff")
        assert hasattr(config, "enable_mypy")
        assert hasattr(config, "enable_bandit")
        assert hasattr(config, "enable_dependency_scan")

        # Reporting Configuration
        assert hasattr(config, "enable_html_reports")
        assert hasattr(config, "enable_json_reports")
        assert hasattr(config, "enable_audit_logging")
        assert hasattr(config, "include_trend_analysis")
        assert hasattr(config, "include_executive_summary")

    def test_default_values(self) -> None:
        """Test config has proper default values."""
        config = FlextQualitySettings()

        # Test quality thresholds
        assert config.min_coverage == 90.0
        assert config.max_complexity == 10
        assert config.max_duplication == 5.0
        assert config.min_security_score == 90.0
        assert config.min_maintainability == 80.0

        # Test service settings
        assert config.analysis_timeout == 300
        assert config.parallel_workers == 4
        assert config.memory_limit_mb == 512

        # Test backend settings
        assert config.enable_ast_analysis is True
        assert config.enable_external_tools is True
        assert config.enable_ruff is True
        assert config.enable_mypy is True
        assert config.enable_bandit is True

    def test_environment_specific_configs(self) -> None:
        """Test environment-specific configuration creation."""
        # Development config should have relaxed thresholds
        dev_config = FlextQualitySettings.create_for_development()
        assert dev_config.min_coverage == 80.0
        assert dev_config.max_complexity == 15
        assert dev_config.parallel_workers == 2
        # enable_audit_logging uses default value (True) since create_for_development doesn't override it
        assert dev_config.enable_audit_logging is True

        # Production config should have strict thresholds
        prod_config = FlextQualitySettings.create_for_production()
        assert prod_config.min_coverage == 95.0
        assert prod_config.max_complexity == 8
        assert prod_config.min_security_score == 95.0
        assert prod_config.parallel_workers == 8
        # enable_audit_logging uses default value (True) since create_for_production doesn't override it
        assert prod_config.enable_audit_logging is True

    def test_config_helper_methods(self) -> None:
        """Test configuration helper methods."""
        config = FlextQualitySettings()

        # Test analysis config
        analysis_config = config.get_analysis_config()
        assert "min_coverage" in analysis_config
        assert "max_complexity" in analysis_config
        assert analysis_config["min_coverage"] == config.min_coverage

        # Test backend config
        backend_config = config.get_backend_config()
        assert "enable_ruff" in backend_config
        assert "enable_mypy" in backend_config
        assert backend_config["enable_ruff"] == config.enable_ruff

        # Test reporting config
        reporting_config = config.get_reporting_config()
        assert "enable_html_reports" in reporting_config
        assert "include_trend_analysis" in reporting_config

        # Test observability config
        obs_config = config.get_observability_config()
        assert "quiet" in obs_config
        assert "log_level" in obs_config

    def test_business_rules_validation(self) -> None:
        """Test business rules validation."""
        config = FlextQualitySettings()

        # Test valid configuration
        result = config.validate_business_rules()
        assert result.is_success

        # Test configuration with conflicting settings
        invalid_config = FlextQualitySettings(
            min_coverage=95.0,
            enable_external_tools=False,
        )
        result = invalid_config.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Coverage analysis requires external tools" in result.error

    def test_reset_functionality(self) -> None:
        """Test singleton reset functionality."""
        # Get initial instance
        instance1 = FlextQualitySettings.get_global_instance()

        # Reset and get new instance
        FlextQualitySettings.reset_global_instance()
        instance2 = FlextQualitySettings.get_global_instance()

        # Should be different instances after reset
        assert instance1 is not instance2
