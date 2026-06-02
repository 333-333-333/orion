import json


# ACT-001 | UC-005 AF-1 | FUN-016 AC-1 | FUN-016 AC-2 | CON-011 AC-2 | TB-OBS-001
def test_jsonl_file_log_sink_writes_one_structured_event_per_line(tmp_path):
    from observability import JsonlFileLogSink, LogEvent

    output_file = tmp_path / "orion-observability.jsonl"
    sink = JsonlFileLogSink(output_file)

    sink.emit(LogEvent(phase="orion_initialization", event_type="started", status="started", metadata={"safe": 1}))
    sink.emit(LogEvent(phase="orion_initialization", event_type="completed", status="completed", metadata={"safe": 2}))

    lines = output_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2
    assert all(isinstance(json.loads(line), dict) for line in lines)


# ACT-001 | UC-002 MF-4 | FUN-016 AC-4 | NFR-007 AC-4 | NFR-008 AC-3 | TB-OBS-001
def test_jsonl_file_log_sink_records_match_structured_event_contract(tmp_path):
    from observability import JsonlFileLogSink, LogEvent

    output_file = tmp_path / "orion-observability-contract.jsonl"
    sink = JsonlFileLogSink(output_file)

    event = LogEvent(
        phase="input_intake",
        event_type="completed",
        status="completed",
        source_context_id="src-abc",
        use_case_id="UC-002",
        requirement_id="FUN-016",
        metadata={"safe": "ok", "raw_text": "LEAK"},
    )
    sink.emit(event)

    payload = json.loads(output_file.read_text(encoding="utf-8").strip())
    assert payload["phase"] == "input_intake"
    assert payload["event_type"] == "completed"
    assert payload["status"] == "completed"
    assert payload["source_context_id"] == "src-abc"
    assert payload["use_case_id"] == "UC-002"
    assert payload["requirement_id"] == "FUN-016"
    assert "raw_text" not in payload
