"""Expose the public API for the pipeline step 011 type assertion package."""

from .orchestrator import extract_type_assertions_from_payload

__all__ = ['extract_type_assertions_from_payload']
