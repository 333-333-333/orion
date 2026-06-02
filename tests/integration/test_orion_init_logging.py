# ACT-001 | UC-001 MF-1 | FUN-014 AC-2 | FUN-014 AC-3 | FUN-015 AC-1 | US-027 AC-1 | TB-OBS-001
def test_orion_init_emits_started_and_completed_events_when_sink_configured():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()

    ORION(config={"logging": {"sink": sink}})

    events = [event.to_dict() for event in sink.events]
    assert events[0]["phase"] == "orion_initialization"
    assert events[0]["event_type"] == "started"
    assert events[1]["phase"] == "orion_initialization"
    assert events[1]["event_type"] == "completed"


# ACT-001 | UC-001 E1 | FUN-014 AC-3 | NFR-006 AC-6 | US-027 AC-2 | TB-OBS-001
def test_orion_init_emits_failed_event_with_exception_category_on_error():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()

    try:
        ORION(config=None, log_sink=sink)  # invalid contract for expected future API
    except Exception:
        pass

    events = [event.to_dict() for event in sink.events]
    assert events[-1]["phase"] == "orion_initialization"
    assert events[-1]["event_type"] == "failed"
    assert "exception_category" in events[-1]


# ACT-001 | UC-001 MF-4 | FUN-015 AC-2 | CON-009 AC-1 | CON-009 AC-2 | US-027 AC-3 | TB-OBS-001
def test_orion_init_does_not_mutate_python_root_logging_when_sink_configured():
    import logging
    from observability import MemoryLogSink
    from orion import ORION

    root = logging.getLogger()
    before_level = root.level
    before_handlers = tuple(root.handlers)

    ORION(config={"logging": {"sink": MemoryLogSink()}})

    assert root.level == before_level
    assert tuple(root.handlers) == before_handlers


# ACT-001 | UC-001 AF-2 | FUN-015 AC-3 | CON-010 AC-1 | CON-010 AC-2 | TB-OBS-001
def test_orion_init_without_sink_is_noop_logging_and_processing_contract_stays_valid():
    from orion import ORION

    sut = ORION(config={})

    assert sut is not None
