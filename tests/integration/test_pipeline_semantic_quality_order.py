# UC-SQ-003 MF-1 | FUN-SQ-003 AC-1 | BR-SQ-008 | TB-SQ-001
def test_orion_process_runs_semantic_quality_between_type_assertion_and_output_generation():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})

    result = sut.process("John uses API. John is a person.")

    assert "semantic_quality_report" in result
    report = result["semantic_quality_report"]
    for key in ["entity_noise", "concept_noise", "relation_gaps", "rdf_readiness", "warnings", "quality_score", "excluded_entities", "excluded_concepts"]:
        assert key in report

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("type_assertion") < completed.index("semantic_quality") < completed.index("output_generation")
