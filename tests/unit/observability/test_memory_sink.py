# ACT-001 | UC-001 MF-4 | FUN-015 AC-1 | FUN-015 AC-2 | NFR-008 AC-2 | TB-OBS-001
def test_memory_log_sink_collects_events_per_instance_in_order():
    from observability import LogEvent, MemoryLogSink

    sink_a = MemoryLogSink()
    sink_b = MemoryLogSink()

    e1 = LogEvent(phase="orion_initialization", event_type="started", status="started", metadata={"safe": 1})
    e2 = LogEvent(phase="orion_initialization", event_type="completed", status="completed", metadata={"safe": 2})

    sink_a.emit(e1)
    sink_a.emit(e2)

    assert [e.to_dict() for e in sink_a.events] == [e1.to_dict(), e2.to_dict()]
    assert sink_b.events == []
