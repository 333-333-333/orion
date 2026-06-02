# UC-REL-004 MF-1 | FUN-REL-002 AC-1 | FUN-REL-001 AC-1 | FUN-REL-001 AC-3 | TB-REL-001
def test_orion_process_runs_relation_extraction_after_concept_extraction_and_preserves_payload():
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

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation") < completed.index("entity_extraction") < completed.index("concept_extraction") < completed.index("relation_extraction")

    required = {
        "relation_id", "subject_text", "subject_ref", "predicate", "object_text", "object_ref",
        "sentence_id", "source_text_id", "confidence", "evidence_span", "start_offset", "end_offset"
    }
    for rel in result["relations"]:
        assert required.issubset(rel.keys())
