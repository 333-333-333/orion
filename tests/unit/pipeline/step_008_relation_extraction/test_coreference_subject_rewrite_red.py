# UC-REL-006 MF-1 | FUN-REL-004 AC-1 | BR-REL-007 | TB-COREF-001
def test_relation_extraction_rewrites_relative_pronoun_subject_from_coreference_and_preserves_evidence_span():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    text = "An information asset is any resource that stores information."
    payload = {
        "source_text_id": "src-rel-coref-001",
        "raw_text": text,
        "preprocessed_text": text,
        "sentences": [{"sentence_id": "sent-0001", "text": text, "index": 0, "start_offset": 0, "end_offset": len(text)}],
        "tokens": [
            {"token_id": "t1", "text": "that", "lemma": "that", "pos": "PRON", "dependency": "nsubj", "head_text": "stores", "start_offset": 37, "end_offset": 41, "sentence_id": "sent-0001", "source_text_id": "src-rel-coref-001"},
            {"token_id": "t2", "text": "stores", "lemma": "store", "pos": "VERB", "dependency": "relcl", "head_text": "resource", "start_offset": 42, "end_offset": 48, "sentence_id": "sent-0001", "source_text_id": "src-rel-coref-001"},
            {"token_id": "t3", "text": "information", "lemma": "information", "pos": "NOUN", "dependency": "dobj", "head_text": "stores", "start_offset": 49, "end_offset": 60, "sentence_id": "sent-0001", "source_text_id": "src-rel-coref-001"},
        ],
        "entities": [],
        "concepts": [{"concept_id": "con-0001", "text": "resource", "start_offset": 28, "end_offset": 36}],
        "coreferences": [
            {
                "mention": "that",
                "mention_span": {"start_offset": 37, "end_offset": 41},
                "antecedent": "resource",
                "antecedent_span": {"start_offset": 28, "end_offset": 36},
                "confidence": 0.93,
                "score_breakdown": {"distance": 0.7, "syntax": 0.23},
                "evidence_span": {"start_offset": 28, "end_offset": 48},
                "status": "resolved"
            }
        ],
    }

    result = extract_relations_from_payload(payload)

    assert len(result["relations"]) >= 1
    rel = result["relations"][0]
    assert rel["subject_text"].lower() == "resource"
    assert rel["subject_text"].lower() != "that"
    assert "evidence_span" in rel and rel["evidence_span"]["end_offset"] >= 60
