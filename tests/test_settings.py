"""Test-specific Django settings."""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Django basics
SECRET_KEY = "test-secret-key-for-flext-quality"
DEBUG = True
USE_TZ = True

# Minimal app configuration
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = []

# Override database settings for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "OPTIONS": {
            "timeout": 20,
        },
        "TEST": {
            "NAME": ":memory:",
        },
    },
}

# Disable foreign key checks for SQLite in tests
if DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
    DATABASES["default"]["OPTIONS"].pop("init_command", None)

# Force syncdb for testing - use the models directly instead of migrations
if "test" in sys.argv or "pytest" in sys.modules:
    # Use a real file-based database for tests to avoid migration issues
    DATABASES["default"]["NAME"] = BASE_DIR / "test_db.sqlite3"

# Test-specific settings
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable logging during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
    },
}

# Celery test settings
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Cache settings for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}
