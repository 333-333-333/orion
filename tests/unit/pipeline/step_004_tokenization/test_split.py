# UC-002 MF-4 | UC-003 MF-4 | FUN-017 AC-1 | FUN-017 AC-2 | CON-010 AC-1 | BR-TOK-001 | TASK-TOK-001 | TB-TOK-001
def test_tokenization_splits_words_and_punctuation_deterministically_and_preserves_sentence_order():
    from pipeline.step_004_tokenization import tokenize_sentences

    payload = {
        "raw_text": "Hola, mundo. Chau!",
        "preprocessed_text": "Hola, mundo. Chau!",
        "source_text_id": "src-tok-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Hola, mundo.", "index": 0, "start_offset": 0, "end_offset": 12},
            {"sentence_id": "sent-0002", "text": "Chau!", "index": 1, "start_offset": 13, "end_offset": 18},
        ],
    }

    result = tokenize_sentences(payload)

    assert result["raw_text"] == payload["raw_text"]
    assert result["preprocessed_text"] == payload["preprocessed_text"]
    assert result["source_text_id"] == payload["source_text_id"]
    assert result["metadata"] == payload["metadata"]
    assert result["operations_applied"] == payload["operations_applied"]
    assert result["sentences"] == payload["sentences"]

    assert "tokens" in result
    token_texts = [t["text"] for t in result["tokens"]]
    assert token_texts == ["Hola", ",", "mundo", ".", "Chau", "!"]


# UC-006 AF-2 | FUN-018 AC-1 | NFR-001 AC-2 | NFR-002 AC-2 | BR-TOK-001 | TASK-TOK-001 | TB-TOK-001
def test_tokenization_is_deterministic_with_stable_token_ids_and_indices():
    from pipeline.step_004_tokenization import tokenize_sentences

    payload = {
        "raw_text": "A, B.",
        "preprocessed_text": "A, B.",
        "source_text_id": "src-tok-det-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "A, B.", "index": 0, "start_offset": 0, "end_offset": 5},
        ],
    }

    first = tokenize_sentences(payload)
    second = tokenize_sentences(payload)

    assert first["tokens"] == second["tokens"]

    ids = [t["token_id"] for t in first["tokens"]]
    assert len(ids) == len(set(ids))
    assert [t["index"] for t in first["tokens"]] == list(range(len(first["tokens"])))
