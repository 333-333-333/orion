"""Expose the public API for the pipeline step 009 triple extraction package."""

from .orchestrator import extract_triples_from_payload

__all__ = ['extract_triples_from_payload']
