"""Plugin registry extending FlextRegistry from flext-core.

Following patterns from:
- flext-api/src/flext_api/registry.py (FlextApiRegistry)
- flext-ldif/src/flext_ldif/services/registry.py (FlextLdifServiceRegistry)
"""

from __future__ import annotations

from typing import ClassVar, Self

from flext_core import (
    FlextProtocols as p,
    FlextRegistry,
    FlextResult as r,
    FlextTypes as t,
)

from flext_quality._models.plugin import FlextQualityPlugin
from flext_quality.plugins.base import (
    FlextQualityPlugin as FlextQualityPluginProtocol,
)


class FlextQualityPluginRegistry(FlextRegistry):
    """Registry for flext-quality validation plugins.

    Follows FlextApiRegistry/FlextLdifServiceRegistry patterns:
    - ClassVar for category names
    - Global singleton instance
    - Local plugin instance cache
    - Typed wrapper methods over FlextRegistry base

    FlextRegistry (parent) provides:
    - _class_plugin_storage: ClassVar[dict] (auto-created per subclass)
    - _class_registered_keys: ClassVar[set] (auto-created per subclass)
    - register_class_plugin(category, name, plugin) -> r[bool]
    - get_class_plugin(category, name) -> r[t.RegistrablePlugin]
    - list_class_plugins(category) -> r[list[str]]

    Usage:
        # Get global registry
        registry = FlextQualityPluginRegistry.get_global()

        # Register plugin
        registry.register_quality_plugin(metadata)

        # Get plugin metadata
        result = registry.get_quality_plugin("ruff")

        # Filter by category/language
        lint_plugins = registry.filter_by_category(Category.LINT)
        python_plugins = registry.filter_by_language("python")
    """

    # Category constants (following FlextApiRegistry pattern)
    QUALITY_PLUGINS: ClassVar[str] = "quality_plugins"
    LANGUAGE_DETECTORS: ClassVar[str] = "language_detectors"

    # Global singleton instance (following FlextApiRegistry pattern)
    _global_instance: ClassVar[FlextQualityPluginRegistry | None] = None

    def __init__(
        self: Self,
        dispatcher: p.CommandBus | None = None,
        **data: t.GeneralValueType,
    ) -> None:
        """Initialize registry with optional dispatcher.

        Args:
            dispatcher: Optional CQRS dispatcher (not used for quality plugins).
            **data: Additional Pydantic model data.

        """
        super().__init__(dispatcher=dispatcher, **data)
        # Local cache for instantiated plugins (following FlextApiRegistry pattern)
        self._plugin_instances: dict[str, FlextQualityPluginProtocol] = {}
        # Metadata cache for quick lookup
        self._metadata_cache: dict[str, FlextQualityPlugin.Metadata] = {}

    # ==================== SINGLETON PATTERN ====================

    @classmethod
    def get_global(cls) -> FlextQualityPluginRegistry:
        """Get or create global registry instance.

        Following FlextApiRegistry.get_global() pattern.

        Returns:
            Global FlextQualityPluginRegistry instance.

        """
        if cls._global_instance is None:
            cls._global_instance = cls()
        return cls._global_instance

    @classmethod
    def reset_global(cls) -> None:
        """Reset global registry instance.

        Used for testing to ensure clean state.
        Following FlextApiRegistry.reset_global() pattern.
        """
        cls._global_instance = None
        # Also clear class-level storage
        cls._class_plugin_storage.clear()
        cls._class_registered_keys.clear()

    # ==================== REGISTRATION METHODS ====================

    def register_quality_plugin(
        self: Self,
        metadata: FlextQualityPlugin.Metadata,
    ) -> r[bool]:
        """Register quality plugin with metadata.

        Following FlextApiRegistry.register_protocol() pattern:
        1. Create unique key
        2. Store in local cache
        3. Delegate to parent register_class_plugin()

        Args:
            metadata: Plugin metadata with name, categories, priority, etc.

        Returns:
            r[bool]: Success if registered (idempotent for same metadata).

        """
        # Determine category based on plugin type
        category = self.QUALITY_PLUGINS
        if FlextQualityPlugin.Category.LANGUAGE in metadata.categories:
            category = self.LANGUAGE_DETECTORS

        # Store metadata in local cache for quick retrieval
        self._metadata_cache[metadata.name] = metadata

        # Delegate to parent class (stores in _class_plugin_storage)
        return self.register_class_plugin(
            category=category,
            name=metadata.name,
            plugin=metadata,
        )

    def register_language_detector(
        self: Self,
        metadata: FlextQualityPlugin.Metadata,
    ) -> r[bool]:
        """Register language detector plugin.

        Convenience method for language detector registration.

        Args:
            metadata: Detector metadata (must have LANGUAGE category).

        Returns:
            r[bool]: Success if registered.

        """
        if FlextQualityPlugin.Category.LANGUAGE not in metadata.categories:
            return r[bool].fail(f"Plugin {metadata.name} is not a language detector")

        self._metadata_cache[metadata.name] = metadata
        return self.register_class_plugin(
            category=self.LANGUAGE_DETECTORS,
            name=metadata.name,
            plugin=metadata,
        )

    # ==================== RETRIEVAL METHODS ====================

    def get_quality_plugin(
        self: Self,
        name: str,
    ) -> r[FlextQualityPlugin.Metadata]:
        """Get quality plugin metadata by name.

        First checks local cache, then parent storage.

        Args:
            name: Plugin name.

        Returns:
            r[Metadata]: Plugin metadata or failure.

        """
        # Check local cache first
        if name in self._metadata_cache:
            return r[FlextQualityPlugin.Metadata].ok(self._metadata_cache[name])

        # Try parent storage (quality plugins)
        result = self.get_class_plugin(self.QUALITY_PLUGINS, name)
        if result.is_failure:
            # Try language detectors
            result = self.get_class_plugin(self.LANGUAGE_DETECTORS, name)

        if result.is_failure:
            return r[FlextQualityPlugin.Metadata].fail(f"Plugin '{name}' not found")

        # Type narrow and cache
        if not isinstance(result.value, FlextQualityPlugin.Metadata):
            return r[FlextQualityPlugin.Metadata].fail(
                f"Plugin '{name}' has invalid type"
            )

        self._metadata_cache[name] = result.value
        return r[FlextQualityPlugin.Metadata].ok(result.value)

    def get_plugin_instance(
        self: Self,
        name: str,
    ) -> r[FlextQualityPluginProtocol]:
        """Get or create plugin instance.

        Following FlextApiRegistry pattern of lazy instantiation.

        Args:
            name: Plugin name.

        Returns:
            r[Plugin]: Instantiated plugin or failure.

        """
        # Check instance cache
        if name in self._plugin_instances:
            return r[FlextQualityPluginProtocol].ok(self._plugin_instances[name])

        # Get metadata and instantiate
        metadata_result = self.get_quality_plugin(name)
        if metadata_result.is_failure:
            return r[FlextQualityPluginProtocol].fail(metadata_result.error)

        metadata = metadata_result.value
        try:
            instance = metadata.plugin_class()
            self._plugin_instances[name] = instance
            return r[FlextQualityPluginProtocol].ok(instance)
        except Exception as e:
            return r[FlextQualityPluginProtocol].fail(
                f"Failed to instantiate plugin '{name}': {e}"
            )

    def list_quality_plugins(self: Self) -> r[list[str]]:
        """List all registered quality plugin names.

        Returns:
            r[list[str]]: List of plugin names.

        """
        result = self.list_class_plugins(self.QUALITY_PLUGINS)
        if result.is_failure:
            return r[list[str]].ok([])
        return result

    def list_language_detectors(self: Self) -> r[list[str]]:
        """List all registered language detector names.

        Returns:
            r[list[str]]: List of detector names.

        """
        result = self.list_class_plugins(self.LANGUAGE_DETECTORS)
        if result.is_failure:
            return r[list[str]].ok([])
        return result

    # ==================== FILTERING METHODS ====================

    def get_all_metadata(self: Self) -> list[FlextQualityPlugin.Metadata]:
        """Get all registered plugin metadata.

        Returns:
            List of all plugin metadata objects.

        """
        # Combine both categories
        all_names: set[str] = set()

        quality_result = self.list_quality_plugins()
        if quality_result.is_success:
            all_names.update(quality_result.value)

        detector_result = self.list_language_detectors()
        if detector_result.is_success:
            all_names.update(detector_result.value)

        metadata_list: list[FlextQualityPlugin.Metadata] = []
        for name in all_names:
            result = self.get_quality_plugin(name)
            if result.is_success:
                metadata_list.append(result.value)

        return metadata_list

    def filter_by_category(
        self: Self,
        category: FlextQualityPlugin.Category,
    ) -> list[FlextQualityPlugin.Metadata]:
        """Filter plugins by category.

        Args:
            category: Plugin category to filter by.

        Returns:
            List of metadata for plugins in the category.

        """
        return [m for m in self.get_all_metadata() if category in m.categories]

    def filter_by_language(
        self: Self,
        language: str,
    ) -> list[FlextQualityPlugin.Metadata]:
        """Filter plugins that support a specific language.

        Args:
            language: Language to filter by (e.g., "python").

        Returns:
            List of metadata for plugins supporting the language.

        """
        return [m for m in self.get_all_metadata() if m.applies_to_language(language)]

    def filter_applicable(
        self: Self,
        language: str,
        categories: list[FlextQualityPlugin.Category] | None = None,
        exclude_language_detectors: bool = True,
    ) -> list[FlextQualityPlugin.Metadata]:
        """Filter plugins applicable to file validation.

        Combines language and category filtering with common exclusions.

        Args:
            language: File language.
            categories: Optional category filter.
            exclude_language_detectors: Exclude LANGUAGE category plugins.

        Returns:
            Sorted list of applicable plugin metadata (by priority).

        """
        applicable = self.filter_by_language(language)

        if categories:
            applicable = [
                m for m in applicable if any(cat in m.categories for cat in categories)
            ]

        if exclude_language_detectors:
            applicable = [
                m
                for m in applicable
                if FlextQualityPlugin.Category.LANGUAGE not in m.categories
            ]

        # Sort by priority (lower = first)
        applicable.sort(key=lambda m: m.priority)

        return applicable

    # ==================== FLEXTSERVICE CONTRACT ====================

    def execute(self: Self) -> r[bool]:
        """FlextService execute method.

        Validates registry is properly initialized.

        Returns:
            r[bool]: Success if registry is ready.

        """
        # Registry is always ready (stateless)
        return r[bool].ok(True)


__all__ = ["FlextQualityPluginRegistry"]
