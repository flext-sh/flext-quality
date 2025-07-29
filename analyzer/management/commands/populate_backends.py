"""Django management command to populate backend and issue type data."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from analyzer.models import AnalysisBackendModel, IssueType


class Command(BaseCommand):
    """Django management command to populate backend and issue type data."""

    help = "Populate backend and issue type data automatically"

    def add_arguments(self, parser: Any) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update existing data",
        )

    def handle(self, *_args: object, **options: Any) -> None:
        """Handle the command execution."""
        self.stdout.write(
            self.style.SUCCESS("🚀 Populating backend and issue type data..."),
        )

        force_update = options["force"]

        # Create or update backends
        self._create_backends(force_update)

        # Create or update issue types
        self._create_issue_types(force_update)

        self.stdout.write(
            self.style.SUCCESS(
                "✅ Backend and issue type data populated successfully!",
            ),
        )

    def _create_backends(self, force_update: bool) -> None:
        """Create or update analysis backends."""
        backends_data = [
            {
                "name": "ast",
                "display_name": "AST Analyzer",
                "description": "Python Abstract Syntax Tree analysis for structural code analysis",
                "capabilities": [
                    "class_analysis",
                    "function_analysis",
                    "variable_analysis",
                    "import_analysis",
                    "complexity_basic",
                ],
                "execution_order": 10,
                "default_enabled": True,
            },
            {
                "name": "external",
                "display_name": "External Tools",
                "description": "Integration with external security and (
                    quality tools (bandit, vulture)",)
                "capabilities": [
                    "security_analysis",
                    "dead_code_detection",
                    "vulnerability_scanning",
                ],
                "execution_order": 20,
                "default_enabled": True,
            },
            {
                "name": "quality",
                "display_name": "Quality Metrics",
                "description": "Code quality metrics using radon (complexity, maintainability, Halstead)",
                "capabilities": [
                    "complexity_analysis",
                    "maintainability_index",
                    "halstead_metrics",
                    "raw_metrics",
                ],
                "execution_order": 30,
                "default_enabled": True,
            },
        ]

        for backend_data in backends_data:
            backend, created = AnalysisBackendModel.objects.get_or_create(
                name=backend_data["name"],
                defaults=backend_data,
            )

            if created:
                self.stdout.write(f"  ✅ Created backend: {backend.display_name}")
            elif force_update:
                for key, value in backend_data.items():
                    if key != "name":
                        setattr(backend, key, value)
                backend.updated_at = timezone.now()
                backend.save()
                self.stdout.write(f"  🔄 Updated backend: {backend.display_name}")
            else:
                self.stdout.write(f"  ℹ️  Backend exists: {backend.display_name}")

    def _create_issue_types(self, force_update: bool) -> None:
        """Create or update issue types."""
        # Get backend objects
        try:
            ast_backend = AnalysisBackendModel.objects.get(name="ast")
            external_backend = AnalysisBackendModel.objects.get(name="external")
            quality_backend = AnalysisBackendModel.objects.get(name="quality")
        except AnalysisBackendModel.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"Backend not found {e}"))
            return

        issue_types_data = [
            # AST Backend Issues
            {
                "backend": ast_backend,
                "code": "AST001",
                "name": "Missing Class Docstring",
                "description": "Class definition without documentation",
                "category": "documentation",
                "severity": "LOW",
                "recommendation": "Add a docstring to document the class purpose and usage",
            },
            {
                "backend": ast_backend,
                "code": "AST002",
                "name": "Missing Function Docstring",
                "description": "Function or method without documentation",
                "category": "documentation",
                "severity": "LOW",
                "recommendation": "Add a docstring to document function parameters and (
                    return value",)
            },
            {
                "backend": ast_backend,
                "code": "AST003",
                "name": "Complex Function",
                "description": "Function with high cyclomatic complexity",
                "category": "complexity",
                "severity": "MEDIUM",
                "recommendation": "Consider breaking down the function into smaller, simpler functions",
            },
            # External Tools Issues (Bandit Security)
            {
                "backend": external_backend,
                "code": "B101",
                "name": "Use of assert detected",
                "description": "Assert statements are removed when compiling to optimized byte code",
                "category": "security",
                "severity": "LOW",
                "recommendation": "Use explicit exception raising instead of assert for production code",
                "documentation_url": "https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html",
            },
            {
                "backend": external_backend,
                "code": "B105",
                "name": "Hardcoded password string",
                "description": "Possible hardcoded password",
                "category": "security",
                "severity": "MEDIUM",
                "recommendation": "Use environment variables or secure configuration for passwords",
                "documentation_url": "https://bandit.readthedocs.io/en/latest/plugins/b105_hardcoded_password_string.html",
            },
            # Quality Backend Issues (Radon)
            {
                "backend": quality_backend,
                "code": "R901",
                "name": "Too Complex Function",
                "description": "Function has very high cyclomatic complexity",
                "category": "complexity",
                "severity": "HIGH",
                "recommendation": "Refactor function to reduce complexity by breaking it into smaller functions",
            },
        ]

        created_count = 0
        updated_count = 0

        for issue_data in issue_types_data:
            issue_type, created = IssueType.objects.get_or_create(
                backend=issue_data["backend"],
                code=issue_data["code"],
                defaults=issue_data,
            )

            if created:
                created_count += 1
            elif force_update:
                for key, value in issue_data.items():
                    if key not in {"backend", "code"}:
                        setattr(issue_type, key, value)
                issue_type.updated_at = timezone.now()
                issue_type.save()
                updated_count += 1

        self.stdout.write(f"  ✅ Created {created_count} issue types")
        if force_update:
            self.stdout.write(f"  🔄 Updated {updated_count} issue types")
