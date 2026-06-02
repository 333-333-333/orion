# UC-002 MF-6 | FUN-ENT-001 AC-1 | FUN-ENT-001 AC-2 | FUN-ENT-001 AC-3 | TB-ENT-001
def test_orion_process_runs_entity_extraction_after_linguistic_annotation_and_preserves_payload():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    result = sut.process("Barack Obama visited Paris.")

    assert "raw_text" in result
    assert "preprocessed_text" in result
    assert "sentences" in result
    assert "tokens" in result
    assert "entities" in result
    assert len(result["entities"]) >= 1

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation") < completed.index("entity_extraction")

    required = {"entity_id", "text", "label", "start_offset", "end_offset", "sentence_id", "source_text_id"}
    for entity in result["entities"]:
        assert required.issubset(entity.keys())
