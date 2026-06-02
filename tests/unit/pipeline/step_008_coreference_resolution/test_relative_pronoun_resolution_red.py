# UC-COREF-001 MF-1 | FUN-COREF-001 AC-1 | BR-COREF-001 | TB-COREF-001
def test_resolves_that_with_deterministic_score_and_evidence_span():
    from pipeline.step_008_coreference_resolution import resolve_coreferences_from_payload

    text = "An information asset is any resource that stores, processes, transmits, or represents information."
    payload = {
        "source_text_id": "src-coref-001",
        "raw_text": text,
        "preprocessed_text": text,
        "sentences": [{"sentence_id": "sent-0001", "text": text, "index": 0, "start_offset": 0, "end_offset": len(text)}],
        "tokens": [
            {"token_id": "t1", "text": "resource", "lemma": "resource", "pos": "NOUN", "dependency": "attr", "head_text": "is", "start_offset": 28, "end_offset": 36, "sentence_id": "sent-0001"},
            {"token_id": "t2", "text": "that", "lemma": "that", "pos": "PRON", "dependency": "nsubj", "head_text": "stores", "start_offset": 37, "end_offset": 41, "sentence_id": "sent-0001"},
            {"token_id": "t3", "text": "stores", "lemma": "store", "pos": "VERB", "dependency": "relcl", "head_text": "resource", "start_offset": 42, "end_offset": 48, "sentence_id": "sent-0001"},
        ],
        "noun_chunks": [
            {"text": "information asset", "start_offset": 3, "end_offset": 20, "sentence_id": "sent-0001"},
            {"text": "resource", "start_offset": 28, "end_offset": 36, "sentence_id": "sent-0001"},
        ],
    }

    result = resolve_coreferences_from_payload(payload)
    assert "coreferences" in result
    assert len(result["coreferences"]) >= 1

    c = next(x for x in result["coreferences"] if x["mention"].lower() == "that")
    assert c["antecedent"].lower() in {"resource", "information asset"}
    assert isinstance(c["confidence"], (int, float))
    assert c["status"] in {"resolved", "unresolved"}
    assert "score_breakdown" in c
    assert "evidence_span" in c


# UC-COREF-001 AF-1 | FUN-COREF-001 AC-2 | BR-COREF-002 | TB-COREF-001
def test_resolves_who_and_which_or_marks_unresolved_with_reason():
    from pipeline.step_008_coreference_resolution import resolve_coreferences_from_payload

    text = "Access control regulates who can access which resource."
    payload = {
        "source_text_id": "src-coref-002",
        "raw_text": text,
        "preprocessed_text": text,
        "sentences": [{"sentence_id": "sent-0001", "text": text, "index": 0, "start_offset": 0, "end_offset": len(text)}],
        "tokens": [
            {"token_id": "t1", "text": "who", "lemma": "who", "pos": "PRON", "dependency": "nsubj", "head_text": "access", "start_offset": 25, "end_offset": 28, "sentence_id": "sent-0001"},
            {"token_id": "t2", "text": "which", "lemma": "which", "pos": "PRON", "dependency": "det", "head_text": "resource", "start_offset": 40, "end_offset": 45, "sentence_id": "sent-0001"},
            {"token_id": "t3", "text": "resource", "lemma": "resource", "pos": "NOUN", "dependency": "dobj", "head_text": "access", "start_offset": 46, "end_offset": 54, "sentence_id": "sent-0001"},
        ],
        "noun_chunks": [
            {"text": "Access control", "start_offset": 0, "end_offset": 14, "sentence_id": "sent-0001"},
            {"text": "resource", "start_offset": 46, "end_offset": 54, "sentence_id": "sent-0001"},
        ],
    }

    result = resolve_coreferences_from_payload(payload)
    mentions = {x["mention"].lower(): x for x in result["coreferences"]}

    assert "who" in mentions
    assert "which" in mentions

    who = mentions["who"]
    if who["status"] == "resolved":
        assert who["antecedent"].lower() in {"actor", "user", "accessor", "access control"}
    else:
        assert who["status"] == "unresolved"
        assert isinstance(who.get("reason"), str) and who["reason"].strip()


# NFR-COREF-001 AC-1 | BR-COREF-003 | TB-COREF-001
def test_coreference_confidence_is_reproducible_for_same_input():
    from pipeline.step_008_coreference_resolution import resolve_coreferences_from_payload

    text = "An information asset is any resource that stores information."
    payload = {
        "source_text_id": "src-coref-003",
        "raw_text": text,
        "preprocessed_text": text,
        "sentences": [{"sentence_id": "sent-0001", "text": text, "index": 0, "start_offset": 0, "end_offset": len(text)}],
        "tokens": [
            {"token_id": "t1", "text": "resource", "lemma": "resource", "pos": "NOUN", "dependency": "attr", "head_text": "is", "start_offset": 28, "end_offset": 36, "sentence_id": "sent-0001"},
            {"token_id": "t2", "text": "that", "lemma": "that", "pos": "PRON", "dependency": "nsubj", "head_text": "stores", "start_offset": 37, "end_offset": 41, "sentence_id": "sent-0001"},
        ],
        "noun_chunks": [{"text": "resource", "start_offset": 28, "end_offset": 36, "sentence_id": "sent-0001"}],
    }

    r1 = resolve_coreferences_from_payload(payload)
    r2 = resolve_coreferences_from_payload(payload)

    c1 = next(x for x in r1["coreferences"] if x["mention"].lower() == "that")
    c2 = next(x for x in r2["coreferences"] if x["mention"].lower() == "that")
    assert c1["confidence"] == c2["confidence"]
    assert c1["score_breakdown"] == c2["score_breakdown"]
