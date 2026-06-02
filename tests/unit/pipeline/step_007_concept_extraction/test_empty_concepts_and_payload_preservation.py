# UC-CONCEPT-001 AF-2 | FUN-CONCEPT-001 AC-3 | BR-CONCEPT-005 | TB-CONCEPT-001
def test_empty_candidates_return_empty_concepts_and_preserve_payload_full():
    from pipeline.step_007_concept_extraction import extract_concepts_from_payload

    class FakeDoc:
        noun_chunks = []

    payload = {
        "raw_text": "Just verbs run quickly.",
        "preprocessed_text": "Just verbs run quickly.",
        "source_text_id": "src-con-005",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [{"sentence_id": "sent-0001", "text": "Just verbs run quickly.", "index": 0, "start_offset": 0, "end_offset": 23}],
        "tokens": [],
        "entities": [],
    }

    result = extract_concepts_from_payload(payload, FakeDoc())

    assert result["raw_text"] == payload["raw_text"]
    assert result["preprocessed_text"] == payload["preprocessed_text"]
    assert result["source_text_id"] == payload["source_text_id"]
    assert result["metadata"] == payload["metadata"]
    assert result["operations_applied"] == payload["operations_applied"]
    assert result["sentences"] == payload["sentences"]
    assert result["tokens"] == payload["tokens"]
    assert result["entities"] == payload["entities"]
    assert result["concepts"] == []
