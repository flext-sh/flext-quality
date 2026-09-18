# from flext-quality_docs/DUPLICATION-DETECTION.md:226
from flext_quality import FlextQualityAnalyzer

analyzer = FlextQualityAnalyzer(".")
result = analyzer.analyze_project(options=AnalysisOptions(include_duplicates=True))

# Duplication issues are included in results
for issue in result.value.issues:
    if issue.rule_id == "duplication_check":
        print(f"Duplicate code: {issue.message}")
