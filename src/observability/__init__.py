"""Expose the public API for the observability package."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol

_SENSITIVE_KEYS = frozenset({"raw_text", "full_input"})


def _sanitize_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    """Copy metadata while removing raw input fields that must not be logged."""
    safe = dict(metadata or {})
    for key in _SENSITIVE_KEYS:
        safe.pop(key, None)
    return safe


@dataclass(frozen=True)
class LogEvent:
    """Immutable structured log event that strips sensitive raw-input metadata."""
    phase: str
    event_type: str
    status: str
    source_context_id: str | None = None
    use_case_id: str | None = None
    requirement_id: str | None = None
    operation_name: str | None = None
    exception_category: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Remove sensitive metadata keys from the immutable event after initialization."""
        object.__setattr__(self, "metadata", _sanitize_metadata(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return the sanitized event payload, omitting unset optional fields."""
        payload: dict[str, Any] = {
            "phase": self.phase,
            "event_type": self.event_type,
            "status": self.status,
        }
        if self.source_context_id is not None:
            payload["source_context_id"] = self.source_context_id
        if self.use_case_id is not None:
            payload["use_case_id"] = self.use_case_id
        if self.requirement_id is not None:
            payload["requirement_id"] = self.requirement_id
        if self.operation_name is not None:
            payload["operation_name"] = self.operation_name
        if self.exception_category is not None:
            payload["exception_category"] = self.exception_category
        payload["metadata"] = _sanitize_metadata(self.metadata)
        return payload


class LogSink(Protocol):
    """Protocol implemented by structured logging destinations."""
    def emit(self, event: LogEvent) -> None:
        """Accept a structured event for delivery by a logging sink."""
        ...


class NullLogSink:
    """Logging sink that intentionally discards every event."""
    def emit(self, event: LogEvent) -> None:
        """Discard the event without side effects."""
        return None


class MemoryLogSink:
    """Logging sink that retains events for observation and tests."""
    def __init__(self) -> None:
        """Initialize the MemoryLogSink."""
        self.events: list[LogEvent] = []

    def emit(self, event: LogEvent) -> None:
        """Append the event to the in-memory event sequence."""
        self.events.append(event)


class JsonlFileLogSink:
    """Logging sink that appends sanitized events to a JSON Lines file."""
    def __init__(self, output_file: str | Path) -> None:
        """Initialize the JsonlFileLogSink."""
        self.output_file = Path(output_file)

    def emit(self, event: LogEvent) -> None:
        """Append one sanitized event as UTF-8 JSON Lines, creating parent directories as needed."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(event.to_dict(), ensure_ascii=False)
        with self.output_file.open('a', encoding='utf-8') as handle:
            handle.write(f"{line}\n")


__all__ = [
    "JsonlFileLogSink",
    "LogEvent",
    "LogSink",
    "MemoryLogSink",
    "NullLogSink",
]
