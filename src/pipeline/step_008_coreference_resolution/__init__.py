"""Expose the public API for the pipeline step 008 coreference resolution package."""

from .orchestrator import resolve_coreferences_from_payload

__all__ = ["resolve_coreferences_from_payload"]
