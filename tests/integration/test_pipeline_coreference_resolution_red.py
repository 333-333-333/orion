# UC-COREF-PIPE-001 MF-1 | FUN-COREF-PIPE-001 AC-1 | FUN-COREF-PIPE-001 AC-2 | BR-COREF-PIPE-001 | BR-REL-007
def test_orion_process_inserts_coreference_stage_before_relation_and_propagates_coref_artifacts_red():
    from observability import MemoryLogSink
    from orion import ORION

    text = "An information asset is any resource that stores information."
    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    result = sut.process(text)

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("concept_extraction") < completed.index("coreference_resolution") < completed.index("relation_extraction")

    assert "coreferences" in result and len(result["coreferences"]) > 0
    first_coref = result["coreferences"][0]
    assert "confidence" in first_coref
    assert "evidence_span" in first_coref

    assert len(result.get("relations", [])) > 0
    assert all((rel.get("subject_text", "").strip().lower() != "that") for rel in result["relations"])
