# UC-TRIPLE-002 MF-1 | NFR-TRIPLE-001 AC-1 | BR-TRIPLE-003 | TB-TRIPLE-001
def test_triple_generation_is_deterministic_deduplicated_and_stable_order():
    from pipeline.step_009_triple_extraction import extract_triples_from_payload

    payload = {
        "raw_text": "Alice builds robots. Alice builds robots.",
        "preprocessed_text": "Alice builds robots. Alice builds robots.",
        "source_text_id": "src-tri-002",
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Alice builds robots.", "index": 0, "start_offset": 0, "end_offset": 20},
            {"sentence_id": "sent-0002", "text": "Alice builds robots.", "index": 1, "start_offset": 21, "end_offset": 41},
        ],
        "tokens": [],
        "entities": [],
        "concepts": [],
        "relations": [
            {"relation_id": "rel-0001", "subject_text": "Alice", "subject_ref": None, "predicate": "builds", "object_text": "robots", "object_ref": None, "sentence_id": "sent-0001", "source_text_id": "src-tri-002", "confidence": 0.91, "evidence_span": {"start_offset": 0, "end_offset": 19}},
            {"relation_id": "rel-0002", "subject_text": "Alice", "subject_ref": None, "predicate": "builds", "object_text": "robots", "object_ref": None, "sentence_id": "sent-0002", "source_text_id": "src-tri-002", "confidence": 0.89, "evidence_span": {"start_offset": 21, "end_offset": 40}},
        ],
    }

    r1 = extract_triples_from_payload(payload)
    r2 = extract_triples_from_payload(payload)

    assert r1["triples"] == r2["triples"]
    assert len(r1["triples"]) == 1
    assert r1["triples"][0]["subject"] == "alice"
    assert r1["triples"][0]["predicate"] == "build"
    assert r1["triples"][0]["object"] == "robot"
