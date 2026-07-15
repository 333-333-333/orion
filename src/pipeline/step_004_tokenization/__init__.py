"""Expose the public API for the pipeline step 004 tokenization package."""

from .orchestrator import tokenize_sentences

__all__ = ["tokenize_sentences"]
