from __future__ import annotations

from typing import Any, Protocol

from pipeline.step_001_input_intake import OrionError
from pipeline.step_013_output_generation.owl_strategy import OwlOutputStrategy
from pipeline.step_013_output_generation.rdf_strategy import RdfOutputStrategy

_BR_OUTPUT_STRATEGY_RDF = 'rdf'
_BR_OUTPUT_STRATEGY_OWL = 'owl'


class OutputStrategy(Protocol):
    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


def resolve_strategy(strategy_name: str, base_iri: str, prefixes: dict[str, str]) -> OutputStrategy:
    if strategy_name == _BR_OUTPUT_STRATEGY_RDF:
        return RdfOutputStrategy(base_iri=base_iri, prefixes=prefixes)
    if strategy_name == _BR_OUTPUT_STRATEGY_OWL:
        return OwlOutputStrategy(base_iri=base_iri, prefixes=prefixes)
    raise OrionError('ORION config error: output_strategy must be one of: rdf, owl')
