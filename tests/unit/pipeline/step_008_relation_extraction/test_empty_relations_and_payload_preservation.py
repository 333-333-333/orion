# UC-REL-001 AF-2 | FUN-REL-001 AC-3 | BR-REL-005 | TB-REL-001
def test_no_relation_candidates_returns_empty_relations_and_preserves_payload():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "raw_text": "Quickly and silently.",
        "preprocessed_text": "Quickly and silently.",
        "source_text_id": "src-rel-005",
        "sentences": [{"sentence_id": "sent-0001", "text": "Quickly and silently.", "index": 0, "start_offset": 0, "end_offset": 20}],
        "tokens": [
            {"token_id": "tok-0001", "text": "Quickly", "lemma": "quickly", "pos": "ADV", "tag": "RB", "dependency": "advmod", "head_text": "silently", "start_offset": 0, "end_offset": 7, "sentence_id": "sent-0001", "source_text_id": "src-rel-005"},
        ],
        "entities": [],
        "concepts": [],
        "custom_marker": {"keep": True},
    }

    result = extract_relations_from_payload(payload)

    assert result["relations"] == []
    assert result["raw_text"] == payload["raw_text"]
    assert result["preprocessed_text"] == payload["preprocessed_text"]
    assert result["sentences"] == payload["sentences"]
    assert result["tokens"] == payload["tokens"]
    assert result["entities"] == payload["entities"]
    assert result["concepts"] == payload["concepts"]
    assert result["custom_marker"] == payload["custom_marker"]
