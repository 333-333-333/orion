# UC-TYPE-003 MF-1 | NFR-TYPE-001 AC-1 | BR-TYPE-005 | TB-TYPE-001
def test_type_assertions_are_deduplicated_deterministic_and_stable_order():
    from pipeline.step_011_type_assertion import extract_type_assertions_from_payload

    payload = {
        "raw_text": "John is a person. John is a person.",
        "preprocessed_text": "John is a person. John is a person.",
        "source_text_id": "src-type-004",
        "sentences": [
            {"sentence_id": "sent-0001", "text": "John is a person.", "index": 0, "start_offset": 0, "end_offset": 17},
            {"sentence_id": "sent-0002", "text": "John is a person.", "index": 1, "start_offset": 18, "end_offset": 35},
        ],
        "tokens": [],
        "entities": [{"entity_id": "ent-0001", "text": "John", "label": "PERSON", "normalized_text": "john", "sentence_id": "sent-0001", "source_text_id": "src-type-004"}],
        "concepts": [{"concept_id": "con-0001", "text": "person", "lemma": "person", "normalized_text": "person", "sentence_id": "sent-0001", "source_text_id": "src-type-004"}],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
    }

    r1 = extract_type_assertions_from_payload(payload)
    r2 = extract_type_assertions_from_payload(payload)

    assert r1["type_assertions"] == r2["type_assertions"]
    assert len(r1["type_assertions"]) == 1
