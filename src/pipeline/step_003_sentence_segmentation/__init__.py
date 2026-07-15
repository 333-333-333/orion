"""Expose the public API for the pipeline step 003 sentence segmentation package."""

from .orchestrator import segment_sentences

__all__ = ["segment_sentences"]
