from __future__ import annotations

from typing import Any

from pipeline.step_008_coreference_resolution.rules import (
    COREF_RELATIVE_PRONOUNS,
    normalize_text,
    noun_chunks_for_sentence,
    resolve_mention,
)


def resolve_coreferences_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    tokens = input_payload.get("tokens", [])
    noun_chunks = input_payload.get("noun_chunks", [])

    coreferences: list[dict[str, Any]] = []
    for token in tokens:
        if normalize_text(token.get("text", "")) not in COREF_RELATIVE_PRONOUNS:
            continue
        sentence_id = token.get("sentence_id", "")
        sentence_chunks = noun_chunks_for_sentence(noun_chunks, sentence_id)
        coreferences.append(resolve_mention(token, sentence_chunks))

    result = {k: v for k, v in input_payload.items() if not k.startswith("_spacy")}
    result["coreferences"] = coreferences
    return result
