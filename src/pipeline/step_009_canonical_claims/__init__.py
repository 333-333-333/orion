"""Expose the public API for the pipeline step 009 canonical claims package."""

from .orchestrator import extract_canonical_claims_from_payload

__all__ = ['extract_canonical_claims_from_payload']
