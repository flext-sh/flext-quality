# from flext-quality/examples/README.md:134
from __future__ import annotations

# examples/integration/flext_ecosystem.py
from flext_quality import QualityAPI
from flext_cli import u
from flext_core import FlextSettings
from flext_observability import create_metric

# Initialize with dependency injection
container = FlextContainer()
quality_api = QualityAPI(container)


# Execute analysis with observability
def analyze_with_monitoring(project_path: str):
    result = quality_api.analyze_project(project_path)

    # Use current API pattern
    data = result.unwrap_or(None)
    if data is not None:
        # Publish metrics to observability stack
        create_metric(
            name="project_quality_score",
            value=data.overall_score,
            tags={"project": project_path},
        )
        return data
    else:
        u.Cli.info(f"Analysis failed: {result.error}")
        return None
