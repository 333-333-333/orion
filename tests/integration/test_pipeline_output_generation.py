# UC-OUT-005 MF-1 | FUN-OUT-004 AC-1 | FUN-OUT-002 AC-3 | FUN-OUT-003 AC-3 | TB-OUT-001
def test_orion_process_runs_output_generation_after_type_assertion_and_preserves_payload_plus_output():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})

    result = sut.process("John is a person. A robin is a bird.")

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
    assert "output" in result
    assert result["output"]["strategy"] == "rdf"
    assert result["output"]["format"] == "rdf"

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation") < completed.index("entity_extraction") < completed.index("concept_extraction") < completed.index("relation_extraction") < completed.index("triple_extraction") < completed.index("taxonomy_induction") < completed.index("type_assertion") < completed.index("semantic_quality") < completed.index("output_generation")
