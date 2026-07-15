"""Implement input-intake strategies for strings and UTF-8 text files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from .exceptions import OrionError


def ensure_non_empty_text(raw_text: str) -> str:
    """Return non-empty text or raise OrionError for an empty input."""
    if raw_text == '':
        raise OrionError('Input text cannot be empty')
    return raw_text


def build_file_source_metadata(path: Path, raw_text: str) -> dict[str, Any]:
    """Build source metadata for text read from a file."""
    return {
        'kind': 'file',
        'path': str(path),
        'start_offset': 0,
        'end_offset': len(raw_text),
    }


def build_string_source_metadata(raw_text: str) -> dict[str, Any]:
    """Build source metadata for text supplied directly as a string."""
    return {
        'kind': 'string',
        'start_offset': 0,
        'end_offset': len(raw_text),
    }


class InputIntakeStrategy(Protocol):
    """Protocol for converting supported input into text and source metadata."""
    def ingest(self, input_data: Any) -> tuple[str, dict[str, Any]]:
        """Return validated text and source metadata for supported input."""
        ...


class StringInputStrategy:
    """For str input, prioritize .txt path when applicable."""

    def ingest(self, input_data: Any) -> tuple[str, dict[str, Any]]:
        """Interpret .txt-suffixed strings as paths; otherwise ingest the string as text."""
        if not isinstance(input_data, str):
            raise OrionError('Input must be text (str) or .txt path')

        candidate = Path(input_data)
        if candidate.suffix == '.txt':
            if not candidate.exists():
                raise OrionError(f'Input path does not exist: {candidate}')
            with candidate.open('r', encoding='utf-8', newline='') as handle:
                raw_text = ensure_non_empty_text(handle.read())
            return raw_text, build_file_source_metadata(candidate, raw_text)

        raw_text = ensure_non_empty_text(input_data)
        return raw_text, build_string_source_metadata(raw_text)


class TxtFileInputStrategy:
    """Input strategy for pathlib Path values that identify UTF-8 .txt files."""
    def ingest(self, input_data: Any) -> tuple[str, dict[str, Any]]:
        """Read a UTF-8 .txt Path and return text with file metadata."""
        if not isinstance(input_data, Path):
            raise OrionError('Input must be text (str) or .txt path')
        if input_data.suffix != '.txt':
            raise OrionError('Only .txt files are supported')
        if not input_data.exists():
            raise OrionError(f'Input path does not exist: {input_data}')

        with input_data.open('r', encoding='utf-8', newline='') as handle:
            raw_text = ensure_non_empty_text(handle.read())
        return raw_text, build_file_source_metadata(input_data, raw_text)


def select_input_strategy(input_data: Any, string_strategy: InputIntakeStrategy, txt_file_strategy: InputIntakeStrategy) -> InputIntakeStrategy:
    """Select the intake strategy for string or Path input and reject unsupported types."""
    if isinstance(input_data, str):
        return string_strategy
    if isinstance(input_data, Path):
        return txt_file_strategy
    raise OrionError('Input must be text (str) or .txt path')
