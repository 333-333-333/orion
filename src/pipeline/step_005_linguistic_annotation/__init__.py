"""Expose the public API for the pipeline step 005 linguistic annotation package."""

from .orchestrator import annotate_tokens

__all__ = ["annotate_tokens"]
