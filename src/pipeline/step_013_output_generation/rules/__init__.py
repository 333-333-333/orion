"""Expose the public API for the step 013 output generation rules package."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .strategy_selection import OutputStrategy
else:
    OutputStrategy = Any


def resolve_strategy(strategy_name: str, base_iri: str, prefixes: dict[str, str]) -> OutputStrategy:
    """Return the configured output strategy or raise OrionError for an unsupported name."""
    from .strategy_selection import resolve_strategy as _resolve_strategy

    return _resolve_strategy(strategy_name, base_iri, prefixes)


__all__ = ["OutputStrategy", "resolve_strategy"]
