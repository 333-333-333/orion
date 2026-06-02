# UC-006 MF-6 | FUN-018 AC-2 | NFR-005 AC-2 | CON-006 AC-2 | BR-TOK-002 | TASK-TOK-002 | TB-TOK-001
def test_token_offsets_are_relative_to_preprocessed_text_and_match_spans():
    from pipeline.step_004_tokenization import tokenize_sentences

    preprocessed = "Uno, dos. Tres!"
    payload = {
        "raw_text": preprocessed,
        "preprocessed_text": preprocessed,
        "source_text_id": "src-tok-off-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": len(preprocessed)}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Uno, dos.", "index": 0, "start_offset": 0, "end_offset": 9},
            {"sentence_id": "sent-0002", "text": "Tres!", "index": 1, "start_offset": 10, "end_offset": 15},
        ],
    }

    result = tokenize_sentences(payload)

    for token in result["tokens"]:
        start = token["start_offset"]
        end = token["end_offset"]
        assert preprocessed[start:end] == token["text"]
        assert start < end
        assert token["source_text_id"] == payload["source_text_id"]
        assert token["sentence_id"] in {"sent-0001", "sent-0002"}


# UC-002 EF-2 | FUN-017 AC-3 | BR-TOK-002 | TASK-TOK-002 | TB-TOK-001
def test_each_token_exposes_required_contract_fields():
    from pipeline.step_004_tokenization import tokenize_sentences

    payload = {
        "raw_text": "Hola.",
        "preprocessed_text": "Hola.",
        "source_text_id": "src-tok-contract-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Hola.", "index": 0, "start_offset": 0, "end_offset": 5},
        ],
    }

    result = tokenize_sentences(payload)

    required = {"token_id", "text", "index", "sentence_id", "source_text_id", "start_offset", "end_offset"}
    assert result["tokens"]
    for token in result["tokens"]:
        assert required.issubset(token.keys())
