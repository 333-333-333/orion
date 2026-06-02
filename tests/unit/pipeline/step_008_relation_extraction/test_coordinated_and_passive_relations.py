# UC-REL-003 MF-1 | FUN-REL-003 AC-1 | BR-REL-005 | TB-REL-003
def test_extracts_two_relations_for_coordinated_verbs_with_textual_evidence_span():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    text = "A risk scenario describes how a threat may exploit a vulnerability and affect an asset."
    payload = {
        "raw_text": text,
        "preprocessed_text": text,
        "source_text_id": "src-rel-003a",
        "sentences": [{"sentence_id": "sent-0001", "text": text, "index": 0, "start_offset": 0, "end_offset": 84}],
        "tokens": [
            {"token_id": "tok-0001", "text": "threat", "lemma": "threat", "pos": "NOUN", "tag": "NN", "dependency": "nsubj", "head_text": "exploit", "start_offset": 35, "end_offset": 41, "sentence_id": "sent-0001", "source_text_id": "src-rel-003a"},
            {"token_id": "tok-0002", "text": "exploit", "lemma": "exploit", "pos": "VERB", "tag": "VB", "dependency": "xcomp", "head_text": "describes", "start_offset": 46, "end_offset": 53, "sentence_id": "sent-0001", "source_text_id": "src-rel-003a"},
            {"token_id": "tok-0003", "text": "vulnerability", "lemma": "vulnerability", "pos": "NOUN", "tag": "NN", "dependency": "dobj", "head_text": "exploit", "start_offset": 56, "end_offset": 69, "sentence_id": "sent-0001", "source_text_id": "src-rel-003a"},
            {"token_id": "tok-0004", "text": "affect", "lemma": "affect", "pos": "VERB", "tag": "VB", "dependency": "conj", "head_text": "exploit", "start_offset": 74, "end_offset": 80, "sentence_id": "sent-0001", "source_text_id": "src-rel-003a"},
            {"token_id": "tok-0005", "text": "asset", "lemma": "asset", "pos": "NOUN", "tag": "NN", "dependency": "dobj", "head_text": "affect", "start_offset": 84, "end_offset": 89, "sentence_id": "sent-0001", "source_text_id": "src-rel-003a"},
        ],
        "entities": [],
        "concepts": [],
    }

    result = extract_relations_from_payload(payload)
    coordination = [r for r in result["relations"] if r["sentence_id"] == "sent-0001"]
    assert len(coordination) == 2
    assert any(r["subject_text"].lower() == "threat" and r["predicate"] == "exploit" and r["object_text"].lower() == "vulnerability" for r in coordination)
    assert any(r["subject_text"].lower() == "threat" and r["predicate"] == "affect" and r["object_text"].lower() == "asset" for r in coordination)
    for rel in coordination:
        span = rel["evidence_span"]
        assert span["start_offset"] <= 35
        assert span["end_offset"] >= 89


# UC-REL-003 AF-1 | FUN-REL-003 AC-2 | BR-REL-006 | TB-REL-003
def test_extracts_passive_by_phrase_with_controls_coverage_in_evidence_span():
    from pipeline.step_008_relation_extraction import extract_relations_from_payload

    text = "A requirement can be satisfied by one or more controls."
    payload = {
        "raw_text": text,
        "preprocessed_text": text,
        "source_text_id": "src-rel-003b",
        "sentences": [{"sentence_id": "sent-0002", "text": text, "index": 0, "start_offset": 0, "end_offset": 54}],
        "tokens": [
            {"token_id": "tok-0006", "text": "requirement", "lemma": "requirement", "pos": "NOUN", "tag": "NN", "dependency": "nsubjpass", "head_text": "satisfied", "start_offset": 2, "end_offset": 13, "sentence_id": "sent-0002", "source_text_id": "src-rel-003b"},
            {"token_id": "tok-0007", "text": "satisfied", "lemma": "satisfy", "pos": "VERB", "tag": "VBN", "dependency": "ROOT", "head_text": "satisfied", "start_offset": 21, "end_offset": 30, "sentence_id": "sent-0002", "source_text_id": "src-rel-003b"},
            {"token_id": "tok-0008", "text": "controls", "lemma": "control", "pos": "NOUN", "tag": "NNS", "dependency": "pobj", "head_text": "by", "start_offset": 46, "end_offset": 54, "sentence_id": "sent-0002", "source_text_id": "src-rel-003b"},
        ],
        "entities": [],
        "concepts": [],
    }

    result = extract_relations_from_payload(payload)
    passive = [r for r in result["relations"] if r["sentence_id"] == "sent-0002"]
    assert len(passive) >= 1
    assert any(
        (r["subject_text"].lower() == "control" and r["predicate"] in {"satisfy", "satisfied_by", "satisfiedby"} and r["object_text"].lower() == "requirement")
        or (r["subject_text"].lower() == "requirement" and r["predicate"] in {"satisfy", "satisfied_by", "satisfiedby"} and r["object_text"].lower() == "control")
        for r in passive
    )
    assert any(r["evidence_span"]["end_offset"] >= 54 for r in passive)
