import pytest


# UC-OUT-004 MF-1 | FUN-014 AC-2 | FUN-016 AC-1 | NFR-007 AC-2 | BR-OUT-008 | TB-OUT-001
def test_output_generation_events_started_completed_and_no_raw_text_memory_sink():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})

    sut.process("John is a person.")

    events = [e.to_dict() for e in sink.events if e.phase == "output_generation"]
    assert any(e["event_type"] == "started" for e in events)
    assert any(e["event_type"] == "completed" for e in events)
    assert all("raw_text" not in e for e in events)
    assert all("raw_text" not in e.get("metadata", {}) for e in events)


# UC-OUT-004 EF-1 | FUN-014 AC-3 | FUN-016 AC-2 | NFR-007 AC-2 | BR-OUT-008 | TB-OUT-001
def test_output_generation_failed_event_and_no_raw_text_jsonl(tmp_path):
    import json
    from observability import JsonlFileLogSink
    from orion import ORION

    class _ExplodeOutputGenerationORION(ORION):
        def _run_output_generation(self, payload):
            raise RuntimeError("boom-output-generation")

    out_file = tmp_path / "output-generation-events.jsonl"
    sut = _ExplodeOutputGenerationORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})

    with pytest.raises(RuntimeError):
        sut.process("John is a person.")

    payloads = [json.loads(line) for line in out_file.read_text(encoding="utf-8").splitlines()]
    events = [p for p in payloads if p["phase"] == "output_generation"]

    assert any(e["event_type"] == "started" for e in events)
    assert any(e["event_type"] == "failed" for e in events)
    assert all("raw_text" not in p for p in events)
    assert all("raw_text" not in p.get("metadata", {}) for p in events)
