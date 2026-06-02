# UC-CONCEPT-002 MF-1 | NFR-CONCEPT-001 AC-1 | BR-CONCEPT-003 | TB-CONCEPT-001
def test_concept_generation_is_deterministic_and_deduplicates_normalized_lemma_text():
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
        "raw_text": "Models model MODEL.",
        "preprocessed_text": "Models model MODEL.",
        "source_text_id": "src-con-003",
        "sentences": [{"sentence_id": "sent-0001", "text": "Models model MODEL.", "index": 0, "start_offset": 0, "end_offset": 19}],
        "tokens": [
            {"token_id": "tok-0001", "text": "Models", "lemma": "model", "pos": "NOUN", "tag": "NNS", "dependency": "nsubj", "start_offset": 0, "end_offset": 6, "sentence_id": "sent-0001", "source_text_id": "src-con-003"},
            {"token_id": "tok-0002", "text": "MODEL", "lemma": "model", "pos": "NOUN", "tag": "NN", "dependency": "dobj", "start_offset": 13, "end_offset": 18, "sentence_id": "sent-0001", "source_text_id": "src-con-003"},
        ],
        "entities": [],
    }
    doc = FakeDoc([FakeChunk("Models", 0, 6, FakeRoot("model")), FakeChunk("MODEL", 13, 18, FakeRoot("model"))])

    run1 = extract_concepts_from_payload(payload, doc)
    run2 = extract_concepts_from_payload(payload, doc)

    keys1 = [(c["lemma"], c["text"].lower()) for c in run1["concepts"]]
    assert len(keys1) == len(set(keys1))
    assert run1["concepts"] == run2["concepts"]
