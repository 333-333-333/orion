import pytest


# UC-002 MF-1 | UC-002 MF-2 | UC-002 MF-3 | FUN-003 AC-1 | FUN-003 AC-2 | NFR-006 AC-2 | TASK-SENT-003 | TB-SENT-001
def test_orion_process_runs_input_intake_then_preprocessing_then_sentence_segmentation_and_preserves_raw_text():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    raw = "Uno. Dos? Tres!"
    result = sut.process(raw)

    assert result["raw_text"] == raw
    assert "sentences" in result
    assert [s["text"] for s in result["sentences"]] == ["Uno.", "Dos?", "Tres!"]

    completed_phases = [e.phase for e in sink.events if e.event_type == "completed"]
    assert completed_phases.index("input_intake") < completed_phases.index("preprocessing") < completed_phases.index("sentence_segmentation")


# UC-002 MF-3 | UC-002 E1 | FUN-014 AC-3 | NFR-007 AC-2 | NFR-008 AC-3 | CON-010 AC-2 | TASK-SENT-003 | TB-SENT-001
def test_sentence_segmentation_events_started_completed_failed_exist_and_never_expose_raw_text():
    from observability import MemoryLogSink
    from orion import ORION

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    sut.process("Primera. Segunda?")

    seg_events = [e.to_dict() for e in sink.events if e.phase == "sentence_segmentation"]
    assert any(e["event_type"] == "started" for e in seg_events)
    assert any(e["event_type"] == "completed" for e in seg_events)

    for event in seg_events:
        assert "raw_text" not in event
        assert "raw_text" not in event.get("metadata", {})

    class _ExplodeSegmentationORION(ORION):
        def _run_sentence_segmentation(self, payload):
            raise RuntimeError("boom")

    failing = _ExplodeSegmentationORION(config={"logging": {"sink": sink}})
    with pytest.raises(RuntimeError):
        failing.process("Falla.")

    seg_events_after_failure = [e.to_dict() for e in sink.events if e.phase == "sentence_segmentation"]
    assert any(e["event_type"] == "failed" for e in seg_events_after_failure)
