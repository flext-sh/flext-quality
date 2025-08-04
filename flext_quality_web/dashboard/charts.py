"""Chart data endpoints for dashboard interface."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from analyzer.models import (
    AnalysisSession,
    Project,
    SecurityIssue,
)
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.utils import timezone

if TYPE_CHECKING:
    from django.http import HttpRequest


def dashboard_summary_stats(request: HttpRequest) -> JsonResponse:
    """Return summary statistics for dashboard charts."""
    # Get basic counts
    projects_count = Project.objects.count()
    sessions_count = AnalysisSession.objects.count()
    completed_sessions = AnalysisSession.objects.filter(status="completed").count()
    security_issues_count = SecurityIssue.objects.count()

    # Calculate average score
    avg_score = (
        AnalysisSession.objects.filter(status="completed").aggregate(
            avg=Avg("overall_score"),
        )["avg"]
        or 0
    )

    return JsonResponse(
        {
            "total_projects": projects_count,
            "total_sessions": sessions_count,
            "completed_sessions": completed_sessions,
            "security_issues": security_issues_count,
            "average_score": round(avg_score, 2),
        },
    )


def quality_trends_chart(request: HttpRequest) -> JsonResponse:
    """Return quality trends data for line chart."""
    days = int(request.GET.get("days", 30))

    # Get sessions from the last N days
    cutoff_date = timezone.now() - timedelta(days=days)
    sessions = (
        AnalysisSession.objects.filter(
            created_at__gte=cutoff_date,
            status="completed",
        )
        .order_by("created_at")
        .values("created_at__date", "overall_score")
    )

    # Group by date and calculate average scores
    data_points: dict[str, list[float]] = {}
    for session in sessions:
        date_str = session["created_at__date"].strftime("%Y-%m-%d")
        if date_str not in data_points:
            data_points[date_str] = []
        data_points[date_str].append(session["overall_score"] or 0)

    # Calculate daily averages
    dates = []
    scores = []
    for date_str in sorted(data_points.keys()):
        dates.append(date_str)
        daily_scores = data_points[date_str]
        avg_score = sum(daily_scores) / len(daily_scores) if daily_scores else 0
        scores.append(round(avg_score, 2))

    return JsonResponse(
        {
            "type": "line",
            "data": {
                "labels": dates,
                "datasets": [
                    {
                        "label": "Quality Score",
                        "data": scores,
                        "borderColor": "rgb(54, 162, 235)",
                        "backgroundColor": "rgba(54, 162, 235, 0.2)",
                        "tension": 0.1,
                    },
                ],
            },
        },
    )


def security_issues_distribution(request: HttpRequest) -> JsonResponse:
    """Return security issues distribution for pie chart."""
    # Count security issues by severity
    severity_counts = (
        SecurityIssue.objects.values("severity")
        .annotate(count=Count("id"))
        .order_by("severity")
    )

    labels = []
    data = []
    colors = {
        "CRITICAL": "#dc3545",  # Red
        "HIGH": "#fd7e14",  # Orange
        "MEDIUM": "#ffc107",  # Yellow
        "LOW": "#28a745",  # Green
        "INFO": "#17a2b8",  # Cyan
    }
    background_colors = []

    for item in severity_counts:
        severity = item["severity"]
        count = item["count"]
        labels.append(severity.title())
        data.append(count)
        background_colors.append(colors.get(severity, "#6c757d"))

    return JsonResponse(
        {
            "type": "pie",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "data": data,
                        "backgroundColor": background_colors,
                        "borderWidth": 1,
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
            },
        },
    )


def projects_comparison_chart(request: HttpRequest) -> JsonResponse:
    """Return projects comparison data for bar chart."""
    # Get projects with their latest analysis session scores
    projects = Project.objects.all()

    project_names: list[str] = []
    scores: list[float] = []

    for project in projects:
        latest_session: AnalysisSession | None = (
            project.analysis_sessions.all()
            .filter(status="completed")
            .order_by("-created_at")
            .first()
        )

        project_names.append(project.name)
        scores.append(latest_session.overall_score if latest_session else 0)

    return JsonResponse(
        {
            "type": "bar",
            "data": {
                "labels": project_names,
                "datasets": [
                    {
                        "label": "Quality Score",
                        "data": scores,
                        "backgroundColor": "rgba(54, 162, 235, 0.8)",
                        "borderColor": "rgb(54, 162, 235)",
                        "borderWidth": 1,
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "max": 100,
                    },
                },
            },
        },
    )


def quality_radar_chart(request: HttpRequest) -> JsonResponse:
    """Return quality metrics radar chart data."""
    # Get the latest completed session for radar chart
    latest_session: AnalysisSession | None = (
        AnalysisSession.objects.all()
        .filter(status="completed")
        .order_by("-created_at")
        .first()
    )

    if not latest_session:
        return JsonResponse(
            {
                "type": "radar",
                "data": {
                    "labels": [
                        "Security",
                        "Complexity",
                        "Documentation",
                        "Duplicates",
                        "Dead Code",
                    ],
                    "datasets": [
                        {
                            "label": "No Data",
                            "data": [0, 0, 0, 0, 0],
                            "backgroundColor": "rgba(255, 99, 132, 0.2)",
                            "borderColor": "rgb(255, 99, 132)",
                            "pointBackgroundColor": "rgb(255, 99, 132)",
                        },
                    ],
                },
            },
        )

    # Calculate metrics based on session data
    security_score: int = max(
        0,
        100 - (SecurityIssue.objects.filter(session=latest_session).count() * 5),
    )
    complexity_score: int = latest_session.overall_score or 0
    documentation_score: int = 80  # Placeholder - would need specific metric
    duplicates_score: int = 75  # Placeholder - would need specific metric
    dead_code_score: int = 85  # Placeholder - would need specific metric

    return JsonResponse(
        {
            "type": "radar",
            "data": {
                "labels": [
                    "Security",
                    "Complexity",
                    "Documentation",
                    "Duplicates",
                    "Dead Code",
                ],
                "datasets": [
                    {
                        "label": "Quality Metrics",
                        "data": [
                            security_score,
                            complexity_score,
                            documentation_score,
                            duplicates_score,
                            dead_code_score,
                        ],
                        "backgroundColor": "rgba(54, 162, 235, 0.2)",
                        "borderColor": "rgb(54, 162, 235)",
                        "pointBackgroundColor": "rgb(54, 162, 235)",
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "scales": {
                    "r": {
                        "beginAtZero": True,
                        "max": 100,
                    },
                },
            },
        },
    )


def issues_timeline_chart(request: HttpRequest) -> JsonResponse:
    """Return issues timeline data for line chart."""
    days = int(request.GET.get("days", 30))

    # Get issues from the last N days
    cutoff_date = timezone.now() - timedelta(days=days)
    issues = (
        SecurityIssue.objects.filter(detected_at__gte=cutoff_date)
        .values("detected_at__date")
        .annotate(count=Count("id"))
        .order_by("detected_at__date")
    )

    dates = []
    counts = []

    for issue_data in issues:
        dates.append(issue_data["detected_at__date"].strftime("%Y-%m-%d"))
        counts.append(issue_data["count"])

    return JsonResponse(
        {
            "type": "line",
            "data": {
                "labels": dates,
                "datasets": [
                    {
                        "label": "Issues Detected",
                        "data": counts,
                        "borderColor": "rgb(255, 99, 132)",
                        "backgroundColor": "rgba(255, 99, 132, 0.2)",
                        "tension": 0.1,
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "scales": {
                    "y": {
                        "beginAtZero": True,
                    },
                },
            },
        },
    )


def complexity_distribution_chart(request: HttpRequest) -> JsonResponse:
    """Return complexity distribution data for bar chart."""
    from analyzer.models import FunctionAnalysis

    # Count functions by complexity level
    complexity_counts = (
        FunctionAnalysis.objects.values("complexity_level")
        .annotate(count=Count("id"))
        .order_by("complexity_level")
    )

    labels = []
    data = []
    colors = {
        "low": "#28a745",  # Green
        "medium": "#ffc107",  # Yellow
        "high": "#fd7e14",  # Orange
        "very_high": "#dc3545",  # Red
    }
    background_colors = []

    for item in complexity_counts:
        level = item["complexity_level"] or "unknown"
        count = item["count"]
        labels.append(level.replace("_", " ").title())
        data.append(count)
        background_colors.append(colors.get(level, "#6c757d"))

    return JsonResponse(
        {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Function Count",
                        "data": data,
                        "backgroundColor": background_colors,
                        "borderWidth": 1,
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "scales": {
                    "y": {
                        "beginAtZero": True,
                    },
                },
            },
        },
    )
