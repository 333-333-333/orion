# UC-TYPE-002 AF-1 | FUN-TYPE-001 AC-3 | BR-TYPE-006 | TB-TYPE-001
def test_no_signal_returns_empty_type_assertions_and_preserves_full_previous_payload():
    from pipeline.step_011_type_assertion import extract_type_assertions_from_payload

    payload = {
        "raw_text": "Quickly and silently.",
        "preprocessed_text": "Quickly and silently.",
        "source_text_id": "src-type-005",
        "sentences": [{"sentence_id": "sent-0001", "text": "Quickly and silently.", "index": 0, "start_offset": 0, "end_offset": 21}],
        "tokens": [{"token_id": "tok-0001", "text": "Quickly", "lemma": "quickly", "pos": "ADV", "sentence_id": "sent-0001", "source_text_id": "src-type-005"}],
        "entities": [],
        "concepts": [],
        "relations": [],
        "triples": [],
        "taxonomy_relations": [],
        "custom_marker": {"keep": True},
    }

    result = extract_type_assertions_from_payload(payload)

    assert result["type_assertions"] == []
    assert result["raw_text"] == payload["raw_text"]
    assert result["preprocessed_text"] == payload["preprocessed_text"]
    assert result["source_text_id"] == payload["source_text_id"]
    assert result["sentences"] == payload["sentences"]
    assert result["tokens"] == payload["tokens"]
    assert result["entities"] == payload["entities"]
    assert result["concepts"] == payload["concepts"]
    assert result["relations"] == payload["relations"]
    assert result["triples"] == payload["triples"]
    assert result["taxonomy_relations"] == payload["taxonomy_relations"]
    assert result["custom_marker"] == payload["custom_marker"]
