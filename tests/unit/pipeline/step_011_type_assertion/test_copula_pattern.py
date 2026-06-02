# UC-TYPE-001 MF-1 | FUN-TYPE-001 AC-1 | BR-TYPE-001 | TB-TYPE-001
def test_extracts_instance_of_from_copula_john_is_a_person():
    from pipeline.step_011_type_assertion import extract_type_assertions_from_payload

    payload = {
        "raw_text": "John is a person.",
        "preprocessed_text": "John is a person.",
        "source_text_id": "src-type-001",
        "sentences": [{"sentence_id": "sent-0001", "text": "John is a person.", "index": 0, "start_offset": 0, "end_offset": 17}],
        "tokens": [
            {"token_id": "tok-0001", "text": "John", "lemma": "John", "pos": "PROPN", "sentence_id": "sent-0001", "source_text_id": "src-type-001"},
            {"token_id": "tok-0002", "text": "is", "lemma": "be", "pos": "AUX", "sentence_id": "sent-0001", "source_text_id": "src-type-001"},
            {"token_id": "tok-0003", "text": "person", "lemma": "person", "pos": "NOUN", "sentence_id": "sent-0001", "source_text_id": "src-type-001"},
        ],
        "entities": [{"entity_id": "ent-0001", "text": "John", "label": "PERSON", "normalized_text": "john", "sentence_id": "sent-0001", "source_text_id": "src-type-001"}],
        "concepts": [{"concept_id": "con-0001", "text": "person", "lemma": "person", "normalized_text": "person", "sentence_id": "sent-0001", "source_text_id": "src-type-001"}],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
    }

    result = extract_type_assertions_from_payload(payload)

    assert "type_assertions" in result
    assert len(result["type_assertions"]) == 1
    ta = result["type_assertions"][0]
    required = {
        "type_assertion_id", "instance", "class", "instance_ref", "class_ref", "relation_type", "source",
        "sentence_id", "source_text_id", "confidence", "evidence_span"
    }
    assert required.issubset(ta.keys())
    assert ta["instance"] == "john"
    assert ta["class"] == "person"
    assert ta["relation_type"] == "instance_of"
    assert ta["source"] == "copula_pattern"
