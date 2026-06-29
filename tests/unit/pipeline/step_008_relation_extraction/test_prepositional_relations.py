from __future__ import annotations


# UC-REL-001 MF-4 | FUN-REL-004 AC-1 | BR-REL-PREP-ROUTE-001 | TASK-PIZZA-RED-002 | TB-REL-001
def test_extracts_from_to_prepositional_relations_for_motion_verbs():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    payload = {
        "raw_text": "Luigi rides from Harbor Market to Pine Street.",
        "preprocessed_text": "Luigi rides from Harbor Market to Pine Street.",
        "source_text_id": "src-rel-prep-001",
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Luigi rides from Harbor Market to Pine Street.", "index": 0, "start_offset": 0, "end_offset": 45},
        ],
        "tokens": [
            {"token_id": "tok-0001", "text": "Luigi", "lemma": "Luigi", "pos": "PROPN", "tag": "NNP", "dependency": "nsubj", "head_text": "rides", "start_offset": 0, "end_offset": 5, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0002", "text": "rides", "lemma": "ride", "pos": "VERB", "tag": "VBZ", "dependency": "ROOT", "head_text": "rides", "start_offset": 6, "end_offset": 11, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0003", "text": "from", "lemma": "from", "pos": "ADP", "tag": "IN", "dependency": "prep", "head_text": "rides", "start_offset": 12, "end_offset": 16, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0004", "text": "Harbor", "lemma": "Harbor", "pos": "PROPN", "tag": "NNP", "dependency": "compound", "head_text": "Market", "start_offset": 17, "end_offset": 23, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0005", "text": "Market", "lemma": "Market", "pos": "PROPN", "tag": "NNP", "dependency": "pobj", "head_text": "from", "start_offset": 24, "end_offset": 30, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0006", "text": "to", "lemma": "to", "pos": "ADP", "tag": "IN", "dependency": "prep", "head_text": "rides", "start_offset": 31, "end_offset": 33, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0007", "text": "Pine", "lemma": "Pine", "pos": "PROPN", "tag": "NNP", "dependency": "compound", "head_text": "Street", "start_offset": 34, "end_offset": 38, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0008", "text": "Street", "lemma": "Street", "pos": "PROPN", "tag": "NNP", "dependency": "pobj", "head_text": "to", "start_offset": 39, "end_offset": 45, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
            {"token_id": "tok-0009", "text": ".", "lemma": ".", "pos": "PUNCT", "tag": ".", "dependency": "punct", "head_text": "rides", "start_offset": 45, "end_offset": 46, "sentence_id": "sent-0001", "source_text_id": "src-rel-prep-001"},
        ],
        "entities": [],
        "concepts": [],
        "coreferences": [],
    }

    result = extract_relations_from_payload(payload)
    by_predicate = {relation["predicate"]: relation for relation in result["relations"]}

    assert by_predicate["ride_from"]["subject_text"] == "luigi"
    assert by_predicate["ride_from"]["object_text"] == "harbor market"
    assert by_predicate["ride_to"]["subject_text"] == "luigi"
    assert by_predicate["ride_to"]["object_text"] == "pine street"
    assert all(relation["object_text"] != "harbor market to pine street" for relation in result["relations"])
