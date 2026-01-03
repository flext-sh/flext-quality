"""Hooks system - Protocol-based hook lifecycle management."""

from __future__ import annotations

from .base import BaseHookImpl
from .manager import HookManager

__all__ = ["BaseHookImpl", "HookManager"]
