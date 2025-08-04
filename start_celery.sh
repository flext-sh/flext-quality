#!/bin/bash

# Start Celery Worker for Code Analyzer
echo "Starting Celery Worker for Code Analyzer..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
	source venv/bin/activate
	echo "Virtual environment activated"
fi

# Set Django settings
export DJANGO_SETTINGS_MODULE=settings.settings

# Change to Django directory and start Celery worker
cd flext_quality_web
celery -A settings.celery worker --loglevel=info --concurrency=2

echo "Celery worker stopped"
