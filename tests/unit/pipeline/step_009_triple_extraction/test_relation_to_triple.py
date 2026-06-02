# UC-TRIPLE-001 MF-1 | FUN-TRIPLE-001 AC-1 | BR-TRIPLE-001 | BR-TRIPLE-002 | TB-TRIPLE-001
def test_valid_relation_maps_to_triple_with_required_fields_and_refs_fallback():
    from pipeline.step_009_triple_extraction import extract_triples_from_payload

    payload = {
        "raw_text": "Alice builds robots.",
        "preprocessed_text": "Alice builds robots.",
        "source_text_id": "src-tri-001",
        "sentences": [{"sentence_id": "sent-0001", "text": "Alice builds robots.", "index": 0, "start_offset": 0, "end_offset": 20}],
        "tokens": [],
        "entities": [{"entity_id": "ent-0001", "text": "Alice", "normalized_text": "alice", "start_offset": 0, "end_offset": 5, "sentence_id": "sent-0001", "source_text_id": "src-tri-001"}],
        "concepts": [{"concept_id": "con-0001", "text": "robots", "lemma": "robot", "normalized_text": "robot", "start_offset": 13, "end_offset": 19, "sentence_id": "sent-0001", "source_text_id": "src-tri-001"}],
        "relations": [
            {"relation_id": "rel-0001", "subject_text": "Alice", "subject_ref": "ent-0001", "predicate": "builds", "object_text": "robots", "object_ref": "con-0001", "sentence_id": "sent-0001", "source_text_id": "src-tri-001", "confidence": 0.92, "evidence_span": {"start_offset": 0, "end_offset": 19}},
            {"relation_id": "rel-0002", "subject_text": "Bob", "subject_ref": None, "predicate": "MENTORED", "object_text": "Charlie", "object_ref": None, "sentence_id": "sent-0001", "source_text_id": "src-tri-001", "confidence": 0.73, "evidence_span": {"start_offset": 0, "end_offset": 19}},
        ],
    }

    result = extract_triples_from_payload(payload)

    assert "triples" in result
    assert len(result["triples"]) == 2

    required = {"triple_id", "subject", "predicate", "object", "subject_ref", "predicate_ref", "object_ref", "relation_id", "sentence_id", "source_text_id", "confidence", "evidence_span"}
    for triple in result["triples"]:
        assert required.issubset(triple.keys())

    first = result["triples"][0]
    assert first["subject"] == "alice"
    assert first["object"] == "robot"
    assert first["predicate"] == "build"
    assert first["subject_ref"] == "ent-0001"
    assert first["object_ref"] == "con-0001"
    assert first["predicate_ref"] == "rel-0001"
    assert first["relation_id"] == "rel-0001"

    second = result["triples"][1]
    assert second["subject"] == "bob"
    assert second["object"] == "charlie"
    assert second["predicate"] == "mentor"
    assert second["subject_ref"] is None
    assert second["object_ref"] is None
    assert second["predicate_ref"] == "rel-0002"
