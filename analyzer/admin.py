"""Django REDACTED_LDAP_BIND_PASSWORD configuration for analyzer models."""

from __future__ import annotations

from django.contrib import REDACTED_LDAP_BIND_PASSWORD
from django.utils.html import format_html

from analyzer.models import Project

# Score thresholds for color coding
GOOD_SCORE_THRESHOLD = 80
FAIR_SCORE_THRESHOLD = 60


@REDACTED_LDAP_BIND_PASSWORD.register(Project)
class ProjectAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin[Project]):
    """Admin interface for Project model."""

    list_display = [
        "name",
        "package_name",
        "package_version",
        "package_type",
        "total_files",
        "python_files",
        "latest_score",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "package_type",
        "is_installed_package",
        "created_at",
        "updated_at",
    ]
    search_fields = ["name", "description", "path", "package_name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-updated_at"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "path")},
        ),
        (
            "Package Information",
            {
                "fields": (
                    "package_name",
                    "package_version",
                    "is_installed_package",
                    "install_location",
                    "package_type",
                ),
            },
        ),
        ("Statistics", {"fields": ("total_files", "total_lines", "python_files")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    @REDACTED_LDAP_BIND_PASSWORD.display(
        description="Latest Score",
        ordering="analysissession__overall_score",
    )
    def latest_score(self, obj: Project) -> str:
        """Display the latest analysis score."""
        # Get the latest analysis session using reverse relationship from AnalysisSession
        from analyzer.models import AnalysisSession

        latest = (
            AnalysisSession.objects.filter(flx_project=obj)
            .order_by("-created_at")
            .first()
        )
        if latest and latest.overall_score:
            color = (
                "green"
                if latest.overall_score >= GOOD_SCORE_THRESHOLD
                else "orange"
                if latest.overall_score >= FAIR_SCORE_THRESHOLD
                else "red"
            )
            return format_html(
                '<span style="color: {}; font-weight: bold">{:.1f} ({})</span>',
                color,
                latest.overall_score,
                latest.quality_grade or "N/A",
            )
        return "-"


# Customize REDACTED_LDAP_BIND_PASSWORD site headers
REDACTED_LDAP_BIND_PASSWORD.site.site_header = "Code Analyzer Administration"
REDACTED_LDAP_BIND_PASSWORD.site.site_title = "Code Analyzer Admin"
REDACTED_LDAP_BIND_PASSWORD.site.index_title = "Welcome to Code Analyzer Administration"
