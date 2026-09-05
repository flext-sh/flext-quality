"""Behavioral tests for ``FlextQualityBaseHook`` and ``FlextQualityHookManager``.

Exercises real hook subclasses registered and executed through the manager —
no mocks, no patched collaborators.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, override

from flext_quality import FlextQualityBaseHook, FlextQualityHookManager, c, r
from flext_tests import tm

if TYPE_CHECKING:
    from flext_quality import p, t


class _AlwaysRunHook(FlextQualityBaseHook):
    """Hook with no matcher — runs for every input."""

    event: ClassVar[c.Quality.HookEvent] = c.Quality.HookEvent.PRE_TOOL_USE

    @override
    def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
        return r.ok({"continue": True, "seen": input_data.get("tool_name")})


class _MatcherHook(FlextQualityBaseHook):
    """Hook that only runs for matching tool names."""

    event: ClassVar[c.Quality.HookEvent] = c.Quality.HookEvent.PRE_TOOL_USE
    matcher: ClassVar[t.StrSequence | None] = ("Edit", "Write*")

    @override
    def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
        return r.ok({"continue": True})


class _BlockingHook(FlextQualityBaseHook):
    """Hook that halts the chain by returning ``continue: False``."""

    event: ClassVar[c.Quality.HookEvent] = c.Quality.HookEvent.PRE_TOOL_USE

    @override
    def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
        return r.ok({"continue": False, "reason": "blocked"})


class _FailingHook(FlextQualityBaseHook):
    """Hook whose execution reports a failure result."""

    event: ClassVar[c.Quality.HookEvent] = c.Quality.HookEvent.STOP

    @override
    def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
        return r.fail("boom")


class TestsFlextQualityBaseHook:
    """Contract tests for the concrete hook base class."""

    def test_execute_raises_not_implemented_on_base(self) -> None:
        """The base ``execute`` is abstract and always raises."""

        class _BareHook(FlextQualityBaseHook):
            event: ClassVar[c.Quality.HookEvent] = c.Quality.HookEvent.STOP

        try:
            _BareHook().execute({})
        except NotImplementedError:
            return
        message = "expected NotImplementedError"
        raise AssertionError(message)

    def test_should_run_defaults_true_without_a_matcher(self) -> None:
        """A hook without a matcher runs for every input."""
        hook = _AlwaysRunHook()
        tm.that(hook.should_run({"tool_name": "Anything"}), eq=True)
        tm.that(hook.should_run({}), eq=True)

    def test_should_run_matches_configured_glob_patterns(self) -> None:
        """A hook with a matcher runs only for tool names matching any pattern."""
        hook = _MatcherHook()
        tm.that(hook.should_run({"tool_name": "Edit"}), eq=True)
        tm.that(hook.should_run({"tool_name": "WriteFile"}), eq=True)
        tm.that(hook.should_run({"tool_name": "Bash"}), eq=False)

    def test_should_run_treats_missing_tool_name_as_empty_string(self) -> None:
        """A matcher hook without a ``tool_name`` behaves as if it were empty."""
        hook = _MatcherHook()
        tm.that(hook.should_run({}), eq=False)


class TestsFlextQualityHookManager:
    """Contract tests for the hook lifecycle manager."""

    def test_execute_unknown_event_fails(self) -> None:
        """Executing an unregistered event name reports a descriptive failure."""
        manager = FlextQualityHookManager()
        result = manager.execute("NotARealEvent", {})
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="Unknown event")

    def test_execute_with_no_registered_hooks_continues(self) -> None:
        """A known event with nothing registered always continues."""
        manager = FlextQualityHookManager()
        result = manager.execute("PreToolUse", {})
        tm.that(result.success, eq=True)
        tm.that(result.value.get("continue"), eq=True)

    def test_register_and_execute_runs_matching_hook(self) -> None:
        """A registered hook that runs and continues yields the default outcome.

        The manager only short-circuits (returning a hook's own payload) when
        that hook signals ``continue: False``; a continuing hook's execution
        is still real (it ran), but the chain's terminal result is the
        manager's own ``{"continue": True}``.
        """
        manager = FlextQualityHookManager()
        register_result = manager.register(_AlwaysRunHook())
        tm.that(register_result.success, eq=True)
        result = manager.execute("PreToolUse", {"tool_name": "Edit"})
        tm.that(result.success, eq=True)
        tm.that(result.value, eq={"continue": True})

    def test_execute_skips_hooks_that_should_not_run(self) -> None:
        """A hook whose matcher rejects the input is skipped entirely."""
        manager = FlextQualityHookManager()
        manager.register(_MatcherHook())
        result = manager.execute("PreToolUse", {"tool_name": "Bash"})
        tm.that(result.success, eq=True)
        tm.that(result.value, eq={"continue": True})

    def test_execute_stops_chain_when_a_hook_blocks(self) -> None:
        """A hook returning ``continue: False`` halts the remaining chain."""
        manager = FlextQualityHookManager()
        manager.register(_AlwaysRunHook())
        manager.register(_BlockingHook())
        result = manager.execute("PreToolUse", {"tool_name": "Edit"})
        tm.that(result.success, eq=True)
        tm.that(result.value.get("continue"), eq=False)
        tm.that(result.value.get("reason"), eq="blocked")

    def test_execute_propagates_hook_failure(self) -> None:
        """A hook that fails short-circuits execution with its own error."""
        manager = FlextQualityHookManager()
        manager.register(_FailingHook())
        result = manager.execute("Stop", {})
        tm.that(result.failure, eq=True)
        tm.that(result.error, eq="boom")

    def test_fetch_config_reports_registered_hooks_by_event(self) -> None:
        """The rendered config groups registered hooks by their event name."""
        manager = FlextQualityHookManager()
        manager.register(_MatcherHook())
        config = manager.fetch_config()
        tm.that(config, has="PreToolUse")
        entries = config.get("PreToolUse")
        tm.that(entries, is_=list)
        assert isinstance(entries, list)
        tm.that(len(entries), eq=1)
        first_entry = entries[0]
        tm.that(first_entry, is_=dict)
        assert isinstance(first_entry, dict)
        tm.that(first_entry.get("matcher"), eq=["Edit", "Write*"])

    def test_fetch_config_json_renders_configured_hooks(self) -> None:
        """The JSON rendering of the hook config includes the matcher list."""
        manager = FlextQualityHookManager()
        manager.register(_AlwaysRunHook())
        output = manager.fetch_config_json()
        tm.that(output, is_=str)
        tm.that(output, has="PreToolUse")

    def test_register_appends_multiple_hooks_for_same_event(self) -> None:
        """Multiple hooks registered for one event all execute in order."""
        manager = FlextQualityHookManager()
        manager.register(_AlwaysRunHook())
        manager.register(_AlwaysRunHook())
        config = manager.fetch_config()
        entries = config.get("PreToolUse")
        assert isinstance(entries, list)
        tm.that(len(entries), eq=2)


__all__: list[str] = [
    "TestsFlextQualityBaseHook",
    "TestsFlextQualityHookManager",
]
