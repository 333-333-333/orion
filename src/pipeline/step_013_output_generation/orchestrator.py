from __future__ import annotations

from typing import Any, Protocol

from pipeline.step_001_input_intake import OrionError

from .namespace import validate_and_resolve_prefixes, validate_base_iri
from .owl_strategy import OwlOutputStrategy
from .rdf_strategy import RdfOutputStrategy

_BR_OUTPUT_STRATEGY_RDF = 'rdf'
_BR_OUTPUT_STRATEGY_OWL = 'owl'


class OutputStrategy(Protocol):
    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


def _resolve_strategy(strategy_name: str, base_iri: str, prefixes: dict[str, str]) -> OutputStrategy:
    if strategy_name == _BR_OUTPUT_STRATEGY_RDF:
        return RdfOutputStrategy(base_iri=base_iri, prefixes=prefixes)
    if strategy_name == _BR_OUTPUT_STRATEGY_OWL:
        return OwlOutputStrategy(base_iri=base_iri, prefixes=prefixes)
    raise OrionError('ORION config error: output_strategy must be one of: rdf, owl')


def generate_output_from_payload(
    input_payload: dict[str, Any],
    output_strategy: str,
    base_iri: str = 'https://orion.local/resource/',
    prefixes: dict[str, str] | None = None,
) -> dict[str, Any]:
    resolved_base_iri = validate_base_iri(base_iri)
    resolved_prefixes = validate_and_resolve_prefixes(resolved_base_iri, prefixes)
    return _resolve_strategy(output_strategy, resolved_base_iri, resolved_prefixes).generate(input_payload)
