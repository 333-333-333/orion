# UC-REL-001 MF-1 | FUN-REL-001 AC-1 | BR-REL-001 | TB-REL-001
def test_extracts_basic_svo_relation_with_required_fields_from_enriched_tokens():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "raw_text": "Alice builds robots.",
        "preprocessed_text": "Alice builds robots.",
        "source_text_id": "src-rel-001",
        "sentences": [{"sentence_id": "sent-0001", "text": "Alice builds robots.", "index": 0, "start_offset": 0, "end_offset": 20}],
        "tokens": [
            {"token_id": "tok-0001", "text": "Alice", "lemma": "Alice", "pos": "PROPN", "tag": "NNP", "dependency": "nsubj", "head_text": "builds", "start_offset": 0, "end_offset": 5, "sentence_id": "sent-0001", "source_text_id": "src-rel-001"},
            {"token_id": "tok-0002", "text": "builds", "lemma": "build", "pos": "VERB", "tag": "VBZ", "dependency": "ROOT", "head_text": "builds", "start_offset": 6, "end_offset": 12, "sentence_id": "sent-0001", "source_text_id": "src-rel-001"},
            {"token_id": "tok-0003", "text": "robots", "lemma": "robot", "pos": "NOUN", "tag": "NNS", "dependency": "dobj", "head_text": "builds", "start_offset": 13, "end_offset": 19, "sentence_id": "sent-0001", "source_text_id": "src-rel-001"},
        ],
        "entities": [],
        "concepts": [],
    }

    result = extract_relations_from_payload(payload)

    assert "relations" in result
    assert len(result["relations"]) == 1
    rel = result["relations"][0]
    required = {
        "relation_id", "subject_text", "subject_ref", "predicate", "object_text", "object_ref",
        "sentence_id", "source_text_id", "confidence", "evidence_span", "start_offset", "end_offset"
    }
    assert required.issubset(rel.keys())
    assert rel["subject_text"] == "Alice"
    assert rel["predicate"] == "build"
    assert rel["object_text"] == "robots"
