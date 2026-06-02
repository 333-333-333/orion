# UC-CONCEPT-003 MF-1 | CON-CONCEPT-001 AC-1 | BR-CONCEPT-004 | TB-CONCEPT-001
def test_concepts_use_preprocessed_offsets_and_sentence_mapping():
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
        "raw_text": "  Neural nets learn. Graph models infer.  ",
        "preprocessed_text": "Neural nets learn. Graph models infer.",
        "source_text_id": "src-con-004",
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Neural nets learn.", "index": 0, "start_offset": 0, "end_offset": 18},
            {"sentence_id": "sent-0002", "text": "Graph models infer.", "index": 1, "start_offset": 19, "end_offset": 37},
        ],
        "tokens": [{"token_id": "tok-0001", "text": "models", "lemma": "model", "pos": "NOUN", "tag": "NNS", "dependency": "nsubj", "start_offset": 25, "end_offset": 31, "sentence_id": "sent-0002", "source_text_id": "src-con-004"}],
        "entities": [],
    }
    doc = FakeDoc([FakeChunk("Graph models", 19, 31, FakeRoot("model"))])

    result = extract_concepts_from_payload(payload, doc)

    concept = next(c for c in result["concepts"] if c["text"] == "Graph models")
    assert concept["start_offset"] == 19
    assert concept["end_offset"] == 31
    assert concept["sentence_id"] == "sent-0002"
