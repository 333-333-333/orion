"""Expose the public API for the step 008 relation extraction rules package."""

from .relation_patterns import _dedupe_stable, _extract_copula_relations, _extract_svo_relations

__all__ = ["_dedupe_stable", "_extract_copula_relations", "_extract_svo_relations"]
