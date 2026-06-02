# ACT-001 | UC-001 AF-2 | FUN-015 AC-3 | CON-010 AC-1 | CON-010 AC-3 | TB-OBS-001
def test_null_log_sink_drops_events_and_never_raises():
    from observability import LogEvent, NullLogSink

    sink = NullLogSink()
    event = LogEvent(phase="orion_initialization", event_type="started", status="started", metadata={"safe": True})

    sink.emit(event)

    assert True
