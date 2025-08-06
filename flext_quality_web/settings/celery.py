"""Celery configuration for background tasks."""

from __future__ import annotations

import os

from celery import Celery  # type: ignore[import-untyped]

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
app = Celery("flext_quality_web")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
# Celery configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)


# Remove debug task as it's not essential for production
# and Celery lacks proper typing support
# If needed, debug tasks can be created in appropriate task modules
