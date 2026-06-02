from __future__ import annotations

from typing import Any


def build_phase1_result(raw_text: str, source_text_id: str, source_metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        'raw_text': raw_text,
        'source_text_id': source_text_id,
        'metadata': {
            'source': source_metadata,
        },
    }
