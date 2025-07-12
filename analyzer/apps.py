from pydantic import Field

"""Django app configuration for analyzer.

from __future__ import annotations

from django.apps import AppConfig

from analyzer import signals  # noqa:
            F401  # TODO: Move import to module level


class AnalyzerConfig(AppConfig):
         """Configuration for the analyzer app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "analyzer"
    verbose_name = "Code Analyzer"

    def ready(self) -> None:
        pass