# from flext-quality_examples/basic/simple_analysis/README.md:272
from flext_observability import create_metric

# Publish quality metrics to observability stack
create_metric(
    name="project_quality_score",
    value=score,
    tags={"project": project_name, "grade": grade},
)
