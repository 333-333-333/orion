# UC-CONCEPT-001 AF-1 | FUN-CONCEPT-001 AC-2 | BR-CONCEPT-002 | TB-CONCEPT-001
def test_entity_labels_are_projected_to_concepts_source_entity_label():
    from pipeline.step_007_concept_extraction import extract_concepts_from_payload

    class FakeDoc:
        noun_chunks = []

    payload = {
        "raw_text": "Ada Lovelace founded Analytical Engine Society.",
        "preprocessed_text": "Ada Lovelace founded Analytical Engine Society.",
        "source_text_id": "src-con-002",
        "sentences": [{"sentence_id": "sent-0001", "text": "Ada Lovelace founded Analytical Engine Society.", "index": 0, "start_offset": 0, "end_offset": 45}],
        "tokens": [],
        "entities": [
            {"entity_id": "ent-0001", "text": "Ada Lovelace", "label": "PERSON", "start_offset": 0, "end_offset": 12, "sentence_id": "sent-0001", "source_text_id": "src-con-002"},
            {"entity_id": "ent-0002", "text": "Analytical Engine Society", "label": "ORG", "start_offset": 21, "end_offset": 45, "sentence_id": "sent-0001", "source_text_id": "src-con-002"},
        ],
    }

    result = extract_concepts_from_payload(payload, FakeDoc())

    assert any(c["source"] == "entity_label" for c in result["concepts"])
    assert any(c["text"] == "Ada Lovelace" for c in result["concepts"])
    assert any(c["text"] == "Analytical Engine Society" for c in result["concepts"])
