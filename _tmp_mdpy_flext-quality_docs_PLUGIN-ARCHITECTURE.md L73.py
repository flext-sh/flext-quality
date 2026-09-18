# from flext-quality/docs/PLUGIN-ARCHITECTURE.md:73
from __future__ import annotations
from flext_quality import m
from pathlib import Path
from flext_core import p
from flext_core import t


class QualityPlugin(Protocol):
    """Plugin interface for quality analyzers."""

    @property
    def name(self) -> str:
        """Plugin name."""
        ...

    @property
    def description(self) -> str:
        """Plugin description."""
        ...

    def analyze(
        self, path: Path, settings: m.Quality.PluginConfigModel | None = None
    ) -> p.Result[AnalysisResult]:
        """Run analysis on path."""
        ...

    def supports_fix(self) -> bool:
        """Whether plugin can auto-fix issues."""
        ...

    def fix(self, path: Path, issues: t.SequenceOf[Issue]) -> p.Result[FixResult]:
        """Apply fixes for issues."""
        ...
