# UC-TRIPLE-001 AF-1 | FUN-TRIPLE-001 AC-2 | BR-TRIPLE-004 | TB-TRIPLE-001
def test_no_relations_returns_empty_triples_and_preserves_previous_payload_complete():
    from pipeline.step_009_triple_extraction import extract_triples_from_payload

    payload = {
        "raw_text": "Only standalone words.",
        "preprocessed_text": "Only standalone words.",
        "source_text_id": "src-tri-003",
        "sentences": [{"sentence_id": "sent-0001", "text": "Only standalone words.", "index": 0, "start_offset": 0, "end_offset": 22}],
        "tokens": [{"token_id": "tok-0001", "text": "Only", "lemma": "only", "pos": "ADV", "tag": "RB", "dependency": "advmod", "start_offset": 0, "end_offset": 4, "sentence_id": "sent-0001", "source_text_id": "src-tri-003"}],
        "entities": [],
        "concepts": [],
        "relations": [],
        "custom_marker": {"keep": True},
    }

    result = extract_triples_from_payload(payload)

    assert result["triples"] == []
    assert result["raw_text"] == payload["raw_text"]
    assert result["preprocessed_text"] == payload["preprocessed_text"]
    assert result["sentences"] == payload["sentences"]
    assert result["tokens"] == payload["tokens"]
    assert result["entities"] == payload["entities"]
    assert result["concepts"] == payload["concepts"]
    assert result["relations"] == payload["relations"]
    assert result["custom_marker"] == payload["custom_marker"]
