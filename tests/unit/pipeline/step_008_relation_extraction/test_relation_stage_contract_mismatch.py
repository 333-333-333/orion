# UC-REL-002 MF-1 | FUN-REL-002 AC-1 | CON-REL-001 AC-1 | BR-REL-003 | TB-REL-002
def test_case_a_controlled_tokens_with_head_text_produce_real_relation():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "source_text_id": "src-rel-case-a",
        "tokens": [
            {"token_id": "t1", "text": "Firewall", "lemma": "firewall", "pos": "NOUN", "dependency": "nsubj", "head_text": "protects", "start_offset": 0, "end_offset": 8, "sentence_id": "s1"},
            {"token_id": "t2", "text": "protects", "lemma": "protect", "pos": "VERB", "dependency": "ROOT", "head_text": "protects", "start_offset": 9, "end_offset": 17, "sentence_id": "s1"},
            {"token_id": "t3", "text": "network", "lemma": "network", "pos": "NOUN", "dependency": "dobj", "head_text": "protects", "start_offset": 18, "end_offset": 25, "sentence_id": "s1"},
        ],
        "entities": [],
        "concepts": [],
    }

    result = extract_relations_from_payload(payload)

    assert len(result["relations"]) >= 1
    assert result["relations"][0]["predicate"] == "protect"


# UC-REL-002 AF-1 | FUN-REL-002 AC-2 | CON-REL-001 AC-2 | BR-REL-004 | TB-REL-002
def test_case_b_pipeline_like_tokens_without_head_text_explain_zero_relations():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "source_text_id": "src-rel-case-b",
        "tokens": [
            {"token_id": "t1", "text": "Firewall", "lemma": "firewall", "pos": "NOUN", "dependency": "nsubj", "start_offset": 0, "end_offset": 8, "sentence_id": "s1"},
            {"token_id": "t2", "text": "protects", "lemma": "protect", "pos": "VERB", "dependency": "ROOT", "start_offset": 9, "end_offset": 17, "sentence_id": "s1"},
            {"token_id": "t3", "text": "network", "lemma": "network", "pos": "NOUN", "dependency": "dobj", "start_offset": 18, "end_offset": 25, "sentence_id": "s1"},
        ],
        "entities": [],
        "concepts": [
            {"concept_id": "c1", "text": "Firewall", "start_offset": 0, "end_offset": 8},
            {"concept_id": "c2", "text": "network", "start_offset": 18, "end_offset": 25},
        ],
    }

    result = extract_relations_from_payload(payload)

    assert len(result["relations"]) == 0
    assert all("head_text" not in t for t in payload["tokens"])
