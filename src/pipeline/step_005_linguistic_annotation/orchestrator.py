from __future__ import annotations

from typing import Any


def _extract_doc_tokens(doc: Any) -> list[dict[str, Any]]:
    extracted: list[dict[str, Any]] = []
    for index, token in enumerate(doc):
        text = getattr(token, "text", None)
        if text is None:
            continue
        start = getattr(token, "idx", None)
        extracted.append({"token": token, "text": text, "start": start, "index": index})
    return extracted


def _find_matching_doc_token(orion_token: dict[str, Any], doc_tokens: list[dict[str, Any]], fallback_index: int) -> tuple[Any | None, int]:
    start_offset = orion_token.get("start_offset")
    text = orion_token.get("text")

    for idx in range(fallback_index, len(doc_tokens)):
        candidate = doc_tokens[idx]
        if candidate["start"] == start_offset and candidate["text"] == text:
            return candidate["token"], idx + 1

    for idx in range(fallback_index, len(doc_tokens)):
        candidate = doc_tokens[idx]
        if candidate["start"] == start_offset:
            return candidate["token"], idx + 1

    if fallback_index < len(doc_tokens):
        return doc_tokens[fallback_index]["token"], fallback_index + 1

    return None, fallback_index


def annotate_tokens(input_payload: dict[str, Any], nlp_model: Any) -> dict[str, Any]:
    preprocessed_text = input_payload["preprocessed_text"]
    doc = nlp_model(preprocessed_text)
    doc_tokens = _extract_doc_tokens(doc)

    annotated_tokens: list[dict[str, Any]] = []
    fallback_index = 0

    for token in input_payload["tokens"]:
        matched_doc_token, fallback_index = _find_matching_doc_token(token, doc_tokens, fallback_index)

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
