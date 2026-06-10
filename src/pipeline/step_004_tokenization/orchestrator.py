from __future__ import annotations

from typing import Any

from pipeline.step_004_tokenization.rules import TOKEN_PATTERN, build_token_id


def tokenize_sentences(input_payload: dict[str, Any]) -> dict[str, Any]:
    preprocessed_text = input_payload["preprocessed_text"]
    source_text_id = input_payload["source_text_id"]

    tokens: list[dict[str, Any]] = []

    for sentence in input_payload["sentences"]:
        sentence_text = sentence["text"]
        sentence_id = sentence["sentence_id"]
        sentence_start_offset = sentence["start_offset"]

        for match in TOKEN_PATTERN.finditer(sentence_text):
            token_text = match.group(0)
            if token_text == "":
                continue

            start_offset = sentence_start_offset + match.start()
            end_offset = sentence_start_offset + match.end()
            token_index = len(tokens)

            tokens.append(
                {
                    "token_id": build_token_id(source_text_id, token_index, sentence_id, start_offset, end_offset, token_text),
                    "text": token_text,
                    "index": token_index,
                    "sentence_id": sentence_id,
                    "source_text_id": source_text_id,
                    "start_offset": start_offset,
                    "end_offset": end_offset,
                }
            )

    return {
        "raw_text": input_payload["raw_text"],
        "source_text_id": source_text_id,
        "metadata": input_payload["metadata"],
        "preprocessed_text": preprocessed_text,
        "operations_applied": input_payload["operations_applied"],
        "sentences": input_payload["sentences"],
        "tokens": tokens,
    }
