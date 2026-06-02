# UC-TRIPLE-003 EF-1 | FUN-TRIPLE-003 AC-1 | BR-TRIPLE-004 | TB-TRIPLE-003
def test_triple_extraction_never_emits_broken_satisfi_predicate_or_object():
    from pipeline.step_009_triple_extraction import extract_triples_from_payload

    payload = {
        "raw_text": "A requirement can be satisfied by one or more controls.",
        "preprocessed_text": "A requirement can be satisfied by one or more controls.",
        "source_text_id": "src-tri-003",
        "sentences": [{"sentence_id": "sent-0001", "text": "A requirement can be satisfied by one or more controls.", "index": 0, "start_offset": 0, "end_offset": 54}],
        "tokens": [],
        "entities": [],
        "concepts": [],
        "relations": [
            {"relation_id": "rel-0001", "subject_text": "requirement", "subject_ref": None, "predicate": "satisfied", "object_text": "controls", "object_ref": None, "sentence_id": "sent-0001", "source_text_id": "src-tri-003", "confidence": 0.8, "evidence_span": {"start_offset": 0, "end_offset": 53}},
        ],
    }

    result = extract_triples_from_payload(payload)
    assert len(result["triples"]) == 1
    triple = result["triples"][0]
    assert triple["predicate"] != "satisfi"
    assert triple["object"] != "satisfi"
    assert triple["predicate"] in {"satisfy", "satisfied", "satisfies"}
