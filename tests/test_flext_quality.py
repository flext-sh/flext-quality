"""Test suite for flext-infrastructure.monitoring.flext-quality basic functionality."""

from __future__ import annotations

from pathlib import Path

from flext_quality.analyzer import CodeAnalyzer


class TestCodeAnalyzer:
    """Test CodeAnalyzer functionality."""

    def test_analyzer_initialization(self) -> None:
        analyzer = CodeAnalyzer(".")
        assert analyzer is not None
        assert analyzer.project_path == Path()

    def test_analyzer_with_path(self, tmp_path: Path) -> None:
        analyzer = CodeAnalyzer(tmp_path)
        assert analyzer.project_path == tmp_path

    def test_find_python_files(self, tmp_path: Path) -> None:
        # Create test files
        (tmp_path / "test.py").write_text("print('hello')")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "test2.py").write_text("print('world')")

        analyzer = CodeAnalyzer(tmp_path)
        files = analyzer._find_python_files()

        assert len(files) == 2
        assert any(f.name == "test.py" for f in files)
        assert any(f.name == "test2.py" for f in files)

    def test_analyze_project_basic(self, tmp_path: Path) -> None:
        # Create a simple Python file
        test_file = tmp_path / "simple.py"
        test_file.write_text(
            """
def hello() -> None:
        return "Hello, World!"

if __name__ == "__main__":
            print(hello())
""",
        )

        analyzer = CodeAnalyzer(tmp_path)
        results = analyzer.analyze_project(
            include_security=False,
            include_complexity=False,
            include_dead_code=False,
            include_duplicates=False,
        )

        assert results["files_analyzed"] == 1
        assert results["total_lines"] > 0
        assert len(results["python_files"]) == 1

    def test_quality_score(self) -> None:
        analyzer = CodeAnalyzer(".")
        analyzer.analysis_results = {
            "issues": {
                "security": [],
                "complexity": [],
                "dead_code": [],
                "duplicates": [],
            },
        }

        score = analyzer.get_quality_score()
        assert score == 100.0

        grade = analyzer.get_quality_grade()
        assert grade == "A+"
