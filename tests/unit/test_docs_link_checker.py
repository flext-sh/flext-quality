"""Public documentation link-checker behavior."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import socket

import anyio
import pytest
from pydantic import ValidationError

from flext_quality import u
from flext_quality.docs import FlextQualityLinkChecker


def test_default_constructor_loads_shipped_validation_settings() -> None:
    config_path = (
        Path(__file__).parents[2]
        / "src"
        / "flext_quality"
        / "docs"
        / "config"
        / "validation_config.yaml"
    )
    shipped = u.Cli.yaml_load_mapping(config_path)
    validation = shipped["validation"]
    link_validation = shipped["link_validation"]
    assert isinstance(validation, Mapping)
    assert isinstance(link_validation, Mapping)

    checker = FlextQualityLinkChecker()

    assert checker.settings.retry_attempts == validation["retry_attempts"]
    assert checker.settings.external_timeout == link_validation["timeout"]


def test_malformed_validation_section_fails_at_typed_boundary(tmp_path: Path) -> None:
    config_path = tmp_path / "validation.yaml"
    config_path.write_text(
        "validation: invalid\n"
        "link_validation:\n"
        "  timeout: 1\n"
        "  user_agent: test\n"
        "  follow_redirects: true\n"
        "  max_redirects: 1\n"
        "  acceptable_status_codes: [200]\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        FlextQualityLinkChecker(str(config_path))


def test_async_transport_failure_returns_typed_result(tmp_path: Path) -> None:
    config_path = tmp_path / "validation.yaml"
    config_path.write_text(
        "validation:\n  retry_attempts: 1\n"
        "link_validation:\n  timeout: 1\n  user_agent: test\n"
        "  follow_redirects: false\n  max_redirects: 1\n"
        "  acceptable_status_codes: [200]\n",
        encoding="utf-8",
    )
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    checker = FlextQualityLinkChecker(str(config_path))
    link = FlextQualityLinkChecker.LinkInfo(
        url=f"http://127.0.0.1:{port}/unreachable",
        text="unreachable",
        type="external",
        file="README.md",
    )

    results = anyio.run(checker.validate_links, [link])

    assert results.broken_links == 1
    assert results.errors[0].url == link.url
    assert results.errors[0].valid is False
    assert results.errors[0].error
