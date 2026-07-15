"""Expose the public API for the pipeline step 006 entity extraction package."""

from .orchestrator import extract_entities_from_doc

__all__ = ["extract_entities_from_doc"]
