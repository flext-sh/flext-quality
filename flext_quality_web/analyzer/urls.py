"""URL configuration for the analyzer Django app.

This module contains URL patterns for the code analysis views.
"""

from __future__ import annotations

from django.urls import path
from analyzer import views

app_name = "analyzer"

urlpatterns = [
    # Basic analyzer URLs - placeholder for now
    path("", views.health_check, name="health"),
]
