"""Expose the public API for the step 008 coreference resolution rules package."""

from .relative_pronoun import COREF_RELATIVE_PRONOUNS, normalize_text, noun_chunks_for_sentence, resolve_mention, resolve_syntactic_relative

__all__ = [
    "COREF_RELATIVE_PRONOUNS",
    "normalize_text",
    "noun_chunks_for_sentence",
    "resolve_mention",
    "resolve_syntactic_relative",
]
