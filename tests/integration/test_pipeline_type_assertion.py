# UC-TYPE-005 MF-1 | FUN-TYPE-002 AC-1 | FUN-TYPE-001 AC-3 | TB-TYPE-001
def test_orion_process_runs_type_assertion_after_taxonomy_induction_and_preserves_payload():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    result = sut.process("John is a person. Apple is an organization.")

    assert "raw_text" in result
    assert "preprocessed_text" in result
    assert "sentences" in result
    assert "tokens" in result
    assert "entities" in result
    assert "concepts" in result
    assert "relations" in result
    assert "triples" in result
    assert "taxonomy_relations" in result
    assert "type_assertions" in result

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation") < completed.index("entity_extraction") < completed.index("concept_extraction") < completed.index("relation_extraction") < completed.index("triple_extraction") < completed.index("taxonomy_induction") < completed.index("type_assertion")
