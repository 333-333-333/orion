import pytest


# UC-006 MF-10 | FUN-014 AC-2 | FUN-016 AC-1 | NFR-007 AC-2 | BR-ENT-005 | TB-ENT-001
def test_entity_extraction_events_started_completed_and_no_raw_text_memory_sink():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    sut.process("Barack Obama visited Paris.")

    events = [e.to_dict() for e in sink.events if e.phase == "entity_extraction"]
    assert any(e["event_type"] == "started" for e in events)
    assert any(e["event_type"] == "completed" for e in events)
    assert all("raw_text" not in e for e in events)
    assert all("raw_text" not in e.get("metadata", {}) for e in events)


# UC-006 EF-3 | FUN-014 AC-3 | FUN-016 AC-2 | NFR-007 AC-2 | BR-ENT-005 | TB-ENT-001
def test_entity_extraction_failed_event_and_no_raw_text_jsonl(tmp_path):
    import json
    from observability import JsonlFileLogSink
    from orion import ORION

    class _ExplodeEntityExtractionORION(ORION):
        def _run_entity_extraction(self, payload):
            raise RuntimeError("boom-entity-extraction")

    out_file = tmp_path / "entity-events.jsonl"
    sut = _ExplodeEntityExtractionORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}, "spacy_model": "en_core_web_lg"})

    with pytest.raises(RuntimeError):
        sut.process("Barack Obama visited Paris.")

    payloads = [json.loads(line) for line in out_file.read_text(encoding="utf-8").splitlines()]
    ent = [p for p in payloads if p["phase"] == "entity_extraction"]

    assert any(e["event_type"] == "started" for e in ent)
    assert any(e["event_type"] == "failed" for e in ent)
    assert all("raw_text" not in p for p in ent)
    assert all("raw_text" not in p.get("metadata", {}) for p in ent)
