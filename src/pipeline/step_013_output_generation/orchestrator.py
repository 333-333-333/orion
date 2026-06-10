from __future__ import annotations

from typing import Any

from .namespace import validate_and_resolve_prefixes, validate_base_iri
from .rules import resolve_strategy


def generate_output_from_payload(
    input_payload: dict[str, Any],
    output_strategy: str,
    base_iri: str = 'https://orion.local/resource/',
    prefixes: dict[str, str] | None = None,
) -> dict[str, Any]:
    resolved_base_iri = validate_base_iri(base_iri)
    resolved_prefixes = validate_and_resolve_prefixes(resolved_base_iri, prefixes)
    return resolve_strategy(output_strategy, resolved_base_iri, resolved_prefixes).generate(input_payload)
