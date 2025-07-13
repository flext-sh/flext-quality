"""Django REDACTED_LDAP_BIND_PASSWORD configuration for analyzer models.

from __future__ import annotations

from typing import Any, ClassVar

from analyzer.models import (
    AnalysisBackendModel,
    AnalysisSession,
    BackendStatistics,
    ClassAnalysis,
    ClassVar,
    DeadCodeIssue,
    DetectedIssue,
    DuplicateCodeBlock,
    DuplicateLocation,
    FileAnalysis,
    FunctionAnalysis,
    ImportAnalysis,
    IssueType,
    PackageAnalysis,
    Project,
    QualityMetrics,
    SecurityIssue,
    VariableAnalysis,
    from,
    import,
    typing,
)
from django.contrib import REDACTED_LDAP_BIND_PASSWORD
from django.utils.html import format_html


@REDACTED_LDAP_BIND_PASSWORD.register(Project)
class ProjectAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
    """Admin interface for Project model."""

    list_display: ClassVar[list[str]] = ["name",
        "package_name",
        "package_version",
        "package_type",
        "total_files",
        "python_files",
        "latest_score",
        "created_at",
        "updated_at",
    ]
    list_filter: ClassVar[list[str]] = ["package_type",
        "is_installed_package",
        "created_at",
        "updated_at",
    ]
    search_fields: ClassVar[list[str]] = ["name", "description", "path", "package_name"]
    readonly_fields: ClassVar[list[str]] = ["created_at", "updated_at"]
    ordering: ClassVar[list[str]] = ["-updated_at"]

    fieldsets: ClassVar = (
        (
            "Basic Information",
            {"fields": ("name", "description", "path")},
        ),
        (
            "Package Information",
            {"fields": (
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

    def latest_score(self, obj) -> str:
        latest = obj.analysis_sessions.first()
        if latest and latest.overall_score:
            color = (
                "green"
                if latest.overall_score >= 80 else "orange" if latest.overall_score >= 60 else "red":
                    )
            return format_html('<span style="color: {}
                font-weight: bold
                ">{:.1f} ({})</span>',
                color,
                latest.overall_score,
                latest.quality_grade or "N/A",
            )
        return "-"

    latest_score.short_description = "Latest Score"
    latest_score.REDACTED_LDAP_BIND_PASSWORD_order_field = "analysis_sessions__overall_score"


class FileAnalysisInline(REDACTED_LDAP_BIND_PASSWORD.TabularInline):
         """Inline REDACTED_LDAP_BIND_PASSWORD for FileAnalysis."""

    model = FileAnalysis
    extra = 0
    readonly_fields:
            ClassVar = ["created_at"]
    fields: ClassVar = ["file_name",
        "lines_of_code",
        "complexity_score",
        "function_count",
        "class_count",
    ]


class SecurityIssueInline(REDACTED_LDAP_BIND_PASSWORD.TabularInline):
         """Inline REDACTED_LDAP_BIND_PASSWORD for SecurityIssue."""

    model = SecurityIssue
    extra = 0
    readonly_fields:
            ClassVar = ["created_at"]
    fields: ClassVar = ["severity",
        "issue_type",
        "file_path",
        "line_number",
        "is_resolved",
    ]


@REDACTED_LDAP_BIND_PASSWORD.register(AnalysisSession)
class AnalysisSessionAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """Admin interface for AnalysisSession model."""

    list_display:
            ClassVar = ["id",
        "flx_project",
        "status_badge",
        "overall_score_badge",
        "duration_display",
        "created_at",
    ]
    list_filter: ClassVar = ["status",
        "include_security",
        "include_dead_code",
        "include_duplicates",
        "created_at",
    ]
    search_fields: ClassVar = ["flx_project__name", "id"]
    readonly_fields: ClassVar = ["id",
        "started_at",
        "completed_at",
        "created_at",
        "duration_display",
        "overall_score",
        "quality_grade",
    ]
    ordering: ClassVar = ["-created_at"]

    fieldsets: ClassVar = (
        (
            "Session Information",
            {"fields": ("id", "flx_project", "status", "error_message")},
        ),
        (
            "Analysis Configuration",
            {"fields": (
                    "include_security",
                    "include_dead_code",
                    "include_duplicates",
                    "include_documentation",
                    "include_complexity",
                    "complexity_threshold",
                    "similarity_threshold",
                ),
            },
        ),
        (
            "Results",
            {"fields": ("overall_score", "quality_grade"),
            },
        ),
        (
            "Timestamps",
            {"fields": (
                    "created_at",
                    "started_at",
                    "completed_at",
                    "duration_display",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    inlines: ClassVar = [SecurityIssueInline]

    def status_badge(self, obj) -> str:
        colors = {"pending": "orange",
            "running": "blue",
            "completed": "green",
            "failed": "red",
            "cancelled": "gray",
        }
        color = colors.get(obj.status, "gray")
        return format_html('<span style="color: {}
            font-weight: bold
            ">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"
    status_badge.REDACTED_LDAP_BIND_PASSWORD_order_field = "status"

    def overall_score_badge(self, obj) -> str:
        if obj.overall_score is None:
            return "-"

        color = (
            "green"
            if obj.overall_score >= 80 else "orange" if obj.overall_score >= 60 else "red":
                )
        return format_html('<span style="color: {}
            font-weight: bold
            ">{:.1f}</span>',
            color,
            obj.overall_score,
        )

    overall_score_badge.short_description = "Score"
    overall_score_badge.REDACTED_LDAP_BIND_PASSWORD_order_field = "overall_score"

    def duration_display(self, obj) -> str:
        duration = obj.duration
        if duration is None:
            return "-"

        if duration < 60:
            return f"{duration}s"
        if duration < 3600:
            return f"{duration // 60}m {duration % 60}s"
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        return f"{hours}h {minutes}m"

    duration_display.short_description = "Duration"


@REDACTED_LDAP_BIND_PASSWORD.register(FileAnalysis)
class FileAnalysisAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """Admin interface for FileAnalysis model."""

    list_display:
            ClassVar = ["file_name",
        "session",
        "lines_of_code",
        "complexity_score_badge",
        "function_count",
        "class_count",
        "created_at",
    ]
    list_filter: ClassVar = ["session__flx_project",
        "session__status",
        "created_at",
    ]
    search_fields: ClassVar = ["file_name", "file_path", "session__flx_project__name"]
    readonly_fields: ClassVar = ["created_at"]
    ordering: ClassVar = ["-complexity_score"]

    def complexity_score_badge(self, obj) -> str:
        score = obj.complexity_score
        color = "green" if score >= 80 else "orange" if score >= 60 else "red":
        return format_html('<span style="color:
            {}
            font-weight: bold
            ">{:.1f}</span>',
            color,
            score,
        )

    complexity_score_badge.short_description = "Complexity"
    complexity_score_badge.REDACTED_LDAP_BIND_PASSWORD_order_field = "complexity_score"


@REDACTED_LDAP_BIND_PASSWORD.register(SecurityIssue)
class SecurityIssueAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """Admin interface for SecurityIssue model."""

    list_display:
            ClassVar = ["severity_badge",
        "issue_type",
        "file_path",
        "line_number",
        "confidence",
        "is_resolved",
        "created_at",
    ]
    list_filter: ClassVar = ["severity",
        "confidence",
        "issue_type",
        "is_resolved",
        "session__flx_project",
        "created_at",
    ]
    search_fields: ClassVar = ["issue_type", "file_path", "description"]
    readonly_fields: ClassVar = ["created_at", "resolved_at"]
    ordering: ClassVar = ["-severity", "-created_at"]

    fieldsets: ClassVar = (
        (
            "Issue Information",
            {"fields": ("severity", "confidence", "issue_type", "test_id")},
        ),
        ("Location", {"fields": ("file_path", "line_number", "code_snippet")}),
        ("Details", {"fields": ("description", "recommendation")}),
        ("Resolution", {"fields": ("is_resolved", "resolved_at", "resolution_notes")}),
        (
            "Metadata",
            {"fields": ("session", "file_analysis", "created_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def severity_badge(self, obj) -> str:
        colors = {"HIGH": "red",
            "MEDIUM": "orange",
            "LOW": "green",
            "INFO": "blue",
        }
        color = colors.get(obj.severity, "gray")
        return format_html('<span style="color: {}
            font-weight: bold
            ">{}</span>',
            color,
            obj.severity,
        )

    severity_badge.short_description = "Severity"
    severity_badge.REDACTED_LDAP_BIND_PASSWORD_order_field = "severity"


@REDACTED_LDAP_BIND_PASSWORD.register(DeadCodeIssue)
class DeadCodeIssueAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """Admin interface for DeadCodeIssue model."""

    list_display:
            ClassVar = ["dead_type",
        "name",
        "file_path",
        "line_number",
        "confidence_badge",
        "size_estimate",
        "is_resolved",
        "created_at",
    ]
    list_filter: ClassVar = ["dead_type",
        "is_resolved",
        "session__flx_project",
        "created_at",
    ]
    search_fields: ClassVar = ["name", "file_path"]
    readonly_fields: ClassVar = ["created_at", "resolved_at"]
    ordering: ClassVar = ["-confidence", "-size_estimate"]

    def confidence_badge(self, obj) -> str:
        confidence = obj.confidence
        color = (
            "green" if confidence >= 0.8 else "orange" if confidence >= 0.6 else "red":
        )
        return format_html('<span style="color:
            {}
            font-weight: bold
            ">{:.1%}</span>',
            color,
            confidence,
        )

    confidence_badge.short_description = "Confidence"
    confidence_badge.REDACTED_LDAP_BIND_PASSWORD_order_field = "confidence"


class DuplicateLocationInline(REDACTED_LDAP_BIND_PASSWORD.TabularInline):
         """Inline REDACTED_LDAP_BIND_PASSWORD for DuplicateLocation."""

    model = DuplicateLocation
    extra = 0
    fields:
            ClassVar = ["file_path", "start_line", "end_line", "function_name"]


@REDACTED_LDAP_BIND_PASSWORD.register(DuplicateCodeBlock)
class DuplicateCodeBlockAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """Admin interface for DuplicateCodeBlock model."""

    list_display:
            ClassVar = ["session",
        "lines_count",
        "similarity_score_badge",
        "locations_count",
        "is_resolved",
        "created_at",
    ]
    list_filter: ClassVar = ["is_resolved",
        "session__flx_project",
        "created_at",
    ]
    search_fields: ClassVar = ["block_hash", "content_preview"]
    readonly_fields: ClassVar = ["created_at", "resolved_at", "locations_count"]
    ordering: ClassVar = ["-lines_count", "-similarity_score"]

    inlines: ClassVar = [DuplicateLocationInline]

    fieldsets: ClassVar = (
        (
            "Block Information",
            {"fields": ("block_hash", "lines_count", "similarity_score")},
        ),
        ("Content", {"fields": ("content_preview",)}),
        ("Resolution", {"fields": ("is_resolved", "resolved_at")}),
        (
            "Metadata",
            {"fields": ("session", "created_at", "locations_count"),
                "classes": ("collapse",),
            },
        ),
    )

    def similarity_score_badge(self, obj) -> str:
        score = obj.similarity_score
        color = "red" if score >= 0.9 else "orange" if score >= 0.8 else "green":
        return format_html('<span style="color:
            {}
            font-weight: bold
            ">{:.1%}</span>',
            color,
            score,
        )

    similarity_score_badge.short_description = "Similarity"
    similarity_score_badge.REDACTED_LDAP_BIND_PASSWORD_order_field = "similarity_score"

    def locations_count(self, obj) -> int:
        return obj.locations.count()

    locations_count.short_description = "Locations"


@REDACTED_LDAP_BIND_PASSWORD.register(QualityMetrics)
class QualityMetricsAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """Admin interface for QualityMetrics model."""

    list_display:
            ClassVar = ["session",
        "overall_score_badge",
        "security_score",
        "complexity_score",
        "technical_debt_ratio",
        "created_at",
    ]
    list_filter: ClassVar = ["session__flx_project",
        "created_at",
    ]
    readonly_fields: ClassVar = ["created_at"]
    ordering: ClassVar = ["-overall_score"]

    fieldsets: ClassVar = (
        ("Overall Quality", {"fields": ("overall_score", "session")}),
        (
            "Component Scores",
            {"fields": (
                    "complexity_score",
                    "maintainability_score",
                    "security_score",
                    "documentation_score",
                    "duplication_score",
                ),
            },
        ),
        (
            "Size Metrics",
            {"fields": (
                    "total_files",
                    "total_lines",
                    "total_functions",
                    "total_classes",
                ),
            },
        ),
        (
            "Complexity Metrics",
            {"fields": (
                    "avg_complexity",
                    "max_complexity",
                    "complex_functions_count",
                ),
            },
        ),
        (
            "Quality Indicators",
            {"fields": (
                    "docstring_coverage",
                    "documented_functions",
                    "security_issues_count",
                    "dead_code_items_count",
                    "duplicate_blocks_count",
                    "duplicate_lines_ratio",
                ),
            },
        ),
        (
            "Technical Debt",
            {"fields": (
                    "technical_debt_ratio",
                    "estimated_debt_hours",
                ),
            },
        ),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def overall_score_badge(self, obj) -> str:
        score = obj.overall_score
        color = "green" if score >= 80 else "orange" if score >= 60 else "red":
        return format_html('<span style="color:
            {}
            font-weight: bold
            ">{:.1f}</span>',
            color,
            score,
        )

    overall_score_badge.short_description = "Overall Score"
    overall_score_badge.REDACTED_LDAP_BIND_PASSWORD_order_field = "overall_score"


@REDACTED_LDAP_BIND_PASSWORD.register(PackageAnalysis)
class PackageAnalysisAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display = (
        "name",
        "session",
        "python_files_count",
        "total_functions",
        "total_classes",
        "avg_complexity",
    )
    list_filter = ("session", "avg_complexity")
    search_fields = ("name", "full_path")
    readonly_fields = ("created_at",)


@REDACTED_LDAP_BIND_PASSWORD.register(ClassAnalysis)
class ClassAnalysisAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display = (
        "name",
        "package_analysis",
        "method_count",
        "complexity_level",
        "has_docstring",
    )
    list_filter = ("complexity_level", "has_docstring", "is_abstract", "is_dataclass")
    search_fields = ("name", "full_name")
    readonly_fields = ("created_at",)


@REDACTED_LDAP_BIND_PASSWORD.register(FunctionAnalysis)
class FunctionAnalysisAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display = (
        "name",
        "function_type",
        "cyclomatic_complexity",
        "complexity_level",
        "has_docstring",
    )
    list_filter = (
        "function_type",
        "complexity_level",
        "has_docstring",
        "has_type_hints",
    )
    search_fields = ("name", "full_name")
    readonly_fields = ("created_at",)


@REDACTED_LDAP_BIND_PASSWORD.register(VariableAnalysis)
class VariableAnalysisAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display = ("name", "variable_type", "scope_type", "is_constant", "is_unused")
    list_filter = ("variable_type", "scope_type", "is_constant", "is_unused")
    search_fields = ("name", "full_name")
    readonly_fields = ("created_at",)


@REDACTED_LDAP_BIND_PASSWORD.register(ImportAnalysis)
class ImportAnalysisAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display = (
        "module_name",
        "import_name",
        "import_type",
        "is_wildcard",
        "is_unused",
    )
    list_filter = ("import_type", "is_wildcard", "is_unused", "is_circular")
    search_fields = ("module_name", "import_name")
    readonly_fields = ("created_at",)


# === BACKEND MANAGEMENT ADMIN ===


@REDACTED_LDAP_BIND_PASSWORD.register(AnalysisBackendModel)
class AnalysisBackendModelAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display: ClassVar = ["name",
        "display_name",
        "is_active",
        "is_available",
        "execution_order",
        "created_at",
    ]
    list_filter: ClassVar = ["is_active", "is_available", "created_at"]
    search_fields: ClassVar = ["name", "display_name", "description"]
    readonly_fields: ClassVar = ["created_at", "updated_at", "last_check_at"]
    ordering: ClassVar = ["execution_order", "name"]

    fieldsets: ClassVar = [(
            "Basic Information",
            {"fields": ["name", "display_name", "description", "version"],
            },
        ),
        (
            "Configuration",
            {"fields": ["is_active",
                    "is_available",
                    "default_enabled",
                    "execution_order",
                    "capabilities",
                ],
            },
        ),
        (
            "Metadata",
            {"fields": ["created_at", "updated_at", "last_check_at"],
                "classes": ["collapse"],
            },
        ),
    ]


@REDACTED_LDAP_BIND_PASSWORD.register(IssueType)
class IssueTypeAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display: ClassVar = ["code",
        "name",
        "backend",
        "category",
        "severity",
        "is_active",
    ]
    list_filter: ClassVar = ["backend",
        "category",
        "severity",
        "is_active",
        "created_at",
    ]
    search_fields: ClassVar = ["code", "name", "description"]
    readonly_fields: ClassVar = ["created_at", "updated_at"]
    ordering: ClassVar = ["backend__name", "code"]

    fieldsets: ClassVar = [(
            "Basic Information",
            {"fields": ["backend", "code", "name", "description"],
            },
        ),
        (
            "Classification",
            {"fields": ["category", "severity", "is_active"],
            },
        ),
        (
            "Documentation",
            {"fields": ["recommendation", "documentation_url", "examples"],
                "classes": ["collapse"],
            },
        ),
        (
            "Metadata",
            {"fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]


@REDACTED_LDAP_BIND_PASSWORD.register(DetectedIssue)
class DetectedIssueAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display: ClassVar = ["issue_type_code",
        "file_path",
        "line_number",
        "severity",
        "is_resolved",
        "detected_at",
    ]
    list_filter: ClassVar = ["issue_type__backend",
        "issue_type__category",
        "issue_type__severity",
        "is_resolved",
        "is_false_positive",
        "confidence",
        "detected_at",
    ]
    search_fields: ClassVar = ["file_path",
        "message",
        "issue_type__code",
        "issue_type__name",
    ]
    readonly_fields: ClassVar = ["detected_at", "severity", "category", "backend_name"]
    date_hierarchy = "detected_at"
    ordering: ClassVar = ["-detected_at"]

    def issue_type_code(self, obj) -> Any:
        return obj.issue_type.code

    issue_type_code.short_description = "Issue Code"
    issue_type_code.REDACTED_LDAP_BIND_PASSWORD_order_field = "issue_type__code"

    def severity(self, obj) -> Any:
        return obj.issue_type.severity

    severity.short_description = "Severity"
    severity.REDACTED_LDAP_BIND_PASSWORD_order_field = "issue_type__severity"

    fieldsets: ClassVar = [(
            "Issue Information",
            {"fields": ["session", "issue_type", "file_analysis"],
            },
        ),
        (
            "Location",
            {"fields": ["file_path", "line_number", "column"],
            },
        ),
        (
            "Details",
            {"fields": ["message",
                    "code_snippet",
                    "confidence",
                    "context",
                    "raw_data",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Classification",
            {"fields": ["backend_name", "category", "severity"],
                "classes": ["collapse"],
            },
        ),
        (
            "Resolution",
            {"fields": ["is_false_positive",
                    "is_resolved",
                    "resolved_at",
                    "resolution_notes",
                ],
            },
        ),
        (
            "Metadata",
            {"fields": ["detected_at"],
                "classes": ["collapse"],
            },
        ),
    ]


@REDACTED_LDAP_BIND_PASSWORD.register(BackendStatistics)
class BackendStatisticsAdmin(REDACTED_LDAP_BIND_PASSWORD.ModelAdmin):
         """TODO: Add docstring."""

    list_display: ClassVar = ["backend",
        "session",
        "status",
        "execution_time",
        "files_processed",
        "issues_found",
        "created_at",
    ]
    list_filter: ClassVar = ["backend", "status", "created_at"]
    search_fields: ClassVar = ["backend__name", "session__name"]
    readonly_fields: ClassVar = ["created_at"]
    date_hierarchy = "created_at"
    ordering: ClassVar = ["-created_at"]

    fieldsets: ClassVar = [(
            "Basic Information",
            {"fields": ["session", "backend", "status"],
            },
        ),
        (
            "Execution Metrics",
            {"fields": ["execution_time", "files_processed", "issues_found"],
            },
        ),
        (
            "Results Breakdown",
            {"fields": ["issues_by_severity", "issues_by_category"],
                "classes": ["collapse"],
            },
        ),
        (
            "Error Information",
            {"fields": ["error_message"],
                "classes": ["collapse"],
            },
        ),
        (
            "Metadata",
            {"fields": ["created_at"],
                "classes": ["collapse"],
            },
        ),
    ]


# Customize REDACTED_LDAP_BIND_PASSWORD site headers
REDACTED_LDAP_BIND_PASSWORD.site.site_header = "Code Analyzer Administration"
REDACTED_LDAP_BIND_PASSWORD.site.site_title = "Code Analyzer Admin"
REDACTED_LDAP_BIND_PASSWORD.site.index_title = "Welcome to Code Analyzer Administration"
