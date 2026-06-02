# ACT-001 | UC-002 MF-1 | FUN-014 AC-2 | FUN-014 AC-3 | US-027 AC-2 | TB-OBS-001
def test_input_intake_process_emits_started_and_completed_events_with_memory_sink():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    sut.process("hola mundo")

    payloads = [e.to_dict() for e in sink.events if e.phase == "input_intake"]
    assert payloads[0]["event_type"] == "started"
    assert payloads[-1]["event_type"] == "completed"


# ACT-001 | UC-002 E1 | FUN-014 AC-3 | NFR-006 AC-6 | TB-OBS-001
def test_input_intake_process_emits_failed_event_with_exception_category_on_invalid_input():
    import pytest
    from observability import MemoryLogSink
    from orion import ORION, OrionError

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    with pytest.raises(OrionError):
        sut.process("")

    payloads = [e.to_dict() for e in sink.events if e.phase == "input_intake"]
    assert payloads[-1]["event_type"] == "failed"
    assert "exception_category" in payloads[-1]


# ACT-001 | UC-002 MF-4 | NFR-007 AC-1 | NFR-007 AC-2 | CON-010 AC-1 | TB-OBS-001
def test_input_intake_events_omit_raw_input_text_even_when_processing_real_text():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    sut.process("texto super secreto")

    payloads = [e.to_dict() for e in sink.events if e.phase == "input_intake"]
    assert all("raw_text" not in p for p in payloads)


# ACT-001 | UC-002 MF-4 | FUN-016 AC-1 | FUN-016 AC-2 | CON-011 AC-1 | CON-011 AC-2 | US-028 AC-1 | US-028 AC-2 | TB-OBS-001
def test_input_intake_can_persist_jsonl_only_when_explicitly_configured(tmp_path):
    import json
    from observability import JsonlFileLogSink
    from orion import ORION

    out_file = tmp_path / "input-intake.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}})

    sut.process("hello")

    lines = out_file.read_text(encoding="utf-8").splitlines()
    payloads = [json.loads(line) for line in lines]
    phases = [p["phase"] for p in payloads if p["event_type"] == "completed"]

    assert len(lines) >= 4
    assert "preprocessing" in [p["phase"] for p in payloads]
    assert phases.index("input_intake") < phases.index("preprocessing")
    assert all("raw_text" not in p for p in payloads)
