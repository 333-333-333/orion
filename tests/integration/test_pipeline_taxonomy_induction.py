# UC-TAX-003 MF-1 | FUN-TAX-002 AC-1 | FUN-TAX-001 AC-4 | TB-TAX-001
def test_orion_process_runs_taxonomy_induction_after_triple_extraction_and_preserves_payload():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    result = sut.process("A robin is a bird. Mammals including dogs are warm-blooded.")

    assert "raw_text" in result
    assert "preprocessed_text" in result
    assert "sentences" in result
    assert "tokens" in result
    assert "entities" in result
    assert "concepts" in result
    assert "relations" in result
    assert "triples" in result
    assert "taxonomy_relations" in result

    completed = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed.index("input_intake") < completed.index("preprocessing") < completed.index("sentence_segmentation") < completed.index("tokenization") < completed.index("linguistic_annotation") < completed.index("entity_extraction") < completed.index("concept_extraction") < completed.index("relation_extraction") < completed.index("triple_extraction") < completed.index("taxonomy_induction")
