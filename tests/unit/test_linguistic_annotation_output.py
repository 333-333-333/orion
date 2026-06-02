# UC-002 MF-5 | FUN-LING-001 AC-1 | BR-LING-003 | TB-LING-001
def test_linguistic_annotation_enriches_each_token_and_preserves_token_contract():
    from orion import ORION

    sut = ORION(config={"spacy_model": "en_core_web_lg"})

    result = sut.process("Birds fly quickly.")

    assert "tokens" in result
    assert len(result["tokens"]) > 0

    first = result["tokens"][0]
    assert "token_id" in first
    assert "text" in first
    assert "index" in first
    assert "sentence_id" in first
    assert "source_text_id" in first
    assert "start_offset" in first
    assert "end_offset" in first

    assert "lemma" in first
    assert "pos" in first
    assert "tag" in first
    assert "dependency" in first


# UC-002 MF-5 | FUN-LING-001 AC-2 | BR-LING-004 | TB-LING-001
def test_linguistic_annotation_keeps_offsets_relative_to_preprocessed_text():
    from orion import ORION

    raw = "  Birds fly quickly.  "
    sut = ORION(config={"spacy_model": "en_core_web_lg"})

    result = sut.process(raw)
    preprocessed = result["preprocessed_text"]

    for token in result["tokens"]:
        span = preprocessed[token["start_offset"]:token["end_offset"]]
        assert span == token["text"]
