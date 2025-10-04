"""Tests for FlextQuality tools utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_quality.tools.utilities import (
    Colors,
    FlextQualityToolsUtilities,
    colorize,
    get_project_root,
    get_stdlib_modules,
    is_stdlib_module,
    normalize_path,
    should_ignore_path,
)


class TestColors:
    """Tests for Colors utility class."""

    def test_colorize_with_color(self) -> None:
        """Test colorizing text with color."""
        result = colorize("test", Colors.RED)
        assert result.startswith(Colors.RED)
        assert result.endswith(Colors.RESET)
        assert "test" in result

    def test_colorize_without_color(self) -> None:
        """Test colorizing text without color."""
        result = colorize("test", "")
        assert result == "test"

    def test_print_colored_success(self) -> None:
        """Test print_colored succeeds."""
        result = Colors.print_colored("test", Colors.GREEN)
        assert result.is_success

    def test_color_constants(self) -> None:
        """Test color constants are defined."""
        assert Colors.RED
        assert Colors.GREEN
        assert Colors.YELLOW
        assert Colors.BLUE
        assert Colors.RESET


class TestPaths:
    """Tests for Paths utility class."""

    def test_should_ignore_path_pycache(self) -> None:
        """Test ignoring __pycache__ path."""
        assert should_ignore_path("src/__pycache__/test.py")
        assert should_ignore_path(Path("__pycache__"))

    def test_should_ignore_path_git(self) -> None:
        """Test ignoring .git path."""
        assert should_ignore_path(".git/config")
        assert should_ignore_path(Path(".git"))

    def test_should_ignore_path_valid(self) -> None:
        """Test not ignoring valid path."""
        assert not should_ignore_path("src/module.py")
        assert not should_ignore_path(Path("tests/test_module.py"))

    def test_get_project_root(self) -> None:
        """Test getting project root."""
        root = get_project_root()
        assert isinstance(root, Path)
        assert root.exists()

    def test_normalize_path(self) -> None:
        """Test normalizing path."""
        path = normalize_path(".")
        assert isinstance(path, Path)
        assert path.is_absolute()

    def test_normalize_path_string(self) -> None:
        """Test normalizing string path."""
        path = normalize_path("/tmp/test")
        assert isinstance(path, Path)
        assert path.is_absolute()

    def test_find_python_files(self, tmp_path: Path) -> None:
        """Test finding Python files."""
        # Create test structure
        (tmp_path / "test1.py").write_text("# test")
        (tmp_path / "test2.py").write_text("# test")
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "test.pyc").write_text("# test")

        utils = FlextQualityToolsUtilities()
        files = utils.Paths.find_python_files(tmp_path)

        assert len(files) == 2
        assert all(f.suffix == ".py" for f in files)
        assert not any("__pycache__" in str(f) for f in files)


class TestStdlib:
    """Tests for Stdlib utility class."""

    def test_get_stdlib_modules(self) -> None:
        """Test getting stdlib modules list."""
        modules = get_stdlib_modules()
        assert isinstance(modules, list)
        assert "os" in modules
        assert "sys" in modules
        assert "pathlib" in modules
        assert modules == sorted(modules)  # Should be sorted

    def test_is_stdlib_module_true(self) -> None:
        """Test identifying stdlib module."""
        assert is_stdlib_module("os")
        assert is_stdlib_module("sys")
        assert is_stdlib_module("pathlib")
        assert is_stdlib_module("os.path")  # Submodule

    def test_is_stdlib_module_false(self) -> None:
        """Test identifying non-stdlib module."""
        assert not is_stdlib_module("flask")
        assert not is_stdlib_module("django")
        assert not is_stdlib_module("pytest")
        assert not is_stdlib_module("flext_core")


class TestFlextQualityToolsUtilities:
    """Tests for FlextQualityToolsUtilities service."""

    def test_initialization(self) -> None:
        """Test utilities service initialization."""
        utils = FlextQualityToolsUtilities()
        assert utils is not None
        assert utils._logger is not None
        assert utils._cli is not None

    def test_execute(self) -> None:
        """Test execute method."""
        utils = FlextQualityToolsUtilities()
        result = utils.execute()
        assert result.is_success

    def test_colors_component(self) -> None:
        """Test Colors component accessible."""
        assert FlextQualityToolsUtilities.Colors.RED
        assert FlextQualityToolsUtilities.Colors.colorize

    def test_paths_component(self) -> None:
        """Test Paths component accessible."""
        assert FlextQualityToolsUtilities.Paths.IGNORE_PATTERNS
        assert callable(FlextQualityToolsUtilities.Paths.get_project_root)

    def test_stdlib_component(self) -> None:
        """Test Stdlib component accessible."""
        assert callable(FlextQualityToolsUtilities.Stdlib.get_stdlib_modules)
        assert callable(FlextQualityToolsUtilities.Stdlib.is_stdlib_module)


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_colorize_function(self) -> None:
        """Test colorize convenience function."""
        result = colorize("test", Colors.BLUE)
        assert Colors.BLUE in result
        assert "test" in result

    def test_get_project_root_function(self) -> None:
        """Test get_project_root convenience function."""
        root = get_project_root()
        assert isinstance(root, Path)

    def test_normalize_path_function(self) -> None:
        """Test normalize_path convenience function."""
        path = normalize_path(".")
        assert isinstance(path, Path)
        assert path.is_absolute()

    def test_should_ignore_path_function(self) -> None:
        """Test should_ignore_path convenience function."""
        assert should_ignore_path("__pycache__")
        assert not should_ignore_path("src/module.py")

    def test_get_stdlib_modules_function(self) -> None:
        """Test get_stdlib_modules convenience function."""
        modules = get_stdlib_modules()
        assert "os" in modules

    def test_is_stdlib_module_function(self) -> None:
        """Test is_stdlib_module convenience function."""
        assert is_stdlib_module("os")
        assert not is_stdlib_module("pytest")
