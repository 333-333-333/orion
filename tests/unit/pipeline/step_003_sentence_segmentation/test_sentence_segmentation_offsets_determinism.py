# UC-006 MF-5 | FUN-015 AC-2 | NFR-001 AC-2 | NFR-002 AC-2 | NFR-005 AC-2 | CON-006 AC-2 | TASK-SENT-002 | TB-SENT-001
def test_sentence_segmentation_is_deterministic_with_stable_sentence_ids_and_offsets_on_preprocessed_text():
    from pipeline.step_003_sentence_segmentation import segment_sentences

    payload = {
        "raw_text": "A. B? C!",
        "preprocessed_text": "A. B? C!",
        "source_text_id": "src-det-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": 8}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
    }

    first = segment_sentences(payload)
    second = segment_sentences(payload)

    assert first["raw_text"] == payload["raw_text"]
    assert first["source_text_id"] == payload["source_text_id"]
    assert first["metadata"] == payload["metadata"]
    assert first["operations_applied"] == payload["operations_applied"]

    assert first["sentences"] == second["sentences"]

    for sentence in first["sentences"]:
        start = sentence["start_offset"]
        end = sentence["end_offset"]
        assert payload["preprocessed_text"][start:end] == sentence["text"]
        assert sentence["sentence_id"]
