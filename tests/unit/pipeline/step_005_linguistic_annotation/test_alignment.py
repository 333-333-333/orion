from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _FakeToken:
    text: str
    idx: int
    lemma_: str
    pos_: str
    tag_: str
    dep_: str
    head: object | None = None

    def __post_init__(self) -> None:
        if self.head is None:
            self.head = self


class _FakeDoc:
    def __init__(self, tokens: list[_FakeToken]) -> None:
        self._tokens = tokens

    def __iter__(self):
        return iter(self._tokens)


class _FakeNlp:
    def __call__(self, _text: str) -> _FakeDoc:
        pizzeria = _FakeToken("Pizzeria", 8, "Pizzeria", "PROPN", "NNP", "ROOT")
        return _FakeDoc(
            [
                _FakeToken("Mario", 0, "Mario", "PROPN", "NNP", "poss", pizzeria),
                _FakeToken("'s", 5, "'s", "PART", "POS", "case", pizzeria),
                pizzeria,
                _FakeToken(".", 16, ".", "PUNCT", ".", "punct", pizzeria),
            ]
        )


# UC-002 MF-5 | FUN-LING-001 AC-3 | BR-LING-006 | TASK-LING-001 | TB-LING-001
def test_linguistic_annotation_aligns_by_span_without_global_shift_on_possessive_split():
    from pipeline.step_005_linguistic_annotation.orchestrator import annotate_tokens

    payload = {
        "raw_text": "Mario's Pizzeria.",
        "preprocessed_text": "Mario's Pizzeria.",
        "source_text_id": "src-ling-align-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": ["unicode_normalization", "collapse_repeated_spaces", "normalize_newlines"],
        "sentences": [
            {"sentence_id": "sent-0001", "text": "Mario's Pizzeria.", "index": 0, "start_offset": 0, "end_offset": 17},
        ],
        "tokens": [
            {"token_id": "tok-0001", "text": "Mario", "index": 0, "sentence_id": "sent-0001", "source_text_id": "src-ling-align-001", "start_offset": 0, "end_offset": 5},
            {"token_id": "tok-0002", "text": "'", "index": 1, "sentence_id": "sent-0001", "source_text_id": "src-ling-align-001", "start_offset": 5, "end_offset": 6},
            {"token_id": "tok-0003", "text": "s", "index": 2, "sentence_id": "sent-0001", "source_text_id": "src-ling-align-001", "start_offset": 6, "end_offset": 7},
            {"token_id": "tok-0004", "text": "Pizzeria", "index": 3, "sentence_id": "sent-0001", "source_text_id": "src-ling-align-001", "start_offset": 8, "end_offset": 16},
            {"token_id": "tok-0005", "text": ".", "index": 4, "sentence_id": "sent-0001", "source_text_id": "src-ling-align-001", "start_offset": 16, "end_offset": 17},
        ],
    }

    result = annotate_tokens(payload, _FakeNlp())
    by_text = {token["text"]: token for token in result["tokens"]}

    assert by_text["'"]["lemma"] == "'s"
    assert by_text["s"]["lemma"] == "'s"
    assert by_text["Pizzeria"]["lemma"] == "Pizzeria"
    assert by_text["Pizzeria"]["pos"] == "PROPN"
    assert by_text["."]["pos"] == "PUNCT"
