# UC-CONCEPT-001 MF-1 | FUN-CONCEPT-001 AC-1 | BR-CONCEPT-001 | TB-CONCEPT-001
def test_noun_chunks_generate_concepts_with_required_fields_and_sources():
    from pipeline.step_007_concept_extraction import extract_concepts_from_payload

    class FakeChunk:
        def __init__(self, text, start_char, end_char, root):
            self.text = text
            self.start_char = start_char
            self.end_char = end_char
            self.root = root

    class FakeRoot:
        def __init__(self, lemma_):
            self.lemma_ = lemma_

    class FakeDoc:
        def __init__(self, noun_chunks):
            self.noun_chunks = noun_chunks

    payload = {
        "raw_text": "Large language models transform text.",
        "preprocessed_text": "Large language models transform text.",
        "source_text_id": "src-con-001",
        "sentences": [{"sentence_id": "sent-0001", "text": "Large language models transform text.", "index": 0, "start_offset": 0, "end_offset": 37}],
        "tokens": [
            {"token_id": "tok-0001", "text": "Large", "lemma": "large", "pos": "ADJ", "tag": "JJ", "dependency": "amod", "start_offset": 0, "end_offset": 5, "sentence_id": "sent-0001", "source_text_id": "src-con-001"},
            {"token_id": "tok-0002", "text": "models", "lemma": "model", "pos": "NOUN", "tag": "NNS", "dependency": "nsubj", "start_offset": 15, "end_offset": 21, "sentence_id": "sent-0001", "source_text_id": "src-con-001"},
        ],
        "entities": [],
    }
    doc = FakeDoc([FakeChunk("Large language models", 0, 21, FakeRoot("model"))])

    result = extract_concepts_from_payload(payload, doc)

    assert "concepts" in result
    assert len(result["concepts"]) >= 1
    required = {"concept_id", "text", "lemma", "source", "start_offset", "end_offset", "sentence_id", "source_text_id", "confidence"}
    assert required.issubset(result["concepts"][0].keys())
    assert any(c["source"] == "noun_chunk" for c in result["concepts"])
