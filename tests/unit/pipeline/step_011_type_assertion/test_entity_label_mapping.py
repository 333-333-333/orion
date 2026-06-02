# UC-TYPE-001 AF-1 | FUN-TYPE-001 AC-2 | BR-TYPE-002 | BR-TYPE-003 | TB-TYPE-001
def test_entity_label_mapping_generates_person_and_org_type_assertions():
    from pipeline.step_011_type_assertion import extract_type_assertions_from_payload

    payload = {
        "raw_text": "John founded Apple.",
        "preprocessed_text": "John founded Apple.",
        "source_text_id": "src-type-002",
        "sentences": [{"sentence_id": "sent-0001", "text": "John founded Apple.", "index": 0, "start_offset": 0, "end_offset": 19}],
        "tokens": [],
        "entities": [
            {"entity_id": "ent-0001", "text": "John", "label": "PERSON", "normalized_text": "john", "sentence_id": "sent-0001", "source_text_id": "src-type-002"},
            {"entity_id": "ent-0002", "text": "Apple", "label": "ORG", "normalized_text": "apple", "sentence_id": "sent-0001", "source_text_id": "src-type-002"},
        ],
        "concepts": [
            {"concept_id": "con-0001", "text": "person", "lemma": "person", "normalized_text": "person", "sentence_id": "sent-0001", "source_text_id": "src-type-002"},
            {"concept_id": "con-0002", "text": "organization", "lemma": "organization", "normalized_text": "organization", "sentence_id": "sent-0001", "source_text_id": "src-type-002"},
        ],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
    }

    result = extract_type_assertions_from_payload(payload)
    got = {(x["instance"], x["class"], x["source"], x["relation_type"]) for x in result["type_assertions"]}

    assert ("john", "person", "entity_label", "instance_of") in got
    assert ("apple", "organization", "entity_label", "instance_of") in got
