import pytest


# UC-CONCEPT-004 MF-1 | FUN-014 AC-2 | FUN-016 AC-1 | NFR-007 AC-2 | BR-CONCEPT-006 | TB-CONCEPT-001
def test_concept_extraction_events_started_completed_and_no_raw_text_memory_sink():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    sut.process("Knowledge graphs connect entities in context.")

    events = [e.to_dict() for e in sink.events if e.phase == "concept_extraction"]
    assert any(e["event_type"] == "started" for e in events)
    assert any(e["event_type"] == "completed" for e in events)
    assert all("raw_text" not in e for e in events)
    assert all("raw_text" not in e.get("metadata", {}) for e in events)


# UC-CONCEPT-004 EF-1 | FUN-014 AC-3 | FUN-016 AC-2 | NFR-007 AC-2 | BR-CONCEPT-006 | TB-CONCEPT-001
def test_concept_extraction_failed_event_and_no_raw_text_jsonl(tmp_path):
    import json
    from observability import JsonlFileLogSink
    from orion import ORION

    class _ExplodeConceptExtractionORION(ORION):
        def _run_concept_extraction(self, payload):
            raise RuntimeError("boom-concept-extraction")

    out_file = tmp_path / "concept-events.jsonl"
    sut = _ExplodeConceptExtractionORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}, "spacy_model": "en_core_web_lg"})

    with pytest.raises(RuntimeError):
        sut.process("Knowledge graphs connect entities in context.")

    payloads = [json.loads(line) for line in out_file.read_text(encoding="utf-8").splitlines()]
    con = [p for p in payloads if p["phase"] == "concept_extraction"]

    assert any(e["event_type"] == "started" for e in con)
    assert any(e["event_type"] == "failed" for e in con)
    assert all("raw_text" not in p for p in con)
    assert all("raw_text" not in p.get("metadata", {}) for p in con)
