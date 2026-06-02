# UC-002 AF-2 | FUN-ENT-001 AC-3 | BR-ENT-004 | TB-ENT-001
def test_extract_entities_from_doc_returns_empty_entities_when_doc_has_no_entities():
    from pipeline.step_006_entity_extraction import extract_entities_from_doc

    class FakeDoc:
        def __init__(self):
            self.ents = []

    payload = {
        "raw_text": "No named entities here.",
        "preprocessed_text": "No named entities here.",
        "source_text_id": "src-ent-empty-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "No named entities here.", "index": 0, "start_offset": 0, "end_offset": 23}
        ],
        "tokens": [],
    }

    result = extract_entities_from_doc(payload, FakeDoc())

    assert "entities" in result
    assert result["entities"] == []
