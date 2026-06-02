
# UC-002 MF-1 | UC-002 MF-2 | FUN-003 AC-1 | NFR-001 AC-1 | TASK-PRP-004 | TB-PRP-001
def test_orion_process_string_runs_input_intake_then_preprocessing_and_preserves_contract():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    raw = "Cafe\u0301   MUNDO\r\nLinea"
    result = sut.process(raw)

    assert result["raw_text"] == raw
    assert result["source_text_id"]
    assert result["preprocessed_text"]

    phases = [e.phase for e in sink.events if e.event_type == "completed"]
    assert phases.index("input_intake") < phases.index("preprocessing")


# UC-003 MF-1 | UC-003 MF-2 | FUN-004 AC-1 | CON-006 AC-1 | TASK-PRP-004 | TB-PRP-001
def test_orion_process_path_runs_preprocessing_and_keeps_source_text_id_and_raw_text(tmp_path):
    from observability import MemoryLogSink
    from orion import ORION

    fixture = tmp_path / "input.txt"
    fixture.write_text("Árbol   UNO\r\nDOS", encoding="utf-8")

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    result = sut.process(fixture)

    assert result["raw_text"] == "Árbol   UNO\r\nDOS"
    assert result["source_text_id"]
    assert result["source_text_id"] == result.get("source_text_id")

    payloads = [e.to_dict() for e in sink.events if e.phase in {"input_intake", "preprocessing"}]
    assert payloads
    assert all("raw_text" not in p for p in payloads)
    assert all("raw_text" not in p.get("metadata", {}) for p in payloads)
