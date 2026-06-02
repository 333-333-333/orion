# UC-002 MF-6 | FUN-ENT-001 AC-1 | BR-ENT-001 | TB-ENT-001
def test_extract_entities_from_doc_adds_entities_and_preserves_existing_payload_fields():
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
        "raw_text": "  Barack Obama visited Paris.  ",
        "preprocessed_text": "Barack Obama visited Paris.",
        "source_text_id": "src-ent-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Barack Obama visited Paris.", "index": 0, "start_offset": 0, "end_offset": 27}
        ],
        "tokens": [
            {"token_id": "tok-0001", "text": "Barack", "index": 0, "sentence_id": "sent-0001", "source_text_id": "src-ent-001", "start_offset": 0, "end_offset": 6, "lemma": "Barack", "pos": "PROPN", "tag": "NNP", "dependency": "compound"}
        ],
    }
    doc = FakeDoc([
        FakeEntity("Barack Obama", "PERSON", 0, 12),
        FakeEntity("Paris", "GPE", 21, 26),
    ])

    result = extract_entities_from_doc(payload, doc)

    assert result["raw_text"] == payload["raw_text"]
    assert result["preprocessed_text"] == payload["preprocessed_text"]
    assert result["source_text_id"] == payload["source_text_id"]
    assert result["sentences"] == payload["sentences"]
    assert result["tokens"] == payload["tokens"]
    assert "entities" in result
    assert len(result["entities"]) == 2

    for entity in result["entities"]:
        assert {"entity_id", "text", "label", "start_offset", "end_offset", "sentence_id", "source_text_id"}.issubset(entity.keys())
