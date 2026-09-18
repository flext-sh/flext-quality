# from flext-quality/docs/getting-started.md:155
from __future__ import annotations
from flext_quality import FlextQualityService
from flext_quality import FlextQualityCodeAnalyzer


# Option 1: Service Layer Approach
def service_analysis():
    service = FlextQualityService()

    # Create project with quality thresholds
    project_result = service.create_project(
        name="my_project",
        project_path="./src",
        _min_coverage=85.0,  # Note: internal parameter name
        _max_complexity=10,
    )

    if project_result.success:
        project = project_result.value
        print(f"✅ Project: {project.name}")
        print(f"📁 Path: {project.project_path}")
        print(f"🎯 Min Coverage: {project.min_coverage}")


# Option 2: Direct Analysis Engine
def direct_analysis():
    # Analyze project directly
    analyzer = FlextQualityCodeAnalyzer("./src")

    # Run comprehensive analysis
    analysis_result = analyzer.analyze_project(
        include_security=True,
        include_complexity=True,
        include_dead_code=True,
        include_duplicates=True,
    )

    # Get results
    score = analyzer.get_quality_score()
    grade = analyzer.get_quality_grade()

    print(f"📊 Quality Score: {score}")
    print(f"🏆 Quality Grade: {grade}")
    print(f"📄 Files Analyzed: {analysis_result.overall_metrics.files_analyzed}")
    print(f"📏 Total Lines: {analysis_result.overall_metrics.total_lines}")


# Run both approaches
run(service_analysis())
direct_analysis()
