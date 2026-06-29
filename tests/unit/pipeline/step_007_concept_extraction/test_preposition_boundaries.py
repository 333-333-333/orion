from __future__ import annotations


class _FakeRoot:
    def __init__(self, lemma_: str) -> None:
        self.lemma_ = lemma_


class _FakeChunk:
    def __init__(self, text: str, start_char: int, root_lemma: str) -> None:
        self.text = text
        self.start_char = start_char
        self.end_char = start_char + len(text)
        self.root = _FakeRoot(root_lemma)


class _FakeDoc:
    def __init__(self, chunks: list[_FakeChunk]) -> None:
        self.noun_chunks = chunks


# UC-007 MF-2 | FUN-CON-003 AC-1 | BR-CON-PP-BOUNDARY-001 | TASK-PIZZA-RED-002 | TB-CON-001
def test_concept_extraction_splits_contextual_prepositional_tails_into_atomic_concepts():
    from pipeline.step_007_concept_extraction import extract_concepts_from_payload

    chunks = [
        _FakeChunk("delivery orders for Mario's Pizzeria", 0, "Pizzeria"),
        _FakeChunk("Harbor Market to Pine Street", 50, "Market"),
        _FakeChunk("Central Cafe at 12:18 p.m.", 100, "Cafe"),
        _FakeChunk("aged parmesan over the edge", 140, "edge"),
    ]
    payload = {
        "raw_text": "",
        "preprocessed_text": "",
        "source_text_id": "src-con-prep-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": [],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "", "index": 0, "start_offset": 0, "end_offset": 200},
        ],
        "tokens": [],
        "entities": [],
    }

    result = extract_concepts_from_payload(payload, _FakeDoc(chunks))
    texts = {concept["text"] for concept in result["concepts"]}

    assert "delivery orders for Mario's Pizzeria" not in texts
    assert "Harbor Market to Pine Street" not in texts
    assert "Central Cafe at 12:18 p.m." not in texts
    assert "aged parmesan over the edge" not in texts
    assert "delivery orders" in texts
    assert "Mario's Pizzeria" in texts
    assert "Harbor Market" in texts
    assert "Pine Street" in texts
    assert "Central Cafe" in texts
    assert "aged parmesan" in texts


# UC-007 MF-2 | FUN-CON-003 AC-2 | BR-CON-LEXICAL-WHITELIST-001 | TB-CON-002
def test_concept_extraction_preserves_lexicalized_prepositional_terms():
    from pipeline.step_007_concept_extraction import extract_concepts_from_payload

    chunks = [
        _FakeChunk("data at rest", 0, "data"),
        _FakeChunk("data in transit", 20, "data"),
        _FakeChunk("defense in depth", 40, "defense"),
    ]
    payload = {
        "raw_text": "",
        "preprocessed_text": "",
        "source_text_id": "src-con-prep-002",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": [],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "", "index": 0, "start_offset": 0, "end_offset": 80},
        ],
        "tokens": [],
        "entities": [],
    }

    result = extract_concepts_from_payload(payload, _FakeDoc(chunks))
    texts = {concept["text"] for concept in result["concepts"]}

    assert {"data at rest", "data in transit", "defense in depth"} <= texts
