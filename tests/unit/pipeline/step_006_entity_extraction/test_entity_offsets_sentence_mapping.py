# UC-006 MF-9 | FUN-ENT-001 AC-2 | BR-ENT-002 | TB-ENT-001
def test_entities_use_offsets_relative_to_preprocessed_text_and_map_to_sentence_id_by_span():
    from pipeline.step_006_entity_extraction import extract_entities_from_doc

    class FakeEntity:
        def __init__(self, text, label_, start_char, end_char):
            self.text = text
            self.label_ = label_
            self.start_char = start_char
            self.end_char = end_char

    class FakeDoc:
        def __init__(self, ents):
            self.ents = ents

    preprocessed_text = "Ana lives in Madrid. Bob works at OpenAI."
    payload = {
        "raw_text": preprocessed_text,
        "preprocessed_text": preprocessed_text,
        "source_text_id": "src-ent-map-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Ana lives in Madrid.", "index": 0, "start_offset": 0, "end_offset": 19},
            {"sentence_id": "sent-0002", "text": "Bob works at OpenAI.", "index": 1, "start_offset": 20, "end_offset": 40},
        ],
        "tokens": [],
    }
    doc = FakeDoc([
        FakeEntity("Ana", "PERSON", 0, 3),
        FakeEntity("Madrid", "GPE", 13, 19),
        FakeEntity("Bob", "PERSON", 20, 23),
        FakeEntity("OpenAI", "ORG", 33, 39),
    ])

    result = extract_entities_from_doc(payload, doc)

    entities = result["entities"]
    assert len(entities) == 4
    for entity in entities:
        assert preprocessed_text[entity["start_offset"]:entity["end_offset"]] == entity["text"]

    by_text = {entity["text"]: entity for entity in entities}
    assert by_text["Ana"]["sentence_id"] == "sent-0001"
    assert by_text["Madrid"]["sentence_id"] == "sent-0001"
    assert by_text["Bob"]["sentence_id"] == "sent-0002"
    assert by_text["OpenAI"]["sentence_id"] == "sent-0002"
