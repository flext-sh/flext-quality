"""Unified plugin orchestrator coordinating all flext-quality validations."""

from __future__ import annotations

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from flext_core import FlextContainer, FlextResult as r, FlextService

from flext_quality.orchestrator.models import (
    PluginCategory,
    PluginMetadata,
    ValidationResult,
    Violation,
)

logger = logging.getLogger(__name__)


def _execute_plugin_in_process(
    plugin_class: type,
    file_path: str,
    content: str,
) -> dict[str, Any]:
    """Execute plugin in subprocess (ProcessPoolExecutor worker).

    This function is executed in a separate process.
    Must be picklable (no lambda, no nested functions).

    Args:
        plugin_class: Plugin class to instantiate
        file_path: File to validate
        content: File content

    Returns:
        Plugin-specific result dict

    """
    try:
        plugin = plugin_class()
        result = plugin.validate(file_path, content)

        if result.is_failure:
            return {"status": "error", "error": result.error}

        return result.unwrap()
    except Exception as e:
        return {"status": "error", "error": str(e)}


class PluginOrchestrator(FlextService[ValidationResult]):
    """Central orchestrator for coordinating all quality plugins.

    Responsibilities:
    - Plugin registration and discovery
    - Dependency resolution (topological sort)
    - Parallel execution via ProcessPoolExecutor
    - Result aggregation and reporting
    - Configuration management
    """

    def __init__(
        self,
        max_parallel_workers: int = 4,
        plugin_timeout: int = 10,
        container: FlextContainer | None = None,
    ) -> None:
        super().__init__()
        self.max_parallel_workers = max_parallel_workers
        self.plugin_timeout = plugin_timeout
        self._container = container or FlextContainer()
        self._plugins: dict[str, PluginMetadata] = {}
        self._plugin_instances: dict[str, Any] = {}
        self._initialized = False

    def register_plugin(self, metadata: PluginMetadata) -> r[None]:
        """Register a plugin with the orchestrator.

        Args:
            metadata: Plugin metadata with capabilities and dependencies

        Returns:
            Success if registered, Failure if duplicate name

        """
        if metadata.name in self._plugins:
            return r[None].fail(f"Plugin {metadata.name} already registered")

        self._plugins[metadata.name] = metadata
        logger.info(
            f"Registered plugin: {metadata.name} (categories: {metadata.categories})"
        )
        return r[None].ok(None)

    def initialize(self) -> r[None]:
        """Initialize all registered plugins.

        Performs:
        1. Dependency resolution (topological sort)
        2. Plugin instantiation
        3. Plugin initialization

        Returns:
            Success if all initialized, Failure with first error

        """
        if self._initialized:
            return r[None].ok(None)

        # 1. Resolve dependencies (topological sort)
        execution_order = self._resolve_dependencies()
        if execution_order.is_failure:
            return execution_order.map(lambda _: None)

        order = execution_order.unwrap()
        logger.info(f"Plugin execution order: {order}")

        # 2. Initialize plugins in dependency order
        for plugin_name in order:
            metadata = self._plugins[plugin_name]

            # Instantiate plugin
            try:
                plugin_instance = metadata.plugin_class()
                self._plugin_instances[plugin_name] = plugin_instance
            except Exception as e:
                return r[None].fail(f"Failed to instantiate {plugin_name}: {e}")

            # Initialize with config
            init_result = plugin_instance.initialize({})
            if init_result.is_failure:
                return r[None].fail(
                    f"Plugin {plugin_name} init failed: {init_result.error}"
                )

        self._initialized = True
        return r[None].ok(None)

    def validate_file(
        self,
        file_path: Path | str,
        content: str,
        categories: list[PluginCategory] | None = None,
    ) -> r[ValidationResult]:
        """Validate file using all applicable plugins in parallel.

        Workflow:
        1. Detect language (LanguageDetectorPlugin)
        2. Filter applicable plugins (by language, category)
        3. Execute plugins in parallel (ProcessPoolExecutor)
        4. Aggregate results
        5. Return unified ValidationResult

        Args:
            file_path: Path to file being validated
            content: File content as string
            categories: Optional filter (LINT, TYPE_CHECK, SECURITY, etc.)

        Returns:
            Success with ValidationResult, Failure with error

        """
        if not self._initialized:
            init_result = self.initialize()
            if init_result.is_failure:
                return r[ValidationResult].fail(f"Init failed: {init_result.error}")

        file_path = Path(file_path) if isinstance(file_path, str) else file_path

        # 1. Detect language
        language_result = self._detect_language(str(file_path), content)
        if language_result.is_failure:
            logger.warning(f"Language detection failed: {language_result.error}")
            language = "unknown"
        else:
            language = language_result.unwrap()

        # 2. Filter applicable plugins
        applicable = self._filter_plugins(
            language=language,
            categories=categories,
        )

        if not applicable:
            # No plugins apply - return empty result
            return r[ValidationResult].ok(
                ValidationResult(
                    status="success",
                    file_path=str(file_path),
                    language=language,
                    violations=(),
                    warnings=(),
                    suggestions=(),
                    total_violations=0,
                    total_warnings=0,
                    has_blocking=False,
                    plugin_results={},
                )
            )

        # 3. Execute plugins in parallel
        execution_result = self._execute_parallel(
            plugins=applicable,
            file_path=str(file_path),
            content=content,
        )

        if execution_result.is_failure:
            return r[ValidationResult].fail(execution_result.error)

        plugin_results = execution_result.unwrap()

        # 4. Aggregate results
        aggregated = self._aggregate_results(
            plugin_results=plugin_results,
            file_path=str(file_path),
            language=language,
        )

        return r[ValidationResult].ok(aggregated)

    def validate_to_json(
        self,
        file_path: Path | str,
        content: str,
    ) -> dict[str, Any]:
        """Validate and return JSON (bash hook compatibility).

        Args:
            file_path: File to validate
            content: File content

        Returns:
            JSON-compatible dict with validation results

        """
        result = self.validate_file(file_path, content)

        if result.is_failure:
            return {
                "status": "error",
                "error": result.error,
                "file": str(file_path),
                "violations": [],
                "warnings": [],
                "suggestions": [],
            }

        return result.unwrap().to_dict()

    def _detect_language(
        self,
        file_path: str,
        content: str,
    ) -> r[str]:
        """Detect language using LanguageDetectorPlugin.

        Args:
            file_path: File path for extension detection
            content: Content for shebang/syntax detection

        Returns:
            Success with language string, Failure if detector unavailable

        """
        detector_meta = self._plugins.get("language-detector")
        if not detector_meta:
            return r[str].fail("LanguageDetectorPlugin not registered")

        try:
            detector = self._plugin_instances.get("language-detector")
            if not detector:
                detector = detector_meta.plugin_class()

            return detector.detect(file_path, content)
        except Exception as e:
            return r[str].fail(f"Language detection error: {e}")

    def _filter_plugins(
        self,
        language: str,
        categories: list[PluginCategory] | None = None,
    ) -> list[PluginMetadata]:
        """Filter plugins by language and category.

        Args:
            language: Detected language (e.g., "python", "typescript")
            categories: Optional category filter

        Returns:
            List of applicable plugin metadata

        """
        applicable = []

        for metadata in self._plugins.values():
            # Skip language detector (already executed)
            if PluginCategory.LANGUAGE in metadata.categories:
                continue

            # Filter by language
            if not metadata.applies_to_language(language):
                continue

            # Filter by category (if specified)
            if categories:
                if not any(cat in metadata.categories for cat in categories):
                    continue

            applicable.append(metadata)

        # Sort by priority (lower = first)
        applicable.sort(key=lambda m: m.priority)

        return applicable

    def _execute_parallel(
        self,
        plugins: list[PluginMetadata],
        file_path: str,
        content: str,
    ) -> r[dict[str, Any]]:
        """Execute plugins in parallel using ProcessPoolExecutor.

        Args:
            plugins: List of plugin metadata to execute
            file_path: File being validated
            content: File content

        Returns:
            Success with dict of plugin results {name: result}

        """
        plugin_results = {}

        with ProcessPoolExecutor(max_workers=self.max_parallel_workers) as executor:
            # Submit all plugins
            futures = {
                executor.submit(
                    _execute_plugin_in_process,
                    metadata.plugin_class,
                    file_path,
                    content,
                ): metadata.name
                for metadata in plugins
            }

            # Collect results as they complete
            for future in as_completed(futures, timeout=self.plugin_timeout):
                plugin_name = futures[future]

                try:
                    result = future.result(timeout=self.plugin_timeout)
                    plugin_results[plugin_name] = result
                except Exception as e:
                    logger.exception(f"Plugin {plugin_name} failed: {e}")
                    plugin_results[plugin_name] = {
                        "status": "error",
                        "error": str(e),
                    }

        return r[dict[str, Any]].ok(plugin_results)

    def _aggregate_results(
        self,
        plugin_results: dict[str, Any],
        file_path: str,
        language: str,
    ) -> ValidationResult:
        """Aggregate results from all plugins into unified ValidationResult.

        Args:
            plugin_results: Dict of plugin results {plugin_name: result}
            file_path: File that was validated
            language: Detected language

        Returns:
            Unified ValidationResult with all violations aggregated

        """
        all_violations: list[Violation] = []
        all_warnings: list[Violation] = []
        all_suggestions: list[Violation] = []

        for plugin_name, result in plugin_results.items():
            if result.get("status") == "error":
                continue

            # Extract violations from plugin-specific format
            violations = self._extract_violations(plugin_name, result)

            for v in violations:
                if v.blocking:
                    all_violations.append(v)
                elif v.severity in {"high", "medium"}:
                    all_warnings.append(v)
                else:
                    all_suggestions.append(v)

        return ValidationResult(
            status="success",
            file_path=file_path,
            language=language,
            violations=tuple(all_violations),
            warnings=tuple(all_warnings),
            suggestions=tuple(all_suggestions),
            total_violations=len(all_violations),
            total_warnings=len(all_warnings),
            has_blocking=len(all_violations) > 0,
            plugin_results=plugin_results,
        )

    def _extract_violations(
        self,
        plugin_name: str,
        result: dict[str, Any],
    ) -> list[Violation]:
        """Extract violations from plugin-specific result format.

        Each plugin returns results in different formats.
        This method normalizes to Violation objects.

        Args:
            plugin_name: Name of plugin that produced result
            result: Plugin-specific result dict

        Returns:
            List of normalized Violation objects

        """
        violations = []

        # Handle different plugin result formats
        if plugin_name == "ruff":
            violations.extend(
                Violation(
                    code=item.get("code", "RUFF-???"),
                    name=item.get("message", "Ruff violation"),
                    severity="high",
                    blocking=True,
                    guidance=item.get("message", ""),
                    category="lint",
                    source_plugin="ruff",
                    line=item.get("location", {}).get("row"),
                    column=item.get("location", {}).get("column"),
                )
                for item in result.get("violations", [])
            )

        elif plugin_name == "mypy":
            violations.extend(
                Violation(
                    code="MYPY-TYPE",
                    name=item.get("message", "Type error"),
                    severity="high",
                    blocking=True,
                    guidance=item.get("message", ""),
                    category="type_check",
                    source_plugin="mypy",
                    line=item.get("line"),
                    column=item.get("column"),
                )
                for item in result.get("violations", [])
            )

        elif plugin_name == "rule-registry":
            # RuleRegistry already returns normalized format
            violations.extend(
                Violation(
                    code=item["code"],
                    name=item["name"],
                    severity=item["severity"],
                    blocking=item["blocking"],
                    guidance=item["guidance"],
                    category=item["category"],
                    source_plugin="rule-registry",
                    line=item.get("line"),
                    column=item.get("column"),
                )
                for item in result.get("violations", [])
            )

        # Add more plugin-specific extractors as needed

        return violations

    def _resolve_dependencies(self) -> r[list[str]]:
        """Resolve plugin dependencies via topological sort.

        Returns:
            Success with ordered plugin names, Failure if circular dependency

        """
        visited = set()
        stack = []

        def visit(name: str, path: set[str]) -> r[None]:
            if name in path:
                cycle = " -> ".join(list(path) + [name])
                return r[None].fail(f"Circular dependency: {cycle}")

            if name in visited:
                return r[None].ok(None)

            metadata = self._plugins[name]
            path.add(name)

            for dep in metadata.depends_on:
                if dep not in self._plugins:
                    return r[None].fail(
                        f"Missing dependency: {dep} (required by {name})"
                    )

                result = visit(dep, path)
                if result.is_failure:
                    return result

            path.remove(name)
            visited.add(name)
            stack.append(name)
            return r[None].ok(None)

        for plugin_name in self._plugins:
            result = visit(plugin_name, set())
            if result.is_failure:
                return r[list[str]].fail(result.error)

        return r[list[str]].ok(stack)

    def execute(self) -> r[ValidationResult]:
        """FlextService execute method (not used directly)."""
        return r[ValidationResult].fail("Use validate_file() method")
