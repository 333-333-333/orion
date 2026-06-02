# UC-TYPE-002 EF-1 | CON-TYPE-001 AC-1 | BR-TYPE-004 | TB-TYPE-001
def test_does_not_emit_subclass_or_subclass_of_from_taxonomic_sentence():
    from pipeline.step_011_type_assertion import extract_type_assertions_from_payload

    payload = {
        "raw_text": "A robin is a bird.",
        "preprocessed_text": "A robin is a bird.",
        "source_text_id": "src-type-003",
        "sentences": [{"sentence_id": "sent-0001", "text": "A robin is a bird.", "index": 0, "start_offset": 0, "end_offset": 18}],
        "tokens": [],
        "entities": [{"entity_id": "ent-0001", "text": "robin", "label": "ANIMAL", "normalized_text": "robin", "sentence_id": "sent-0001", "source_text_id": "src-type-003"}],
        "concepts": [{"concept_id": "con-0001", "text": "bird", "lemma": "bird", "normalized_text": "bird", "sentence_id": "sent-0001", "source_text_id": "src-type-003"}],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
    }

    result = extract_type_assertions_from_payload(payload)

    assert all(x["relation_type"] == "instance_of" for x in result["type_assertions"])
    assert all(x["source"] != "subclass_pattern" for x in result["type_assertions"])
