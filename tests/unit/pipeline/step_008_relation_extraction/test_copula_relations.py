# UC-REL-001 AF-1 | FUN-REL-001 AC-2 | BR-REL-002 | TB-REL-001
def test_extracts_simple_copula_relation_x_is_y():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "raw_text": "Paris is a city.",
        "preprocessed_text": "Paris is a city.",
        "source_text_id": "src-rel-002",
        "sentences": [{"sentence_id": "sent-0001", "text": "Paris is a city.", "index": 0, "start_offset": 0, "end_offset": 16}],
        "tokens": [
            {"token_id": "tok-0001", "text": "Paris", "lemma": "Paris", "pos": "PROPN", "tag": "NNP", "dependency": "nsubj", "head_text": "is", "start_offset": 0, "end_offset": 5, "sentence_id": "sent-0001", "source_text_id": "src-rel-002"},
            {"token_id": "tok-0002", "text": "is", "lemma": "be", "pos": "AUX", "tag": "VBZ", "dependency": "ROOT", "head_text": "is", "start_offset": 6, "end_offset": 8, "sentence_id": "sent-0001", "source_text_id": "src-rel-002"},
            {"token_id": "tok-0003", "text": "city", "lemma": "city", "pos": "NOUN", "tag": "NN", "dependency": "attr", "head_text": "is", "start_offset": 11, "end_offset": 15, "sentence_id": "sent-0001", "source_text_id": "src-rel-002"},
        ],
        "entities": [],
        "concepts": [],
    }

    result = extract_relations_from_payload(payload)

    assert len(result["relations"]) == 1
    rel = result["relations"][0]
    assert rel["subject_text"] == "Paris"
    assert rel["predicate"] in {"be", "is"}
    assert rel["object_text"] == "city"
