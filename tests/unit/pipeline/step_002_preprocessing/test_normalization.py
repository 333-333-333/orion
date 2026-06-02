
# UC-002 AF-1 | FUN-003 AC-1 | NFR-001 AC-1 | TASK-PRP-002 | TB-PRP-001
def test_preprocessing_unicode_normalization_is_deterministic_and_repeatable():
    from pipeline.step_002_preprocessing import preprocess_input

    decomposed = "Cafe\u0301"
    payload = {
        "raw_text": decomposed,
        "source_text_id": "src-unicode-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": len(decomposed)}},
    }

    r1 = preprocess_input(payload)
    r2 = preprocess_input(payload)

    assert r1["preprocessed_text"] == r2["preprocessed_text"]
    assert r1["preprocessed_text"] != decomposed


# UC-002 AF-2 | FUN-003 AC-1 | NFR-005 AC-1 | TASK-PRP-002 | TB-PRP-001
def test_preprocessing_collapses_repeated_spaces_and_normalizes_newlines_only():
    from pipeline.step_002_preprocessing import preprocess_input

    raw = "Hola   mundo\r\n\r\nLinea   dos\rLinea   tres"
    payload = {
        "raw_text": raw,
        "source_text_id": "src-space-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": len(raw)}},
    }

    result = preprocess_input(payload)

    assert "   " not in result["preprocessed_text"]
    assert "\r" not in result["preprocessed_text"]
    assert "\n" in result["preprocessed_text"]


# UC-002 EF-2 | FUN-003 AC-1 | CON-010 AC-1 | TASK-PRP-002 | TB-PRP-001
def test_preprocessing_does_not_do_tokenization_segmentation_or_lemmatization_side_effects():
    from pipeline.step_002_preprocessing import preprocess_input

    raw = "Running runners run"
    payload = {
        "raw_text": raw,
        "source_text_id": "src-no-nlp-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": len(raw)}},
    }

    result = preprocess_input(payload)

    assert "tokenization" not in result
    assert "tokens" not in result
    assert "sentences" not in result
    assert "lemmas" not in result
    assert "Running" in result["preprocessed_text"]
