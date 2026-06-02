# UC-REL-003 MF-1 | NFR-REL-001 AC-1 | BR-REL-004 | TB-REL-001
def test_relation_generation_is_deterministic_deduplicated_and_stable_order():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "raw_text": "Alice builds robots. Alice builds robots.",
        "preprocessed_text": "Alice builds robots. Alice builds robots.",
        "source_text_id": "src-rel-004",
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Alice builds robots.", "index": 0, "start_offset": 0, "end_offset": 20},
            {"sentence_id": "sent-0002", "text": "Alice builds robots.", "index": 1, "start_offset": 21, "end_offset": 41},
        ],
        "tokens": [
            {"token_id": "tok-0001", "text": "Alice", "lemma": "Alice", "pos": "PROPN", "tag": "NNP", "dependency": "nsubj", "head_text": "builds", "start_offset": 0, "end_offset": 5, "sentence_id": "sent-0001", "source_text_id": "src-rel-004"},
            {"token_id": "tok-0002", "text": "builds", "lemma": "build", "pos": "VERB", "tag": "VBZ", "dependency": "ROOT", "head_text": "builds", "start_offset": 6, "end_offset": 12, "sentence_id": "sent-0001", "source_text_id": "src-rel-004"},
            {"token_id": "tok-0003", "text": "robots", "lemma": "robot", "pos": "NOUN", "tag": "NNS", "dependency": "dobj", "head_text": "builds", "start_offset": 13, "end_offset": 19, "sentence_id": "sent-0001", "source_text_id": "src-rel-004"},
            {"token_id": "tok-0004", "text": "Alice", "lemma": "Alice", "pos": "PROPN", "tag": "NNP", "dependency": "nsubj", "head_text": "builds", "start_offset": 21, "end_offset": 26, "sentence_id": "sent-0002", "source_text_id": "src-rel-004"},
            {"token_id": "tok-0005", "text": "builds", "lemma": "build", "pos": "VERB", "tag": "VBZ", "dependency": "ROOT", "head_text": "builds", "start_offset": 27, "end_offset": 33, "sentence_id": "sent-0002", "source_text_id": "src-rel-004"},
            {"token_id": "tok-0006", "text": "robots", "lemma": "robot", "pos": "NOUN", "tag": "NNS", "dependency": "dobj", "head_text": "builds", "start_offset": 34, "end_offset": 40, "sentence_id": "sent-0002", "source_text_id": "src-rel-004"},
        ],
        "entities": [],
        "concepts": [],
    }

    r1 = extract_relations_from_payload(payload)
    r2 = extract_relations_from_payload(payload)

    assert r1["relations"] == r2["relations"]
    assert len(r1["relations"]) == 1
