"""Expose the public API for the pipeline step 010 taxonomy induction package."""

from .orchestrator import extract_taxonomy_relations_from_payload

__all__ = ['extract_taxonomy_relations_from_payload']
