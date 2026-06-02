# UC-CONCEPT-001 MF-1 | UC-CONCEPT-002 MF-1 | FUN-CONCEPT-001 AC-1 | FUN-CONCEPT-001 AC-2 | FUN-CONCEPT-001 AC-3 | TB-CONCEPT-001
def test_orion_process_runs_concept_extraction_after_entity_extraction_and_preserves_payload():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    result = sut.process("Barack Obama discussed neural networks in Paris.")

    assert "raw_text" in result
    assert "preprocessed_text" in result
    assert "sentences" in result
    assert "tokens" in result
    assert "entities" in result
    assert "concepts" in result

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation") < completed.index("entity_extraction") < completed.index("concept_extraction")

    required = {"concept_id", "text", "lemma", "source", "start_offset", "end_offset", "sentence_id", "source_text_id", "confidence"}
    for concept in result["concepts"]:
        assert required.issubset(concept.keys())
