"""Public configuration-manager behavior."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import pytest

from flext_quality import t, u
from flext_quality.docs import FlextQualityConfigManager


def test_loads_shipped_configuration_by_default() -> None:
    manager = FlextQualityConfigManager()
    audit_rules = FlextQualityConfigManager.AuditRules.model_validate(
        u.Cli.yaml_load_mapping(manager.config_dir / "audit_rules.yaml")
    )
    style_guide = FlextQualityConfigManager.StyleGuide.model_validate(
        u.Cli.yaml_load_mapping(manager.config_dir / "style_guide.yaml")
    )

    assert manager.config_dir.name == "config"
    assert manager.get_audit_rules() == audit_rules
    assert manager.get_style_guide() == style_guide
    validation = u.Cli.yaml_load_mapping(manager.config_dir / "validation_config.yaml")
    link_validation = validation.get("link_validation")
    assert isinstance(link_validation, Mapping)
    assert (
        manager.get_validation_config().link_validation.timeout
        == link_validation.get("timeout")
    )


def test_missing_required_configuration_fails(tmp_path: Path) -> None:
    manager = FlextQualityConfigManager(tmp_path)

    with pytest.raises(FileNotFoundError):
        manager.get_audit_rules()


def test_validate_configs_reports_missing_files(tmp_path: Path) -> None:
    manager = FlextQualityConfigManager(tmp_path)

    issues = manager.validate_configs()

    assert len(issues) == 6
    assert sum("Missing required settings file" in issue for issue in issues) == 3
    assert sum("Invalid" in issue for issue in issues) == 3


def test_get_all_configs_returns_typed_and_raw_sections() -> None:
    manager = FlextQualityConfigManager()

    configs = manager.get_all_configs()

    assert set(configs) == {
        "audit_rules",
        "style_guide",
        "validation_config",
        "raw_configs",
    }
    raw_configs = configs["raw_configs"]
    assert isinstance(raw_configs, dict)
    for name in ("audit_rules", "style_guide", "validation_config"):
        shipped = u.Cli.yaml_load_mapping(manager.config_dir / f"{name}.yaml")
        assert raw_configs[name] == shipped


def test_raw_configuration_round_trips_nested_mappings_and_lists(
    tmp_path: Path,
) -> None:
    fixture = t.json_mapping_adapter().validate_python({
        "outer": {
            "nested": {"enabled": True, "thresholds": [1, 2, 3]},
            "entries": [{"name": "first", "tags": ["a", "b"]}],
        }
    })
    (tmp_path / "nested.yaml").write_text(
        u.Cli.yaml_dump_str(fixture), encoding="utf-8"
    )
    manager = FlextQualityConfigManager(tmp_path)

    loaded = manager.get_config("nested")
    round_trip_path = tmp_path / "round-trip.yaml"
    round_trip_path.write_text(u.Cli.yaml_dump_str(loaded), encoding="utf-8")
    round_tripped = u.Cli.yaml_load_mapping(round_trip_path)

    assert loaded == fixture
    assert round_tripped == fixture
