import pytest


# UC-002 MF-1 | UC-002 MF-2 | UC-002 MF-3 | UC-002 MF-4 | FUN-017 AC-1 | FUN-017 AC-2 | TASK-TOK-003 | TB-TOK-001
def test_orion_process_includes_tokenization_output_and_preserves_previous_phase_data():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    result = sut.process("Hola, mundo. Chau!")

    assert result["raw_text"] == "Hola, mundo. Chau!"
    assert "preprocessed_text" in result
    assert "sentences" in result
    assert "tokens" in result

    token_texts = [t["text"] for t in result["tokens"]]
    assert token_texts == ["Hola", ",", "mundo", ".", "Chau", "!"]


# UC-006 MF-7 | FUN-014 AC-2 | NFR-006 AC-2 | NFR-007 AC-2 | NFR-008 AC-2 | CON-010 AC-2 | TASK-TOK-003 | TB-TOK-001
def test_tokenization_events_started_completed_failed_exist_and_do_not_expose_raw_text():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    sut.process("Uno, dos.")

    tok_events = [e.to_dict() for e in sink.events if e.phase == "tokenization"]
    assert any(e["event_type"] == "started" for e in tok_events)
    assert any(e["event_type"] == "completed" for e in tok_events)

    for event in tok_events:
        assert "raw_text" not in event
        assert "raw_text" not in event.get("metadata", {})

    class _ExplodeTokenizationORION(ORION):
        def _run_tokenization(self, payload):
            raise RuntimeError("boom-tokenization")

    failing = _ExplodeTokenizationORION(config={"logging": {"sink": sink}})
    with pytest.raises(RuntimeError):
        failing.process("Falla tokenization.")

    tok_events_after_failure = [e.to_dict() for e in sink.events if e.phase == "tokenization"]
    assert any(e["event_type"] == "failed" for e in tok_events_after_failure)


# UC-006 MF-7 | FUN-016 AC-1 | FUN-016 AC-2 | NFR-006 AC-2 | NFR-007 AC-2 | CON-011 AC-1 | TASK-TOK-003 | TB-TOK-001
def test_tokenization_events_persist_jsonl_with_pipeline_order_and_without_raw_text(tmp_path):
    import json
    from observability import JsonlFileLogSink
    from orion import ORION

    out_file = tmp_path / "tokenization-events.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}})

    sut.process("Uno, dos. Tres!")

    payloads = [json.loads(line) for line in out_file.read_text(encoding="utf-8").splitlines()]

    tok_events = [p for p in payloads if p["phase"] == "tokenization"]
    assert any(e["event_type"] == "started" for e in tok_events)
    assert any(e["event_type"] == "completed" for e in tok_events)

    completed_phases = [p["phase"] for p in payloads if p["event_type"] == "completed"]
    assert completed_phases.index("input_intake") < completed_phases.index("preprocessing") < completed_phases.index("sentence_segmentation") < completed_phases.index("tokenization")

    assert all("raw_text" not in p for p in tok_events)
    assert all("raw_text" not in p.get("metadata", {}) for p in tok_events)


# UC-006 EF-1 | FUN-014 AC-3 | FUN-016 AC-2 | NFR-006 AC-6 | NFR-007 AC-2 | CON-011 AC-1 | TASK-TOK-003 | TB-TOK-001
def test_tokenization_failed_event_persists_jsonl_without_raw_text(tmp_path):
    import json
    import pytest
    from observability import JsonlFileLogSink
    from orion import ORION

    class _ExplodeTokenizationORION(ORION):
        def _run_tokenization(self, payload):
            raise RuntimeError("boom-tokenization-jsonl")

    out_file = tmp_path / "tokenization-events-failed.jsonl"
    sut = _ExplodeTokenizationORION(config={"logging": {"sink": JsonlFileLogSink(out_file)}})

    with pytest.raises(RuntimeError):
        sut.process("Falla tokenization jsonl.")

    payloads = [json.loads(line) for line in out_file.read_text(encoding="utf-8").splitlines()]
    tok_events = [p for p in payloads if p["phase"] == "tokenization"]

    assert any(e["event_type"] == "started" for e in tok_events)
    assert any(e["event_type"] == "failed" for e in tok_events)
    assert all("raw_text" not in p for p in tok_events)
    assert all("raw_text" not in p.get("metadata", {}) for p in tok_events)
