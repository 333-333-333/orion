# UC-004 MF-3 | NFR-001 AC-1 | BR-ENT-003 | TB-ENT-001
def test_entity_id_is_deterministic_for_same_payload_and_doc_entities():
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

    payload = {
        "raw_text": "Grace Hopper worked at Harvard.",
        "preprocessed_text": "Grace Hopper worked at Harvard.",
        "source_text_id": "src-ent-det-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Grace Hopper worked at Harvard.", "index": 0, "start_offset": 0, "end_offset": 30}
        ],
        "tokens": [],
    }
    doc = FakeDoc([
        FakeEntity("Grace Hopper", "PERSON", 0, 12),
        FakeEntity("Harvard", "ORG", 23, 30),
    ])

    result1 = extract_entities_from_doc(payload, doc)
    result2 = extract_entities_from_doc(payload, doc)

    ids1 = [entity["entity_id"] for entity in result1["entities"]]
    ids2 = [entity["entity_id"] for entity in result2["entities"]]
    assert ids1 == ids2
