from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .strategy_selection import OutputStrategy
else:
    OutputStrategy = Any


def resolve_strategy(strategy_name: str, base_iri: str, prefixes: dict[str, str]) -> OutputStrategy:
    from .strategy_selection import resolve_strategy as _resolve_strategy

    return _resolve_strategy(strategy_name, base_iri, prefixes)


__all__ = ["OutputStrategy", "resolve_strategy"]
