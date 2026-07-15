"""Expose the public API for the pipeline step 008 relation extraction package."""

from .orchestrator import extract_relations_from_payload

__all__ = ["extract_relations_from_payload"]
