import pytest


# UC-006 MF-8 | FUN-014 AC-2 | FUN-016 AC-1 | NFR-007 AC-2 | BR-LING-005 | TB-LING-001
def test_linguistic_annotation_events_started_completed_and_no_raw_text_memory_sink():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}, "spacy_model": "en_core_web_lg"})

    sut.process("Birds fly.")

    events = [e.to_dict() for e in sink.events if e.phase == "linguistic_annotation"]
    assert any(e["event_type"] == "started" for e in events)
    assert any(e["event_type"] == "completed" for e in events)
    assert all("raw_text" not in e for e in events)
    assert all("raw_text" not in e.get("metadata", {}) for e in events)


# UC-006 EF-2 | FUN-014 AC-3 | FUN-016 AC-2 | NFR-007 AC-2 | BR-LING-005 | TB-LING-001
def test_linguistic_annotation_failed_event_and_no_raw_text_jsonl(tmp_path):
    import json
    from observability import JsonlFileLogSink
    from orion import ORION

    class _ExplodeLinguisticORION(ORION):
        def _run_linguistic_annotation(self, payload):
            raise RuntimeError("boom-linguistic")

    out_file = tmp_path / "ling-events.jsonl"
    sut = _ExplodeLinguisticORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}, "spacy_model": "en_core_web_lg"})

    with pytest.raises(RuntimeError):
        sut.process("Birds fly.")

    payloads = [json.loads(line) for line in out_file.read_text(encoding="utf-8").splitlines()]
    ling = [p for p in payloads if p["phase"] == "linguistic_annotation"]

    assert any(e["event_type"] == "started" for e in ling)
    assert any(e["event_type"] == "failed" for e in ling)
    assert all("raw_text" not in p for p in ling)
    assert all("raw_text" not in p.get("metadata", {}) for p in ling)
