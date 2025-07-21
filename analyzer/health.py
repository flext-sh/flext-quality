"""Health check utilities for the dc-code-analyzer application."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    from celery import current_app

    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False


def check_database() -> dict[str, Any]:
    """Check database connection health."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return {
                "status": "healthy" if result and result[0] == 1 else "unhealthy",
                "details": "Database connection successful",
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "details": f"Database connection failed: {e!s}",
        }


def check_cache() -> dict[str, Any]:
    """Check cache connection health."""
    try:
        test_key = "health_check_test"
        test_value = "ok"

        cache.set(test_key, test_value, 30)
        cached_value = cache.get(test_key)

        if cached_value == test_value:
            cache.delete(test_key)
            return {"status": "healthy", "details": "Cache working properly"}
        return {"status": "unhealthy", "details": "Cache test failed"}
    except (ConnectionError, TimeoutError, OSError) as e:
        return {"status": "unhealthy", "details": f"Cache connection failed: {e!s}"}


def check_redis() -> dict[str, Any]:
    """Check Redis connection health."""
    if not REDIS_AVAILABLE:
        return {"status": "unknown", "details": "Redis client not available"}

    try:
        redis_url = getattr(settings, "CELERY_BROKER_URL", "redis://localhost:6379/0")
        r = redis.from_url(redis_url)
        r.ping()
    except (ConnectionError, TimeoutError, redis.RedisError) as e:
        return {"status": "unhealthy", "details": f"Redis connection failed: {e!s}"}
    else:
        return {"status": "healthy", "details": "Redis connection successful"}


def check_celery() -> dict[str, Any]:
    """Check Celery workers health."""
    if not CELERY_AVAILABLE:
        return {"status": "unknown", "details": "Celery not available"}

    try:
        # Check if workers are available
        inspect = current_app.control.inspect()
        stats = inspect.stats()

        if stats:
            active_workers = len(stats)
            return {
                "status": "healthy",
                "details": f"Celery has {active_workers} active workers",
            }
        return {"status": "unhealthy", "details": "No active Celery workers found"}
    except (OSError, ConnectionError, TimeoutError) as e:
        return {"status": "unhealthy", "details": f"Celery check failed: {e!s}"}


@csrf_exempt
@never_cache
@require_http_methods(["GET", "HEAD"])
def health_check(request: HttpRequest) -> JsonResponse:
    """Comprehensive health check endpoint."""
    start_time = time.time()

    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "redis": check_redis(),
        "celery": check_celery(),
    }

    # Determine overall status
    overall_status = "healthy"
    for check_result in checks.values():
        if check_result["status"] == "unhealthy":
            overall_status = "unhealthy"
            break
        if check_result["status"] == "unknown" and overall_status == "healthy":
            overall_status = "degraded"

    response_time = time.time() - start_time

    response_data = {
        "status": overall_status,
        "timestamp": time.time(),
        "response_time_ms": round(response_time * 1000, 2),
        "version": "1.0.0",
        "checks": checks,
        "environment": {
            "debug": settings.DEBUG,
            "python_version": (
                f"{settings.PYTHON_VERSION}"
                if hasattr(settings, "PYTHON_VERSION")
                else "unknown"
            ),
        },
    }

    # Set HTTP status code based on health
    status_code = 200 if overall_status == "healthy" else 503

    return JsonResponse(response_data, status=status_code)


@csrf_exempt
@never_cache
@require_http_methods(["GET", "HEAD"])
def readiness_check(request: HttpRequest) -> JsonResponse:
    """Readiness check endpoint for Kubernetes."""
    # Check critical services only
    db_check = check_database()

    if db_check["status"] == "healthy":
        return JsonResponse({"status": "ready"}, status=200)
    return JsonResponse(
        {"status": "not ready", "reason": db_check["details"]},
        status=503,
    )


@csrf_exempt
@never_cache
@require_http_methods(["GET", "HEAD"])
def liveness_check(request: HttpRequest) -> JsonResponse:
    """Liveness check endpoint for Kubernetes."""
    return JsonResponse({"status": "alive", "timestamp": time.time()}, status=200)
