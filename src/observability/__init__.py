from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol

_SENSITIVE_KEYS = frozenset({"raw_text", "full_input"})


def _sanitize_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    safe = dict(metadata or {})
    for key in _SENSITIVE_KEYS:
        safe.pop(key, None)
    return safe


@dataclass(frozen=True)
class LogEvent:
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
        object.__setattr__(self, "metadata", _sanitize_metadata(self.metadata))

    def to_dict(self) -> dict[str, Any]:
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
    def emit(self, event: LogEvent) -> None: ...


class NullLogSink:
    def emit(self, event: LogEvent) -> None:
        return None


class MemoryLogSink:
    def __init__(self) -> None:
        self.events: list[LogEvent] = []

    def emit(self, event: LogEvent) -> None:
        self.events.append(event)


class JsonlFileLogSink:
    def __init__(self, output_file: str | Path) -> None:
        self.output_file = Path(output_file)

    def emit(self, event: LogEvent) -> None:
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
