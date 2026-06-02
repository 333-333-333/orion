# UC-002 MF-1 | UC-002 MF-2 | UC-002 MF-3 | UC-002 MF-4 | UC-002 MF-5 | FUN-LING-001 AC-1 | TB-LING-001
def test_orion_process_runs_linguistic_annotation_after_tokenization_and_preserves_payload():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    result = sut.process("Hola mundo. Birds fly.")

    assert "raw_text" in result
    assert "preprocessed_text" in result
    assert "sentences" in result
    assert "tokens" in result

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation")

    assert all("lemma" in t and "pos" in t and "tag" in t and "dependency" in t for t in result["tokens"])
