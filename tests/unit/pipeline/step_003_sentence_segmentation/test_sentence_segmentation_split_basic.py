# UC-002 MF-3 | UC-003 MF-3 | FUN-003 AC-2 | FUN-004 AC-2 | FUN-013 AC-2 | CON-010 AC-1 | TASK-SENT-001 | TB-SENT-001
def test_sentence_segmentation_splits_by_dot_question_exclamation_no_empty_and_keeps_order():
    from pipeline.step_003_sentence_segmentation import segment_sentences

    payload = {
        "raw_text": "Alpha.  Beta?\n\nGamma!   Delta.",
        "preprocessed_text": "Alpha. Beta?\nGamma! Delta.",
        "source_text_id": "src-sent-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
    }

    result = segment_sentences(payload)

    assert "sentences" in result
    texts = [s["text"] for s in result["sentences"]]
    assert texts == ["Alpha.", "Beta?", "Gamma!", "Delta."]
    assert all(t.strip() for t in texts)
