"""Orchestrate the coreference resolution pipeline stage while preserving the payload contract."""

from __future__ import annotations

from typing import Any

from pipeline.step_008_coreference_resolution.rules import (
    COREF_RELATIVE_PRONOUNS,
    normalize_text,
    noun_chunks_for_sentence,
    resolve_mention,
    resolve_syntactic_relative,
)


def _nonreferential_content_marker(token: dict[str, Any], sentence_tokens: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Represent relative-looking complementizers that do not refer to an antecedent."""
    mention_start = int(token.get("start_offset", -1))
    prior = [item for item in sentence_tokens if int(item.get("end_offset", -1)) <= mention_start]
    if not prior or str(prior[-1].get("text", "")).casefold() not in {"possibility", "probability"}:
        return None
    return {
        "mention": str(token.get("text", "")),
        "mention_span": {"start_offset": mention_start, "end_offset": int(token.get("end_offset", -1))},
        "antecedent": "",
        "antecedent_span": {"start_offset": -1, "end_offset": -1},
        "confidence": 1.0,
        "score_breakdown": {"distance": 1.0, "position": 1.0, "noun_bonus": 0.0, "total": 1.0},
        "evidence_span": {"start_offset": mention_start, "end_offset": int(token.get("end_offset", -1))},
        "status": "non_referential",
        "reason": "content_clause_complementizer",
        "resolution_reason": "content_clause_complementizer",
    }


def resolve_coreferences_from_payload(input_payload: dict[str, Any]) -> dict[str, Any]:
    """Resolve supported relative pronouns and attach auditable coreference records."""
    tokens = input_payload.get("tokens", [])
    noun_chunks = input_payload.get("noun_chunks", [])
    concepts = input_payload.get("concepts", [])

    coreferences: list[dict[str, Any]] = []
    for token in tokens:
        if normalize_text(token.get("text", "")) not in COREF_RELATIVE_PRONOUNS:
            continue
        sentence_id = token.get("sentence_id", "")
        sentence_tokens = [item for item in tokens if item.get("sentence_id") == sentence_id]
        content_marker = _nonreferential_content_marker(token, sentence_tokens)
        if content_marker is not None:
            coreferences.append(content_marker)
            continue
        syntactic = resolve_syntactic_relative(token, sentence_tokens)
        if syntactic is not None:
            coreferences.append(syntactic)
            continue
        sentence_chunks = noun_chunks_for_sentence(noun_chunks or concepts, sentence_id)
        coreferences.append(resolve_mention(token, sentence_chunks))

    result = {k: v for k, v in input_payload.items() if not k.startswith("_spacy")}
    result["coreferences"] = coreferences
    return result
