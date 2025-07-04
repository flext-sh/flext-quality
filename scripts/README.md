# 🛠️ DC Code Analyzer - Scripts and Utilities

> **Module**: Scripts and utilities for DC Code Analyzer operations and maintenance | **Audience**: DevOps Engineers, System Administrators, Developers | **Status**: Production Ready

## 📋 **Overview**

Comprehensive collection of scripts and utilities for the DC Code Analyzer application, providing essential functionality for deployment, maintenance, analysis operations, and system management. These scripts demonstrate best practices for Django application automation and code analysis workflows.

---

## 🧭 **Navigation Context**

**🏠 Root**: [PyAuto Home](../../README.md) → **📂 Component**: [DC Code Analyzer](../README.md) → **📂 Current**: Scripts and Utilities

---

## 🎯 **Module Purpose**

This scripts module provides essential automation utilities for the DC Code Analyzer, including service management, deployment automation, analysis execution, maintenance tasks, and utility functions for the Django-based code analysis system.

### **Key Script Categories**

- **Service Management** - Service startup and management scripts
- **Analysis Scripts** - Code analysis execution and automation
- **Deployment Scripts** - Deployment and environment setup
- **Maintenance Scripts** - System maintenance and cleanup
- **Utility Scripts** - Common utilities and helper functions
- **Development Scripts** - Development workflow automation

---

## 📁 **Scripts Structure**

```
scripts/
├── service_management/
│   ├── start_all.sh                      # Start all services
│   ├── start_server.sh                   # Start Django server
│   ├── start_celery.sh                   # Start Celery workers
│   ├── start_redis.sh                    # Start Redis server
│   ├── stop_all.sh                       # Stop all services
│   └── restart_services.sh               # Restart all services
├── analysis/
│   ├── run_analysis.py                   # Run code analysis
│   ├── batch_analysis.py                 # Batch project analysis
│   ├── scheduled_analysis.py             # Scheduled analysis tasks
│   └── analysis_monitor.py               # Monitor analysis progress
├── deployment/
│   ├── deploy.sh                         # Production deployment
│   ├── setup_environment.sh              # Environment setup
│   ├── migrate_database.sh               # Database migrations
│   └── collect_static.sh                 # Collect static files
├── maintenance/
│   ├── cleanup_old_sessions.py           # Clean old analysis sessions
│   ├── backup_database.py                # Database backup
│   ├── optimize_database.py              # Database optimization
│   └── clear_cache.py                    # Clear application cache
├── utilities/
│   ├── check_detected_issues.py          # Check detected issues
│   ├── generate_reports.py               # Generate analysis reports
│   ├── export_data.py                    # Export analysis data
│   └── import_projects.py                # Import projects for analysis
└── development/
    ├── setup_dev_env.sh                  # Development environment setup
    ├── run_tests.sh                      # Run test suite
    ├── generate_fixtures.py              # Generate test fixtures
    └── debug_analysis.py                 # Debug analysis issues
```

---

## 🔧 **Script Categories**

### **1. Service Management Scripts**

#### **Start All Services (start_all.sh)**

```bash
#!/bin/bash
# Start all DC Code Analyzer services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Starting DC Code Analyzer services..."

# Activate virtual environment if exists
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Start Redis
echo "Starting Redis server..."
redis-server --daemonize yes

# Wait for Redis to start
sleep 2

# Start Celery workers
echo "Starting Celery workers..."
cd "$PROJECT_ROOT"
celery -A code_analyzer_web worker --loglevel=info --detach

# Start Celery beat for scheduled tasks
echo "Starting Celery beat..."
celery -A code_analyzer_web beat --loglevel=info --detach

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &

echo "All services started successfully!"
echo "DC Code Analyzer is available at http://localhost:8000"
echo ""
echo "To stop all services, run: ./scripts/stop_all.sh"
```

#### **Start Celery Workers (start_celery.sh)**

```bash
#!/bin/bash
# Start Celery workers for background task processing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
WORKER_NAME="dc_analyzer_worker"
CONCURRENCY=4
LOG_LEVEL="info"
LOG_FILE="$PROJECT_ROOT/logs/celery.log"

# Ensure log directory exists
mkdir -p "$PROJECT_ROOT/logs"

# Activate virtual environment
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

cd "$PROJECT_ROOT"

# Stop existing workers
echo "Stopping existing Celery workers..."
celery -A code_analyzer_web control shutdown || true

# Start new worker
echo "Starting Celery worker..."
celery -A code_analyzer_web worker \
    --loglevel=$LOG_LEVEL \
    --concurrency=$CONCURRENCY \
    --hostname=$WORKER_NAME@%h \
    --logfile=$LOG_FILE \
    --detach

# Start Celery beat for scheduled tasks
echo "Starting Celery beat..."
celery -A code_analyzer_web beat \
    --loglevel=$LOG_LEVEL \
    --logfile="$PROJECT_ROOT/logs/celery-beat.log" \
    --detach

echo "Celery workers started successfully!"
echo "Worker name: $WORKER_NAME"
echo "Concurrency: $CONCURRENCY"
echo "Log file: $LOG_FILE"
```

### **2. Analysis Scripts**

#### **Run Code Analysis (run_analysis.py)**

```python
#!/usr/bin/env python3
"""Run code analysis for projects in DC Code Analyzer.

This script provides CLI interface for running code analysis
on projects with various configuration options.
"""

import argparse
import sys
import os
import django
from pathlib import Path
from typing import List, Dict, Any, Optional

# Django setup
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_analyzer_web.settings')
django.setup()

from analyzer.models import Project, AnalysisSession
from analyzer.tasks import run_analysis_task
from analyzer.multi_backend_analyzer import MultiBackendAnalyzer

class AnalysisRunner:
    """Code analysis runner."""

    def __init__(self):
        self.analyzer = MultiBackendAnalyzer()

    def run_analysis(
        self,
        project_id: int,
        backends: List[str],
        config: Dict[str, Any],
        async_mode: bool = True
    ) -> AnalysisSession:
        """Run analysis for a project."""
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValueError(f"Project with ID {project_id} not found")

        # Create analysis session
        session = AnalysisSession.objects.create(
            project=project,
            status='pending',
            configuration={
                'backends': backends,
                **config
            }
        )

        if async_mode:
            # Queue async task
            run_analysis_task.delay(session.id)
            print(f"Analysis queued for project: {project.name}")
            print(f"Session ID: {session.id}")
        else:
            # Run synchronously
            print(f"Running analysis for project: {project.name}")
            self._run_sync_analysis(session)

        return session

    def _run_sync_analysis(self, session: AnalysisSession):
        """Run analysis synchronously."""
        session.status = 'running'
        session.save()

        try:
            # Get project path
            project_path = Path(session.project.repository_url)
            
            # Run analysis with selected backends
            backends = session.configuration.get('backends', ['ast', 'quality'])
            results = self.analyzer.analyze_project(
                project_path,
                backends=backends,
                config=session.configuration
            )

            # Save results
            for backend_name, backend_results in results.items():
                session.analysis_results.create(
                    backend_name=backend_name,
                    status='success',
                    result_data=backend_results
                )

            session.complete_analysis()
            print(f"Analysis completed successfully!")
            
            log.error summary
            self._print_results_summary(session)

        except Exception as e:
            session.mark_as_error(str(e))
            print(f"Analysis failed: {e}")
            sys.exit(1)

    def _print_results_summary(self, session: AnalysisSession):
        """Print analysis results summary."""
        print("\n" + "="*60)
        print("Analysis Results Summary")
        print("="*60)
        
        for result in session.analysis_results.all():
            print(f"\n{result.backend_name}:")
            print(f"  Status: {result.status}")
            
            if result.status == 'success':
                data = result.result_data
                if 'metrics' in data:
                    print("  Metrics:")
                    for key, value in data['metrics'].items():
                        print(f"    - {key}: {value}")
                
                if 'issues' in data:
                    print(f"  Issues found: {len(data['issues'])}")
                
                if 'score' in data:
                    print(f"  Quality score: {data['score']}")

    def list_projects(self) -> List[Project]:
        """List all available projects."""
        return list(Project.objects.all().order_by('name'))

    def list_backends(self) -> List[str]:
        """List available analysis backends."""
        return self.analyzer.list_available_backends()

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Run code analysis for DC Code Analyzer projects"
    )
    
    parser.add_argument(
        'project_id',
        type=int,
        help='Project ID to analyze'
    )
    
    parser.add_argument(
        '--backends',
        nargs='+',
        default=['ast', 'quality'],
        help='Analysis backends to use (default: ast quality)'
    )
    
    parser.add_argument(
        '--sync',
        action='store_true',
        help='Run analysis synchronously (default: async)'
    )
    
    parser.add_argument(
        '--depth',
        choices=['shallow', 'normal', 'deep'],
        default='normal',
        help='Analysis depth (default: normal)'
    )
    
    parser.add_argument(
        '--include-tests',
        action='store_true',
        help='Include test files in analysis'
    )
    
    parser.add_argument(
        '--list-projects',
        action='store_true',
        help='List available projects'
    )
    
    parser.add_argument(
        '--list-backends',
        action='store_true',
        help='List available backends'
    )

    args = parser.parse_args()

    runner = AnalysisRunner()

    # Handle list commands
    if args.list_projects:
        print("Available projects:")
        for project in runner.list_projects():
            print(f"  {project.id}: {project.name} ({project.language})")
        return

    if args.list_backends:
        print("Available backends:")
        for backend in runner.list_backends():
            print(f"  - {backend}")
        return

    # Run analysis
    config = {
        'depth': args.depth,
        'include_tests': args.include_tests
    }

    try:
        session = runner.run_analysis(
            project_id=args.project_id,
            backends=args.backends,
            config=config,
            async_mode=not args.sync
        )

        if not args.sync:
            print(f"\nTo check analysis status:")
            print(f"  python manage.py analysis_status {session.id}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### **Batch Analysis (batch_analysis.py)**

```python
#!/usr/bin/env python3
"""Run batch analysis for multiple projects.

This script allows running analysis on multiple projects
with configurable parallelism and reporting.
"""

import argparse
import sys
import os
import django
import time
from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Django setup
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_analyzer_web.settings')
django.setup()

from analyzer.models import Project, AnalysisSession
from analyzer.tasks import run_analysis_task

class BatchAnalyzer:
    """Batch analysis runner."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results = []

    def analyze_projects(
        self,
        project_ids: List[int],
        backends: List[str],
        config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze multiple projects."""
        projects = self._get_projects(project_ids)
        
        print(f"Starting batch analysis for {len(projects)} projects...")
        print(f"Using {self.max_workers} parallel workers")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_project = {
                executor.submit(
                    self._analyze_project,
                    project,
                    backends,
                    config
                ): project
                for project in projects
            }
            
            for future in as_completed(future_to_project):
                project = future_to_project[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    print(f"✓ {project.name}: {result['status']}")
                except Exception as e:
                    print(f"✗ {project.name}: Failed - {e}")
                    self.results.append({
                        'project': project.name,
                        'status': 'failed',
                        'error': str(e)
                    })
        
        return self.results

    def _get_projects(self, project_ids: List[int]) -> List[Project]:
        """Get projects by IDs or all if none specified."""
        if project_ids:
            return list(Project.objects.filter(id__in=project_ids))
        else:
            return list(Project.objects.all())

    def _analyze_project(
        self,
        project: Project,
        backends: List[str],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze single project."""
        start_time = time.time()
        
        # Create analysis session
        session = AnalysisSession.objects.create(
            project=project,
            status='pending',
            configuration={
                'backends': backends,
                **config
            }
        )
        
        # Queue analysis task
        run_analysis_task.delay(session.id)
        
        duration = time.time() - start_time
        
        return {
            'project': project.name,
            'session_id': session.id,
            'status': 'queued',
            'duration': duration
        }

    def generate_report(self) -> Dict[str, Any]:
        """Generate batch analysis report."""
        total = len(self.results)
        successful = len([r for r in self.results if r['status'] == 'queued'])
        failed = len([r for r in self.results if r['status'] == 'failed'])
        
        report = {
            'summary': {
                'total_projects': total,
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / total * 100) if total > 0 else 0
            },
            'projects': self.results
        }
        
        return report

    def print_report(self):
        """Print analysis report."""
        report = self.generate_report()
        
        print("\n" + "="*60)
        print("Batch Analysis Report")
        print("="*60)
        print(f"Total projects: {report['summary']['total_projects']}")
        print(f"Successful: {report['summary']['successful']}")
        print(f"Failed: {report['summary']['failed']}")
        print(f"Success rate: {report['summary']['success_rate']:.1f}%")
        
        if report['summary']['failed'] > 0:
            print("\nFailed projects:")
            for result in self.results:
                if result['status'] == 'failed':
                    print(f"  - {result['project']}: {result.get('error', 'Unknown error')}")

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Run batch analysis for multiple projects"
    )
    
    parser.add_argument(
        '--project-ids',
        nargs='+',
        type=int,
        help='Project IDs to analyze (default: all projects)'
    )
    
    parser.add_argument(
        '--backends',
        nargs='+',
        default=['ast', 'quality'],
        help='Analysis backends to use'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    parser.add_argument(
        '--depth',
        choices=['shallow', 'normal', 'deep'],
        default='normal',
        help='Analysis depth'
    )
    
    parser.add_argument(
        '--language',
        help='Filter projects by language'
    )
    
    parser.add_argument(
        '--framework',
        help='Filter projects by framework'
    )

    args = parser.parse_args()

    # Build configuration
    config = {
        'depth': args.depth,
        'batch_mode': True
    }

    # Get project IDs based on filters
    project_ids = args.project_ids or []
    
    if not project_ids and (args.language or args.framework):
        # Filter projects
        projects = Project.objects.all()
        if args.language:
            projects = projects.filter(language=args.language)
        if args.framework:
            projects = projects.filter(framework=args.framework)
        project_ids = list(projects.values_list('id', flat=True))

    # Run batch analysis
    analyzer = BatchAnalyzer(max_workers=args.workers)
    
    try:
        analyzer.analyze_projects(
            project_ids=project_ids,
            backends=args.backends,
            config=config
        )
        
        log.error report
        analyzer.print_report()
        
    except Exception as e:
        print(f"Batch analysis failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### **3. Maintenance Scripts**

#### **Check Detected Issues (check_detected_issues.py)**

```python
#!/usr/bin/env python3
"""Check and analyze detected issues from code analysis.

This script provides utilities for examining, filtering, and
reporting on issues detected during code analysis.
"""

import argparse
import sys
import os
import django
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict
import json

# Django setup
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_analyzer_web.settings')
django.setup()

from analyzer.models import Project, AnalysisSession, Issue

class IssueChecker:
    """Issue checking and reporting utilities."""

    def __init__(self):
        self.issues = []
        self.stats = defaultdict(int)

    def check_project_issues(
        self,
        project_id: Optional[int] = None,
        session_id: Optional[int] = None,
        severity: Optional[str] = None,
        issue_type: Optional[str] = None
    ) -> List[Issue]:
        """Check issues for a project or session."""
        query = Issue.objects.all()
        
        if session_id:
            query = query.filter(session_id=session_id)
        elif project_id:
            query = query.filter(session__project_id=project_id)
        
        if severity:
            query = query.filter(severity=severity)
        
        if issue_type:
            query = query.filter(type=issue_type)
        
        self.issues = list(query.select_related('session', 'session__project'))
        return self.issues

    def analyze_issues(self) -> Dict[str, Any]:
        """Analyze issue patterns and statistics."""
        if not self.issues:
            return {"error": "No issues found"}
        
        # Calculate statistics
        for issue in self.issues:
            self.stats['total'] += 1
            self.stats[f'severity_{issue.severity}'] += 1
            self.stats[f'type_{issue.type}'] += 1
            self.stats[f'backend_{issue.backend_name}'] += 1
        
        # Find most common issues
        issue_messages = defaultdict(int)
        for issue in self.issues:
            issue_messages[issue.message] += 1
        
        most_common = sorted(
            issue_messages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Group by file
        issues_by_file = defaultdict(list)
        for issue in self.issues:
            issues_by_file[issue.file_path].append(issue)
        
        # Files with most issues
        files_by_issue_count = sorted(
            [(file, len(issues)) for file, issues in issues_by_file.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'statistics': dict(self.stats),
            'most_common_issues': [
                {'message': msg, 'count': count}
                for msg, count in most_common
            ],
            'files_with_most_issues': [
                {'file': file, 'issue_count': count}
                for file, count in files_by_issue_count
            ],
            'severity_distribution': {
                'critical': self.stats.get('severity_critical', 0),
                'high': self.stats.get('severity_high', 0),
                'medium': self.stats.get('severity_medium', 0),
                'low': self.stats.get('severity_low', 0)
            }
        }

    def generate_report(self, format: str = 'text') -> str:
        """Generate issue report in specified format."""
        analysis = self.analyze_issues()
        
        if format == 'json':
            return json.dumps(analysis, indent=2)
        
        elif format == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'Project', 'File', 'Line', 'Column',
                'Type', 'Severity', 'Message', 'Backend'
            ])
            
            # Write issues
            for issue in self.issues:
                writer.writerow([
                    issue.session.project.name,
                    issue.file_path,
                    issue.line_number or '',
                    issue.column_number or '',
                    issue.type,
                    issue.severity,
                    issue.message,
                    issue.backend_name
                ])
            
            return output.getvalue()
        
        else:  # text format
            report = []
            report.append("="*60)
            report.append("Code Analysis Issues Report")
            report.append("="*60)
            
            stats = analysis['statistics']
            report.append(f"\nTotal issues: {stats['total']}")
            
            report.append("\nSeverity Distribution:")
            for severity, count in analysis['severity_distribution'].items():
                report.append(f"  {severity}: {count}")
            
            report.append("\nMost Common Issues:")
            for item in analysis['most_common_issues'][:5]:
                report.append(f"  - {item['message'][:60]}... ({item['count']} occurrences)")
            
            report.append("\nFiles with Most Issues:")
            for item in analysis['files_with_most_issues'][:5]:
                report.append(f"  - {item['file']}: {item['issue_count']} issues")
            
            return '\n'.join(report)

    def fix_suggestions(self) -> List[Dict[str, Any]]:
        """Generate fix suggestions for common issues."""
        suggestions = []
        
        # Group issues by type
        issues_by_type = defaultdict(list)
        for issue in self.issues:
            issues_by_type[issue.type].append(issue)
        
        # Generate suggestions
        for issue_type, issues in issues_by_type.items():
            if issue_type == 'complexity':
                suggestions.append({
                    'issue_type': 'complexity',
                    'count': len(issues),
                    'suggestion': 'Refactor complex functions into smaller, more focused functions',
                    'priority': 'medium'
                })
            elif issue_type == 'unused-variable':
                suggestions.append({
                    'issue_type': 'unused-variable',
                    'count': len(issues),
                    'suggestion': 'Remove unused variables or use them if they were intended to be used',
                    'priority': 'low'
                })
            elif issue_type == 'missing-docstring':
                suggestions.append({
                    'issue_type': 'missing-docstring',
                    'count': len(issues),
                    'suggestion': 'Add docstrings to functions and classes for better documentation',
                    'priority': 'low'
                })
        
        return sorted(suggestions, key=lambda x: x['count'], reverse=True)

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Check and analyze detected code issues"
    )
    
    parser.add_argument(
        '--project-id',
        type=int,
        help='Filter by project ID'
    )
    
    parser.add_argument(
        '--session-id',
        type=int,
        help='Filter by analysis session ID'
    )
    
    parser.add_argument(
        '--severity',
        choices=['low', 'medium', 'high', 'critical'],
        help='Filter by severity'
    )
    
    parser.add_argument(
        '--type',
        help='Filter by issue type'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file (default: stdout)'
    )
    
    parser.add_argument(
        '--fix-suggestions',
        action='store_true',
        help='Show fix suggestions'
    )

    args = parser.parse_args()

    checker = IssueChecker()
    
    # Check issues
    issues = checker.check_project_issues(
        project_id=args.project_id,
        session_id=args.session_id,
        severity=args.severity,
        issue_type=args.type
    )
    
    if not issues:
        print("No issues found matching criteria")
        return
    
    print(f"Found {len(issues)} issues")
    
    # Generate report
    report = checker.generate_report(format=args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)
    
    # Show fix suggestions if requested
    if args.fix_suggestions:
        print("\n" + "="*60)
        print("Fix Suggestions")
        print("="*60)
        
        suggestions = checker.fix_suggestions()
        for suggestion in suggestions:
            print(f"\n{suggestion['issue_type']} ({suggestion['count']} issues):")
            print(f"  Suggestion: {suggestion['suggestion']}")
            print(f"  Priority: {suggestion['priority']}")

if __name__ == "__main__":
    main()
```

---

## 🔧 **Usage Examples**

### **Starting Services**

```bash
# Start all services
cd /home/marlonsc/pyauto/dc-code-analyzer
./scripts/start_all.sh

# Start individual services
./scripts/start_redis.sh
./scripts/start_celery.sh
./scripts/start_server.sh

# Restart all services
./scripts/restart_services.sh
```

### **Running Analysis**

```bash
# Run analysis for a specific project
python scripts/run_analysis.py 1 --backends ast quality --depth deep

# Run batch analysis for all Python projects
python scripts/batch_analysis.py --language Python --workers 8

# Schedule periodic analysis
python scripts/scheduled_analysis.py --interval hourly
```

### **Maintenance Tasks**

```bash
# Check detected issues
python scripts/check_detected_issues.py --severity high --format json

# Clean up old analysis sessions
python scripts/cleanup_old_sessions.py --days 30

# Backup database
python scripts/backup_database.py --output /backups/dc_analyzer_backup.sql

# Optimize database
python scripts/optimize_database.py
```

---

## 🔗 **Cross-References**

### **Component Documentation**

- [DC Code Analyzer Overview](../README.md) - Main component documentation
- [Test Suite](../tests/README.md) - Testing documentation
- [API Documentation](../docs/api/) - REST API reference

### **Django Documentation**

- [Django Management Commands](https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/) - Custom commands
- [Celery Documentation](https://docs.celeryproject.org/) - Task queue
- [Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/) - Deployment guide

### **External References**

- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/) - Shell scripting
- [Python Script Best Practices](https://realpython.com/run-python-scripts/) - Python scripting
- [Code Analysis Tools](https://github.com/analysis-tools-dev/static-analysis) - Analysis tools

---

**📂 Module**: Scripts & Utilities | **🏠 Component**: [DC Code Analyzer](../README.md) | **Tools**: Bash, Python, Django | **Updated**: 2025-06-19
