"""Orchestrate the input intake pipeline stage while preserving the payload contract."""

from __future__ import annotations

from typing import Any

from .result import build_phase1_result
from .source_id import build_source_text_id
from .strategies import (
    InputIntakeStrategy,
    StringInputStrategy,
    TxtFileInputStrategy,
    select_input_strategy,
)


def process_input_intake(
    input_data: Any,
    config: dict[str, Any],
    string_strategy: InputIntakeStrategy | None = None,
    txt_file_strategy: InputIntakeStrategy | None = None,
) -> dict[str, Any]:
    """Select an intake strategy and return validated text with deterministic source metadata."""
    effective_string_strategy = string_strategy or StringInputStrategy()
    effective_txt_file_strategy = txt_file_strategy or TxtFileInputStrategy()

    strategy = select_input_strategy(
        input_data=input_data,
        string_strategy=effective_string_strategy,
        txt_file_strategy=effective_txt_file_strategy,
    )
    raw_text, source_metadata = strategy.ingest(input_data)

    source_text_id = build_source_text_id(
        raw_text=raw_text,
        source_kind=source_metadata.get('kind', 'string'),
        config=config,
    )

    return build_phase1_result(raw_text, source_text_id, source_metadata)
