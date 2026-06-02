import pytest


# UC-006 AF-1 | FUN-015 AC-1 | NFR-006 AC-1 | TASK-PRP-003 | TB-PRP-001
def test_preprocessing_operations_applied_reports_expected_operations_in_order():
    from pipeline.step_002_preprocessing import preprocess_input

    raw = "Cafe\u0301   UNO\r\nDOS"
    payload = {
        "raw_text": raw,
        "source_text_id": "src-ops-001",
        "metadata": {"source": {"kind": "string", "start_offset": 0, "end_offset": len(raw)}},
    }

    result = preprocess_input(payload)

    assert result["operations_applied"] == [
        "unicode_normalization",
        "collapse_repeated_spaces",
        "normalize_newlines",
    ]


# UC-002 E1 | NFR-007 AC-1 | CON-010 AC-1 | TASK-PRP-003 | TB-PRP-001
def test_preprocessing_failed_event_omits_raw_text_from_event_payload_when_error_happens():
    from observability import MemoryLogSink
    from orion import ORION, OrionError

    sink = MemoryLogSink()
    sut = ORION(config={"logging": {"sink": sink}})

    with pytest.raises(OrionError):
        sut.process("   \n\t")

    failed = [e.to_dict() for e in sink.events if e.phase == "preprocessing" and e.event_type == "failed"]
    assert failed
    assert all("raw_text" not in item for item in failed)
    assert all("raw_text" not in item.get("metadata", {}) for item in failed)
