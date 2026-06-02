# UC-TRIPLE-003 MF-1 | FUN-TRIPLE-002 AC-1 | FUN-TRIPLE-001 AC-1 | FUN-TRIPLE-001 AC-2 | TB-TRIPLE-001
def test_orion_process_runs_triple_extraction_after_relation_extraction_and_preserves_payload():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    result = sut.process("Barack Obama leads innovation in Paris.")

    assert "raw_text" in result
    assert "preprocessed_text" in result
    assert "sentences" in result
    assert "tokens" in result
    assert "entities" in result
    assert "concepts" in result
    assert "relations" in result
    assert "triples" in result

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation") < completed.index("entity_extraction") < completed.index("concept_extraction") < completed.index("relation_extraction") < completed.index("triple_extraction")

    required = {"triple_id", "subject", "predicate", "object", "subject_ref", "predicate_ref", "object_ref", "relation_id", "sentence_id", "source_text_id", "confidence", "evidence_span"}
    for triple in result["triples"]:
        assert required.issubset(triple.keys())
