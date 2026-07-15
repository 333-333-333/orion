"""Build the canonical payload produced by input intake."""

from __future__ import annotations

from typing import Any


def build_phase1_result(raw_text: str, source_text_id: str, source_metadata: dict[str, Any]) -> dict[str, Any]:
    """Build the input-intake payload consumed by downstream pipeline stages."""
    return {
        'raw_text': raw_text,
        'source_text_id': source_text_id,
        'metadata': {
            'source': source_metadata,
        },
    }
