import pytest

# ACT-001 | UC-001 MF-4 | FUN-014 AC-1 | FUN-014 AC-2 | NFR-006 AC-1 | NFR-008 AC-2 | TB-OBS-001
def test_log_event_requires_phase_event_type_status_and_safe_metadata_only():
    from observability import LogEvent

    event = LogEvent(
        phase="orion_initialization",
        event_type="started",
        status="started",
        source_context_id="src-001",
        use_case_id="UC-001",
        requirement_id="FUN-014",
        metadata={"safe": "ok"},
    )

    payload = event.to_dict()

    assert payload["phase"] == "orion_initialization"
    assert payload["event_type"] == "started"
    assert payload["status"] == "started"
    assert payload["source_context_id"] == "src-001"
    assert payload["use_case_id"] == "UC-001"
    assert payload["requirement_id"] == "FUN-014"
    assert payload["metadata"] == {"safe": "ok"}


# ACT-001 | UC-002 MF-4 | FUN-014 AC-3 | NFR-006 AC-5 | TB-OBS-001
def test_log_event_supports_operation_applied_and_operation_name_when_applicable():
    from observability import LogEvent

    event = LogEvent(
        phase="input_intake",
        event_type="operation_applied",
        status="completed",
        operation_name="normalize_whitespace",
        metadata={"safe": True},
    )

    payload = event.to_dict()

    assert payload["event_type"] == "operation_applied"
    assert payload["operation_name"] == "normalize_whitespace"


# ACT-001 | UC-002 E1 | FUN-014 AC-3 | NFR-006 AC-6 | TB-OBS-001
def test_log_event_requires_exception_category_on_failed_status():
    from observability import LogEvent

    event = LogEvent(
        phase="input_intake",
        event_type="failed",
        status="failed",
        exception_category="orion_validation_error",
        metadata={"safe": "x"},
    )

    payload = event.to_dict()

    assert payload["exception_category"] == "orion_validation_error"


# ACT-001 | UC-002 MF-4 | FUN-014 AC-6 | NFR-007 AC-1 | NFR-007 AC-2 | TB-OBS-001
def test_log_event_omits_raw_input_text_and_sensitive_full_content_by_default():
    from observability import LogEvent

    event = LogEvent(
        phase="input_intake",
        event_type="completed",
        status="completed",
        metadata={"safe": "yes", "raw_text": "SECRET", "full_input": "SENSITIVE"},
    )

    payload = event.to_dict()

    assert "raw_text" not in payload
    assert "full_input" not in payload
    assert "raw_text" not in payload.get("metadata", {})
    assert "full_input" not in payload.get("metadata", {})
