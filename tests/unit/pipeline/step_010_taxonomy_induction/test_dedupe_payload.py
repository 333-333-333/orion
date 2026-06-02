# UC-TAX-002 MF-1 | UC-TAX-001 AF-3 | FUN-TAX-001 AC-3 | FUN-TAX-001 AC-4 | NFR-TAX-001 AC-1 | BR-TAX-004 | BR-TAX-005 | TB-TAX-001
def test_taxonomy_is_deterministic_deduplicated_stable_and_preserves_payload_when_no_signal():
    from pipeline.step_010_taxonomy_induction import extract_taxonomy_relations_from_payload

    payload = {
        "raw_text": "A robin is a bird. A robin is a bird.",
        "preprocessed_text": "A robin is a bird. A robin is a bird.",
        "source_text_id": "src-tax-002",
        "sentences": [
            {"sentence_id": "sent-0001", "text": "A robin is a bird.", "index": 0, "start_offset": 0, "end_offset": 18},
            {"sentence_id": "sent-0002", "text": "A robin is a bird.", "index": 1, "start_offset": 19, "end_offset": 37},
        ],
        "tokens": [
            {"token_id": "tok-0001", "text": "robin", "lemma": "robin", "pos": "NOUN", "sentence_id": "sent-0001", "source_text_id": "src-tax-002"},
            {"token_id": "tok-0002", "text": "bird", "lemma": "bird", "pos": "NOUN", "sentence_id": "sent-0001", "source_text_id": "src-tax-002"},
            {"token_id": "tok-0003", "text": "robin", "lemma": "robin", "pos": "NOUN", "sentence_id": "sent-0002", "source_text_id": "src-tax-002"},
            {"token_id": "tok-0004", "text": "bird", "lemma": "bird", "pos": "NOUN", "sentence_id": "sent-0002", "source_text_id": "src-tax-002"},
        ],
        "concepts": [
            {"concept_id": "con-0001", "text": "robin", "lemma": "robin", "normalized_text": "robin", "sentence_id": "sent-0001", "source_text_id": "src-tax-002"},
            {"concept_id": "con-0002", "text": "bird", "lemma": "bird", "normalized_text": "bird", "sentence_id": "sent-0001", "source_text_id": "src-tax-002"},
        ],
        "relations": [],
        "triples": [],
        "entities": [],
        "custom_marker": {"keep": True},
    }

    r1 = extract_taxonomy_relations_from_payload(payload)
    r2 = extract_taxonomy_relations_from_payload(payload)

    assert r1["taxonomy_relations"] == r2["taxonomy_relations"]
    assert len(r1["taxonomy_relations"]) == 1

    no_signal_payload = {
        **payload,
        "raw_text": "Quickly and silently.",
        "preprocessed_text": "Quickly and silently.",
        "sentences": [{"sentence_id": "sent-0009", "text": "Quickly and silently.", "index": 0, "start_offset": 0, "end_offset": 21}],
        "tokens": [{"token_id": "tok-0099", "text": "Quickly", "lemma": "quickly", "pos": "ADV", "sentence_id": "sent-0009", "source_text_id": "src-tax-002"}],
        "concepts": [],
    }

    r3 = extract_taxonomy_relations_from_payload(no_signal_payload)
    assert r3["taxonomy_relations"] == []
    assert r3["custom_marker"] == payload["custom_marker"]
    assert r3["relations"] == payload["relations"]
    assert r3["triples"] == payload["triples"]
