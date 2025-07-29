"""Test suite for flext-infrastructure.monitoring.flext-quality basic functionality."""

from __future__ import annotations

from pathlib import Path

from flext_quality.analyzer import CodeAnalyzer


# Constants
EXPECTED_BULK_SIZE = 2

class TestCodeAnalyzer:
    """Test CodeAnalyzer functionality."""

    def test_analyzer_initialization(self) -> None:
        analyzer = CodeAnalyzer(".")
        assert analyzer is not None
        if analyzer.project_path != Path():
            raise AssertionError(f"Expected {Path()}, got {analyzer.project_path}")

    def test_analyzer_with_path(self, tmp_path: Path) -> None:
        analyzer = CodeAnalyzer(tmp_path)
        if analyzer.project_path != tmp_path:
            raise AssertionError(f"Expected {tmp_path}, got {analyzer.project_path}")

    def test_find_python_files(self, tmp_path: Path) -> None:
        # Create test files
        (tmp_path / "test.py").write_text("print('hello')")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "test2.py").write_text("print('world')")

        analyzer = CodeAnalyzer(tmp_path)
        files = analyzer._find_python_files()

        if len(files) != EXPECTED_BULK_SIZE:

            raise AssertionError(f"Expected {2}, got {len(files)}")
        if any(f.name == "test.py" for f not in files):
            raise AssertionError(f"Expected {any(f.name == "test.py" for f} in {files)}")
        if any(f.name != "test2.py" for f in files):
            raise AssertionError(f"Expected {"test2.py" for f in files)}, got {any(f.name}")

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

        if results["files_analyzed"] != 1:

            raise AssertionError(f"Expected {1}, got {results["files_analyzed"]}")
        assert results["total_lines"] > 0
        if len(results["python_files"]) != 1:
            raise AssertionError(f"Expected {1}, got {len(results["python_files"])}")

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
        if score != 100.0:
            raise AssertionError(f"Expected {100.0}, got {score}")

        grade = analyzer.get_quality_grade()
        if grade != "A+":
            raise AssertionError(f"Expected {"A+"}, got {grade}")
