from __future__ import annotations

import importlib
from typing import Any

import pytest


_SPACY_MODEL_CACHE: dict[str, Any] = {}


def _cached_orion_spacy_model(self: Any) -> Any:
    model_name = self._orion_config.spacy_model
    cached = _SPACY_MODEL_CACHE.get(model_name)
    if cached is not None:
        self._nlp_model = cached
        return cached
    spacy = importlib.import_module("spacy")
    model = spacy.load(model_name)
    _SPACY_MODEL_CACHE[model_name] = model
    self._nlp_model = model
    return model


def _annotate_tokens_with_cached_active_doc(self: Any, input_payload: dict[str, Any]) -> dict[str, Any]:
    # NFR-SMOKE-001 AC-4 | BR-SMOKE-006: smoke harness optimization only; reuse the exact spaCy Doc.
    from pipeline.step_005_linguistic_annotation.orchestrator import (
        _extract_doc_tokens,
        _find_matching_doc_token,
    )

    preprocessed_text = input_payload["preprocessed_text"]
    doc = self._load_spacy_model()(preprocessed_text)
    self._active_doc = doc
    doc_tokens = _extract_doc_tokens(doc)

    annotated_tokens: list[dict[str, Any]] = []
    for token in input_payload["tokens"]:
        matched_doc_token = _find_matching_doc_token(token, doc_tokens)
        lemma = token["text"]
        pos = ""
        tag = ""
        dependency = ""
        head_text = ""
        if matched_doc_token is not None:
            lemma = getattr(matched_doc_token, "lemma_", lemma) or lemma
            pos = getattr(matched_doc_token, "pos_", "") or ""
            tag = getattr(matched_doc_token, "tag_", "") or ""
            dependency = getattr(matched_doc_token, "dep_", "") or ""
            head = getattr(matched_doc_token, "head", None)
            head_text = getattr(head, "text", "") if head is not None else ""

        annotated_token = dict(token)
        annotated_token["lemma"] = lemma
        annotated_token["pos"] = pos
        annotated_token["tag"] = tag
        annotated_token["dependency"] = dependency
        annotated_token["head_text"] = head_text
        annotated_tokens.append(annotated_token)

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": input_payload["source_text_id"],
        "metadata": input_payload["metadata"],
        "preprocessed_text": preprocessed_text,
        "operations_applied": input_payload["operations_applied"],
        "sentences": input_payload["sentences"],
        "tokens": annotated_tokens,
    }


@pytest.fixture(scope="session", autouse=True)
def _reuse_spacy_model_across_smoke_orion_instances() -> None:
    # NFR-SMOKE-001 AC-4 | BR-SMOKE-006: smoke harness optimization only; semantics unchanged.
    from orion import ORION

    original_load_spacy_model = ORION._load_spacy_model
    original_run_linguistic_annotation = ORION._run_linguistic_annotation
    ORION._load_spacy_model = _cached_orion_spacy_model
    ORION._run_linguistic_annotation = _annotate_tokens_with_cached_active_doc
    try:
        yield
    finally:
        ORION._load_spacy_model = original_load_spacy_model
        ORION._run_linguistic_annotation = original_run_linguistic_annotation
        _SPACY_MODEL_CACHE.clear()
